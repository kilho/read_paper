# AI Research Wiki: Updated Architecture and Implementation Plan (v2)

## 1. Vision and Goals

Build a **Git-based, AI-maintained research knowledge system** that helps researchers quickly understand AI papers, accumulate knowledge, and discover relationships between research topics.

The system should combine:

- **Curated paper discovery:** Identify influential, high-quality, and emerging research.
- **Fast paper understanding:** Understand a paper in 5 minutes, or 10 minutes for technically challenging work.
- **Deep technical knowledge:** Explain terminology, motivations, assumptions, algorithms, and worked examples.
- **Interconnected knowledge:** Understand how papers, methods, and research topics relate.
- **Human-in-the-loop learning:** Continuously improve both the wiki content and the skills used to generate it.
- **Reusable infrastructure:** Maintain consistent schemas, skills, prompts, and harnesses.
- **Efficient knowledge transfer:** Use progressive disclosure to provide the right amount of information.

The ultimate objective is not simply to summarize papers. It is to build a **continuously improving research understanding system**.

---

## 2. Updated System Architecture

Metadata and relationships should be integrated into the wiki rather than maintained as an independent knowledge layer.

### Proposed components

| Component | Responsibility |
|---|---|
| **Paper Discovery** | Find and prioritize important papers |
| **Sources** | Preserve original papers, code, and references |
| **Wiki** | Store paper explanations, concepts, relationships, and topic syntheses |
| **Schemas** | Enforce consistent wiki structure and content requirements |
| **Skills** | Define reusable research workflows |
| **Prompts** | Provide reusable instructions for individual tasks |
| **Harness** | Orchestrate execution, validation, and updates |
| **Evaluation** | Measure understanding, correctness, and knowledge quality |
| **Human Feedback** | Improve wiki content and the underlying generation process |

### Architectural principles

**1. Wiki is the single source of truth for research knowledge.**

Store relationships directly within Markdown pages using YAML frontmatter and cross-references.

For example:

```yaml
id: arxiv-xxxx.xxxxx
title: Example Paper
year: 2026
topics: []

relationships:
  - paper: arxiv-yyyy.yyyyy
    type: extends
    reason: Improves contextual representation.

  - paper: arxiv-zzzz.zzzzz
    type: contrasts_with
    reason: Uses retrieval instead of rewriting.
```

A graph or search index can be generated from the wiki later.

Leave paper topic tags empty until enough papers have been reviewed to establish a useful taxonomy.

**2. Schemas define knowledge structure.**

Schemas determine what information must be captured and how it should be organized.

**3. Skills define how to generate and use knowledge.**

Skills are reusable procedures for reading, explaining, comparing, and updating papers.

**4. Harnesses manage execution.**

The harness coordinates skills, validates outputs, and updates the repository.

**5. Humans improve both content and process.**

Human corrections should improve the current wiki entry and, when generalizable, the skills responsible for generating it.

---

## 3. Paper Discovery and Prioritization

The system should not depend entirely on manually supplied papers. It should actively discover and rank important research.

### 3.1 Paper sources

| Source | What to discover |
|---|---|
| **Top conferences** | Accepted papers, oral presentations, best papers |
| **arXiv** | Emerging and trending research |
| **Semantic Scholar / OpenAlex** | Citation counts, influential papers, citation networks |
| **Papers with Code / GitHub** | Implementations, benchmarks, and practical impact |
| **Research labs** | Papers from leading academic and industrial research groups |
| **Researcher watchlists** | New publications by influential researchers |
| **Community signals** | Trending papers, discussions, and research attention |

#### Conference coverage

Initially focus on:

- **ML:** NeurIPS, ICML, ICLR
- **NLP:** ACL, EMNLP, NAACL
- **Vision:** CVPR, ICCV, ECCV
- **Systems:** MLSys
- **Graphics:** SIGGRAPH, SIGGRAPH Asia

Conference quality should be interpreted within the research field rather than using a single global ranking.

### 3.2 Paper ranking

Use a multi-signal prioritization system.

| Signal | Priority | Rationale |
|---|---|---|
| Best paper / outstanding paper | Very high | Strong recognition from the research community |
| Oral / spotlight presentation | High | Selective recognition within a conference |
| Citation impact | High | Evidence of research influence |
| Recent research momentum | High | Identifies emerging directions |
| Strong experimental results | Medium | Demonstrates effectiveness |
| Relevance to research interests | High | Maximizes personal utility |
| Research institution / author | High | Useful discovery signal |
| Code availability | Medium | Supports implementation and verification |

**Important distinction:** These signals indicate which papers deserve attention, not whether their technical claims are correct.

In particular:

- Recent papers should use citation velocity rather than raw citation counts.
- Older papers should be evaluated using accumulated impact.
- Institution and author reputation should be discovery signals, not evidence of technical quality.
- Oral and spotlight categories vary across conferences.
- Best-paper status should strongly influence priority, but not replace critical reading.

### 3.3 Three discovery tracks

Maintain three reading queues.

#### A. Must-read papers

- Best-paper award winners
- Foundational, highly influential work
- Papers that establish major new research directions

#### B. State-of-the-art papers

- Strong results on important benchmarks
- New methods outperforming established approaches
- Papers that substantially change the current technical landscape

#### C. Emerging papers

- Recent arXiv publications
- Rapidly growing citation or community attention
- New methods from tracked researchers or labs
- Research ideas gaining traction

This prevents the reading list from being dominated by either established classics or recent hype.

#### Discovery output

The system generates a prioritized reading list containing:

- Paper title and link
- Publication venue and recognition
- Research topic
- Importance score
- Why the paper matters
- Relationship to previously read papers
- Suggested reading priority

Users can approve papers for ingestion, change their priority, or mark them as irrelevant.

---

## 4. Wiki Content: Optimized for 5–10 Minute Understanding

This is the most important part of the system.

Use a standardized paper schema organized around:

**What → Why → When → How → Example → Differentiator**

Each paper should have a consistent structure.

### 4.1 Proposed paper wiki schema

| Section | Required content | Target |
|---|---|---|
| **1. Overview** | Core contribution in 2–3 sentences | 20 seconds |
| **2. What + Terminology** | Problem and proposed solution, followed by a short table of topic-specific or ambiguous terms | 45 seconds |
| **3. Why** | Why the challenge matters, how prior work tackled it, what gap remained, and what this paper does differently to address it | 45 seconds |
| **4. When** | A realistic use case, what the contribution helps verify or accomplish, and what requires a separate check | 45 seconds |
| **5. How** | Core mechanism or evaluation workflow | 2 minutes |
| **6. Worked Example** | Concrete input, intermediate steps, output | 2 minutes |
| **7. Differentiators** | Detailed comparison with the closest related methods, expanding on the main difference introduced in Why | 1 minute |
| **8. Relationships** | Connections to concepts and other papers | 30 seconds |

**Default target: approximately five minutes.** Evidence and Technical Depth are optional additions generated on demand, not part of initial ingestion. Cite the core explanation even when neither section is present.

These are reading-time targets, not rigid content limits. A difficult paper may require additional detail.

### 4.2 Explain terminology in context

Use a short **Terminology** table after **What**, with columns **Term**, **Meaning in this paper**, and **Why it matters**. For each essential topic-specific or ambiguous term, provide:

1. A concise definition.
2. Why it matters to the paper.
3. A simple example when needed.

For example, in a retrieval paper:

**Contrastive learning**

A training approach that encourages representations of positive pairs to be closer than representations of negative pairs.

**Why it matters:** The method learns to distinguish relevant documents from irrelevant ones.

**Example:** A query and its relevant passage form a positive pair, while an unrelated passage forms a negative pair.

Avoid explaining general terminology that the intended reader is already likely to know.

Instead, focus on terminology necessary to understand the paper's contribution.

### 4.3 Explain when to use the method

Start with a concrete task a reader might actually face. For a benchmark, explain who or what it can evaluate, what its score can verify, and what needs a separate evaluation.

Every paper should answer:

- Under what assumptions does the method work?
- What input or supervision does it require?
- When is it preferable to existing methods?
- What are its computational requirements?
- Under what conditions might it fail?

This helps translate research knowledge into practical decisions.

### 4.4 Require worked examples

Every important algorithm should include a concrete example.

For a retrieval method:

1. Example query and documents
2. Initial representations
3. Intermediate transformations
4. Similarity or scoring calculations
5. Final retrieval results
6. Comparison against a baseline

For an RL paper:

1. Initial state
2. Model action
3. Reward calculation
4. Policy update
5. Resulting behavior

Examples should be sufficiently detailed to make the core mechanism understandable.

Label each example as:

- **Paper example:** Directly supported by the paper.
- **Derived example:** Reconstructed from the paper's method.
- **Illustrative example:** Simplified example created for explanation.

This distinction is essential for technical accuracy.

### 4.5 Explicitly compare related methods

Every paper should identify its closest alternatives.

| Dimension | Proposed method | Closest baseline |
|---|---|---|
| Problem formulation | What changes? | Existing formulation |
| Core technique | Main innovation | Previous technique |
| Training | Required supervision | Baseline supervision |
| Inference | Main procedure | Baseline procedure |
| Complexity | Computational cost | Baseline cost |
| Strengths | Demonstrated advantages | Baseline advantages |
| Limitations | Known weaknesses | Baseline weaknesses |

Only include comparisons supported by the paper or other identified sources.

---

## 5. Progressive Disclosure

The wiki should support different levels of understanding without duplicating information unnecessarily.

### Level 0: Paper index

One sentence explaining the paper's importance.

Used for browsing and ranking.

### Level 1: Five-minute explanation

Contains:

- What
- Why
- When
- Core algorithm
- Simplified example
- Main differentiator

This is the default reading experience produced by `ingest-paper`.

### Level 2: Ten-minute technical explanation

Use `explain-detail` to add **Evidence** and **Technical Depth** to the canonical page, or pass a focus to expand only the relevant section.

Adds:

- Detailed algorithm
- Important equations
- Worked numerical example
- Training and inference details
- Experimental evidence

### Level 3: Deep technical reference

Contains:

- Full mathematical derivations
- Implementation details
- Pseudocode
- Additional experiments
- Source code references
- Detailed limitations

#### Storage recommendation

Do not create three independent summaries.

Instead, use one canonical paper page with a concise core and expandable technical sections.

An agent can extract different levels of detail based on the task.

This minimizes duplication and inconsistency.

---

## 6. Wiki Schema and Validation

Every wiki entry should follow a schema. Use **multiple schemas for different knowledge types**, rather than forcing every page into one structure.

| Wiki type | Schema |
|---|---|
| Paper | What, Why, When, How, Example, Differentiator; optional Evidence and Technical Depth |
| Concept | Definition, Intuition, Formulation, Examples, Related Methods |
| Topic | Overview, Taxonomy, Representative Papers, Evolution, Open Problems |
| Comparison | Problem, Methods, Differences, Evidence, Trade-offs |
| Research Question | Motivation, Existing Approaches, Gaps, Hypotheses |

Each schema should define:

- Required sections
- Optional sections
- Metadata fields
- Relationship types
- Source citation requirements
- Validation rules

### Validation example

For a paper entry:

- Is the main contribution clearly explained?
- Are essential terms defined?
- Are assumptions stated?
- Is there a worked example?
- Are the closest baselines identified?
- Are experimental claims source-grounded?
- Are relationships valid?
- Are unsupported statements flagged?

The harness should validate these requirements before accepting generated content.

Schemas should also have version numbers so future changes can be migrated consistently.

---

## 7. Human-in-the-Loop Improvement

Treat human feedback as a first-class system component. There are two distinct improvement targets.

### 7.1 Improve wiki knowledge

Users should be able to:

- Correct inaccurate explanations.
- Add missing technical details.
- Request clearer examples.
- Identify important relationships.
- Remove irrelevant content.
- Change the emphasis of a paper explanation.

#### Example

**Human feedback:**

> The explanation of the loss function is too abstract. Add a numerical example showing how the positive and negative samples affect the loss.

The system should:

1. Update the relevant wiki section.
2. Preserve the existing correct information.
3. Verify the new example.
4. Record the modification in Git.

### 7.2 Improve skills and prompts

Repeated human corrections can reveal systematic weaknesses in the generation workflow.

For example:

**Observation:** Multiple paper entries fail to explain the role of negative samples in contrastive learning.

**Possible skill improvement:**

Add a requirement to `paper-understand`:

> For contrastive learning objectives, explain positive and negative sample construction and provide a small numerical example illustrating the loss.

Future paper entries can benefit from the improved skill.

### Proposed feedback workflow

**Human correction → Feedback classification → Wiki update → Skill improvement proposal → Evaluation → Human approval → Skill update**

| Feedback type | Action |
|---|---|
| Factual error | Correct the wiki |
| Missing paper-specific detail | Expand the wiki |
| Poor explanation | Improve the wiki; consider a prompt change |
| Repeated systematic error | Propose a skill update |
| Missing workflow capability | Propose a new skill or harness change |
| Schema limitation | Propose a schema revision |

**Important:** Do not automatically modify skills based on a single correction.

A correction might reflect a paper-specific issue rather than a generalizable weakness.

Store proposed skill changes as Git pull requests with evaluation results.

---

## 8. Skills, Prompts, and Harness

These components should remain separate.

### 8.1 Skills

Reusable research capabilities:

| Skill | Function |
|---|---|
| `discover-papers` | Find and prioritize relevant papers |
| `ingest-paper` | Parse sources and create a wiki entry |
| `explain-detail` | Add or expand Evidence and Technical Depth on demand |
| `understand-paper` | Generate technical explanations and examples |
| `explain-method` | Explain algorithms, equations, and terminology |
| `compare-papers` | Identify methodological differences |
| `connect-knowledge` | Discover paper and concept relationships |
| `synthesize-topic` | Create integrated topic-level knowledge |
| `improve-wiki` | Apply human corrections |
| `improve-skill` | Propose improvements to reusable workflows |

### 8.2 Prompts

Prompts should be smaller reusable instructions invoked by skills.

Examples:

- Explain a mathematical equation.
- Generate a numerical example.
- Identify assumptions.
- Compare against a baseline.
- Explain terminology.
- Verify experimental claims.

Avoid duplicating prompts across skills.

### 8.3 Harness

The harness should coordinate:

1. Paper discovery
2. Ranking and selection
3. Source acquisition
4. Wiki generation
5. Schema validation
6. Source verification
7. Relationship updates
8. Human review
9. Git persistence
10. Feedback-driven improvements

For reliability, deterministic tasks such as schema validation, identifier resolution, and duplicate detection should be implemented as code rather than LLM prompts.

---

## 9. Updated Repository Structure

```text
ai-research-wiki/
│
├── README.md
├── AGENTS.md
├── pyproject.toml
│
├── discovery/
│   ├── sources.yaml
│   ├── conferences.yaml
│   ├── researchers.yaml
│   ├── topics.yaml
│   └── reading-queue.yaml
│
├── sources/
│   ├── papers/
│   └── references/
│
├── wiki/
│   ├── index.md
│   │
│   ├── papers/
│   │   ├── 2024/
│   │   ├── 2025/
│   │   └── 2026/
│   │
│   ├── concepts/
│   ├── topics/
│   ├── comparisons/
│   └── research-questions/
│
├── schemas/
│   ├── paper.schema.yaml
│   ├── concept.schema.yaml
│   ├── topic.schema.yaml
│   ├── comparison.schema.yaml
│   └── relationship.schema.yaml
│
├── skills/
│   ├── discover-papers/
│   ├── ingest-paper/
│   ├── explain-detail/
│   ├── understand-paper/
│   ├── explain-method/
│   ├── compare-papers/
│   ├── connect-knowledge/
│   ├── synthesize-topic/
│   ├── improve-wiki/
│   └── improve-skill/
│
├── prompts/
│   ├── explain-equation.md
│   ├── generate-example.md
│   ├── identify-assumptions.md
│   └── verify-claims.md
│
├── harness/
│   ├── discover.py
│   ├── rank.py
│   ├── ingest.py
│   ├── validate.py
│   ├── link.py
│   └── maintain.py
│
├── evals/
│   ├── comprehension/
│   ├── factuality/
│   ├── coverage/
│   └── regression/
│
└── templates/
    ├── paper.md
    ├── concept.md
    └── comparison.md
```

Relationships and paper metadata remain inside wiki files.

The `discovery/` directory contains paper selection configurations and reading queues, not a separate knowledge graph.

Use feedback as temporary input to verify that wiki and skill updates address it. Keep the resulting changes, not separate feedback records.

---

## 10. Evaluation Strategy

Evaluate both the **quality of the wiki** and the **quality of the skills**.

### Wiki evaluation

| Metric | Objective |
|---|---|
| Factual accuracy | Avoid incorrect technical claims |
| Coverage | Preserve essential paper details |
| Explanation quality | Make methods understandable |
| Example correctness | Ensure worked examples are valid |
| Reading efficiency | Support 5–10 minute comprehension |
| Relationship quality | Identify meaningful connections |

### Skill evaluation

| Metric | Objective |
|---|---|
| Schema compliance | Produce consistent outputs |
| First-pass acceptance | Minimize required human corrections |
| Error recurrence | Avoid repeating previously corrected mistakes |
| Generalization | Improve across different paper types |
| Cost and latency | Reduce processing overhead |

### Human evaluation

A particularly useful metric is:

**How much time does a researcher need to understand a paper using the wiki, compared with reading the original paper?**

Test this with technical questions requiring explanations, calculations, and comparisons, not merely factual recall.

---

## 11. Updated Implementation Roadmap

### Phase 1: Paper understanding MVP

**Priority: Highest**

Build:

1. Paper schema
2. Paper ingestion skill
3. Five-minute core with `ingest-paper`; optional ten-minute explanation with `explain-detail`
4. Worked example generation
5. Source verification
6. Human correction workflow

**Deliverable:** A paper wiki entry that is accurate, concise, and sufficiently detailed for technical understanding.

### Phase 2: Paper discovery

Build:

1. Conference paper ingestion
2. Award and presentation-type tracking
3. Citation and momentum signals
4. Researcher and institution watchlists
5. Personalized paper ranking
6. Reading queue

**Deliverable:** A continuously updated, prioritized list of papers worth reading.

### Phase 3: Knowledge relationships

Build:

1. Concept pages
2. Typed relationships
3. Paper comparisons
4. Topic synthesis
5. Cross-paper knowledge retrieval

**Deliverable:** A connected research wiki rather than isolated summaries.

### Phase 4: Self-improving research workflow

Build:

1. Coverage checks against feedback and relevant changes
2. Skill improvement proposals
3. Prompt and schema revisions
4. Regression evaluation
5. Human-approved updates

**Deliverable:** A system that improves its research explanations and workflows over time.

### Phase 5: Advanced knowledge transfer

Build:

1. Query-aware progressive disclosure
2. Task-specific context packages
3. Efficient cross-paper retrieval
4. Research gap discovery
5. Automated topic maintenance

**Deliverable:** A research assistant that uses accumulated knowledge to support new research.

---

## 12. Key Design Decisions

| Decision | Recommendation |
|---|---|
| Metadata and relationships | **Integrate into wiki Markdown** |
| Paper selection | Automated discovery with quality and relevance ranking |
| Reading time | **5 minutes by default, 10 minutes for deeper understanding** |
| Paper structure | What, Why, When, How, Example, Differentiator; optional Evidence and Technical Depth |
| Terminology | Explain important terms in context |
| Examples | Mandatory for important algorithms |
| Wiki consistency | Schema-driven generation and validation |
| Knowledge relationships | Typed links between papers and concepts |
| Skills | Reusable, portable `SKILL.md` workflows |
| Harness | Centralized orchestration and validation |
| Human intervention | Correct wiki content and improve generation skills |
| Skill updates | Proposed automatically, approved by humans |
| Knowledge delivery | Progressive disclosure |
| Storage | Git + Markdown, with derived indexes as needed |
| Evaluation | Accuracy, comprehension, coverage, efficiency, and regression |

---

## 13. Three Strongest Recommendations

### 1. Optimize for understanding rather than completeness

A 5-minute explanation that makes the algorithm understandable is more valuable than a comprehensive 30-page summary.

The challenge is identifying the minimum information necessary to understand the paper without losing critical technical details.

### 2. Make human corrections improve future generations

The most valuable long-term feature may be the feedback loop:

**Read → Correct → Generalize feedback → Improve skill → Generate better wiki entries**

This transforms your personal reading experience into reusable research expertise.

### 3. Combine research discovery with accumulated knowledge

The paper discovery system should not rank papers solely by citations, awards, or popularity.

It should also consider what you already know.

For example, if you have studied several conversational retrieval methods, a new paper that introduces a fundamentally different retrieval formulation may be more valuable than another incremental improvement.

This enables **knowledge-aware paper recommendation**.

---

## 14. Suggested Next Step

Before implementation, finalize three specifications:

1. **Paper Wiki Schema v1:** Exact sections, fields, required examples, and expected reading depth.
2. **Paper Discovery and Ranking v1:** Sources, quality signals, personalized priorities, and reading queue.
3. **Human Feedback Protocol v1:** How corrections are applied, generalized, and verified without retaining feedback records.

These three specifications will determine most of the system's quality. The skills, prompts, and harness can then be designed around them.

**Guiding principle:** Build a system that helps you understand better, not merely one that stores more papers.

---

## 15. To-Do List

- [ ] **Add a special-topics folder.** Create `wiki/topics/special/` for topic syntheses built from selected wiki pages. Each synthesis should link to the pages it draws on rather than duplicate their content.
- [x] **Create a commit-driven skill improvement workflow.** [`improve-skill`](../.github/skills/improve-skill/SKILL.md) reviews the latest commit's diff and proposes evaluated skill changes for human approval. Skip one-off corrections.
