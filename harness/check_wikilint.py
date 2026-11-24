import argparse
import re
import sys
from pathlib import Path
from urllib.parse import urlsplit

import yaml
from jsonschema import Draft202012Validator


ROOT = Path(__file__).resolve().parents[1]
PAPERS = ROOT / "wiki" / "papers"
SCHEMA = yaml.safe_load((ROOT / "schemas" / "paper.schema.yaml").read_text(encoding="utf-8"))
VALIDATOR = Draft202012Validator(SCHEMA)
ALGORITHM_SCHEMA = yaml.safe_load((ROOT / "schemas" / "algorithm.schema.yaml").read_text(encoding="utf-8"))
ALGORITHM_VALIDATOR = Draft202012Validator(ALGORITHM_SCHEMA)
ALGORITHM_SUFFIX = "_algorithm"


def is_algorithm_path(path):
    return path.stem.endswith(ALGORITHM_SUFFIX)


def paper_paths(pattern="*/*.md"):
    return sorted(path for path in PAPERS.glob(pattern) if not is_algorithm_path(path))


def read_page(path):
    lines = path.read_text(encoding="utf-8").splitlines()
    if not lines or lines[0] != "---":
        raise ValueError("missing YAML frontmatter")
    try:
        end = lines.index("---", 1)
    except ValueError:
        raise ValueError("unclosed YAML frontmatter") from None
    return yaml.safe_load("\n".join(lines[1:end])), "\n".join(lines[end + 1 :])


def table_cells(line):
    line = line.strip()
    if not line.startswith("|") or not line.endswith("|"):
        return []
    return [cell.strip() for cell in re.split(r"(?<!\\)\|", line)[1:-1]]


def has_terminology_table(content, columns):
    lines = content.strip().splitlines()
    if len(lines) < 3 or table_cells(lines[0]) != columns:
        return False
    separator = table_cells(lines[1])
    return (
        len(separator) == len(columns)
        and all(re.fullmatch(r":?-{3,}:?", cell) for cell in separator)
        and all(len(row) == len(columns) and all(row) for row in map(table_cells, lines[2:]))
    )


def split_sections(body):
    parts = re.split(r"^## (.+)$", body, flags=re.M)
    return parts, parts[1::2], dict(zip(parts[1::2], parts[2::2]))


def has_table(content, first_column, min_rows=1):
    lines = [line for line in content.splitlines() if line.strip().startswith("|")]
    if len(lines) < 2 + min_rows:
        return False
    header = table_cells(lines[0])
    separator = table_cells(lines[1])
    rows = [table_cells(line) for line in lines[2:]]
    return (
        len(header) >= 3
        and header[0] == first_column
        and len(separator) == len(header)
        and all(re.fullmatch(r":?-{3,}:?", cell) for cell in separator)
        and all(len(row) == len(header) and all(row) for row in rows)
    )


def validate_algorithm_page(path):
    metadata, body = read_page(path)
    errors = [
        f"{error.json_path}: {error.message}"
        for error in ALGORITHM_VALIDATOR.iter_errors(metadata)
    ]
    if errors:
        raise ValueError("; ".join(errors))
    if re.findall(r"^# (.+)$", body, re.M) != [metadata["title"]]:
        errors.append("expected one H1 matching the frontmatter title")
    parts, headings, sections = split_sections(body)
    rules = ALGORITHM_SCHEMA["x-page"]
    if headings != rules["headings"]:
        errors.append("expected these H2 sections in order: " + ", ".join(rules["headings"]))
    errors.extend(f"empty section: {name}" for name, content in sections.items() if not content.strip())
    walkthrough = sections.get("Phase Walkthrough", "")
    if len(re.findall(r"^### \S", walkthrough, re.M)) < rules["min_phases"]:
        errors.append(f"Phase Walkthrough must have at least {rules['min_phases']} H3 phases")
    if not any(f"**{label}:**" in walkthrough for label in rules["example_types"]):
        errors.append("Phase Walkthrough must include a recognized example label")
    if not has_table(sections.get("Phase Comparison", ""), rules["phase_table_first_column"]):
        errors.append(
            f"Phase Comparison must be a Markdown table with a '{rules['phase_table_first_column']}' "
            "column, at least two phase columns, and complete rows"
        )
    citable_text = "\n".join([parts[0], *(content for name, content in sections.items() if name != "Source Locators")])
    unknown = set(re.findall(r"\[(S[0-9]+)\]", citable_text)) - metadata["sources"].keys()
    if unknown:
        errors.append("unknown source IDs: " + ", ".join(sorted(unknown)))
    errors.extend(
        f"{name} must cite a source ID"
        for name in rules["cited_headings"]
        if name in sections and not re.search(r"\[S[0-9]+\]", sections[name])
    )
    expected_locators = {f"- {key}: {value}" for key, value in metadata["sources"].items()}
    if expected_locators != set(sections.get("Source Locators", "").strip().splitlines()):
        errors.append("Source Locators must list each frontmatter source as '- ID: locator'")
    if errors:
        raise ValueError("; ".join(errors))
    return metadata


def check_companion(path, metadata, pages):
    companion = pages.get(metadata["paper"])
    if not companion:
        return f"{path}: companion paper page not found: {metadata['paper']}"
    paper = companion[1]
    mismatched = [key for key in ("title", "year") if metadata[key] != paper[key]]
    if metadata["source"]["url"] != paper["source"]["url"]:
        mismatched.append("source URL")
    if mismatched:
        return f"{path}: must match companion paper {metadata['paper']}: " + ", ".join(mismatched)
    return None


def validate_page(path):
    metadata, body = read_page(path)
    errors = [
        f"{error.json_path}: {error.message}"
        for error in VALIDATOR.iter_errors(metadata)
    ]
    if errors:
        raise ValueError("; ".join(errors))

    entry_id = metadata["id"]
    source = metadata["source"]
    if entry_id.startswith("arxiv-"):
        paper = entry_id.removeprefix("arxiv-")
        if source["url"] != f"https://arxiv.org/pdf/{paper}{source['version']}":
            errors.append("source URL must match the paper ID and version")
    else:
        try:
            url = urlsplit(source["url"])
            valid_url = (
                bool(url.hostname)
                and url.username is None
                and "\\" not in url.netloc
                and url.port != 0
            )
        except ValueError:
            valid_url = False
        if not valid_url:
            errors.append("source URL must be an HTTP(S) URL with a host and no credentials")
    if re.findall(r"^# (.+)$", body, re.M) != [metadata["title"]]:
        errors.append("expected one H1 matching the frontmatter title")

    parts, headings, sections = split_sections(body)
    rules = SCHEMA["x-page"]
    optional = set(rules["optional_headings"])
    expected_headings = [
        name for name in rules["headings"] if name not in optional or name in sections
    ]
    if headings != expected_headings:
        errors.append("expected these H2 sections in order: " + ", ".join(expected_headings))
    errors.extend(
        f"empty section: {name}"
        for name, content in sections.items()
        if not content.strip() and name not in rules["allow_empty"]
    )
    article = entry_id.startswith(("blog-", "news-", "web-"))
    not_applicable = rules["article_not_applicable"] if article else {}
    terminology = sections.get("Terminology", "")
    columns = rules["terminology_columns"]
    if terminology.strip() != not_applicable.get("Terminology") and not has_terminology_table(terminology, columns):
        errors.append("Terminology must be a Markdown table with nonempty rows: " + " | ".join(columns))
    example = sections.get("Worked Example", "")
    if example.strip() != not_applicable.get("Worked Example") and not any(
        f"**{label}:**" in example for label in rules["example_types"]
    ):
        errors.append("Worked Example must include a recognized example label")

    citable_text = "\n".join([parts[0], *(content for name, content in sections.items() if name != "Source Locators")])
    citations = set(re.findall(r"\[(S[0-9]+)\]", citable_text))
    sources = metadata["sources"]
    unknown = citations - sources.keys()
    if unknown:
        errors.append("unknown source IDs: " + ", ".join(sorted(unknown)))
    core_text = "\n".join(
        sections.get(name, "")
        for name in rules["headings"]
        if name not in optional and name not in {"Source Locators", "FAQ"}
    )
    if not re.search(r"\[S[0-9]+\]", core_text):
        errors.append("the core explanation must cite a source ID")
    for name in rules["optional_headings"]:
        if name in sections and not re.search(r"\[S[0-9]+\]", sections[name]):
            errors.append(f"{name} must cite a source ID")
    expected_locators = {f"- {key}: {value}" for key, value in sources.items()}
    if expected_locators != set(sections.get("Source Locators", "").strip().splitlines()):
        errors.append("Source Locators must list each frontmatter source as '- ID: locator'")
    if errors:
        raise ValueError("; ".join(errors))
    return metadata


def main(argv=None):
    parser = argparse.ArgumentParser(description="Check wiki page structure and references for canonical pages and an optional draft.")
    parser.add_argument("--candidate", type=Path, help="check a draft outside wiki/papers without publishing it")
    args = parser.parse_args(argv)
    pages = {}
    algorithms = []
    failures = []
    paths = sorted(PAPERS.rglob("*.md"))
    if not paths and not args.candidate:
        failures.append("No canonical paper pages found.")
    for path in paths:
        try:
            if is_algorithm_path(path):
                metadata = validate_algorithm_page(path)
                if path != PAPERS / str(metadata["year"]) / f"{metadata['paper']}{ALGORITHM_SUFFIX}.md":
                    raise ValueError("canonical path must be wiki/papers/<year>/<paper>_algorithm.md")
                algorithms.append((path, metadata))
                continue
            metadata = validate_page(path)
            paper_id = metadata["id"]
            if paper_id in pages:
                raise ValueError(f"duplicate paper ID: {paper_id}")
            if path != PAPERS / str(metadata["year"]) / f"{paper_id}.md":
                raise ValueError("canonical path must be wiki/papers/<year>/<id>.md")
            pages[paper_id] = (path, metadata)
        except (ValueError, OSError, yaml.YAMLError) as error:
            failures.append(f"{path}: {error}")
    if args.candidate:
        try:
            if args.candidate.resolve().is_relative_to(PAPERS):
                raise ValueError("candidate must be outside wiki/papers")
            if read_page(args.candidate)[0].get("kind") == "algorithm":
                metadata = validate_algorithm_page(args.candidate)
                algorithms = [item for item in algorithms if item[1]["paper"] != metadata["paper"]]
                algorithms.append((args.candidate, metadata))
            else:
                metadata = validate_page(args.candidate)
                pages[metadata["id"]] = (args.candidate, metadata)
        except (ValueError, OSError, yaml.YAMLError, AttributeError) as error:
            failures.append(f"{args.candidate}: {error}")
    for path, metadata in pages.values():
        for relationship in metadata.get("relationships", []):
            target = relationship["paper"]
            if target == metadata["id"] or target not in pages:
                failures.append(f"{path}: invalid relationship target: {target}")
    failures.extend(filter(None, (check_companion(path, metadata, pages) for path, metadata in algorithms)))
    if failures:
        print("\n".join(failures), file=sys.stderr)
        return 1
    print(f"Checked {len(paths)} canonical page(s)" + (" and one candidate." if args.candidate else "."))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
