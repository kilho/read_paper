---
name: explain-detail
description: Add source-verified Evidence and Technical Depth to an existing research wiki entry, or expand a requested topic within either section.
---

# Explain a paper in detail

1. **Find the entry:** Accept a wiki path, paper ID, title, or source URL, plus an optional focus (e.g., a metric, derivation, or ablation). Start from the canonical wiki page and its pinned source. Reuse its local extract; check the original for figures, equations, or ambiguous text. If no entry exists, use [ingest-paper](../ingest-paper/SKILL.md) first.
2. **Expand on demand:** With no specific focus, add or refine both sections for a roughly ten-minute technical reading path. With a focus, update only the relevant section; preserve unrelated material. Follow the [schema's heading order](../../../schemas/paper.schema.yaml).
   - **Evidence:** Explain the evaluation setup, metrics, and closest baselines; report key results and informative ablations where available. State what the results support and what they do not establish. For articles without experiments, assess the claims and supporting sources instead of inventing results.
   - **Technical Depth:** Explain the detailed mechanism and define notation. Include key equations, training and inference steps (or the evaluation and scoring workflow for a benchmark), and a checked numerical or step-by-step example where useful. For deeper requests, add derivations, pseudocode, implementation references, or limitations only as relevant and supported.
3. **Verify and publish:** Check claims, numbers, and examples against exact source locators. Reuse citation IDs or add new ones to both frontmatter and Source Locators. Preserve the core explanation, accepted corrections, and FAQ. Check that the draft addresses the request, then run `python3 -m harness.check_wikilint --candidate <draft>` on a draft outside `wiki/papers/`. If validation fails, do not change the canonical page. If the user asks for a draft or review before applying, show the diff and leave the canonical page unchanged. Otherwise, apply the validated diff to the canonical wiki page without a separate approval prompt, run `python3 -m harness.check_wikilint`, and report the updated path.
