---
name: principle-take-small-verified-steps
description: "Advances work in small steps, each proven on the real artifact with the narrowest check that can go red; runs the full suite once, on the way into the default branch; backs every number with a measurement. Use when planning or executing multi-step work, choosing which tests to run, optimising or benchmarking, and before declaring any task done."
---

# Small Verified Steps

The chance of a defect grows with the size of a change, and you know a behaviour only as far as you have checked it. So work in **baby steps**, each the smallest move visibly toward the goal and each ending in a state you can check: **orient, step, learn**, and repeat. Check each step with the narrowest test that can catch what you just changed: a full run proves nothing a targeted one didn't, and costs minutes every time.

- **Slice vertically.** Each step is a **tracer bullet**: a thin path through every layer, growing from a **walking skeleton**. A working system grows from a simpler working system (**Gall's law**).
- **Prove it on the real artifact.** Run the feature the way a person would, as the repo's run recipe says (`### Run`), writing only to its sandbox; read the actual value, open the actual screenshot or output. "It compiles", a passing mock and a subagent's "done" are claims, not proof.
- **A check counts only if it can go red.** Break the behaviour on purpose and watch the check fail before you trust it passing. Test through the public interface so refactors keep it green (`tdd`).
- **Build the lever.** For repetitive edits or checks, write the script, codemod or generator. It does the work the same way every time, and a reviewer can rerun it.
- **Make the change easy, then make the easy change** (**preparatory refactoring**). Refactoring commits and behaviour commits stay separate.
- **Stop at red.** When a step fails, fix it before building the next one on top.

## Which checks to run

| When | Run |
|---|---|
| Each red → green cycle | The one test you are working on |
| The work is done and synced with its target branch | The tests for the code it touched (its file, module or package), plus typecheck and lint on changed files, once. After a later sync or fix, rerun only the tests that change touched |
| A merge request into the default branch is ready | The full suite and e2e, once: in the merge request's pipeline where the repo has one, with only the checks the pipeline leaves out run locally; without a pipeline, locally |
| A merge into an integration branch | Nothing more: no full suite, no e2e, no pipeline |
| A prompt, model, model setting or tool changed and the user wants it measured | That component's evals, smallest case set first (`principle-let-models-judge`) |

- A passing targeted run on unchanged code needs no second, wider run "to make sure".
- Code tests never call a model, the network or a GPU: they use fakes, fixtures and recorded answers. Model behaviour is measured by evals, and evals are not tests.
- A slow test is a defect: fix it as the FIRST section of `tdd` says. Report a slow suite with its time and its ten slowest tests, and mark the tests that need real I/O so targeted runs can skip them.

## Numbers

Optimise only what a measurement shows matters. Work in this order: fix the bug, build the missing tool, measure, then optimise. No tuning loops on a harness that still has the bug.

- **Estimate first.** A **back-of-the-envelope** figure from known costs tells you what the result should be. A measurement far from the estimate is measuring something else.
- **Find the bottleneck.** Profile (CPU profiler, **flame graph**, query plan, the **USE method**) and name the one resource or code path that limits the result. By **Amdahl's law**, speeding up a part helps only by that part's share.
- **Rule out impostors:** errors, cached or skipped work, a debug build, an untuned baseline, the load generator as the bottleneck.
- **Keep the evidence with the number:** what ran, how many runs, the spread when it decides the question, and the source of every figure.

## Reporting done

State what was run and what was observed. Quote output as the command printed it, and the test runner's own summary line: a run of zero tests, or with skips you can't explain, proves nothing.

```
Done: CSV export skips empty rows.
Proof: test_export_skips_empty_rows failed before the fix (3 rows != 2) and passes after;
`app export --in sample.csv` writes 2 rows. Full suite once: 412 passed in 1m10s.
```

## When it bends

A **spike** exists to learn, not to ship: use the `prototype` skill and throw the code away.

**Terms:** baby steps, spike, vertical slice, tracer bullet, walking skeleton, Gall's law, red-green-refactor, FIRST tests, mutation testing, test impact analysis, preparatory refactoring, atomic commits, premature optimisation, critical path, back-of-the-envelope estimation, profiling, bottleneck, Amdahl's law, percentiles, tail latency.
