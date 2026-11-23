---
name: search-related
description: Find papers related to one or more seed papers by reading Related Work, following incoming and outgoing citations, and searching any user-given focus terms; save a prioritized reading shortlist.
---

# Search for related papers

1. **Identify the seeds and focus terms.** Accept a paper or list by wiki path/ID, arXiv URL, DOI, OpenAlex ID, or exact title. Resolve unfamiliar publisher URLs or supplied PDFs to a stable ID or exact title from their metadata. Do not send private documents or notes to public APIs. Disambiguate before using a title match.
   - The user may add focus terms, such as `/search-related AWM ReasoningBank`. These can be paper names, acronyms, terminology, methods, or tricks mentioned in a seed. Treat an argument as a seed if it is any accepted seed input above: a wiki path/ID, URL, DOI, OpenAlex ID, or quoted exact title that you have disambiguated to one paper. Treat other arguments, including unquoted short names or acronyms, as focus terms. If an argument could be either a seed or a focus term, ask. If no seed is given, use the paper under discussion. If the seed is unclear, ask. Pass only seeds to the harness.
   - Resolve each focus term in the seed first. Find where the seed mentions it, which reference it cites, and the role it plays, such as a baseline, a component, or prior work. Use that context to disambiguate acronyms before searching.
2. **Select related work from each seed.** Start with its canonical wiki page and matching extract in `sources/`; open the original if the extract is missing or incomplete. Read the seed's Related Work and baseline comparisons, and use the bibliography to resolve references. Select papers the seed substantively discusses in connection with the same problem, method, or evaluation, or that directly address the user's focus. Record the concrete overlap and the seed's section or page. A bibliography entry or OpenAlex reference alone is not enough. If you cannot inspect the source, disclose the gap instead of presenting unreviewed references as recommendations.
3. **Screen later citing papers.** Use `python3 -m harness.search_related --preview <seed> [<seed> ...]` to gather leads from OpenAlex, not as the final shortlist. Read the abstract of every later citing paper you plan to recommend. If the abstract is unclear, check the introduction, methods, or citation context. Keep it only if you can explain what problem it tackles and how that overlaps with the seed or the user's focus. Exclude incidental mentions and broad topic overlap without a concrete connection. If coverage is thin, check another catalog source or Google Scholar manually and verify the citation. Use OpenAlex alone for citation counts.
4. **Search each focus term.** Search beyond the citation graph for the focus term's original paper, follow-up or competing papers, and blogs, official docs, or code repositories that explain it. Open each item before keeping it. Keep it only if you can state how it explains, extends, or competes with the focus term as used in the seed. Prefer primary sources such as the original paper, author or lab posts, and official repositories over secondary summaries. Do not treat popularity as evidence.
5. **Verify ranking evidence.** Check [Verified papers](../../../discovery/resources/bestpaper_list.md#verified-papers) first. Reuse an existing entry and its official evidence link when the paper, venue edition, and label match. Use the [resource catalog](../../../discovery/resources/resource_list.md#conference-labels-examples-not-exhaustive-coverage) to find additional candidates relevant to the seed and verify awards or presentation labels in the matching year's official program or announcement.
   - Add newly verified Best Paper, Outstanding Paper, Spotlight, or Oral papers to the verified list with the paper link, venue and year, exact label, and official evidence URL. If the paper is already listed for that edition, add only the new label and its source to the existing row. A missing label is unknown; do not treat a presentation as an award.
   - Use author or institution bonuses only for an explicitly tracked researcher or institution whose identity or publication-time affiliation is verified, not a prestige guess. These are selection signals, not evidence that claims are correct.
6. **Save only screened papers.** Write a temporary JSON array of evidence records and run `python3 -m harness.search_related --require-relevance --evidence <file.json> <seed> [<seed> ...]`. Each record has `paper` (DOI, arXiv ID, OpenAlex ID or exact title), `kind`, `source` (public HTTP(S) evidence URL), and `note` (the concrete overlap and where it is supported). For a paper selected from the seed, use `related-work` or `baseline` and cite the relevant seed passage. For a screened later paper, use `citing-paper` and cite its abstract or the section read. Set `seed` to the input or its stable ID. Add `title` for a verified ID missing from OpenAlex. Use `award`, `presentation`, `author`, or `institution` only as ranking signals for candidates that passed review. Citation impact leads within the screened set. Use `--coverage-note` for gaps and return fewer results rather than padding the list. Record a focus-term paper as `related-work` or `baseline` when the seed discusses it, or as `citing-paper` when it cites the seed. The harness ranks only works linked to a seed, so list other focus-term papers, blogs, docs, and repositories under a separate **Focus findings** heading. Give each item a title, a link, the matching focus term, and a one-line note about its connection to the seed. Do not add to the reading queue or publish wiki pages unless asked.

Example evidence:

```json
[
  {
    "paper": "<verified candidate DOI or arXiv ID>",
    "seed": "<seed input>",
    "kind": "related-work",
    "source": "https://example.org/replace-with-seed-source",
    "note": "<exact source locator and verified relevance>"
  }
]
```
