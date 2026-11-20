---
name: ingest-paper
description: Turn an arXiv paper, conference paper, blog post, or news article into a source-verified wiki page, or revise an existing entry.
---

# Ingest a selected paper

Follow the [schema](../../../schemas/paper.schema.yaml) and use [τ-bench](../../../wiki/papers/2024/arxiv-2406.12045.md) as the style example, not a source for other papers.

1. **Read:** Open the full source; stop if only an abstract or snippet is available. Pin the version when available; otherwise use the canonical URL. Reuse an existing entry for the same work, even from a different link. Keep arXiv IDs version-free; otherwise use a stable lowercase slug prefixed with `conference-`, `blog-`, `news-`, or `web-`. Store entries at `wiki/papers/<year>/<id>.md`. For revisions, follow the [correction workflow](../../../feedback/wiki/README.md) and preserve accepted fixes and FAQ entries.
2. **Draft:** Make Overview through Evidence a standalone five-minute read, with optional depth on the same page. Use the publication year and listed byline (or `authors: []` for unsigned non-arXiv sources). Leave `topics: []` until a taxonomy exists and start with an empty FAQ.
   - **Overview / What:** State the contribution in 2–3 sentences, then clarify what it is (and what it isn't if easily confused). Name inputs, assumptions, and outputs; for benchmarks, name what's tested, what's provided, and what's measured.
   - **Terminology:** Define only essential or easily confused terms in the schema's table. Give their meaning here and why they matter.
   - **Why / When:** Explain the challenge, prior approach, gap, and main differentiator. Give a realistic task, who would use the contribution, and what needs a separate check. Put detailed comparisons in **Differentiators**.
   - **How / Worked Example:** Show the mechanism with inputs, intermediate steps, and outputs. Use a schema example label and independently check the steps or math. Put derivations in **Technical Depth**.
   - **Articles without a method:** Explain the main claim and evidence rather than inventing a mechanism or result. Use the schema's not-applicable text only when there is no specialized terminology or no procedure to demonstrate.
3. **Verify:** Cite exact locators (headings or paragraphs for web articles). For news and commentary, distinguish what the author reports from what primary evidence establishes. Flag unsupported claims. Check that readers can explain the contribution and, where applicable, work the example and compare alternatives.
4. **Publish:** Save the draft outside `wiki/papers/` and run `python3 -m harness.validate --candidate <draft>`. After approval, save the canonical page, add new pages to the [index](../../../wiki/index.md), and run `python3 -m harness.validate`. Report unresolved claims or review.
