---
name: principle-test-what-breaks
description: "Tests what breaks, not only the user flow: names every limit and failure mode in the spec, adds limit, cost and fault tests beside functional ones, attacks finished work with hostile input, keeps checks on a trigger, and turns escaped defects into tests. Use when specifying, choosing test cases, testing code that takes outside data, or after a bug escaped."
---

# Test What Breaks

**Functional testing** follows the user flow: the expected input and the output it should give. Most failures in real runs come from elsewhere: an input nobody expected, a limit nobody named, a dependency that refused or hung. So every stage of the work asks one question, **what breaks?**: the spec names it, the build tests it, a break pass attacks it, the pipeline keeps checking it, and each defect that escapes teaches it.

A limit or a fault found by a real run costs a failed run, a diagnosis and a rerun. Named in the spec, it costs one fast test (**shift left**; **defect prevention** over defect detection).

## Spec: name what breaks

Written into the spec's **Limits and Failure Modes** (`write-spec`), before any code.

- **Operating envelope.** For each stage: the input size range, each external cap (bytes, tokens, pixels, rate), each resource cap (memory, open files, connections), and each time cap (lease TTL, timeout, budget) against the longest step inside it. Size concurrency with **Little's law**: in flight = arrival rate × latency.
- **Worst real inputs.** Pull the largest, strangest and most broken samples from the real source before building: the biggest file, the oddest format, the category with **data skew**.
- **A stated outcome for every bad input**: refuse it at the edge, scale it to fit, **quarantine** it with its reason, or keep the rest and mark the gap. Chosen here, never discovered in a run.
- **A failure mode per dependency.** It refuses (413, 429, 5xx), hangs, answers garbage, or slows down: say what the system does for each.
- **Timing risks** (race conditions, **lost update**, **replication lag**) are answered by the design, since they rarely fail a test run.
- **Abuser stories** from a short **threat model** (**STRIDE**) when the change takes input from outside or touches auth, money or secrets: "As an attacker, I cannot…".
- **Quality targets come from data**: performance and size goals from production, usage or the source, never guessed.

## Build: test the limits, costs and faults

Inside the `tdd` loop: its robustness cases test each bad input at its stated outcome. The envelope adds these.

- **Each limit is a named constant**, checked at the edge before the call, so a **boundary value analysis** test reaches it: just inside, at, and just over.
- **Assert costs, not only results** (**resource budget test**): count calls, bytes held and open handles through a fake, and assert the count stays constant or linear as N grows. Never time a unit test.
- **Each named fault runs through a fake**: the fake dependency refuses, hangs or answers garbage; a **fake clock** makes "outlasts the six-minute lease" take a millisecond. A timing risk is proven by forcing the interleaving through the seam, never with a sleep.

## Break: attack the finished work

The `break-change` pass, after building and before review. It hunts for what the spec did not name.

- **Hostile mindset** (**fault-based testing**, **error guessing**): assume it breaks and find where, from the [fault checklist](fault-checklist.md), the envelope and this code's past bugs. Attack only agreed seams, with input or faults they can really meet.
- **Generate input, don't hand-pick it**: **property-based testing** (Hypothesis, fast-check), **fuzzing**, and the **worst-case fixture corpus**. For a real input too large to keep, test the rule it trips with a synthetic input built at the boundary.
- **Fault injection** at every seam: refusal, hang, garbage, a worker killed mid-step, a step that outlasts its lease, a full disk. What a rerun must then do is in `principle-design-for-operations` (crash-only).
- **Real integrations**: a real database or broker in a throwaway container (Testcontainers), **consumer-driven contract tests** between services, and assertions on the content returned, never only the status code.
- **Check the data itself** with **data quality checks** on the input and the output: row count in range, **completeness**, **uniqueness**, **validity** (Great Expectations, Deequ, pandera).
- **Every break becomes a failing test first**, then a fix where it first went wrong (`principle-fix-root-causes`).
- **Rehearse at full size** before the first real run of a new stage, and before a release that changes its envelope: a **scale test** on a production-like machine and production-like data (anonymised real data, or synthetic data that keeps its distributions, from a generator such as Synthetic Data Vault), writing to the sandbox, then the first real run on a small slice while you watch its logs. **Load, soak and stress tests** run apart from the loop, repeated and in isolation, with third-party APIs stubbed.

## Loops: every check runs on a trigger

The pipeline's triggers, which `set-up-repo` writes under `### Checks` and CI runs. What you run while working stays in `principle-take-small-verified-steps`.

- **No check runs only by hand.** Unit and integration tests on each pipeline run; e2e before a merge request into the default branch is ready (`tdd`'s pyramid); scale and soak tests nightly or before a release, read the next morning; a **smoke test** after each deploy.
- **Every change triggers the loop**: code, config, infrastructure and test code.
- **Red means stop.** Fix it or revert it within minutes; a failing test is fixed, never skipped or commented out; nothing lands on a red pipeline.
- **Each loop has a time budget.** When one slows, move tests down the pyramid and delete duplicates.

## Learn: every escaped defect becomes a test

- **An escaped defect** (a bug a real run, a user or a manual check found) gets a root cause, a test for its whole class, and the stage above that should have caught it (`diagnose-bug`).
- **Count escaped defects by category** (limit, bad input, dependency fault, timing, config, logic). The largest category names the stage to strengthen (`run-retro`).
- **Measure coverage per area, never as one total**: 80% overall can hide a module at 0%. **Mutation testing** shows whether the tests catch a change. A metric made into a target gets gamed.

## When it bends

A one-off script run once by hand and watched needs the functional tests only. Anything that takes outside data, runs at scale, runs unattended or calls an external service gets the whole skill.

**Terms:** functional testing, data testing, shift left, operating envelope, boundary value analysis, fault-based testing, error guessing, property-based testing, fuzzing, fault injection, chaos engineering, consumer-driven contract test, data quality checks, scale test, soak test, smoke test, escaped defect, mutation testing. Source: Gayathri Mohan, *Full Stack Testing* (O'Reilly, 2022).
