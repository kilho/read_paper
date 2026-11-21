---
name: improve-skill
description: Review the latest local commit for recurring workflow gaps and propose evaluated updates to reusable skills or task prompts.
---

# Improve reusable guidance from the latest commit

1. **Inspect:** From the repository root, pin `git rev-parse HEAD`, then run `git --no-pager show --root --diff-merges=first-parent <sha>` using that SHA. Compare a merge with its first parent; ignore staged and unstaged changes as evidence.
2. **Triage:** Read the relevant skill or task prompt. Look for corroboration in earlier commits, including source-verified corrections that a human approved and that were applied to canonical wiki pages. Also use retained feedback summaries in relevant GitHub issues or pull requests when available. Drafts and self-review are not acceptance. Skip normal content additions, one-off fixes, and guidance that already exists. If no recurring gap is supported, report why and stop without editing.
3. **Propose:** Draft the smallest actionable change in the skill or task prompt that owns the workflow. State when the new guidance applies and what outcome should change. Keep paper facts out of reusable guidance; route schema or harness changes separately. Do not overwrite local edits.
4. **Evaluate:** Compare the old and proposed instructions on the triggering case and one independent case that should still work. Record the expected and observed behavior, checks run, and limitations; distinguish a walkthrough from an executed test.
5. **Verify coverage:** Before presenting the proposal or opening a PR, match each in-scope feedback item and relevant change from the triggering commit to the exact proposed instruction. Check the reverse too: each proposed edit must be supported by that evidence. Fix omissions or partial coverage and recheck. Explain intentional exclusions in the review. Keep raw feedback and the working coverage mapping out of tracked files; cite relevant feedback summaries in the proposal.
6. **Review:** Present the proposed diff and evaluation. When authorized to open a PR, put only the proposal on a dedicated branch and open a draft PR with the evidence and results. Leave merge and adoption to human review.
