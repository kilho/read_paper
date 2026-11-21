# read_paper

Browse the [research wiki](wiki/index.md) or try its [five-minute comprehension check](evals/comprehension/arxiv-2406.12045.md).
Use [ingest-paper](.github/skills/ingest-paper/SKILL.md) with an arXiv, conference, blog, or news URL to add an entry, or with an existing entry to revise it.
Use [explain-detail](.github/skills/explain-detail/SKILL.md) with an existing entry and an optional focus to add deeper evidence or technical explanation.
Use [search-related](.github/skills/search-related/SKILL.md) with one or more seed papers to inspect Related Work and save a ranked list of references and citing papers. For a citation-only preview, run `python3 -m harness.search_related --preview arxiv-2406.12045`. Omit `--preview` to save a new report under `discovery/related/`. Set `OPENALEX_API_KEY` if you need a higher OpenAlex request quota.
Use [improve-skill](.github/skills/improve-skill/SKILL.md) to review the latest commit for reusable workflow improvements.

`sources/` is a local, Git-ignored cache of originals and searchable extracts for follow-up questions. A fresh clone can rebuild it from the source URLs in wiki frontmatter.

## Lint the wiki

With Python 3.10 or later:

```sh
python3 -m pip install -r requirements.txt
python3 -m harness.check_wikilint
python3 -m unittest discover -s tests
```

Check an unpublished draft with `python3 -m harness.check_wikilint --candidate /path/to/draft.md`. This checks structure and references, not factual accuracy.
