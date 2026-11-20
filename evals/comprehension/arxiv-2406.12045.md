# τ-bench comprehension check

Read through **Differentiators** in the [wiki entry](../../wiki/papers/2024/arxiv-2406.12045.md), aiming for five minutes. Close the page before answering. Record reading time and score one point per correct answer; no human timing data has been collected yet.

1. What does the benchmark check at the end of an episode? Give one example of a policy violation it could miss.
2. A task passes two of four trials. Compute pass^2 and pass@2 from the six pairs of trials. Why are the answers different?
3. Give one capability that this benchmark exercises beyond producing a correct tool call from a complete initial instruction.

<details>
<summary>Answer key</summary>

1. It checks the final database state and the required user-facing output. It could miss skipping confirmation if both checks pass.
2. Pass^2 is 1/6: only one pair has both successes. Pass@2 is 5/6: only one pair has no success.
3. For example, the agent has to obtain missing information or explicit authorization through a conversation before acting.

</details>
