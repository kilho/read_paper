# read_paper

Browse the [research wiki](wiki/index.md) or try its [five-minute comprehension check](evals/comprehension/arxiv-2406.12045.md).
Use [ingest-paper](.github/skills/ingest-paper/SKILL.md) with an arXiv, conference, blog, or news URL to add an entry, or with an existing entry to revise it.
Use [explain-detail](.github/skills/explain-detail/SKILL.md) with an existing entry and an optional focus to add deeper evidence or technical explanation.
Use [improve-skill](.github/skills/improve-skill/SKILL.md) to review the latest commit for reusable workflow improvements.

`sources/` is a local, Git-ignored cache of originals and searchable extracts for follow-up questions. A fresh clone can rebuild it from the source URLs in wiki frontmatter.

## Validate the wiki

With Python 3.10 or later:

```sh
python3 -m pip install -r requirements.txt
python3 -m harness.validate
python3 -m unittest discover -s tests
```

Check an unpublished draft with `python3 -m harness.validate --candidate /path/to/draft.md`. This checks structure and references, not factual accuracy.
