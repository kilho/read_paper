---
name: ingest-paper-algorithm
description: Write a companion algorithm walkthrough (wiki/papers/<year>/<id>_algorithm.md) for an already-ingested algorithmic paper, carrying concrete toy examples through each phase, modeled on a worked TabPFN explanation.
---

# Write an algorithm walkthrough for a paper

This skill complements the canonical paper page. It does not replace it. It writes a separate page, `wiki/papers/<year>/<id>_algorithm.md`, that follows the [algorithm schema](../../../schemas/algorithm.schema.yaml). Do not invoke `/ingest-paper` or use the paper schema here. Never modify the canonical paper page `<id>.md`.

Use it for papers whose contribution is a procedure with distinct phases, such as data generation, training, and inference. Stop for benchmarks, surveys, or articles without such a procedure.

Read the [TabPFN example](examples/arxiv-2207.01848_algorithm.md) before drafting. It is the target for structure, tone, concreteness, and depth. Imitate its moves, not its facts: write in plain language, use small numeric tables, state explicitly what the method does *not* use or output, and add "**Paper actually:**" notes next to simplifications. Every claim must come from the paper you are explaining.

1. **Resolve the paper:** Find the canonical page `wiki/papers/<year>/<id>.md` by ID or source URL. If it is missing, stop and ask the user to ingest the paper first. Copy its `title`, `year`, and `source` into the new frontmatter, and set `paper: <id>`. Reuse the pinned extract in `sources/papers/<id>/`, downloading that exact version with `pdftotext -layout` only if it is missing. If `<id>_algorithm.md` exists, revise it: make only the requested changes and keep accepted fixes.
2. **Map the algorithm before writing:** From the source, list each phase. For each phase, record:
   - its inputs and outputs;
   - which data and labels are available or hidden;
   - whether parameters are updated;
   - the exact preprocessing, objective, and reported scale.

   Also note what a reader might assume the method uses but it does not, such as names, text, or positions. Note what the method does not output, such as a causal graph or a symbolic rule. Record a section, equation, table, or appendix locator for each item. Group the locators into `S1`, `S2`, …. If the paper does not specify a step, say so rather than filling the gap.
3. **Draft per the schema:** Use exactly these H2s, in order: Core Idea, Input Contract, Phase Walkthrough, Phase Comparison, Key Distinctions, Takeaway, and Source Locators. Follow each heading's `guidance` in the schema. Cite `[S#]` in every section except Takeaway and Source Locators. Choose one running toy example and carry it through the page.
   - **Core Idea:** Contrast the conventional approach with the paper's approach as short bullet lists. Cover what is learned, and when computation happens. Then add an "**Important distinction.**" paragraph that corrects the most likely misreading.
   - **Input Contract:** Show the toy instance as a table and as the literal arrays or tokens the method receives. Answer the questions a reader would ask, such as "Does it use feature names? Label names? Positions?", each with a direct yes or no. Explain how inputs become tokens or states and what attention or access is allowed.
   - **Phase Walkthrough:** Add one H3 per phase (at least two), as numbered steps with tiny concrete inputs, intermediate values, and outputs. Use H4s for alternatives inside a phase, such as two data generators. Begin each toy example with `**Illustrative example:**`, `**Derived example:**`, or `**Paper example:**`. Label stand-in functions and put the paper's actual procedure next to them. Include the reported training scale with locators. Mark any uncomputed output, such as a probability, as illustrative.
   - **Phase Comparison:** Write a table with the first column `Aspect` and one column per phase. Include rows such as data, names used, values, labels, query labels, gradient updates, objective, parameters, and data-generating relationship. Cite the rows below the table.
   - **Key Distinctions:** Give a one-line formula contrast of what is conditioned on, such as `f_θ(x) → y` versus `f_θ(D_train, x) → y`. Add a "**Subtle point.**" about what the method does not recover.
   - **Takeaway:** State the key insight and the reusable research pattern in 3–4 numbered steps. If the reader's interests are known, add one sentence labeled as an implication, not from the paper.
   - **Source Locators:** List each frontmatter source as `- S#: locator`.
4. **Verify:** Check every number, equation, procedure step, and "does not use" claim against its locator. Recompute all toy arithmetic. Confirm that every illustrative value is labeled. Could a first-time reader trace the toy example through every phase? Could they say which parameters change in each phase?
5. **Validate and publish:** Save the draft outside `wiki/papers/` and run `python3 -m harness.check_wikilint --candidate <draft>`. If validation fails, fix the draft; do not publish. If the user asked for a draft only, show it. Otherwise:
   - Save it to `wiki/papers/<year>/<id>_algorithm.md`.
   - In `wiki/index.md`, add `  - [Algorithm walkthrough](papers/<year>/<id>_algorithm.md)` under the paper's entry.
   - Run `python3 -m harness.check_wikilint` and report any unresolved claims.
