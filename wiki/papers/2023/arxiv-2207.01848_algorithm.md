---
schema_version: 1
kind: algorithm
paper: arxiv-2207.01848
title: "TabPFN: A Transformer That Solves Small Tabular Classification Problems in a Second"
year: 2023
source:
  version: v6
  url: https://arxiv.org/pdf/2207.01848v6
sources:
  S1: "Section 2, Equations 1–2 and Figure 1, pp. 2–3"
  S2: "Section 3 and footnote 1, pp. 3–5"
  S3: "Sections 4.3–4.5 and Figure 2, pp. 5–6; Appendix C.1, pp. 26–27"
  S4: "Appendix C.2.1, p. 27; Appendix C.2.6, pp. 28–29"
  S5: "Appendix D, Algorithm 1, p. 29; Appendices E.1–E.3, pp. 29–30"
---

# TabPFN: A Transformer That Solves Small Tabular Classification Problems in a Second

## Core Idea

Conventional per-dataset fitting:

- Learn model parameters from the labeled rows of one table.
- Repeat the fitting for the next table, then predict with its fitted model.

TabPFN:

- Learn a reusable prediction procedure offline by predicting held-out rows in many synthetic tables.
- At use time, feed the labeled rows and query features into the same pretrained network. A forward pass produces class probabilities without refitting the weights. [S1] [S2]

**Important distinction.** Structural causal models generate some of the training tables; TabPFN does not infer a causal graph for a new table or estimate intervention effects. It directly approximates the posterior predictive distribution: probabilities obtained by averaging predictions over possible generating mechanisms under the prior, given the observed data. [S1] [S3]

## Input Contract

**Illustrative example:** Three labeled rows and one query. The names below are for the reader, not the model. The same row values will serve first as a synthetic exercise and then as a separate mock real table. [S1]

| Row | Feature A | Feature B | Class |
| --- | ---: | ---: | --- |
| 1 | 1 | 2 | 0 |
| 2 | 2 | 6 | 0 |
| 3 | 3 | 4 | 1 |
| 4 | 4 | 6 | Unknown to the predictor |

```python
X_context = [[1, 2], [2, 6], [3, 4]]
y_context = [0, 0, 1]
X_query = [[4, 6]]
```

- **Feature names or text?** No. A row is a numerical vector, not a sequence of feature-name tokens. **Label names?** No. The labels supplied are numerical class IDs. [S1] [S3]
- **Positions?** Yes for slots within a row: column 1 must mean the same thing across all rows in a given pass. No for row position as an identifier: the labeled rows are treated as a set. Feature slots and class IDs are rotated during prior-fitting, so a particular slot or ID need not have the same meaning across tasks. [S1] [S2] [S4]
- **Query labels or other query rows?** No. There is one token per row: conceptually `Embed(x, y)` for a labeled row and `Embed(x)` for a query. Labeled rows attend to one another; each query attends only to labeled rows, not to itself or other queries. A residual connection still carries its own state. The output is one probability vector over classes per query. [S1] [S5]

**Paper actually:** The arrays above are the raw task values, not the final embeddings. The method normalizes features with statistics from labeled rows only. Its encoder scales the feature values by the ratio of maximum to actual width and zero-pads to 100 columns. Inference can also use a power transform fitted on labeled rows. [S4] [S5]

## Phase Walkthrough

### Phase 1: Generate one synthetic task

**Illustrative example:** Build the four-row table from the Input Contract. TabPFN samples one generator per dataset: a Bayesian neural network (BNN) or a structural causal model (SCM), with equal probability. The alternatives below produce the same tiny table only to make the two procedures easy to compare. [S3]

#### BNN route

1. Use the stand-in function `t = 2A - B` with noise set to zero for the example. **Paper actually:** sample a neural network's architecture and weights for the task; sample each row's input and run it through that network with sampled noise. [S3]
2. With inputs `(1,2), (2,6), (3,4), (4,6)`, the stand-in produces continuous targets `[0, -2, 2, 2]`. [S3]

#### SCM route

1. Use the stand-in graph equations `H = e_H`, `A = H`, `B = 2H + e_B`, `t = 2H - B`. **Paper actually:** sample a layered network and its edge weights, drop edges to form a directed acyclic graph, and choose feature and target nodes. Sample one activation for the dataset (Tanh, LeakyReLU, ELU, or Identity). For each row, each node applies that activation to its weighted parent inputs plus sampled noise. The selected target can be a cause or an effect of selected features. [S3]
2. For noise pairs `(e_H, e_B) = (1,0), (2,2), (3,-2), (4,-2)`, keep the resulting `A`, `B`, and `t`. These give the same four inputs and targets as above; the node `H` and the graph are not part of the prediction input. [S3]

#### Convert targets to classes for either route

1. Take two classes and choose the observed target `0` as the boundary. Count the boundaries strictly below each target: `[0, -2, 2, 2]` becomes `[0, 0, 1, 1]`. Equality stays in the lower bin. **Paper actually:** sample the class count and the corresponding number of boundaries from the targets, then shuffle the class IDs. For the toy, take the shuffle that leaves the IDs unchanged. [S3]
2. Pass the four feature rows and class IDs to prior-fitting. At this point all four labels are known, but no Transformer weights have been updated. [S1] [S5]

### Phase 2: Prior-fit on synthetic tasks

**Illustrative example:** Hold out row 4 of the generated table. Its label `1` is available to the loss but absent from the model input. [S1] [S5]

1. Condition on rows 1–3 with labels `[0, 0, 1]`. For the stand-in normalization arithmetic, use their column means `[2, 4]` and sample standard deviations `[1, 2]`. The normalized context vectors are `[[-1, -1], [0, 1], [1, 0]]` and the query is `[2, 1]`. Applying the paper's encoder rule for two columns scales these coordinates by 50 and appends 98 zeros to each vector. **Paper actually:** normalize using labeled rows, rotate feature slots and class IDs during training, and draw task splits uniformly at random; the toy uses the identity rotations and a chosen split. [S1] [S4] [S5]
2. Predict a distribution for the query. If the modeled probabilities for `[0, 1]` were `[0.25, 0.75]` (illustrative, not computed), the held-out label `1` gives cross-entropy `-ln(0.75) ≈ 0.288`. With more queries, Algorithm 1 sums their negative log probabilities; no query label is provided as context. [S1] [S5]
3. Backpropagate the loss to update the shared Transformer weights, then repeat across tasks. **Paper actually:** the final 12-layer model used Adam and trained for 18,000 steps at 512 datasets per batch, or 9,216,000 synthetic datasets of 1,024 rows each. The authors report 20 hours on eight NVIDIA RTX 2080 Ti GPUs. [S2] [S5]

### Phase 3: Predict on a new table with frozen weights

**Illustrative example:** Now treat the table in the Input Contract as a new observed dataset, unrelated to either toy generator. Row 4's label is unknown; the synthetic label from Phase 2 is not carried into this task. [S1]

1. Use the three labeled rows to compute preprocessing statistics. With the same illustrative normalization, the query `[4, 6]` becomes `[2, 1]`, then `[100, 50, 0, …, 0]` after scaling and padding. The model receives the three labeled tokens and the one unlabeled query token, not the boundary or graph from Phase 1. [S1] [S4] [S5]
2. Run the fixed network. If it returns `[0.3, 0.7]` (illustrative, not computed), class `1` is the most probable prediction, not a known ground-truth label. There is no held-out loss or gradient update in this prediction step. [S1]
3. **Paper actually:** one forward pass is enough for a prediction; the paper also evaluates an ensemble of up to 32 passes using different feature rotations, class-ID rotations, and optional power transforms. The available combinations cap the number of passes: with two features, two classes and two transform choices, this toy permits at most eight distinct ensemble members. [S2] [S4]

## Phase Comparison

| Aspect | Generate a task | Prior-fit | Predict on a new table |
| --- | --- | --- | --- |
| Data | Samples from one BNN or SCM | Synthetic context and queries | Observed context and queries |
| Feature names | No semantic names supplied | Not used | Not used |
| Feature values | Drawn or read from graph nodes | Numeric, normalized and encoded | Numeric, normalized and encoded |
| Context labels | Discretized targets with shuffled IDs | Numerical IDs in context tokens | Observed numerical IDs in context tokens |
| Query labels | Generated with the rest of the table | Used in the loss, hidden from the input | Not supplied |
| Gradient updates | None | Yes | None |
| Objective | Produce a classification task | Minimize held-out cross-entropy | Predict class probabilities |
| Parameters | Generator sampled for each task | Shared Transformer weights updated | Same Transformer weights frozen |
| Data-generating relationship | Sampled from the prior | Varies across tasks; not supplied as input | Unknown |

Sources: generators and label construction [S3]; conditioning and loss [S1]; preprocessing and architecture [S4] [S5].

## Key Distinctions

`f_{θ_table}(x) → class probabilities` (fit weights per table) versus `f_θ(D_context, x) → class probabilities` (freeze weights; change the labeled context). Both predictions depend on data, but the new table enters TabPFN as input rather than through an optimizer. [S1]

**Subtle point.** Even on the synthetic example, guessing class 1 does not mean TabPFN has recovered `2A - B`, the class boundary, or the hidden node `H`. Its target is a probability distribution over the query's label, not a symbolic rule or a graph. [S1] [S3]

## Takeaway

The unit of pretraining is a classification task, not an isolated row. The reusable pattern is:

1. Define a distribution over generators that reflects plausible structure in the target domain.
2. Sample tasks and withhold part of each task's answers.
3. Train one model to predict those answers from the evidence that remains visible.
4. On a new task, supply fresh evidence and keep the learned weights fixed.

## Source Locators

- S1: Section 2, Equations 1–2 and Figure 1, pp. 2–3
- S2: Section 3 and footnote 1, pp. 3–5
- S3: Sections 4.3–4.5 and Figure 2, pp. 5–6; Appendix C.1, pp. 26–27
- S4: Appendix C.2.1, p. 27; Appendix C.2.6, pp. 28–29
- S5: Appendix D, Algorithm 1, p. 29; Appendices E.1–E.3, pp. 29–30
