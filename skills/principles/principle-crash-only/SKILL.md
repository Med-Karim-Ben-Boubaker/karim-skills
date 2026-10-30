---
name: principle-crash-only
description: "Keeps state correct when work fails, stops halfway, runs twice or runs concurrently: crash-only design, where a failure stops the run with the real error and the next run converges from current state; idempotent operations, atomic writes, idempotent consumers, one writer per piece of state, bounded waits. Use when writing jobs, pipelines, ETL, migrations, queue consumers, webhooks, scheduled tasks, or code with retries, error handling or concurrent workers. For where a fix belongs, use principle-fix-root-causes; for choosing a consistency model, use principle-name-the-trade-off."
---

# Crash-Only

**Crash-only software** has one way to stop, crashing, and one way to recover, running again. A failure stops the run with the real error; the next run starts from current state and reaches the correct end. Design every operation that changes state so that this is safe: ask what happens if it **fails**, **stops halfway**, **runs twice**, or **runs at the same time** as another.

- **Fail fast and loud.** When a call fails, a required field is missing or an assumption breaks, raise the error with its context and let it reach the caller. The run stops; the state stays recoverable; the rerun picks it up. Catch only a specific error you can truly recover from, and recover by doing the real work.
- **Real result or an error.** Every step returns the real result or raises. Guardrail: a failed step never yields default, placeholder, mock or made-up values, a simpler stand-in algorithm, or a success status. A degraded result exists only when the user decided on it: it comes from a real source (a cached copy with its age) and every caller can see it is degraded.
- **Idempotent operations.** A repeat gives the same end state. Use upserts, **idempotency keys**, deduplication by message ID, and "set to X" instead of "add X".
- **Converge from current state** (**reconciliation**). Read what exists, compare it with the goal, apply the difference. Each run works from what is, not from what the last run intended.
- **Atomic steps.** Group related writes in a **transaction**; write to a temp path and rename it into place. A crash leaves the old state or the new one, never a mix. Anything a run leaves behind (a lock, a temp file, a claimed job) carries what the next run needs to recognise it as stale.
- **At-least-once delivery plus an idempotent consumer gives effectively-once processing.** Use the **transactional outbox** when a database write and a message must both happen.
- **Separate before serialising.** Give each writer its own file, key, partition or table, and merge at read time (**single-writer principle**). When one invariant truly spans shared state, serialise it in structure: a transaction, **optimistic concurrency** (version check, compare-and-swap), a lock with a **fencing token**, or one owning process.
- **Bound every wait.** A timeout on every remote call. Retry only transient errors (timeout, 429, 503, version conflict) on idempotent operations, a fixed number of times with **exponential backoff and jitter**; after the last attempt, raise.

**The test:** kill it at each step and run it again; run two copies at once; make each dependency fail. The end state is the same, and every failure surfaces as an error.

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

-- Webhooks arrive at least once: the event ID turns a duplicate into a no-op.
INSERT INTO payments (event_id, order_id, amount) VALUES ($1, $2, $3)
ON CONFLICT (event_id) DO NOTHING;
```

## When it bends

A one-off command you run once by hand, and watch, can skip the rerun rules; it still fails loudly. Anything scheduled, retried, triggered by events or run by more than one worker gets all of it.

**Terms:** crash-only software, fail-fast, error masking, idempotence, idempotency key, reconciliation loop, atomicity, transaction, at-least-once delivery, exactly-once semantics, transactional outbox, single-writer principle, optimistic concurrency control, compare-and-swap (CAS), fencing token, lost update, race condition, exponential backoff with jitter.
