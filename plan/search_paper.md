# Paper discovery and prioritization

This is the Phase 2 implementation plan for [Paper Discovery and Prioritization](initial_plan.md#3-paper-discovery-and-prioritization). Start with on-demand searches and a hand-curated reading queue. Discovery recommends what to read; it does not download full texts, ingest papers, or judge whether their claims are correct.

## One skill, four modes

Add `.github/skills/discover-papers/SKILL.md`. All four modes need the same source lookup, identity resolution, wiki comparison, output, and queue rules. The skill translates a request into an explicit mode, filters, and result count; Python retrieves, deduplicates, ranks or samples, and validates changes. Keep provider quirks in adapters and mode-specific ranking in code, not in separate skills. Split a skill only if a workflow later has a different purpose or approval boundary (e.g., a scheduled watchlist digest).

| Request | Mode | Candidate pool and order |
|---|---|---|
| “Find papers on conversational retrieval since 2023” | `topic` | Search OpenAlex and arXiv by title and abstract. Rank by query match, using title matches above abstract-only matches, then publication date and stable ID. Require at least one match; report materially different query terms if used. |
| “What's trending in retrieval?” | `trending` | Default to papers published in the past 90 days. Rank papers with positive citation gain across two comparable OpenAlex observations at least seven days apart by `(new_count - old_count) / days_between * 30`, a 30-day rate. Missing history is unknown, not zero. If fewer papers qualify than requested, show a separate **recent, not trending** list ordered by publication date. Add community signals later and label them by source. |
| “What are the most cited papers on retrieval?” | `cited` | Use OpenAlex citation totals within the requested topic and date filters. Report provider, count, and observation date; do not merge counts from different providers. Omit unknown counts from the ranked list, distinguish them from known zeroes, and note the age bias. |
| “Give me three random papers” | `random` | Sample without replacement from the deduplicated, eligible pool. With no filters, use the configured arXiv categories and the past 12 months. Return the seed, pool size, and pool scope. Repeatability means the same seed **and the same candidate set**, not the same live results. |

Require a topic for `topic`; let the other modes take optional topic, field, date, and venue filters. Default to five results. Use bounded queries and disclose provider failures, result caps, and cache age. If a provider fails, return clearly labeled partial results when possible; never relax explicit filters silently. For `random`, sample from the full fetched pool after filtering, not from already-ranked top picks; make clear this is not a uniform draw across all papers.

**Modes are how papers are found; tracks are why they belong on the reading list.** Keep one queue with optional `must-read`, `state-of-the-art`, or `emerging` labels (the three tracks from the initial plan). A `cited` result isn't automatically `must-read`, and a `topic` result isn't state of the art without supporting evidence. Leave the track unset if it is unclear.

## Source catalog and storage

Put the “where to find or download” catalog in `discovery/resources/`, not `sources/`. The latter is already a [Git-ignored cache of originals and extracts](../README.md#L8), populated by [ingest-paper](../.github/skills/ingest-paper/SKILL.md#L10-L12) after selection.

| Path | Purpose |
|---|---|
| `discovery/resources/README.md` | Human reference: source coverage, supported signals, official docs, open full-text routes, access limitations, and date last checked. |
| `discovery/resources/providers.yaml` | Machine config: provider IDs, capabilities, enabled flags, endpoint or feed URL, and request budget. Credentials stay in environment variables; never commit them. |
| `discovery/topics.yaml` | Optional reusable topic aliases and arXiv categories for default searches. Independent of wiki `topics` tags. |
| `discovery/reading-queue.yaml` | Tracked, human-editable to-read list and decisions; not a paper metadata catalog. |
| `discovery/.cache/` | Git-ignored normalized search responses and provider-scoped citation snapshots with observation dates; no PDFs or credentials. Refresh on demand at first. |
| `schemas/reading-queue.schema.yaml`, `harness/discover.py`, `tests/test_discovery.py` | Queue contract, command entry point, and offline fixture tests. Add provider modules as needed. |

| Resource | Use and full-text route |
|---|---|
| [arXiv API](https://info.arxiv.org/help/api/user-manual.html) | Topic search and recent preprints. Return the abstract page and any PDF link supplied by arXiv. |
| [OpenAlex API](https://help.openalex.org/api/) | Topic search, publication metadata, DOI, and citation totals. Return an open-access location if supplied; otherwise return the landing page and mark full-text access unknown. |
| [OpenReview](https://openreview.net/) and [ACL Anthology](https://aclanthology.org/) | Add later for venue-specific results and official paper pages. Take award and presentation labels from the venue's official program or announcement, not from search snippets. |
| [Hugging Face Daily Papers](https://huggingface.co/papers) and lab or researcher watchlists | Add later for community attention and emerging work. Record the source and what the signal actually measures; it is not a citation or quality score. |

## From search results to the wiki

1. **Resolve identity before ranking.** Normalize version-free arXiv IDs and DOI spellings, keep all verified aliases, and collapse records that share an identifier or are explicitly linked by a source. Prefer an existing wiki ID, then a confirmed arXiv ID, then DOI, then stable provider ID for new queue entries. A similar title and author list is a review hint, not enough to merge a preprint and conference record. Do not assign new wiki IDs in discovery; ingestion owns that decision.
2. **Make ranking knowledge-aware.** Build a lookup from canonical wiki frontmatter and page titles on each run. Exclude exact wiki matches from recommendations by default (allow `include_known`); label already-queued candidates instead of treating them as new. Compare remaining candidates' title and abstract with the nearest wiki entries using shared terms, then show a linked **what's new to this wiki** note: e.g., “same retrieval task as [wiki entry], but evaluates multi-turn reformulation instead of indexing.” Use wiki entries as a proxy for accumulated knowledge, not proof the reader has read them. If no good comparison exists, say so. Once these comparisons are reliable, let verified complementarity break close `topic` ties; do not override the explicit `cited`, `trending`, or `random` order. Do not depend on populated `topics` or infer typed relationships automatically.
3. **Return a short list with reasons.** Each result includes a stable ID, title, year and venue if known, landing page, optional lawful full-text link, relevant metric and date, why it ranked, and a linked comparison when available. Put mode, filters, sources, result limits, and partial-coverage warnings in the result header. Citations, momentum, and awards are selection signals, not evidence that a claim is correct.
4. **Save only selected items.** Searching is read-only except for the local cache. An explicit add or a user's approval upserts the selected paper by ID or verified alias, validates the proposed `reading-queue.yaml`, and writes it atomically. Preserve the existing queue ID and manual priority, track, status, and notes on re-add. Never rewrite the queue silently on a fresh search or refresh.
5. **Read and ingest separately.** Queue statuses are `to-read`, `reading`, `read`, and `skipped`; priorities are `high`, `normal`, and `low`. Show `to-read` and `reading` first, ordered by explicit priority and then oldest `added_on`. Marking a paper read does not require ingestion. An accepted wiki page can be linked with `wiki_id` but does not automatically mark a paper read. To ingest, hand the approved link to `ingest-paper` for full-source verification, caching, and publication review.

Each queue entry stores `id`, `title`, `url`, `added_on`, `status`, `priority`, and `why_read`; optional fields are `aliases` (verified alternative IDs), `track`, `wiki_id`, and `notes`. Store a short reason to read, not provider payloads, citation histories, or copies of wiki explanations. Use `notes` to record why a paper was skipped if helpful.

## Build order and acceptance checks

1. **First usable slice: topic search and queue.** Build the source catalog, arXiv adapter, normalized candidate shape, wiki/queue lookup, search output, and explicit add/list/status commands. Test a search with a duplicate arXiv version, a paper already in the wiki, and a selected paper added twice. The second add must preserve hand-edited priority and notes. A search alone must not change any tracked files.
2. **Add OpenAlex, `cited`, and `random`.** Test linked DOI/arXiv duplicates versus title-only similarities, known zero versus missing citations, and a repeatable random draw from the same fixture pool. Verify an unavailable provider leaves a visible warning and does not erase queue data.
3. **Add `trending` and useful wiki comparisons.** Cache citation observations on searches or explicit refreshes. Test two dated observations, insufficient history, an older paper outside the window, and a large total with slower recent growth. Check that the recent fallback is never labeled trending. Test that a topical result can point to what a nearby wiki entry does not cover without marking a user as having read it.
4. **Expand only after the on-demand flow works.** Add venue/award adapters, watchlists, community feeds, and optional scheduled refresh in that order as needed. Keep refresh read-only with respect to the queue unless the user opts into a separate workflow.

Use offline provider fixtures for ranking and queue tests; make one opt-in live smoke check per enabled adapter. MVP acceptance: ask for a topic, get a short, explained list with source links, save one paper, and see it in the to-read list without creating or changing a wiki page. Phase 2 acceptance adds all four modes and the wiki comparison described above.
