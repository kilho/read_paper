# Isolate batch paper ingestion from comparison

- **Feedback:** Long conversations that ingest and compare several full papers at once accumulate unnecessary source context. Give each paper its own session before comparing the batch.
- **Affected workflow:** The [ingest-paper-batch skill](../.github/skills/ingest-paper-batch/SKILL.md) runs separate ingestion sessions and starts synthesis only when every selected paper is canonical and indexed.
- **Expected improvement:** Each ingestion can focus on one source, and synthesis can work from validated wiki pages and targeted source locators rather than previous conversations.
