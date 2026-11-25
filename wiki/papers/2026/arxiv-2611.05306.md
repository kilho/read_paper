---
schema_version: 4
id: arxiv-2611.05306
title: "You don’t need long context"
year: 2026
authors: [Peter Belcak, Saurav Muralidharan, Jindong Jiang, Yonggan Fu, Wonmin Byeon, Hanrong Ye, Ryan Angilly, Ali Taghibakhshi, Shih-Yang Liu, Siru Ouyang, Greg Heinrich, Pavlo Molchanov]
topics: []
source:
  version: v1
  url: https://arxiv.org/pdf/2611.05306v1
sources:
  S1: "Section 1 and Figures 1–2, pp. 1–3"
  S2: "Sections 2.1–2.4 and Figure 3, pp. 3–7"
  S3: "Sections 3–3.1 and Figure 5, pp. 9–10; Appendix A, p. 20"
  S4: "Section 4 and Figure 6, pp. 11–13; Appendix E.2, pp. 25–26; Appendix F, Table 11, p. 27"
  S5: "Sections 5–6 and Table 2, pp. 14–15"
  S6: "Appendix B, Equations 1–4, pp. 20–21"
  S7: "Appendix D, Tables 9–10, p. 24"
relationships:
  - paper: arxiv-2611.14320
    type: contrasts_with
    reason: This paper compacts the active run to resume it; WikiTrace links lessons from past runs to source evidence for use on new tasks.
  - paper: arxiv-2310.06770
    type: uses
    reason: The paper evaluates context management on SWE-bench Verified, a human-validated subset rather than the original full suite.
---

# You don’t need long context

## Overview

The paper tests whether an AI agent can work with less information in view at each step, saving computing work without losing much task accuracy. **Context** is what the model can see at one time: the task, previous messages, and results from tools such as a test runner. The researchers changed what they sent to existing models, not how the models were trained. [S1] [S2]

- **When the work takes many steps:** Imagine an AI coding assistant fixing a bug. Instead of passing every earlier command and test result into the next conversation, the assistant writes a short note: “I changed the date parser. The time-zone test still fails. Check how the parser handles UTC next.” The next conversation starts with the original task and that note. The paper calls replacing the old messages with a short note **compaction**. [S2] [S3]
- **When the source material is long:** Imagine the same assistant needs to check a large API manual. Rather than putting the whole manual into the conversation, the researchers' setup leaves the manual in a file. The assistant searches the file and reads the relevant pages or passages as needed. [S2] [S4]

In the main experiments, the two closed-weight models usually did about as well as when given the full history or the full documents; some open-weight models lost much more accuracy under tight limits. **Old information can still matter.** If the note leaves out the exact error message, the assistant may need to look up that message in a saved log. The point is to avoid showing the model everything at once, not to throw away the original information. [S3] [S4] [S5] [S7]

## What

The study starts with either a task that generates a long sequence of tool actions and observations or a question with a large source document collection. The harness changes how the model sees the history or documents, while the final patch, tool outcome, or answer is still scored by the benchmark. The main accuracy experiments use Claude Opus 4.5 and GPT 5.6 Sol; separate open-weight model measurements inform the cost estimates. [S1] [S2] [S6]

## Terminology

| Term | Meaning in this paper | Why it matters |
| --- | --- | --- |
| Peak live context | The length of the largest conversation segment during a task, not the sum of all segments. [S2] | A short peak does not imply few tokens spent across the whole run. |
| Full-history accumulation (FHA) | Append each action and observation to one conversation without replacing old messages. [S2] | This is the long-horizon baseline, distinct from giving a long document up front in the long-input experiments. |
| End-of-conversation compaction (EoCC) | When the conversation reaches a set length, write a short progress note and start a new conversation with the original task and the note. [S2] | The new conversation doesn't contain all the old messages. The note can leave out details. |
| Single-action compaction (SAC) | After each tool action and its result, update the progress note and start a new conversation. [S2] | The same task can still take many actions. |
| Selective input reading | Leave documents in files and let the agent choose which passages to load using search and bounded reads. [S2] [S4] | Large source inputs can remain available without all of their tokens entering the model. |

## Why

**Why solve this problem?** A coding agent's log can grow even when the next decision needs only a few facts. The paper's system measurements show lower decode throughput at longer contexts; its cloud analysis estimates a higher cost per output token at fixed GPU prices. [S1] [S6]

**What did prior work do?** The released mini-swe-agent uses a minimal ReAct loop: take an action, observe the result, and append both to the conversation. This preserves all previous observations, but the default loop does not bound the growing history. Likewise, the standard full-input baselines place the entire benchmark input in context. [S2] [S4]

**What does this paper do differently, and why?** The agent still takes actions and checks the results, but it can start a new conversation with a progress note instead of keeping every old message in view. For long documents, the agent reads specific passages from files instead of receiving all the text up front. If the note leaves out an important detail, the agent needs another way to find the original. [S2] [S3] [S4]

## When

An engineer building a coding agent can compare compaction policies on long patch-and-test tasks. Across six long-horizon benchmarks, at most 5 of 22 threshold configurations per model lost more than two percentage points versus full history. The authors separately tested per-action compaction on SWE-bench Verified and Terminal-Bench 2.1. On SWE-bench Verified, GPT 5.6 Sol went from 84.4% to 82.4% resolved, while median peak context fell from 18K to 7K tokens. [S3] [S5]

The outcome depends on the model and context budget: in a separate experiment on SWE-bench Verified, the quantized open-weight Qwen 3 Coder Next fell from 53.0% resolved with full history to 3.6% with EoCC at a 16K total limit and 12K compaction threshold. The authors attribute much of that drop to verbose runs leaving too little room for progress between compactions. [S7]

Those scores measure task success, not whether the agent can recall arbitrary details from earlier turns. For workflows that need exact old tool output, the authors suggest storing the trace separately and making it searchable; they do not establish that a compact summary alone can reproduce it. They also do not show that short context suffices for every workload. An engineer should separately check retrieval, task success, and actual latency and billing in the intended environment. [S3] [S5] [S6]

## How

1. **Keep the action loop.** Give the model the task. It takes an action, sees the result, and uses that observation to choose what to do next. Full history leaves those turns in one conversation. [S2]
2. **Start a new conversation with a progress note.** With EoCC, once the conversation crosses a set threshold, ask the model to write a short note about what it found, what it changed, and what to do next. A higher total context limit reserves room to write the note; the conversation terminates if the note is not completed in time. Start the new conversation with the same instructions, the original task, and the note. With SAC, write that note after every tool action and its result. [S2] [S3]
3. **Keep large source inputs outside the prompt.** For long-input benchmarks, give the agent the question and file information. It searches and reads bounded passages, and uses EoCC if that working conversation grows too large. [S2] [S4]
4. **Compare outcomes and token use separately.** Sparse reads and shorter conversations change both what evidence the agent sees and what inference consumes. The authors report benchmark scores and token accounting; their optimized retail cost adds a context-dependent pricing assumption. [S3] [S4] [S6]

![A source file stays outside the model conversation. Bounded excerpts enter the active conversation, and a task brief carries progress into a fresh conversation.](arxiv-2611.05306.png)

*Original diagram based on [Sections 2.4.1–2.4.2](https://arxiv.org/pdf/2611.05306v1#page=7). Reading a file excerpt and compacting a conversation solve different problems: one controls how much source text enters, and the other controls how much working history stays.* [S2]

## Worked Example

**Paper example:** In a recorded LongBench v2 run, the question asks for a translation using a Kalamang grammar file of 18,830 lines. The agent searches for the word *kademor* and finds a hit at line 3,840. It then requests lines 3,835–3,870: a 36-line excerpt that describes *kademor* as “to be mad” and discusses how the verb introduces an object. A further bounded read checks grammar and examples rather than treating the keyword match as the answer. The trace shows intermediate evidence entering context, not a reported final translation, typical read size, or success rate. The benchmark scores the final multiple-choice answer separately. [S2] [S4]

## Differentiators

- **Short context is not short total work.** Compaction can require the agent to read or do something again. Peak context, total tokens and task accuracy should be tracked independently. [S2] [S3]
- **Optimized cost is not the API bill.** On LongBench v2, GPT 5.6 Sol went from 70.8% to 72.6% with selective reading and compaction (16K limit, 12K threshold). The estimated optimized cost fell from $79.20 to $18.04, but the same run's nominal cost at standard rates rose to $90.20. The estimate extrapolates from throughput measurements of three open-weight models; it is not a measured discount for the tested closed-weight endpoint or an isolated effect of compaction. [S4] [S6]
- **The authors tested a progress note, not a new model.** Section 5 tests existing models that write a note after each action. Section 5.1 proposes training a model specifically to read and update those notes, which the authors call a *semantic state space model*. The paper does not test that proposed model. [S5]

## Relationships

- **Contrasts with** [WikiTrace](arxiv-2611.14320.md#how): compaction carries progress forward within one active task; WikiTrace carries lessons across tasks and lets the agent inspect their source runs. [S2] [S3]
- **Uses** [SWE-bench](../2024/arxiv-2310.06770.md) via the human-validated Verified subset to compare patch success across context policies. The results are not for the original full suite. [S2] [S5]

## Source Locators

- S1: Section 1 and Figures 1–2, pp. 1–3
- S2: Sections 2.1–2.4 and Figure 3, pp. 3–7
- S3: Sections 3–3.1 and Figure 5, pp. 9–10; Appendix A, p. 20
- S4: Section 4 and Figure 6, pp. 11–13; Appendix E.2, pp. 25–26; Appendix F, Table 11, p. 27
- S5: Sections 5–6 and Table 2, pp. 14–15
- S6: Appendix B, Equations 1–4, pp. 20–21
- S7: Appendix D, Tables 9–10, p. 24

## FAQ

### Can the agent recover a detail left out of the progress note?

Not from the note alone. The paper suggests saving the full conversation separately and letting the agent search it. That way, the note tells the agent where to pick up the task, and the saved record can supply the exact earlier message when needed. [S2] [S3]
