# Concrete walkthroughs for algorithmic papers

- **Affected workflow:** [ingest-paper-algorithm skill](../.github/skills/ingest-paper-algorithm/SKILL.md) and the [algorithm schema](../schemas/algorithm.schema.yaml). This feedback was prompted by the generic [TabPFN page](../wiki/papers/2023/arxiv-2207.01848.md).
- **Expected improvement:** For method papers, add a companion `<id>_algorithm.md` page alongside the canonical paper page, without replacing it. The page should:
  - show the input contract, including information the method does not use;
  - trace labeled toy examples through each phase;
  - contrast the phases in a table;
  - define terms at first use rather than relying on generic summaries.
