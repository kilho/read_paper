---
name: ingest-paper
description: Turn a selected arXiv paper into a source-verified research wiki page, or prepare a correction to an existing page.
---

# Ingest a selected paper

1. Resolve the supplied arXiv URL to an exact version and read that version of the full paper. Use the version-free arXiv ID to locate the canonical page under `wiki/papers/<year>/`. Stop if the primary source is unavailable rather than writing from the abstract alone.
2. Read [the paper schema](../../../schemas/paper.schema.yaml). If the page exists, start from that page and check [the feedback directory](../../../feedback/wiki/) before editing. Carry forward accepted corrections unless new evidence contradicts them; explicitly flag any proposed reversal.
3. Use a five-minute core and add deeper technical material to the same page. State the problem, assumptions, mechanism, and closest supported alternatives. Walk through an input, intermediate steps, and output. Label the example as paper, derived, or illustrative and recompute its result independently.
4. Review the draft against the pinned source. Attach section, equation, figure, or table locators to the claims they support. Verify numerical results against the actual table or figure and separate author-reported findings from interpretation. Do not treat structural validation as factual verification.
5. Write the candidate outside `wiki/papers/` and run `python3 -m harness.validate --candidate <draft>` from the repository root. For a revision, show the diff against the canonical page and wait for approval before replacing it. Capture feedback as described in the [correction workflow](../../../feedback/wiki/README.md).
6. Once publishing is authorized, save the canonical page and add its index entry if new. Run `python3 -m harness.validate` again. Report what was verified and whether any claim or human review remains outstanding.
