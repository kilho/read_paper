import argparse
import json
import math
import os
import re
import sys
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import quote, urlencode, urlsplit
from urllib.request import Request, urlopen

from harness.check_wikilint import PAPERS, ROOT, read_page


API = "https://api.openalex.org/works"
FIELDS = "id,doi,display_name,publication_year,cited_by_count,referenced_works,locations,primary_location,best_oa_location"
ARXIV = r"(?:\d{4}\.\d{4,5}|[a-z][a-z.-]*/\d{7})"
BONUSES = {"related-work": 0.30, "baseline": 0.30, "bibliography": 0,
           "citing-paper": 0.30, "award": 0.35, "presentation": 0.20, "author": 0.10, "institution": 0.10}
CONTEXT = {"related-work", "baseline", "bibliography", "citing-paper"}
RELEVANCE = CONTEXT - {"bibliography"}


def identifier(value):
    value = value.strip().lower().rstrip("/")
    arxiv = re.fullmatch(
        rf"(?:https?://(?:www\.)?arxiv\.org/(?:abs|pdf|html)/|10\.48550/arxiv\.|arxiv[:-])?({ARXIV})(?:v\d+)?(?:\.pdf)?",
        value.removeprefix("https://doi.org/"),
    )
    if arxiv:
        return f"arxiv:{arxiv[1]}"
    work = re.fullmatch(r"(?:https?://openalex\.org/(?:works/)?)?(w\d+)", value)
    if work:
        return work[1].upper()
    doi = re.fullmatch(r"(?:https?://(?:dx\.)?doi\.org/|doi:)?(10\.\d{4,}/\S+)", value)
    if doi:
        return f"doi:{doi[1]}"
    return None


def aliases(work):
    values = [work.get("id"), work.get("doi")]
    for location in work.get("locations") or []:
        values.extend((location.get("landing_page_url"), location.get("pdf_url")))
    return {key for value in values if value and (key := identifier(value))}


def title_key(title):
    return "".join(char for char in title.casefold() if char.isalnum())


class OpenAlex:
    def __init__(self):
        self.api_key = os.environ.get("OPENALEX_API_KEY")
        self.records = {}

    def get(self, path="", **params):
        headers = {"Accept": "application/json", "User-Agent": "read-paper-discovery/1.0"}
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"
        request = Request(f"{API}{path}?{urlencode(dict(select=FIELDS, **params))}", headers=headers)
        try:
            with urlopen(request, timeout=15) as response:
                return json.load(response)
        except HTTPError as exc:
            if exc.code == 404:
                return {}
            raise ValueError(f"OpenAlex HTTP {exc.code}") from None
        except (URLError, TimeoutError, json.JSONDecodeError):
            raise ValueError("OpenAlex request failed or returned invalid JSON") from None

    def resolve(self, value):
        key = identifier(value)
        if key and key in self.records:
            return self.records[key]
        if key:
            if key.startswith("arxiv:"):
                path = "https://doi.org/10.48550/arxiv." + key[6:]
            elif key.startswith("doi:"):
                path = "https://doi.org/" + key[4:]
            else:
                path = key
            work = self.get("/" + quote(path, safe=":/"))
        else:
            if urlsplit(value).scheme:
                raise ValueError("use a wiki page, exact title, DOI, arXiv URL, or OpenAlex ID")
            response = self.get(filter=f'title.search:"{value.replace(chr(34), "")}"', per_page=20)
            matches = [w for w in response.get("results", [])
                       if title_key(w.get("display_name") or "") == title_key(value)]
            if len(matches) > 1:
                raise ValueError("ambiguous title; supply a stable ID")
            work = matches[0] if matches else {}
        if not work.get("id"):
            raise ValueError("no matching OpenAlex work")
        for alias in aliases(work) | ({key} if key else set()):
            self.records[alias] = work
        return work


def wiki_pages():
    return [(path, read_page(path)[0]) for path in sorted(PAPERS.glob("*/*.md"))]


def resolve_seed(value, client, pages):
    key = identifier(value)
    matches = [meta for path, meta in pages if value in {meta["id"], str(path), path.relative_to(ROOT).as_posix()}
               or title_key(value) == title_key(meta["title"])
               or (key and key == identifier(meta["source"]["url"]))]
    if len(matches) > 1:
        raise ValueError("ambiguous wiki title; use a wiki ID")
    if matches:
        meta = matches[0]
        for query in dict.fromkeys(filter(None, (identifier(meta["source"]["url"]), meta["title"]))):
            try:
                return client.resolve(query)
            except ValueError as exc:
                if str(exc) != "no matching OpenAlex work":
                    raise
        raise ValueError("no matching OpenAlex work for wiki entry")
    return client.resolve(value)


def load_evidence(path):
    if path is None:
        return []
    rows = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(rows, list) or len(rows) > 100:
        raise ValueError("evidence must be a JSON array with at most 100 records")
    for row in rows:
        if not isinstance(row, dict):
            raise ValueError("each evidence record must be an object")
        for field in ("paper", "kind", "source", "note"):
            if not isinstance(row.get(field), str) or not row[field].strip():
                raise ValueError(f"evidence requires a nonempty {field}")
        url = urlsplit(row["source"])
        if (row["kind"] not in BONUSES or url.scheme not in {"http", "https"} or not url.hostname
                or url.username or url.password or re.search(r'[\s<>]', row["source"])):
            raise ValueError("evidence requires a supported kind and an HTTP(S) source URL")
        if row["kind"] in CONTEXT and (not isinstance(row.get("seed"), str) or not row["seed"].strip()):
            raise ValueError("evidence describing a relationship requires a seed")
        if "title" in row and (not isinstance(row["title"], str) or not row["title"].strip()):
            raise ValueError("evidence title must be a nonempty string")
        if "seed" in row and not isinstance(row["seed"], str):
            raise ValueError("evidence seed must be a string")
    return rows


def discover(client, inputs, pages, evidence, per_seed, include_known=False, *, require_relevance=False):
    warnings = []

    def attempt(label, call):
        try:
            return call()
        except ValueError as exc:
            warnings.append(f"{label}: {exc}.")
            return {}

    seeds = {}
    seed_labels = {}
    records = []
    for value in inputs:
        seed = attempt(f"Seed {value}", lambda: resolve_seed(value, client, pages))
        if seed:
            seeds[seed["id"]] = seed
            seed_labels[value] = seed["id"]
            seed_labels.update(dict.fromkeys(aliases(seed), seed["id"]))
    if not seeds:
        raise ValueError("No seeds resolved. " + " ".join(warnings))

    outgoing = defaultdict(set)
    for seed_id, seed in seeds.items():
        label = seed.get("display_name") or seed_id
        refs = sorted({key for ref in seed.get("referenced_works") or []
                       if (key := identifier(ref)) and key.startswith("W")})
        if not refs:
            warnings.append(f"{label}: no outgoing references returned by OpenAlex.")
        if len(refs) > 300:
            warnings.append(f"{label}: outgoing references capped at 300 of {len(refs)}.")
        for ref in refs[:300]:
            outgoing[ref].add(seed_id)
        response = attempt(f"Incoming citations for {label}", lambda: client.get(
            filter=f"cites:{identifier(seed_id)}", sort="cited_by_count:desc", per_page=per_seed))
        incoming = response.get("results", [])
        total = (response.get("meta") or {}).get("count", len(incoming))
        if total > len(incoming):
            warnings.append(f"{label}: retrieved {len(incoming)} of {total} indexed citing papers, by citation count.")
        records.extend((work, {("cites-seed", seed_id)}, []) for work in incoming)

    keys = sorted(outgoing)
    for start in range(0, len(keys), 100):
        batch = keys[start:start + 100]
        response = attempt("Outgoing reference batch", lambda: client.get(
            filter="openalex:" + "|".join(batch), per_page=len(batch)))
        found = set()
        for work in response.get("results", []):
            key = identifier(work["id"])
            found.add(key)
            records.append((work, {("cited-by-seed", seed_id) for seed_id in outgoing.get(key, ())}, []))
        if len(found & set(batch)) < len(batch):
            warnings.append(f"Outgoing reference batch: {len(set(batch) - found)} records unavailable.")

    for row in evidence:
        links = set()
        if row["kind"] in CONTEXT:
            value = row["seed"]
            seed_id = seed_labels.get(value) or seed_labels.get(identifier(value))
            if not seed_id:
                warnings.append(f"Evidence seed {value} is not a resolved input; skipped.")
                continue
            links.add(("cites-seed" if row["kind"] == "citing-paper" else row["kind"], seed_id))
        key = identifier(row["paper"])
        work = next((work for work, _, _ in records if key and key in aliases(work)), None)
        if not work:
            work = attempt(f"Evidence for {row['paper']}", lambda: client.resolve(row["paper"]))
        if not work and links and (key := identifier(row["paper"])):
            landing = (f"https://arxiv.org/abs/{key[6:]}" if key.startswith("arxiv:") else
                       f"https://doi.org/{key[4:]}" if key.startswith("doi:") else f"https://openalex.org/{key}")
            work = {"id": landing, "display_name": row.get("title") or row["paper"]}
        if work:
            records.append((work, links, [row]))

    known = {key for _, meta in pages for value in (meta["id"], meta["source"]["url"])
             if (key := identifier(value))}
    seed_keys = set().union(*(aliases(seed) for seed in seeds.values()))
    groups = []
    for work, links, notes in records:
        keys = aliases(work)
        group = (keys, [work], set(links), list(notes))
        for existing in groups[:]:
            if keys & existing[0]:
                groups.remove(existing)
                keys.update(existing[0])
                group[1].extend(existing[1])
                group[2].update(existing[2])
                group[3].extend(existing[3])
        groups.append(group)

    candidates = []
    for keys, works, links, notes in groups:
        if not links or keys & seed_keys or (not include_known and keys & known):
            continue
        if require_relevance and not any(row["kind"] in RELEVANCE for row in notes):
            continue
        # Pick one citation record for an aliased work, never add counts together.
        work = max(works, key=lambda w: (citation_count(w), bool(w.get("doi")), w["id"]))
        context = max((BONUSES[row["kind"]] for row in notes if row["kind"] in CONTEXT), default=0)
        recognition = sum(BONUSES[kind] for kind in {row["kind"] for row in notes} - CONTEXT)
        coverage = 0.05 * min(3, len({seed for _, seed in links}) - 1)
        count = citation_count(work)
        score = math.log10(1 + max(count, 0)) + context + recognition + coverage
        candidates.append((score, work, links, notes, bool(keys & known)))
    candidates.sort(key=lambda c: (-c[0], -citation_count(c[1]), c[1]["id"]))
    return seeds, candidates, warnings


def citation_count(work):
    count = work.get("cited_by_count")
    return count if type(count) is int and count >= 0 else -1


def md(text):
    return re.sub(r"([\\`*_{}\[\]<>#!|$])", r"\\\1", " ".join(str(text).split()))


def report(seeds, candidates, warnings, checked, limit, *, require_relevance=False):
    lines = ["# Related paper shortlist", "", f"OpenAlex checked: {checked.date().isoformat()} (UTC).",
             "", "## Seed papers", ""]
    for work in seeds.values():
        lines.append(f"- [{md(work.get('display_name') or work['id'])}](<{work['id']}>)")
    lines.extend(("", "## Prioritized reading list", "",
                  "Citation impact leads the score: log10(1 + OpenAlex citations), plus bounded bonuses for "
                  "verified context, venue recognition, watchlist matches, and links to multiple seeds. "
                  "Unknown counts get no citation points; totals favor older work. These are reading signals, not proof of quality.", ""))
    if require_relevance:
        lines.extend(("Only papers with supplied relevance evidence are eligible; a citation or award alone does not qualify.", ""))
    if not candidates:
        lines.extend(("No eligible candidates found in the accessible data.", ""))
    for rank, (score, work, links, notes, known) in enumerate(candidates[:limit], 1):
        count = citation_count(work)
        citation = f"{count:,}" if count >= 0 else "unknown"
        year = work.get("publication_year") or "year unknown"
        location = work.get("primary_location") or {}
        venue = (location.get("source") or {}).get("display_name")
        pdf = (work.get("best_oa_location") or {}).get("pdf_url")
        lines.append(f"{rank}. [{md(work.get('display_name') or work['id'])}](<{work['id']}>) "
                     f"({year}{', ' + md(venue) if venue else ''}) — **{citation} OpenAlex citations**, score {score:.2f}"
                     + ("; already in the wiki" if known else ""))
        if pdf and re.fullmatch(r"https?://[^\s<>]+", pdf):
            lines.append(f"   - [Open PDF](<{pdf}>)")
        for kind, seed in sorted(links):
            if kind not in CONTEXT:
                relationship = "Cites" if kind == "cites-seed" else "Cited by"
                lines.append(f"   - {relationship} [{md(seeds[seed].get('display_name') or seed)}](<{seed}>).")
        for key in sorted({(row["kind"], row.get("seed", ""), row["note"], row["source"]) for row in notes}):
            kind, seed, note, source = key
            lines.append(f"   - [{md(kind)}](<{source}>){f' ({md(seed)})' if seed else ''}: {md(note)}")
    lines.extend(("", f"Shown: {min(limit, len(candidates))} of {len(candidates)} eligible candidates.", "",
                  "## Coverage", "", "OpenAlex citation links are indexed metadata, not proof that the papers discuss "
                  "each other in depth. Related Work, awards, and presentation labels are only reported when supplied "
                  "with source evidence; absent labels are unknown.", ""))
    lines.extend(f"- {md(warning)}" for warning in warnings)
    return "\n".join(lines).rstrip() + "\n"


def main(argv=None):
    parser = argparse.ArgumentParser(description="Rank papers cited by or citing one or more seed papers.")
    parser.add_argument("seeds", nargs="+", help="Wiki path/ID, arXiv or DOI URL, OpenAlex ID, or exact title")
    parser.add_argument("--evidence", type=Path, help="Source-checked JSON annotations from the search-related skill")
    parser.add_argument("--require-relevance", action="store_true", help="Require related-work, baseline, or citing-paper evidence")
    parser.add_argument("--coverage-note", action="append", default=[], help="Record a source limitation in the saved report")
    parser.add_argument("--limit", type=int, default=15, help="Number of ranked recommendations to show")
    parser.add_argument("--per-seed", type=int, default=40, help="Maximum indexed incoming citations per seed (1–100)")
    parser.add_argument("--include-known", action="store_true", help="Include exact matches already in the wiki")
    destination = parser.add_mutually_exclusive_group()
    destination.add_argument("--output", type=Path, help="Write a new Markdown shortlist to this path")
    destination.add_argument("--preview", action="store_true", help="Print only, without saving a shortlist")
    args = parser.parse_args(argv)
    if not (1 <= len(args.seeds) <= 10 and 1 <= args.per_seed <= 100 and 1 <= args.limit <= 200):
        parser.error("use 1–10 seeds, --per-seed 1–100 and --limit 1–200")
    if args.require_relevance and args.evidence is None:
        parser.error("--require-relevance requires --evidence")
    checked = datetime.now(timezone.utc)
    try:
        seeds, candidates, warnings = discover(OpenAlex(), args.seeds, wiki_pages(), load_evidence(args.evidence),
                                               args.per_seed, args.include_known, require_relevance=args.require_relevance)
        text = report(seeds, candidates, warnings + args.coverage_note, checked, args.limit,
                      require_relevance=args.require_relevance)
        if args.preview:
            print(text, end="")
        else:
            path = args.output or ROOT / "discovery" / "related" / f"{checked:%Y%m%dT%H%M%S%fZ}.md"
            path.parent.mkdir(parents=True, exist_ok=True)
            with path.open("x", encoding="utf-8") as handle:
                handle.write(text)
            print(f"Saved {min(args.limit, len(candidates))} ranked recommendations to {path}")
        for warning in warnings:
            print(warning, file=sys.stderr)
    except (OSError, ValueError) as exc:
        print(f"search-related: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
