---
name: principle-small-verified-steps
description: "Advances work in small steps, each proven on the real artifact with a check that can go red before the next starts: vertical slices, tracer bullets, scripts for repetitive edits, refactor commits kept apart from behaviour commits. Use when planning or executing multi-step work (features, refactors, migrations, sweeps of similar edits), when ordering commits, and before declaring any task done. For test design, use tdd; for debugging, use principle-fix-root-causes."
---

# Small Verified Steps

The chance of a defect grows with the size of a change, and you know a behaviour only as far as you have tested it. So work in **baby steps**, each the smallest move visibly toward the goal and each ending in a state you can check: **orient, step, learn**, and repeat.

- **Slice vertically.** Each step is a **tracer bullet**: a thin path that runs end to end through every layer, growing from a **walking skeleton**. A working system grows from a simpler working system (**Gall's law**).
- **Prove it on the real artifact.** Run the feature, read the actual value, open the actual output. "It compiles", a passing mock and a subagent's "done" are claims, not proof.
- **A check counts only if it can go red.** Break the behaviour on purpose and watch the check fail before you trust it passing (the idea behind **mutation testing**). Test through the public interface so refactors keep it green (`tdd` skill). Keep the loop tight: **FIRST** tests (fast, independent, repeatable, self-validating, timely) and a **ten-minute build**: the full build and test run stays fast enough to run on every change.
- **Build the lever.** For repetitive edits or checks, write the script, codemod or generator. It does the work the same way every time, and a reviewer can rerun it.
- **Make the change easy, then make the easy change** (**preparatory refactoring**). Refactoring commits and behaviour commits stay separate; stack them so the sequence proves itself (failing test, then the fix).
- **Stop at red.** When a step fails, fix it before building the next one on top.

## Example: vertical slices

Adding a discount to orders:

1. The API returns `discount: 0` on every order. Check: one real request.
2. Pricing applies a percentage discount. Check: a unit test, red then green.
3. The checkout page shows it. Check: open the page.

Each step runs end to end. Slicing by layer (all schema, then all API, then all UI) leaves nothing to check until the end.

## Reporting done

State what was run and what was observed:

```
Done: CSV export skips empty rows.
Proof: test_export_skips_empty_rows failed before the fix (3 rows != 2) and passes after;
`app export --in sample.csv` writes 2 rows.
```

## When it bends

A **spike** exists to learn, not to ship: use the `prototype` skill and throw the code away.

**Terms:** baby steps, spike, incremental delivery, test-first programming, ten-minute build, vertical slice, tracer bullet, walking skeleton, Gall's law, red-green-refactor, FIRST tests, mutation testing, continuous integration, preparatory refactoring, atomic commits.
