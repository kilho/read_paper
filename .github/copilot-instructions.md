# Copilot instructions

- Optimize for understanding, not summary volume. Prioritize the [paper-understanding MVP](../plan/initial_plan.md#phase-1-paper-understanding-mvp) before discovery or automation.
- Keep one canonical Markdown page per paper, with metadata and typed links in frontmatter. Derive indexes and graphs from the wiki.
- Follow [ingest-paper](skills/ingest-paper/SKILL.md) for authoring and the [schema](../schemas/paper.schema.yaml) for structure. Ground claims in sources; popularity is not evidence. Use deterministic code for validation, ID resolution, and deduplication.
- Keep schemas, workflow skills, task prompts, and harness orchestration separate.
- After answering a paper question, append a concise, sourced H3 Q&A to its **FAQ** unless it is already covered. Leave the rest of the page unchanged and validate.
- Preserve accepted [corrections](../feedback/wiki/README.md). Propose skill or prompt changes for recurring issues in a pull request with evaluation results for human approval.
