# read_paper

A Git-based research wiki focused on understanding papers, not just summarizing them.

Start with the [wiki index](wiki/index.md) and the [τ-bench entry](wiki/papers/2024/arxiv-2406.12045.md). To add a selected paper, use the [ingest-paper skill](.github/skills/ingest-paper/SKILL.md). To propose a fix, follow the [correction workflow](feedback/wiki/README.md).

Use the [τ-bench comprehension check](evals/comprehension/arxiv-2406.12045.md) to test the five-minute reading path.

## Validate the wiki

With Python 3.10 or later:

```sh
python3 -m pip install -r requirements.txt
python3 -m harness.validate
python3 -m unittest discover -s tests
```

Use `python3 -m harness.validate --candidate /path/to/draft.md` to validate a proposed page without publishing it. Validation checks structure and reference consistency, not whether the paper supports a claim.
