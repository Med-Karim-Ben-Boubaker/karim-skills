---
name: principle-design-for-operations
description: "Keeps software correct and identical wherever it runs: crash-only design (fails, stops halfway, runs twice, runs concurrently), idempotent jobs, append-only data runs, and twelve-factor config, logs and releases. Use when writing jobs, pipelines, ETL, workers, CLIs, retries, config, env vars, secrets, logging, deployment or releases."
---

# Design for Operations

Software runs many times, in many places, and stops at bad moments. Design it so a failure stops the run with the real error (`principle-fix-root-causes`), the next run converges from the current state, and the same build behaves the same on a laptop and on the server.

## Crash-only

**Crash-only software** has one way to stop, crashing, and one way to recover, running again. Ask of every operation that changes state: what if it **fails**, **stops halfway**, **runs twice**, or **runs at the same time** as another?

- **Idempotent operations.** A repeat gives the same end state: upserts, **idempotency keys**, deduplication by message ID, "set to X" instead of "add X".
- **Converge from current state** (**reconciliation**). Read what exists, compare it with the goal, apply the difference.
- **Atomic steps.** Group related writes in a transaction; write to a temp path and rename it into place. Anything a run leaves behind (a lock, a temp file, a claimed job) carries what the next run needs to recognise it as stale.
- **At-least-once delivery plus an idempotent consumer** gives effectively-once processing. Use the **transactional outbox** when a database write and a message must both happen.
- **Separate before serialising.** Give each writer its own file, key, partition or table, and merge at read time (**single-writer principle**). When one invariant truly spans shared state, serialise it: a transaction, **optimistic concurrency**, or a lock with a **fencing token**.
- **Bound every wait.** A timeout on every remote call. Retry only transient errors on idempotent operations, a fixed number of times with **exponential backoff and jitter**; after the last attempt, raise.

**The test:** kill it at each step and run it again; run two copies at once; make each dependency fail. The end state is the same, and every failure surfaces as an error.

## Data runs

- **Append-only runs.** Each run writes its own partition and writes its completion marker last; readers see complete runs only.
- **Tasks are functions of their input partition**, so any task can rerun and only new partitions need work.
- **A backfill is a new run**, never an edit in place.
- **Write, audit, publish.** One step validates a run, and one step swaps the pointer readers follow. An agent's runs write to the sandbox the repo's run recipe names (`### Run`) and are compared with the default branch's output on the same input; publishing to the real location waits for a person's OK.

## Twelve-factor

The same build runs everywhere when:

| Factor | Rule |
|---|---|
| Config | Comes only from the environment, parsed once at the edge into a typed settings object. Code holds no default for anything that differs between deploys. Keep three kinds apart: **arguments** say what this run does (`--town`, `--limit`, `--json`); **config** says where and with what it runs (URLs, models, concurrency); **secrets** are keys, never printed, logged or committed. |
| Names | Name the kind of value: one prefix per app, `__` between area and name, addresses end in `_URL`, filesystem paths in `_PATH`. |
| Backing services | Databases, buckets and model APIs are attached by URL, and the scheme picks the adapter (`s3://`, `file://`), so dev and prod differ only in config. |
| Dependencies | Declared, locked, and installed frozen. |
| Build, release, run | A release is an immutable build plus its config. Deploy by switching releases; roll back by switching back. |
| Processes | Stateless; state lives in backing services. |
| Concurrency | Scale out with more processes. Concurrency is config, not a flag. |
| Disposability | Fast start. On SIGTERM, finish or hand back in-flight work within a grace period. |
| Dev/prod parity | Same CLI, same image, same commands; only config differs. |
| Logs | Structured events to stdout or the telemetry pipeline; the platform routes and stores them. |
| Admin processes | One-off commands run on the same release with the same config. |

## Example

```python
# Masks the failure: the report looks real and the run reports success.
try:
    rates = fetch_rates(day)
except Exception:
    rates = DEFAULT_RATES

# Crash-only: the run stops with the real error, and the rerun converges.
rates = fetch_rates(day)
```

```sql
-- A rerun replaces the day's rows instead of doubling them.
BEGIN;
DELETE FROM daily_sales WHERE day = '2026-10-29';
INSERT INTO daily_sales SELECT ... WHERE day = '2026-10-29';
COMMIT;
```

## When it bends

A one-off command you run once by hand, and watch, can skip the rerun rules; it still fails loudly. Anything scheduled, retried, triggered by events or run by more than one worker gets all of it.

**Terms:** crash-only software, fail-fast, idempotence, idempotency key, reconciliation loop, atomicity, transactional outbox, single-writer principle, optimistic concurrency, compare-and-swap, fencing token, exponential backoff with jitter, functional data engineering, write–audit–publish, medallion architecture, Twelve-Factor App, backing service, immutable release, disposability, dev/prod parity.
