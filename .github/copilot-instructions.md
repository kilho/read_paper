# Copilot instructions

## Project direction

- Optimize for research understanding, not summary volume. The default reading path should teach a paper's contribution and core mechanism in about five minutes, with a deeper technical path of about ten minutes.
- Prioritize the paper-understanding MVP: a paper schema, ingestion, worked examples, source verification, and human corrections. Follow the roadmap in [the initial plan](../plan/initial_plan.md) before expanding into automated discovery, cross-paper synthesis, or automated skill improvement.

## Wiki content and storage

- Treat wiki Markdown as the source of truth for research knowledge. Keep metadata and typed relationships in page frontmatter and cross-references. Derive search indexes and graphs from the wiki rather than maintaining a second knowledge store.
- Maintain one canonical page per paper. Put the concise reading path first and expand it with equations, implementation details, and evidence on the same page. Do not maintain separate summaries for each reading depth.
- Structure paper entries as TL;DR, What, Why, When, How, Worked Example, Differentiators, Evidence, and Relationships. Define essential terms in context, state assumptions and failure conditions, and compare with the closest supported baselines.
- Give each important algorithm a worked example with inputs, intermediate steps, and outputs. Label it as a **paper example**, **derived example**, or **illustrative example**, and check the reasoning or calculations.
- Ground technical claims, reported results, and comparisons in identifiable sources. Flag unsupported claims instead of filling gaps. Use awards, citations, and reputation to prioritize reading, not to establish correctness.

## Implementation and review

- Use versioned, page-type-specific schemas. Validate required fields, sections, and relationships before accepting generated pages. Use deterministic code for schema checks, identifier resolution, and deduplication.
- Keep schemas, skills, prompts, and the harness separate: schemas define content contracts, skills define reusable workflows, prompts handle focused tasks, and the harness orchestrates and validates execution.
- Apply human corrections to the wiki and preserve correct content. Do not automatically change skills or prompts after one correction. Propose changes for recurring issues in a pull request with evaluation results for human approval.
- Evaluate whether readers can explain the method, work through an example, and compare it with alternatives within the target reading time. Schema compliance alone is not evidence of understanding.
