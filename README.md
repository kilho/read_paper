# read_paper

Browse the [research wiki](wiki/index.md) or try its [five-minute comprehension check](evals/comprehension/arxiv-2406.12045.md).
To add an entry, give [ingest-paper](.github/skills/ingest-paper/SKILL.md) an arXiv, conference, blog, or news URL. To revise one, follow the [correction workflow](feedback/wiki/README.md).

## Validate the wiki

With Python 3.10 or later:

```sh
python3 -m pip install -r requirements.txt
python3 -m harness.validate
python3 -m unittest discover -s tests
```

Check an unpublished draft with `python3 -m harness.validate --candidate /path/to/draft.md`. This checks structure and references, not factual accuracy.
