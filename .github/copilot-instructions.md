# Copilot instructions

- Optimize for understanding, not summary volume. Prioritize the [paper-understanding MVP](../plan/initial_plan.md#phase-1-paper-understanding-mvp) before discovery or automation.
- Keep one canonical Markdown page per paper or article, with metadata and typed links in frontmatter. Derive indexes and graphs from the wiki.
- Follow [ingest-paper](skills/ingest-paper/SKILL.md) for authoring and the [schema](../schemas/paper.schema.yaml) for structure. Ground claims in sources; popularity is not evidence. Use deterministic code for validation, ID resolution, and deduplication.
- In **What**, state what the contribution is, what goes in, and what comes out or is measured. If it resembles something readers might confuse it with, name that alternative early and explain the key distinction: "This is X, not Y."
- In **Why**, separately explain why the challenge matters, how named prior work tackled it and what it missed, and what this paper does differently and why. In **When**, give a concrete reader use case and say what needs a separate check.
- Teach essential terms in context and walk through a checked example from input to outcome. A page that passes schema validation is not necessarily understandable; review whether a new reader can explain the setup, distinguish it from prior work, and apply the example.
- Keep schemas, workflow skills, task prompts, and harness orchestration separate.
- For paper questions, check the wiki and matching local extract in `sources/` before re-fetching; consult the original when the extract is insufficient. Append a concise, sourced H3 Q&A to the **FAQ** unless already covered. Leave the rest of the page unchanged and validate.
- Preserve accepted [corrections](../feedback/wiki/README.md) in the wiki without creating separate feedback records unless requested. Use [improve-skill](skills/improve-skill/SKILL.md) to review the latest commit for recurring workflow gaps. Propose skill or prompt changes in a pull request with evaluation results for human approval.
