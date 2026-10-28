# Optimize

Move **one number** (latency, memory, bundle size, throughput, an eval score) while the behaviour holds. You own the metric and the experiment's integrity.

A one-off regression ("this got slow") is a bug: use diagnosing-bugs. This branch is deliberate, iterative improvement.

## Process

### 1. Fix the metric

Call the Skill tool with "how" over the target first, so the workload and every later hypothesis are grounded in how the code actually runs.

Name one metric, the direction that counts as better, a workload that reproduces the user's complaint, and a stop condition that pairs a target with a minimum number of attempts, so a lucky early win doesn't end the run. Use the user's numbers when given.

### 2. Build and freeze the harness

Call the Skill tool with "principle-build-the-lever": one repeatable command that runs the workload and prints the metric, sampled enough to clear the noise (median of N runs, not one). Prove it's sensitive: an easier workload must score visibly better. Then freeze it: no harness edits during the run.

Call the Skill tool with "principle-explain-the-number" on the baseline: name what limits it and rule out that it measures something other than the work. Record the baseline and a green run of the test suite before any change.

### 3. Loop: one change, one measurement

Keep a log outside the tree, one row per attempt: hypothesis, change, before, after, delta, tests, kept or reverted.

Each iteration:

1. Name one hypothesis tied to a mechanism ("X blocks first paint, defer it"), not "try memoizing something". Cheapest first: don't do the work, don't do it twice, do less, do it later, do it concurrently, do it cheaper.
2. Make that one change.
3. Measure with the frozen harness and run the tests.
4. Keep it only if the metric moves past noise and the tests stay green. Otherwise revert it in full.

Call the Skill tool with "principle-sequence-verifiable-units": never stack untested changes. One commit per kept change. Call the Skill tool with "principle-laziness-protocol": a change that holds the number while simplifying the code is a win; a win that breaks behaviour is reverted.

When several independent hypotheses are live, call the Skill tool with "principle-separate-before-serializing-shared-state" and test each in its own worktree.

### 4. Stop honestly

Stop when the stop condition is met, or when the remaining ideas are marginal. On a plateau, change the category of hypothesis before concluding. Never relax the target to declare victory.

Report baseline to final with the delta, iterations kept vs reverted, each kept change in one line, and the next idea you'd try.

## Anti-patterns

- **Claiming a win from reading the code.** Only the harness decides.
- **Tuning the harness mid-run.** A moved ruler measures nothing.
- **Keeping "might help" changes.** Unmeasured changes get reverted.
