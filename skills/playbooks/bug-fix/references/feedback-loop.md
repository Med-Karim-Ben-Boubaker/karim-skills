# Building the feedback loop

The loop is the fix. With a tight signal that goes red on *this* bug, bisection and hypotheses just consume it. Without one, staring at code won't save you.

## Ways to build one, roughly in order

1. A failing test at whatever seam reaches the bug.
2. A curl or HTTP script against a running dev server.
3. A CLI call with a fixture input, diffed against a known-good snapshot.
4. A headless browser script (Playwright) asserting on DOM, console, or network.
5. A replayed capture: a saved request, payload, or event log run through the code path.
6. A throwaway harness: the smallest slice of the system that hits the bug in one call.
7. A fuzz loop: 1000 random inputs, for "sometimes wrong".
8. A bisection harness for `git bisect run`, when the bug appeared between two known states.
9. A differential loop: the same input through old and new versions, outputs diffed.
10. Last resort, a human in the loop, driven by [`../scripts/hitl-loop.template.sh`](../scripts/hitl-loop.template.sh).

## Tighten it

Faster (skip unrelated setup), sharper (assert the exact symptom, not "didn't crash"), deterministic (pin time, seed randomness, isolate filesystem and network).

**Flaky bugs:** aim for a higher reproduction rate, not a clean repro. Loop the trigger, add stress, narrow timing windows. 50% is debuggable; 1% is not.

## The bar

One command you have already run, shown with its (redacted) output, that is:

- **Red-capable:** it hits the real code path and asserts the user's exact symptom.
- **Deterministic:** same verdict every run, or a pinned high rate for flaky bugs.
- **Fast:** seconds.
- **Agent-runnable:** no human, except through that HITL script.

## When you can't build one

Stop and say so. List what you tried. Ask for access to an environment that reproduces it, a redacted capture (HAR, logs, core dump), or permission for temporary instrumentation.
