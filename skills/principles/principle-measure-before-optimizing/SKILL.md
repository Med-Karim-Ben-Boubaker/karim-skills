---
name: principle-measure-before-optimizing
description: "Optimises only what measurement shows matters: estimates first, profiles to name the bottleneck, reports percentiles with spread, and rules out what else a number could be measuring. Use when something is slow, when optimising, benchmarking or load testing, or before reporting or acting on a speedup, latency, throughput, cost or eval score. For a regression from a known-good baseline, use diagnosing-bugs."
---

# Measure Before Optimizing

Optimise only what a measurement shows matters; anything else is **premature optimisation**. The clean, simple design is often the fast one: fewer layers, copies and round trips. Design the **critical path** to be simple, then measure.

- **Estimate first.** A **back-of-the-envelope** figure from known costs (memory vs disk vs network latency, bytes per row, requests per second) tells you what the result should be. A measurement far from the estimate is measuring something else.
- **Find the bottleneck.** Profile (CPU profiler, **flame graph**, query plan, system counters with the **USE method**: utilisation, saturation, errors) and name the one resource or code path that limits the result. By **Amdahl's law**, speeding up a part helps only by that part's share. Ask "why not twice as fast?"; if you cannot answer, you do not know what you measured.
- **Report distributions.** **Percentiles** (p50, p95, p99), not averages; **tail latency** dominates at scale. Warm up, repeat the runs, and show the spread; the gap must exceed the noise.
- **Rule out impostors.** Errors, cached or skipped work, dead code the compiler removed, a debug build, an untuned baseline, the load generator as the bottleneck, **coordinated omission**.
- **Keep the evidence with the number:** run count, spread, the limiter. Eval scores get the same treatment: every trial did the task, and the gap holds across trials.

## Reporting a number

```
Change: insert in batches of 500 instead of one row at a time.
Result (time to load 500 rows): p50 41 → 12 ms, p95 88 → 25 ms, p99 140 → 61 ms;
  10 runs each after 2 warm-ups, spread ±4 ms.
Limiter now: disk fsync on commit (iostat: disk 95% busy).
Estimate: 500 rows at ~0.02 ms each ≈ 10 ms, close to the new p50.
Ruled out: no errors in the logs; same build and dataset for both sides.
```

**Terms:** premature optimisation, critical path, back-of-the-envelope estimation, profiling, flame graph, USE method, bottleneck, theory of constraints, Amdahl's law, Little's law, percentiles, tail latency, coordinated omission, benchmark warm-up, statistical noise.
