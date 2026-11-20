---
name: improve-skill
description: Review the latest local commit for recurring workflow gaps and propose evaluated updates to reusable skills.
---

# Improve a skill from the latest commit

1. **Inspect:** From the repository root, pin `git rev-parse HEAD`, then run `git --no-pager show --root --diff-merges=first-parent <sha>` using that SHA. Compare a merge with its first parent; ignore staged and unstaged changes as evidence.
2. **Triage:** Read the relevant `SKILL.md` and look for corroboration in [accepted wiki corrections](../../../feedback/wiki/) or earlier commits. Cite the triggering SHA and changed paths. Skip normal content additions, one-off fixes, and guidance the skill already covers. If no recurring gap is supported, report why and stop without editing.
3. **Propose:** Draft the smallest actionable change in the skill that owns the workflow. State when the new guidance applies and what outcome should change. Keep paper facts out of skills; route schema or harness changes separately. Do not overwrite local edits.
4. **Evaluate:** Compare the old and proposed instructions on the triggering case and one independent case that should still work. Record the expected and observed behavior, checks run, and limitations; distinguish a walkthrough from an executed test.
5. **Review:** Present the proposed diff and evaluation. When authorized to open a PR, put only the proposal on a dedicated branch and open a draft PR with the evidence and results. Leave merge and adoption to human review.
