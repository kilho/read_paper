---
schema_version: 4
id: conference-acl-long-850
title: "AppWorld: A Controllable World of Apps and People for Benchmarking Interactive Coding Agents"
year: 2024
authors:
  - Harsh Trivedi
  - Tushar Khot
  - Mareike Hartmann
  - Ruskin Manku
  - Vinty Dong
  - Edward Li
  - Shashank Gupta
  - Ashish Sabharwal
  - Niranjan Balasubramanian
topics: []
source:
  url: https://aclanthology.org/2024.acl-long.850.pdf
sources:
  S1: "§1 (Introduction), pp. 1–2; Figure 1"
  S2: "§2 (AppWorld Engine), pp. 3–4; Figure 2"
  S3: "§3.1–3.4 (benchmark generation, evaluation, and dataset), pp. 4–6; Figure 3; Tables 1–2"
  S4: "§4.1–4.3 (methods, results, and analysis), pp. 7–9; Table 3; Figure 4"
  S5: "§5 (Related Work), p. 9; §7 (Limitations), pp. 9–10"
relationships:
  - paper: arxiv-2404.07972
    type: contrasts_with
    reason: "Both provide controllable environments and task evaluation, but AppWorld tests interactive code over simulated app APIs while OSWorld tests GUI and keyboard control of desktop environments."
  - paper: arxiv-2406.12045
    type: contrasts_with
    reason: "Both test agents using tools against application state, but AppWorld emphasizes iterative program generation across everyday apps while τ-bench emphasizes policy-constrained retail and airline conversations with simulated users."
---

# AppWorld: A Controllable World of Apps and People for Benchmarking Interactive Coding Agents

## Overview

AppWorld pairs a controllable simulator of everyday apps and people with 750 benchmark tasks that require agents to write and iteratively run code against app APIs. Rather than score a short sequence of tool calls against one reference trace, it uses database-state tests to check task completion and unintended changes. [S1] [S2] [S3]

## What

This is an interactive coding benchmark and its app simulator, not a new agent model. An agent receives a natural-language task, API documentation, and access to a stateful execution shell; it writes code, calls APIs, and uses their outputs to decide what code to run next. The tasks cover nine simulated day-to-day apps and people, and their test suites measure both whether each task succeeds and whether an agent succeeds consistently across variations of a scenario. [S2] [S3]

![AppWorld Engine’s simulated apps and people connect to an interactive coding task whose final database changes are checked by state-based tests.](conference-acl-long-850.png)

*Paper Figure 2, p. 3. The left panel shows the simulated apps and people; the right shows an agent iterating with APIs before tests check the resulting state. Caption summarized from the paper. [Source](https://aclanthology.org/2024.acl-long.850.pdf#page=3) [S2]*

## Terminology

| Term | Meaning in this paper | Why it matters |
| --- | --- | --- |
| Task scenario vs. task | A scenario is a blueprint; each task is a particular instruction and starting state instantiated from it. The benchmark has 250 scenarios with three tasks each. [S3] | Variants change people, data, or conditions, so one success does not prove reliable handling of the whole scenario. |
| Stateful execution shell | A notebook-style environment where the agent can execute code snippets and reuse variables across turns. [S2] | The agent can inspect intermediate results, then write later code based on what it learned. |
| State-based evaluation | Tests compare the final database changes with required changes and changes explicitly allowed by the task. [S3] | Different API sequences can pass, while unrelated side effects can fail the tests. |
| Task Goal Completion (TGC) | Percentage of individual tasks for which all evaluation tests pass. [S3] | Measures task-level success. |
| Scenario Goal Completion (SGC) | Percentage of scenarios for which the agent passes all tests on every task variant. [S3] | Measures consistency across related tasks, not just success on one instance. |

## Why

**Why solve this problem?** Everyday digital requests often require reasoning across apps, inspecting intermediate API results, and writing control flow to handle the data found. A benchmark that tests only a few independent API calls misses this interactive coding work and can miss collateral changes made while pursuing the goal. [S1] [S3]

**What did prior work do?** The paper contrasts AppWorld with tool-use benchmarks that generally ask for short, one-to-four-call sequences and often judge against a reference solution or answer. Such evaluation is a poor fit when a task needs many dependent calls and loops, or when several different final states can satisfy the request. [S1] [S5]

**What does AppWorld do differently, and why?** It provides a stateful shell over documented APIs for nine simulated apps, then evaluates the resulting database diff against required and permitted changes. This makes alternative valid solutions testable while rejecting many unintended side effects. The trade-off is scope and engineering effort: the benchmark covers a designed set of nine API-accessible apps rather than arbitrary live apps or user interfaces, and the authors built the engine and task generators themselves. [S2] [S3] [S5]

## When

**Use AppWorld to compare coding agents on multi-step digital-assistant requests**, such as approving only a supervisor’s roommates’ Venmo requests from the current month. Each task’s score can verify whether all required state changes occurred without disallowed changes; SGC additionally checks whether the agent handles all variants in a scenario. The paper compares ReAct, Plan-and-Execute, Full Code + Reflexion, and iterative parallel function calling with GPT-4o, GPT-4 Turbo, LLaMA 3, and DeepSeek, as well as CodeAct and ToolLLaMA. [S3] [S4]

In the paper’s results, GPT-4o with ReAct achieved **48.8% TGC on the normal test set** and **30.2% on the challenge set**; SGC was **32.1%** and **13.0%**, respectively. The challenge set requires using an API from an unseen app. These results test the 2024 models and simulator, not performance on real services or UI-only workflows; those require separate evaluation. [S3] [S4] [S5]

## How

1. **Generate a task:** A scenario setup program combines the scenario with a base database and date/time, then creates a supervisor, instruction, task-specific starting database, and expected evaluation data. It adds realistic distractors and hurdles while keeping the task solvable. [S3]
2. **Interactively write code:** The agent consults API documentation and runs code in the persistent shell. API results and error messages become observations for its next code block; tasks may require loops, dependent calls, and many lines of code. [S2] [S3]
3. **Check the final state:** Evaluation tests examine the database diff. All required changes must be present, and every other change must be among the explicitly allowed changes. TGC counts passing task instances; SGC counts scenarios for which all their variants pass. [S3]

## Worked Example

**Paper example:** The task in Figure 1 asks the agent to play a Spotify playlist long enough for today’s workout; the schedule is in SimpleNote. In the example, the note says Tuesday’s workout is 45 minutes and the simulated date is Tuesday. The song lengths below are illustrative. [S1]

1. The agent calls SimpleNote APIs to find and read the workout note, then checks the current day. It learns the relevant target is 45 minutes; it cannot safely choose a playlist before reading the note and date.
2. It calls Spotify APIs to list playlists and inspect their songs. Suppose, for illustration, one candidate has song lengths of 25 and 20 minutes (45 total), while another totals 40 minutes. The first meets the target; the second does not. These song lengths are toy values, not reported paper data.
3. The agent calls the API to play the qualifying playlist. For this illustrative trace, a test requiring the correct playlist to be playing would pass for the 45-minute candidate and fail for the 40-minute one. AppWorld’s general evaluator also checks for disallowed database changes; the paper does not specify the exact tests for this Figure 1 task. [S1] [S3]

## Differentiators

- **Versus simple tool-use tasks:** AppWorld tasks can require up to 26 unique APIs and hundreds of API calls, with results from earlier calls informing later code. The task is not just a fixed tool-call sequence. [S3] [S5]
- **Versus reference-trace grading:** State-based tests allow multiple valid action paths, and also check for side effects by constraining the permitted database diff. [S3]
- **Versus real desktop benchmarks:** AppWorld agents interact through APIs in a simulator, not screenshots, mouse clicks, or live app interfaces. This makes state control and checking practical but limits what the scores establish about UI agents. [S2] [S5]

## Relationships

Compared with [OSWorld](arxiv-2404.07972.md), AppWorld tests agents that write code against simulated app APIs rather than agents that control desktop GUIs and keyboards. Compared with [τ-bench](arxiv-2406.12045.md), it focuses on interactive program generation and a broad set of app workflows rather than policy-constrained retail and airline conversations with simulated users.

## Source Locators

- S1: §1 (Introduction), pp. 1–2; Figure 1
- S2: §2 (AppWorld Engine), pp. 3–4; Figure 2
- S3: §3.1–3.4 (benchmark generation, evaluation, and dataset), pp. 4–6; Figure 3; Tables 1–2
- S4: §4.1–4.3 (methods, results, and analysis), pp. 7–9; Table 3; Figure 4
- S5: §5 (Related Work), p. 9; §7 (Limitations), pp. 9–10

## FAQ
