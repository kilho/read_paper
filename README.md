# read_paper

Browse the [research wiki](wiki/index.md).

## Use the skills

Call a skill in Copilot CLI with `/<skill> <inputs>`. A paper can be given as a URL, an arXiv ID, a wiki ID or path (`@wiki/papers/...`), or an exact title. Add plain-language instructions after the inputs to narrow the task.

A typical reading loop:

1. `/ingest-paper <url>`: add a paper to the wiki.
2. `/search-related <paper> [focus terms]`: find what to read next.
3. `/ingest-paper-batch @discovery/related/<report>.md top 3`: ingest the best candidates and link them to the existing entries.
4. `/explain-detail <paper> [focus]`: go deeper on a paper you care about.
5. Ask questions about a paper. Answers are added to its **FAQ**.

### [ingest-paper](.github/skills/ingest-paper/SKILL.md)

Turns an arXiv, conference, blog, or news source into a source-verified wiki page, or revises an existing page.

| Call | Effect |
| --- | --- |
| `/ingest-paper https://arxiv.org/pdf/2404.07972` | Creates a new entry from the source (an existing entry for the same work is reused). |
| `/ingest-paper arxiv-2404.07972 fix the worked example to use Figure 3` | Revises only what you asked and keeps the rest of the page. |
| `/ingest-paper <url> draft only` | Shows the draft without publishing it. |

### [search-related](.github/skills/search-related/SKILL.md)

Reads a seed's Related Work, screens papers that cite it, and saves a ranked shortlist under `discovery/related/`.

| Call | Effect |
| --- | --- |
| `/search-related arxiv-2611.14320` | Seed only: finds references the seed discusses and later papers that cite it. |
| `/search-related arxiv-2611.14320 arxiv-2404.07972` | Multiple seeds: one combined shortlist. |
| `/search-related arxiv-2611.14320 AWM ReasoningBank` | Seed plus focus terms: also searches papers, blogs, docs, and code on those terms. Results not linked to the seed are listed under **Focus findings**. |
| `/search-related AWM ReasoningBank` | Focus terms only: uses the paper currently under discussion as the seed. |

Seeds are IDs, URLs, DOIs, wiki paths, or quoted exact titles, such as `"Agent Workflow Memory"`. Unquoted names, acronyms, methods, terms, or tricks are treated as focus terms. The skill first finds where the seed mentions each focus term to work out what it means, then searches for it. It asks if an input could be either a seed or a focus term.

For a citation-only preview without saving a report, run `python3 -m harness.search_related --preview arxiv-2406.12045`. Set `OPENALEX_API_KEY` if you need a higher OpenAlex request quota.

### [ingest-paper-batch](.github/skills/ingest-paper-batch/SKILL.md)

Ingests several papers, each in a fresh CLI process, then runs one more process to compare them and add links between them.

| Call | Effect |
| --- | --- |
| `/ingest-paper-batch <paper> <paper> ...` | Ingests the listed papers (titles, IDs, URLs, or wiki paths). |
| `/ingest-paper-batch @discovery/related/terminal-bench-2026-11-21.md top 3, skip the seed; compare with Terminal-Bench` | Selects papers from a shortlist, applies the filters, and compares them with an existing entry. |

Papers already in the wiki are skipped. The runner also accepts already-selected papers directly: `python3 -m harness.ingest_paper_batch --help`.

### [explain-detail](.github/skills/explain-detail/SKILL.md)

Adds the **Evidence** and **Technical Depth** sections to an existing entry.

| Call | Effect |
| --- | --- |
| `/explain-detail arxiv-2611.14320` | Adds or refines both sections, about a ten-minute technical read. |
| `/explain-detail arxiv-2611.14320 the regression metric` | Expands only the section that covers the focus, such as a metric, derivation, or ablation. |

### [improve-skill](.github/skills/improve-skill/SKILL.md)

`/improve-skill` takes no inputs. It reviews the latest commit for recurring workflow gaps and proposes an evaluated change to a skill or task prompt. It does not edit anything if it finds no gap.

`sources/` is a local, Git-ignored cache of originals and searchable extracts for follow-up questions. A fresh clone can rebuild it from the source URLs in wiki frontmatter.

## Lint the wiki

With Python 3.10 or later:

```sh
python3 -m pip install -r requirements.txt
python3 -m harness.check_wikilint
python3 -m unittest discover -s tests
```

Check an unpublished draft with `python3 -m harness.check_wikilint --candidate /path/to/draft.md`. This checks structure and references, not factual accuracy.
