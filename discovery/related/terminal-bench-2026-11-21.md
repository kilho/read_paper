# Related paper shortlist

OpenAlex checked: 2026-11-21 (UTC).

## Seed papers

- [Terminal-Bench: Benchmarking Agents on Hard, Realistic Tasks in Command Line Interfaces](<https://openalex.org/W7125193990>)

## Prioritized reading list

Citation impact leads the score: log10(1 + OpenAlex citations), plus bounded bonuses for verified context, venue recognition, watchlist matches, and links to multiple seeds. Unknown counts get no citation points; totals favor older work. These are reading signals, not proof of quality.

Only papers with supplied relevance evidence are eligible; a citation or award alone does not qualify.

1. [SWE-bench: Can Language Models Resolve Real-World GitHub Issues?](<https://openalex.org/W4387561453>) (2023, International Conference on Learning Representations) — **2,627 OpenAlex citations**, score 3.92
   - [presentation](<https://iclr.cc/virtual/2024/session/15084>): ICLR 2024: Oral (Oral 4A).
   - [related-work](<https://arxiv.org/pdf/2601.11868v1#page=11>) (2601.11868): Section 6, p. 11, places SWE-bench in repository-level software engineering. Appendix D and Table 5, p. 84, describe the Verified-subset adapter: execute tests on patches for real GitHub issues, a narrower use of outcome-based verification than the seed's mixed CLI tasks.
2. [OSWorld: Benchmarking Multimodal Agents for Open-Ended Tasks in Real Computer Environments](<https://openalex.org/W4415797693>) (2024, neural information processing systems) — **1,982 OpenAlex citations**, score 3.60
   - [Open PDF](<https://arxiv.org/pdf/2404.07972>)
   - Cited by [Terminal-Bench: Benchmarking Agents on Hard, Realistic Tasks in Command Line Interfaces](<https://openalex.org/W7125193990>).
   - [related-work](<https://arxiv.org/pdf/2601.11868v1#page=11>) (2601.11868): Section 6, p. 11, contrasts computer-use benchmarks with the seed's terminal-shell focus. OSWorld is the GUI counterpart: realistic initial computer states and execution-based checks for open-ended desktop and web tasks (OSWorld abstract).
3. [AppWorld: A Controllable World of Apps and People for Benchmarking Interactive Coding Agents](<https://openalex.org/W4402671485>) (2024, Proceedings of the conference - Association for Computational Linguistics. Meeting) — **612 OpenAlex citations**, score 3.09
   - [Open PDF](<https://aclanthology.org/2024.acl-long.850.pdf>)
   - [related-work](<https://arxiv.org/pdf/2601.11868v1#page=84>) (2601.11868): Section 6, p. 11, and Table 5, p. 84, identify AppWorld as a stateful, multi-application adapter. It tests interactive coding through app APIs rather than general-purpose CLI work.
4. [SkillsBench: Benchmarking How Well Agent Skills Work Across Diverse Tasks](<https://openalex.org/W7129079999>) (2026, arXiv (Cornell University)) — **444 OpenAlex citations**, score 2.95
   - [Open PDF](<https://arxiv.org/pdf/2602.12670>)
   - Cites [Terminal-Bench: Benchmarking Agents on Hard, Realistic Tasks in Command Line Interfaces](<https://openalex.org/W7125193990>).
   - [citing-paper](<https://arxiv.org/abs/2602.12670>) (2601.11868): Abstract, evaluation metrics and Section 7: uses deterministic verifiers and Terminal-Bench's task-macro pass-rate aggregation, then pairs runs with and without curated skills to isolate their effect.
5. [Meta-Harness: End-to-End Optimization of Model Harnesses](<https://openalex.org/W7147383744>) (2026, arXiv (Cornell University)) — **443 OpenAlex citations**, score 2.95
   - [Open PDF](<https://arxiv.org/pdf/2603.28052>)
   - Cites [Terminal-Bench: Benchmarking Agents on Hard, Realistic Tasks in Command Line Interfaces](<https://openalex.org/W7125193990>).
   - [citing-paper](<https://arxiv.org/html/2603.28052#S4.SS3>) (2601.11868): Abstract and Section 4.3: searches over harness code using traces and evaluates the resulting harnesses on TerminalBench-2. This is benchmark-specific optimization, not held-out task transfer.
6. [SWE-Lancer: Can Frontier LLMs Earn \$1 Million from Real-World Freelance Software Engineering?](<https://openalex.org/W4407759089>) (2025, arXiv (Cornell University)) — **158 OpenAlex citations**, score 2.70
   - [Open PDF](<https://arxiv.org/pdf/2502.12115>)
   - [presentation](<https://icml.cc/virtual/2025/poster/43573>): ICML 2025: Spotlight Poster.
   - [related-work](<https://arxiv.org/pdf/2601.11868v1#page=84>) (2601.11868): Section 6, p. 11, and Table 5, p. 84, discuss and describe the adapter for paid freelance engineering tasks. SWE-Lancer also tests choosing between implementation proposals, unlike the seed's final-container-state tasks.
7. [SWE-bench Goes Live\!](<https://openalex.org/W4414887410>) (2025, neural information processing systems) — **204 OpenAlex citations**, score 2.61
   - [Open PDF](<https://arxiv.org/pdf/2505.23419>)
   - Cited by [Terminal-Bench: Benchmarking Agents on Hard, Realistic Tasks in Command Line Interfaces](<https://openalex.org/W7125193990>).
   - [related-work](<https://arxiv.org/pdf/2601.11868v1#page=84>) (2601.11868): Table 5, p. 84, describes the SWE-bench Live adapter: continuously refreshed real issue-resolution tasks are a focused comparison for contamination and performance on new repository work.
8. [MLGym: A New Framework and Benchmark for Advancing AI Research Agents](<https://openalex.org/W4407806895>) (2025, arXiv (Cornell University)) — **191 OpenAlex citations**, score 2.58
   - [Open PDF](<https://arxiv.org/pdf/2502.14499>)
   - Cited by [Terminal-Bench: Benchmarking Agents on Hard, Realistic Tasks in Command Line Interfaces](<https://openalex.org/W7125193990>).
   - [related-work](<https://arxiv.org/pdf/2601.11868v1#page=84>) (2601.11868): Section 6, p. 11, and Table 5, p. 84, describe MLGym as a specialized adapter for open-ended ML experimentation, training and analysis rather than the seed's mixed CLI workloads.
9. [CORE-Bench: Fostering the Credibility of Published Research Through a Computational Reproducibility Agent Benchmark](<https://openalex.org/W4403707291>) (2024, Transactions on machine learning research) — **187 OpenAlex citations**, score 2.57
   - Cited by [Terminal-Bench: Benchmarking Agents on Hard, Realistic Tasks in Command Line Interfaces](<https://openalex.org/W7125193990>).
   - [related-work](<https://arxiv.org/pdf/2601.11868v1#page=84>) (2601.11868): Table 5, p. 84, describes the CORE-Bench adapter: set up dependencies, run published research code and answer analysis tasks. It isolates the environment setup and research reproduction work present in the broader terminal benchmark.
10. [ProgramBench: Can Language Models Rebuild Programs From Scratch?](<https://openalex.org/W7160416041>) (2026, arXiv (Cornell University)) — **109 OpenAlex citations**, score 2.34
   - [Open PDF](<https://arxiv.org/pdf/2605.03546>)
   - Cites [Terminal-Bench: Benchmarking Agents on Hard, Realistic Tasks in Command Line Interfaces](<https://openalex.org/W7125193990>).
   - [citing-paper](<https://arxiv.org/abs/2605.03546>) (2601.11868): Abstract and agent-scaffold discussion: reconstructs complete CLI programs under a minimal agent in a container. Tests compare executable behavior rather than prescribing an implementation, extending the seed's outcome-checking approach to full programs.
11. [Harness-Bench: Evaluating Agent Harnesses across Models and Realistic Workflows](<https://openalex.org/W7162690279>) (2026, arXiv (Cornell University)) — **87 OpenAlex citations**, score 2.24
   - [Open PDF](<https://arxiv.org/pdf/2605.27922>)
   - Cites [Terminal-Bench: Benchmarking Agents on Hard, Realistic Tasks in Command Line Interfaces](<https://openalex.org/W7125193990>).
   - [citing-paper](<https://arxiv.org/abs/2605.27922>) (2601.11868): Abstract and related work: directly contrasts executable tasks with Terminal-Bench and compares model-harness configurations under shared offline environments and budgets. It collects traces and validator output to diagnose how runs fail, not just whether they finish.
12. [Rethinking the Evaluation of Harness Evolution for Agents](<https://openalex.org/W7168361355>) (2026, arXiv (Cornell University)) — **80 OpenAlex citations**, score 2.21
   - [Open PDF](<https://arxiv.org/pdf/2607.12227>)
   - Cites [Terminal-Bench: Benchmarking Agents on Hard, Realistic Tasks in Command Line Interfaces](<https://openalex.org/W7125193990>).
   - [citing-paper](<https://arxiv.org/abs/2607.12227>) (2601.11868): Abstract and Tables 1-3: uses Terminal-Bench 2.1 to test whether harness evolution beats matched-budget test-time search or transfers to held-out tasks. A useful counterpoint to benchmark-specific harness optimization.
13. [LLM-Supported Natural Language to Bash Translation](<https://openalex.org/W4411119257>) (2025, Conference of the North American Chapter of the Association for Computational Linguistics: Human Language Technologies (NAACL-HLT)) — **19 OpenAlex citations**, score 1.60
   - [Open PDF](<https://aclanthology.org/2025.naacl-long.555.pdf>)
   - Cited by [Terminal-Bench: Benchmarking Agents on Hard, Realistic Tasks in Command Line Interfaces](<https://openalex.org/W7125193990>).
   - [related-work](<https://arxiv.org/pdf/2601.11868v1#page=11>) (2601.11868): Section 6, Language Models and the Terminal, p. 11: natural-language-to-Bash translation isolates command generation; the seed tests completing a multi-step objective in a live shell.

Shown: 13 of 13 eligible candidates.

## Coverage

OpenAlex citation links are indexed metadata, not proof that the papers discuss each other in depth. Related Work, awards, and presentation labels are only reported when supplied with source evidence; absent labels are unknown.

- Terminal-Bench: Benchmarking Agents on Hard, Realistic Tasks in Command Line Interfaces: retrieved 35 of 458 indexed citing papers, by citation count.
- Outgoing reference batch: 9 records unavailable.
- Incoming screening was targeted, not exhaustive; broad model reports were not included solely because they list a Terminal-Bench score. Adapters in Appendix D and Table 5 are integrations, not members of the 89-task Terminal-Bench 2.0 suite.
- [The Koala Benchmarks for the Shell](https://www.usenix.org/conference/atc25/presentation/lamprou), discussed in Section 6, focuses on shell program performance rather than agent task completion. Its USENIX ATC 2025 Best Paper award is in the [conference catalog](../resources/bestpaper_list.md#verified-papers); it is unranked here because OpenAlex returned HTTP 429 for the exact-title lookup.
