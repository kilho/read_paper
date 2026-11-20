# Wiki corrections

1. Record the paper ID, affected section, requested change, and supporting source (or mark it as a clarity request). Save the record in this directory with status `proposed`.
2. Start from the current canonical file, not a fresh generation. Make a separate draft, verify the change against the pinned source, and run `python3 -m harness.validate --candidate <draft>`.
3. Present the focused diff for review. After the reviewer approves it, apply the change, mark the feedback `accepted`, and run `python3 -m harness.validate`. Retain the record so future ingestions carry forward the correction. Record who or what reviewed the change; a self-review is not human approval.

Keep paper-specific corrections out of reusable skills. A recurring issue can motivate a separate, evaluated skill change.
