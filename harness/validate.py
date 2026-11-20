import argparse
import re
import sys
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator


ROOT = Path(__file__).resolve().parents[1]
PAPERS = ROOT / "wiki" / "papers"
SCHEMA = yaml.safe_load((ROOT / "schemas" / "paper.schema.yaml").read_text(encoding="utf-8"))
VALIDATOR = Draft202012Validator(SCHEMA)


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


def validate_page(path):
    metadata, body = read_page(path)
    errors = [
        f"{error.json_path}: {error.message}"
        for error in VALIDATOR.iter_errors(metadata)
    ]
    if errors:
        raise ValueError("; ".join(errors))

    paper = metadata["id"].removeprefix("arxiv-")
    if metadata["source"]["url"] != f"https://arxiv.org/pdf/{paper}{metadata['source']['version']}":
        errors.append("source URL must match the paper ID and version")
    if re.findall(r"^# (.+)$", body, re.M) != [metadata["title"]]:
        errors.append("expected one H1 matching the frontmatter title")

    parts = re.split(r"^## (.+)$", body, flags=re.M)
    headings = parts[1::2]
    sections = dict(zip(headings, parts[2::2]))
    rules = SCHEMA["x-page"]
    if headings != rules["headings"]:
        errors.append("expected these H2 sections in order: " + ", ".join(rules["headings"]))
    errors.extend(
        f"empty section: {name}"
        for name, content in sections.items()
        if not content.strip() and name not in rules["allow_empty"]
    )
    columns = rules["terminology_columns"]
    if not has_terminology_table(sections.get("Terminology", ""), columns):
        errors.append("Terminology must be a Markdown table with nonempty rows: " + " | ".join(columns))
    if not any(f"**{label}:**" in sections.get("Worked Example", "") for label in rules["example_types"]):
        errors.append("Worked Example must include a recognized example label")

    citable_text = "\n".join([parts[0], *(content for name, content in sections.items() if name != "Source Locators")])
    citations = set(re.findall(r"\[(S[0-9]+)\]", citable_text))
    sources = metadata["sources"]
    unknown = citations - sources.keys()
    if unknown:
        errors.append("unknown source IDs: " + ", ".join(sorted(unknown)))
    if not re.search(r"\[S[0-9]+\]", sections.get("Evidence", "")):
        errors.append("Evidence must cite a source ID")
    expected_locators = {f"- {key}: {value}" for key, value in sources.items()}
    if expected_locators != set(sections.get("Source Locators", "").strip().splitlines()):
        errors.append("Source Locators must list each frontmatter source as '- ID: locator'")
    if errors:
        raise ValueError("; ".join(errors))
    return metadata


def main(argv=None):
    parser = argparse.ArgumentParser(description="Validate canonical paper pages and an optional draft.")
    parser.add_argument("--candidate", type=Path, help="validate a draft outside wiki/papers without publishing it")
    args = parser.parse_args(argv)
    pages = {}
    failures = []
    paths = sorted(PAPERS.rglob("*.md"))
    if not paths and not args.candidate:
        failures.append("No canonical paper pages found.")
    for path in paths:
        try:
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
            metadata = validate_page(args.candidate)
            pages[metadata["id"]] = (args.candidate, metadata)
        except (ValueError, OSError, yaml.YAMLError) as error:
            failures.append(f"{args.candidate}: {error}")
    for path, metadata in pages.values():
        for relationship in metadata.get("relationships", []):
            target = relationship["paper"]
            if target == metadata["id"] or target not in pages:
                failures.append(f"{path}: invalid relationship target: {target}")
    if failures:
        print("\n".join(failures), file=sys.stderr)
        return 1
    print(f"Validated {len(paths)} canonical page(s)" + (" and one candidate." if args.candidate else "."))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
