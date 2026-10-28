---
name: perf
description: "Playbook for moving one number (latency, memory, bundle size, throughput, an eval score) against a baseline while behaviour holds. Use for 'make X faster', 'reduce memory', 'improve the score'. A sudden regression ('this got slow') is a bug-fix."
user-invocable: false
---

# Perf

**You own the measurement.** Only the harness decides; reading the code never proves a win.

1. **Fix the metric.** Call the Skill tool with "how" over the target. Name one metric, which direction is better, a workload that reproduces the complaint, and a stop condition (target plus a minimum number of attempts). *Done when:* all four are written down.
2. **Build and freeze the harness** (**principle-build-the-lever**). One command that runs the workload and prints the metric, median of N runs. Prove it's sensitive: an easier workload scores visibly better. *Done when:* the baseline number and a green test run are recorded, and the harness is frozen.
3. **Explain the baseline** (**principle-explain-the-number**). *Done when:* you can name what limits the number, and have ruled out that it measures something else.
4. **Loop: one hypothesis, one change, one measurement.** Cheapest first: don't do it, don't do it twice, do less, do it later, do it concurrently, do it cheaper. Keep a change only if the metric moves past noise and the tests stay green; otherwise revert it fully (**principle-sequence-verifiable-units**). *Done when:* each attempt is a row in a log outside the tree: hypothesis, change, before, after, kept or reverted. One commit per kept change.
5. **Stop honestly.** Stop at the stop condition or when ideas turn marginal. On a plateau, change the category of hypothesis first. Never relax the target. Then run the **reviewing** playbook. *Done when:* review returned a verdict.

**Reply:** baseline → final with the delta and unit, attempts kept vs reverted, each kept change in one line, the log path, the next idea you'd try.
