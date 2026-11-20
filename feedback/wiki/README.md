# Wiki corrections

1. Save a `proposed` record here: paper ID, section, requested fix, and source (or mark it as a clarity request).
2. Draft from the canonical page, verify against its source, and run `python3 -m harness.validate --candidate <draft>`.
3. Show the diff. After human approval, apply it, run `python3 -m harness.validate`, and retain the record as `accepted` with the reviewer noted. Self-review is not approval.

Keep paper-specific fixes out of reusable skills.
