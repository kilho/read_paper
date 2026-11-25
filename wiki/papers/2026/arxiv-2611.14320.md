---
schema_version: 4
id: arxiv-2611.14320
title: "Don't Just Trust Your Memory: Evidence-Linked Memory Reduces Memory-Induced Degradation in LLM Agents"
year: 2026
authors: [Yukyeong Lee, Yumin Choi, Jinheon Baek, Sung Ju Hwang]
topics: []
source:
  version: v1
  url: https://arxiv.org/pdf/2611.14320v1
sources:
  S1: "§1–2 (introduction and related work), pp. 1–3"
  S2: "§3.1–3.4 (problem, memory construction, and source access), pp. 3–5; Figures 2–4; Appendix B"
  S3: "§4.1–4.3 (experiment setup, results, Gain, and Regression), pp. 5–6; Table 1; Figure 5; Appendix A"
  S4: "§5.1–5.5 (analysis, cost, and generalization), pp. 6–8; Figures 6–10; Table 2"
  S5: "§5.6 (resolving conflicting insights) and Figure 11, pp. 8–9; Limitations, p. 8"
relationships:
  - paper: conference-acl-long-850
    type: evaluates
    reason: "The paper evaluates WikiTrace on selected AppWorld normal and challenge tasks involving simulated app APIs."
---

# Don't Just Trust Your Memory: Evidence-Linked Memory Reduces Memory-Induced Degradation in LLM Agents

## Overview

WikiTrace is an evidence-linked memory system for large language model (LLM) agents, not a way to guarantee that stored lessons are correct. It turns past task runs into concise lessons linked to their source summaries and raw trajectories, allowing an agent to check a lesson while solving a new task. [S1] [S2]

## What

The input is a fixed collection of past tasks, action/observation trajectories, and success-or-failure labels, without gold explanations. A compiler creates an indexed, read-only memory; a test agent receives the resulting insights and can inspect linked evidence with terminal tools before acting. The output is the agent's task actions and result, not a verified or permanently corrected memory. [S2]

![WikiTrace compiles trajectories into linked insights and summaries; an agent consults source evidence when a lesson is incomplete, conflicting, or from a failed run.](arxiv-2611.14320.png)

*Paper [Figure 2, p. 3](https://arxiv.org/pdf/2611.14320v1#page=3): “Overview of WikiTrace. (a) A compiler turns each past run into a compilation, a diagnosis of why the run succeeded or failed, and insights, each a concise lesson. All layers stay linked. (b) Each layer's documents follow a fixed template. (c) The agent starts from every insight and descends through the links under the conditions shown.” Notice that source access is selective rather than automatic verification. [S2]*

*Figure and caption by Lee et al., licensed under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/); the figure is cropped.*

## Terminology

| Term | Meaning in this paper | Why it matters |
| --- | --- | --- |
| Trajectory | A past run's actions and observations, stored with its task and outcome. [S2] | It preserves the evidence behind a lesson, even when the lesson is misleading. |
| Compilation | A generated account of a run's decisions and supporting observations, or plausible failure causes. [S2] | It is a navigable intermediate summary, not a verified diagnosis. |
| Insight | A concise lesson, its applicability, and links to the run and compilation it came from. [S2] | It is cheap to read but can be wrong, incomplete, or conflict with another insight. |
| Descent | Reading a linked compilation or raw trajectory to investigate an insight. [S2] | It can recover details missing from the compressed lesson. |
| Gain vs. Regression | Gain is success on tasks whose majority no-memory outcome was failure; Regression is failure on tasks whose majority no-memory outcome was success. [S3] | Overall score alone can hide cases in which memory harms previously solvable tasks. |

## Why

**Why solve this problem?** A run gives the memory compiler one outcome for a sequence of actions. That outcome does not tell the compiler which actions mattered, which were incidental, or when the same advice will apply. In the paper's ALFWorld example, ExpeL learned that an object beside a lit lamp was enough to finish the task. But in the successful source run, the episode ended only after the agent picked up the pencil. On a new task, the agent followed the rule, left the vase on the desk, and failed. The log can expose this mismatch without proving which actions were necessary. A follow-up experiment could vary the action a lesson recommends while keeping the rest of the task fixed to test whether the lesson holds. [S1] [S2]

**What did prior work do?** ExpeL extracts and maintains rules from experiences, while ReasoningBank distills strategies from successes and failures and retrieves them by task similarity. The paper's adapted baselines give the agent extracted guidance without a linked path back to the original trajectory, making it harder to inspect the basis of an individual lesson. [S1] [S3]

**What does WikiTrace do differently, and why?** It keeps each per-run insight linked to the compiler's account and the unchanged source run, and prompts the agent to inspect evidence when a lesson is uncertain or incomplete. This trades more storage, context, and reading cost for the opportunity to reassess guidance; the link itself does not prove that the interpretation or action is correct. [S2] [S4] [S5]

## When

An agent developer can use WikiTrace when reusing prior runs for tasks such as controlling simulated apps or completing crafting tasks, especially when concise lessons disagree or omit a necessary detail. The linked observations can help the agent decide whether a lesson fits the current situation, but a separate check is still needed for correctness, safety, and use in real environments. [S2] [S3] [S5]

The authors compare WikiTrace with no memory, AWM, ExpeL, ReasoningBank, and **Insights Only** on eight suites across five benchmarks, including [AppWorld](../2024/conference-acl-long-850.md). With DeepSeek-V4-Flash, the mean of suite scores was **90.2** for WikiTrace, **87.0** for Insights Only, and **79.5** for no memory; suite metrics differ. Mean Regression was **4.5%** versus **6.5%** for Insights Only. These are averages over three trials in the paper's selected benchmark setups, not guarantees for other agents or tasks. [S3]

## How

1. **Build once:** For each no-memory training run, a compiler reads the task, trajectory, and binary outcome. It writes one compilation and up to three separately sourced insights; the raw run remains unchanged. [S2]
2. **Freeze and present:** The corpus is indexed and mounted read-only. At test time the agent sees all insights, plus identifiers and titles for insights from three similar past tasks. [S2]
3. **Inspect selectively:** The prompt asks the agent to follow links when an insight lacks details, conflicts, came from a failed run, or an action fails. It can read a summary or raw actions and observations before choosing how to proceed. The paper compares this with the same insights supplied without source access or the descent prompt. [S2] [S3]
4. **Act without rewriting the store:** The agent can revise its interpretation during the current task; the experiment does not update the stored insight documents. [S2] [S5]

## Worked Example

**Paper example:** In PlanCraft, the agent must craft acacia slabs. A lesson from a failed run suggests giving up if placing one plank already appears to produce another item; a conflicting lesson from a successful run says to keep adding the ingredients because the displayed output is only a preview. [S5]

1. WikiTrace opens the linked runs. In the failed acacia-slab run, the agent repeatedly placed a plank in the grid and took it back. In the successful crimson-slab run, the agent kept adding crimson planks until a slab appeared. The successful run suggests a procedure for acacia, but does not itself verify the acacia recipe. [S5]
2. The agent recognizes that the intermediate button or pressure plate is a preview, not an item automatically consumed from the grid. On the acacia task, it places three acacia planks in a row and takes the resulting six acacia slabs. [S5]
3. In the paper's illustrated run, WikiTrace succeeds. The Insights Only agent instead takes the intermediate button, consumes a plank, and declares the task impossible. This is one qualitative example, not a measured success rate or a permanent repair to the stored rule. [S5]

## Differentiators

- **Source-linked rather than insight-only:** The same insight can be checked against a summary and raw run instead of being accepted solely as a compressed rule. The comparison also changes the prompt to encourage descent, so it tests the access-and-prompt package. [S2] [S3]
- **Preserve rather than silently merge:** Insights are generated per run and are not merged or deleted, so conflicting lessons remain visible and their sources can be compared. [S2]
- **Report harm as well as help:** Gain and Regression separate newly solved tasks from previously solved tasks that fail; an additional no-memory rerun estimates the variation that can occur without memory. [S3]

The source checks have costs and limits: every insight is initially included in the prompt, so scaling to larger memories requires a retrieval method not tested here. In the reported experiments WikiTrace cost **1.17×** as much per task as Insights Only, averaged across suites, and the qualitative failure labels were made by LLM judges rather than establishing causation. [S4] [S5]

## Evidence

**Evaluation setup.** The paper compares six conditions on eight suites from ALFWorld, ScienceWorld, PlanCraft, AppWorld, and τ3-bench Retail. In each of three trials, memory methods build once from the same no-memory training trajectories and test on the same held-out tasks. The builders and the Pi test agent use DeepSeek-V4-Flash at high reasoning effort. Table 1 averages each suite's native metric (e.g., ALFWorld success rate versus ScienceWorld mean score), then gives each suite equal weight in the overall average. Insights Only is the closest comparison: it gets the identical lessons but neither the source files nor the instruction to consult them. [S3]

**Why measure Gain and Regression separately?** Aggregate performance can improve even when memory breaks some tasks the agent previously solved. The paper groups tasks by the majority outcome across three no-memory trials. Gain measures the with-memory success rate within the baseline-failure group; Regression measures the with-memory failure rate within the baseline-success group. The authors also measure Regression on additional no-memory runs to show how often outcomes flip without memory. [S3]

**Main result.** WikiTrace outscored Insights Only in all eight suites (+3.2 points on average); PlanCraft Unseen rose from 73.0 to 81.3, while ScienceWorld rose from 94.9 to 96.1. Mean Regression was 4.5% for WikiTrace, 6.5% for Insights Only, and 9.7% for the independent no-memory reruns. Mean Gain was 35 percentage points above the rerun baseline for WikiTrace versus 27 for Insights Only. This supports providing the evidence and prompting the agent to consult it together; it does not isolate the effect of the files from the prompt. [S3]

**What went wrong?** In a separate analysis, the authors examined 355 failures with memory on tasks solved in all three no-memory runs. An LLM judge linked 184 of those failures (52%) to a memory item the agent followed. The largest of the four memory-linked categories was a wrong item (70 of 355 failures, about 20%); other cases included valid guidance applied outside its scope or used incorrectly. These are judge-assigned explanations for a selected set of failures, not causal estimates for all runs. [S2]

**What failed runs add.** On PlanCraft and ScienceWorld, both memory variants scored better when built from failures alone than from successes alone, and best when built from both. But with failure-only memory, Regression was 9.3% and 9.4% for Insights Only, versus 7.1% and 8.9% for WikiTrace, respectively. That is a reason to compare how failures are preserved and checked, not just whether they are included. In a separate analysis of three text-world benchmarks, agents opened source files on 44% of hard runs versus 22% of easy runs (difficulty was defined by no-memory success across three trials). The agent chose when to open files, so the comparison does not establish the causal benefit of opening a file on a given task. [S4]

## Relationships

WikiTrace is evaluated on selected tasks from [AppWorld](../2024/conference-acl-long-850.md), which supplies an interactive simulated app environment and task-level evaluation. WikiTrace changes how the agent reuses past experience; AppWorld is one of the benchmarks used to measure it. [S3]

## Technical Depth

### Build the evidence links

For training run $i$, the compiler maps $(x_i, r_i, s_i)$ to $(c_i, I_i)$: the task $x_i$, recorded trajectory $r_i$, and binary outcome $s_i$ produce one compilation $c_i$ and a set $I_i$ of at most three insights. Success compilations summarize decisions and observations; failure compilations give plausible diagnoses rather than labels for individual actions. Each insight links directly to the compilation and the unchanged turn log. Separate indexes list the contents of each layer. At test time, all insights are in the initial message; the three similar runs supply starting points for investigation, not a filter on which insights the agent receives. The agent can check a summary or jump straight to the log, then revise its plan without rewriting memory. [S2]

### Calculate Gain and Regression

Let $B_i$ be task $i$'s majority outcome over three reference no-memory trials, and $M_{i,t}$ its binary outcome with memory on trial $t$. Within a suite, count each applicable task–trial pair: $\text{Gain} = \Pr(M_{i,t}=1 \mid B_i=0)$ and $\text{Regression} = \Pr(M_{i,t}=0 \mid B_i=1)$. For the no-memory rerun comparison, replace the with-memory outcome with an outcome from one of three additional no-memory trials, leaving $B_i$ fixed. [S3]

**Illustrative example:** Suppose two tasks are baseline failures and eight are baseline successes. Across three memory trials per task, memory solves 3 of 6 attempts in the first group and fails 2 of 24 in the second. Gain is 50% and Regression is 8.3%. Overall, it solves $(3+22)/30 = 83.3\%$, compared with the majority baseline's $8/10 = 80\%$. The average improves even though two attempts on previously solvable tasks now fail. [S3]

## Source Locators

- S1: §1–2 (introduction and related work), pp. 1–3
- S2: §3.1–3.4 (problem, memory construction, and source access), pp. 3–5; Figures 2–4; Appendix B
- S3: §4.1–4.3 (experiment setup, results, Gain, and Regression), pp. 5–6; Table 1; Figure 5; Appendix A
- S4: §5.1–5.5 (analysis, cost, and generalization), pp. 6–8; Figures 6–10; Table 2
- S5: §5.6 (resolving conflicting insights) and Figure 11, pp. 8–9; Limitations, p. 8

## FAQ
