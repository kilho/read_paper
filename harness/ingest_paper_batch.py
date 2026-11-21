import argparse
import json
import re
import shutil
import subprocess
import sys
import uuid

import yaml

from harness import check_wikilint as wiki
from harness.search_related import title_key


PROMPTS = wiki.ROOT / ".github" / "skills" / "ingest-paper-batch" / "prompts"
PAPER_ID = re.compile(wiki.SCHEMA["properties"]["id"]["pattern"])
ARXIV_REF = re.compile(
    r"(?:arxiv[:-]|https?://(?:www\.)?arxiv\.org/(?:abs|pdf|html)/)?"
    r"(\d{4}\.\d{4,5})(?:v\d+)?(?:\.pdf)?(?:[?#].*)?", re.I
)


def reference_id(reference):
    arxiv = ARXIV_REF.fullmatch(reference)
    if arxiv:
        return f"arxiv-{arxiv[1]}"
    path = re.fullmatch(r"(?:\./)?wiki/papers/\d{4}/([^/]+)\.md", reference)
    paper_id = path[1] if path else reference
    return paper_id if PAPER_ID.fullmatch(paper_id) else None


def unique_references(references):
    papers = {}
    for reference in references:
        reference = reference.strip()
        if not reference:
            raise ValueError("a paper reference cannot be empty")
        key = reference_id(reference) or reference
        papers.setdefault(key, reference)
    return papers.values()


def check_indexed(paper_id):
    if not PAPER_ID.fullmatch(paper_id):
        raise ValueError(f"invalid canonical paper ID: {paper_id}")
    paths = list(wiki.PAPERS.glob(f"*/{paper_id}.md"))
    if len(paths) != 1:
        raise ValueError(f"expected exactly one canonical page for {paper_id}")
    page = paths[0]
    metadata = wiki.validate_page(page)
    if metadata["id"] != paper_id or page.parent.name != str(metadata["year"]):
        raise ValueError(f"canonical path or metadata does not match {paper_id}")
    index = wiki.PAPERS.parent / "index.md"
    link = page.relative_to(index.parent).as_posix()
    if f"]({link})" not in index.read_text(encoding="utf-8"):
        raise ValueError(f"{paper_id} is not linked in wiki/index.md")


def run_session(command, phase, label, data):
    session_id = str(uuid.uuid4())
    print(f"Starting {label} (session {session_id})", flush=True)
    instructions = (PROMPTS / f"{phase}.md").read_text(encoding="utf-8").rstrip()
    prompt = f"{instructions}\n\nJSON input:\n{json.dumps(data, ensure_ascii=False)}"
    result = subprocess.run(
        [*command, "--session-id", session_id, "--silent", "--no-ask-user", "--prompt", prompt],
        cwd=wiki.ROOT, stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, text=True, check=False,
    )
    if result.stdout:
        print(result.stdout.rstrip(), flush=True)
    if result.returncode:
        raise ValueError(f"{label}: Copilot exited with status {result.returncode}")
    return result.stdout.splitlines()


def existing_paper(reference, pages):
    paper_id = reference_id(reference)
    matches = [meta["id"] for path, meta in pages if (
        paper_id == meta["id"] or reference in {str(path), meta["source"]["url"]}
        or title_key(reference) == title_key(meta["title"])
    )]
    if len(matches) > 1:
        raise ValueError(f"ambiguous wiki match for {reference}; use a canonical paper ID")
    return matches[0] if matches else None


def run_batch(args):
    references = unique_references(args.papers)
    compare_with = list(dict.fromkeys(args.compare_with))
    if wiki.main([]):
        raise ValueError("fix wiki validation failures before starting the batch")
    for paper_id in compare_with:
        check_indexed(paper_id)

    pages = [(path, wiki.read_page(path)[0]) for path in sorted(wiki.PAPERS.glob("*/*.md"))]
    existing_ids = {meta["id"] for _, meta in pages}
    pending = []
    for reference in references:
        paper_id = existing_paper(reference, pages)
        if paper_id:
            print(f"Skipped existing wiki paper: {paper_id}", flush=True)
        else:
            pending.append(reference)
    if not pending:
        print("No new papers to ingest; synthesis skipped.", flush=True)
        return

    command = copilot_command(args)
    completed = {}
    failures = []
    for reference in pending:
        try:
            output = run_session(command, "ingest", reference, {
                "paper": reference, "constraints": args.ingest_constraints,
            })
            reports = [line.removeprefix("INGEST_RESULT ") for line in output if line.startswith("INGEST_RESULT ")]
            if len(reports) != 1:
                raise ValueError("no unambiguous canonical completion report")
            paper_id = reports[0]
            expected = reference_id(reference)
            if expected and paper_id != expected:
                raise ValueError(f"reported {paper_id}, expected {expected}")
            if paper_id in existing_ids:
                print(f"Skipped existing wiki paper: {paper_id}", flush=True)
                continue
            check_indexed(paper_id)
            completed[paper_id] = None
        except (ValueError, OSError, yaml.YAMLError) as error:
            failures.append(reference)
            print(f"Blocked: {reference}: {error}", file=sys.stderr, flush=True)

    print("Published: " + (", ".join(completed) or "none"), flush=True)
    if failures:
        raise ValueError(f"synthesis skipped; {len(failures)} ingestion(s) blocked")
    if not completed:
        print("No new papers to ingest; synthesis skipped.", flush=True)
        return
    if wiki.main([]):
        raise ValueError("synthesis skipped; wiki validation failed after ingestion")

    output = run_session(command, "synthesize", "synthesis", {
        "papers": list(completed),
        "compare_with": [paper for paper in compare_with if paper not in completed],
        "constraints": args.synthesis_constraints,
    })
    validation_failed = wiki.main([])
    if validation_failed or output.count("SYNTHESIS_COMPLETE") != 1:
        raise ValueError("synthesis did not report verified completion or failed wiki validation")
    for paper_id in dict.fromkeys([*completed, *compare_with]):
        check_indexed(paper_id)


def copilot_command(args):
    copilot = shutil.which("copilot")
    if copilot is None:
        raise ValueError("Copilot CLI was not found on PATH")
    command = [copilot]
    if args.model:
        command.extend(["--model", args.model])
    for flag, values in (("--allow-tool", args.allow_tool), ("--allow-url", args.allow_url)):
        if values:
            command.extend([flag, *values])
    if args.assisted_approval:
        command.append("--assisted-approval")
    return command


def main(argv=None):
    parser = argparse.ArgumentParser(description="Ingest selected papers in fresh Copilot sessions, then synthesize.")
    parser.add_argument("papers", nargs="+", help="selected paper titles, IDs, URLs, or wiki paths (one per argument)")
    parser.add_argument("--compare-with", action="append", default=[], metavar="ID", help="existing wiki ID to include in synthesis")
    parser.add_argument("--ingest-constraints", default="", help="instructions for each single-paper session")
    parser.add_argument("--synthesis-constraints", default="", help="instructions only for the synthesis session")
    parser.add_argument("--model", help="optional model override for the fresh sessions")
    parser.add_argument("--allow-tool", action="append", default=[], metavar="RULE", help="explicit Copilot tool permission; repeatable")
    parser.add_argument("--allow-url", action="append", default=[], metavar="URL", help="explicit Copilot URL permission; repeatable")
    parser.add_argument("--assisted-approval", action="store_true", help="opt in to Copilot assisted permission review")
    args = parser.parse_args(argv)
    try:
        run_batch(args)
    except (ValueError, OSError, yaml.YAMLError) as error:
        print(f"Batch stopped: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
