---
name: search-related
description: Find papers related to one or more seed papers by reading Related Work and following incoming and outgoing citations; save a prioritized reading shortlist.
---

# Search for related papers

1. **Identify the seeds.** Accept a paper or list by wiki path/ID, arXiv URL, DOI, OpenAlex ID, or exact title. Resolve unfamiliar publisher URLs or supplied PDFs to a stable ID or exact title from their metadata. Do not send private documents or notes to public APIs. Disambiguate before using a title match.
2. **Read each seed.** Start with its canonical wiki page and matching version in `sources/`. Read Related Work, baseline comparisons, and the bibliography. If the local extract is absent or insufficient, open the original, using a local text extraction for a lawful PDF if needed. If full text is unavailable, state that coverage is partial; provider references do not establish that the seed discusses them in depth. Record the papers most relevant to the seed or requested focus, why each matters, and the section/page that supports it.
3. **Find citing papers.** Run `python3 -m harness.search_related --preview <seed> [<seed> ...]` to retrieve OpenAlex references and later works that cite each seed. Inspect likely close matches for how they use or extend the seed, rather than assuming a citation is a substantive connection. If coverage is thin, try another catalog source or a manual Google Scholar check; verify links against publisher records. Keep OpenAlex as the single source of citation counts in the ranking. Never invent counts or use Google Scholar and OpenAlex counts interchangeably.
4. **Verify ranking evidence.** Check [Verified papers](../../../discovery/resources/bestpaper_list.md#verified-papers) first. Reuse an existing entry and its official evidence link when the paper, venue edition, and label match. Use the [resource catalog](../../../discovery/resources/resource_list.md#conference-labels-examples-not-exhaustive-coverage) to find additional candidates relevant to the seed and verify awards or presentation labels in the matching year's official program or announcement.
   - Add newly verified Best Paper, Outstanding Paper, Spotlight, or Oral papers to the verified list with the paper link, venue and year, exact label, and official evidence URL. If the paper is already listed for that edition, add only the new label and its source to the existing row. A missing label is unknown; do not treat a presentation as an award.
   - Use author or institution bonuses only for an explicitly tracked researcher or institution whose identity or publication-time affiliation is verified, not a prestige guess. These are selection signals, not evidence that claims are correct.
5. **Save the shortlist.** Write a temporary JSON array of evidence records and run `python3 -m harness.search_related --evidence <file.json> <seed> [<seed> ...]`. Each record has `paper` (DOI, arXiv ID, OpenAlex ID or exact title), `kind`, `source` (public HTTP(S) evidence URL), and `note` (what is verified and where). Add `title` when using a verified ID missing from OpenAlex. Use `related-work`, `baseline`, or `bibliography` with `seed` set to the input or its stable ID. A separately verified incoming citation can use `citing-paper` with `seed`. Use `award`, `presentation`, `author`, or `institution` for source-backed ranking signals. Citation impact leads, with bounded bonuses for context and recognition. Use `--coverage-note` to record gaps such as unavailable full text. Check the saved list for relevance to the user's focus. Do not add to the reading queue or publish wiki pages unless asked.

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
