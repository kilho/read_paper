---
name: ingest-paper
description: Turn a selected arXiv paper into a source-verified research wiki page, or prepare a correction to an existing page.
---

# Ingest a selected paper

Follow the [schema](../../../schemas/paper.schema.yaml) and use [τ-bench](../../../wiki/papers/2024/arxiv-2406.12045.md) as the style example, not a source for other papers.

1. **Read:** Pin and read the full arXiv version. Stop if unavailable. Find the canonical page at `wiki/papers/<year>/arxiv-<id>.md` using the version-free ID. For revisions, start from that page and follow the [correction workflow](../../../feedback/wiki/README.md); preserve accepted fixes and FAQ entries.
2. **Draft:** Make Overview through Evidence a standalone five-minute read, with a roughly ten-minute deeper path on the same page. Leave `topics: []` until a taxonomy exists. Start new pages with an empty FAQ.
   - **Overview / What:** State the contribution in 2–3 sentences, then clarify what it is (and what it isn't if easily confused). Name inputs, assumptions, and outputs; for benchmarks, name what's tested, what's provided, and what's measured.
   - **Terminology:** Define only essential or easily confused terms in the schema's table. Give their meaning here and why they matter.
   - **Why / When:** Explain the challenge, prior approach, gap, and main differentiator. Give a realistic task, who would use the contribution, and what needs a separate check. Put detailed comparisons in **Differentiators**.
   - **How / Worked Example:** Show the mechanism with inputs, intermediate steps, and outputs. Use a schema example label and independently check the steps or math. Put derivations in **Technical Depth**.
3. **Verify:** Check claims and numbers against the pinned source, cite exact locators, and distinguish reported results from interpretation. Flag unsupported claims. Check that readers can explain the contribution, work the example, and compare alternatives.
4. **Publish:** Save the draft outside `wiki/papers/` and run `python3 -m harness.validate --candidate <draft>`. After approval, save the canonical page, add new pages to the [index](../../../wiki/index.md), and run `python3 -m harness.validate`. Report unresolved claims or review.
