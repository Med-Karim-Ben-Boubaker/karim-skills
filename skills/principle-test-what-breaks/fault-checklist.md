# Fault checklist

Walk the list for each data system the change touches, and **Any stage** for every change with workers, leases or external services. Every item that applies becomes a test case, or a line in the spec's **Limits and Failure Modes**; every item that doesn't apply is marked so, with the reason.

**Any stage with workers, leases or external services**
- Concurrency × per-worker cost fits every resource cap (memory, open files, connections).
- The longest single step fits inside the lease's TTL, or the lease is renewed during the step.
- Every external cap (bytes, pixels, tokens, rate) is checked before the call, not discovered by the refusal.
- Storage calls per item stay constant as the input grows.
- **Repeat flow**: the same input or request a second time gives the outcome the spec states (no duplicate, or a clear refusal).
- **Multi-user flow**: two users or workers act on the same item at once, and one's action does not corrupt the other's.
- One item's failure (a refusal, a corrupt record) stops that item, not the whole run, when the spec says the run continues.

**Input documents and files**
- The largest real file, and one just over every cap it meets.
- A file of the wrong type, an empty file, a truncated or corrupt file, a file with a broken text layer or encoding.
- A file missing a field the code reads; a field present but empty.

**Database**
- The input limits match the column limits (type, length), and the error reaches the user.
- Input with quotes, SQL syntax, Unicode and empty values is stored intact.
- A write interrupted halfway leaves no partial rows across related tables, also when it spans services.
- Retries and their timeout: what repeats, and what the user sees meanwhile.
- Concurrency: **lost update** (two writers, one decrement), **dirty or partial read** (flag set before the count), two buyers of the last item.
- **Replication lag**: **read-your-writes**, **monotonic reads** (time going backwards across refreshes), **consistent prefix** (an answer before its question), **write conflicts** between leaders.

**Cache**
- Expiry at the **TTL** refreshes the value.
- The cache is down: the fallback path or the recovery flow works.
- The cache and the database drift apart: which one wins, and when they resync.
- A distributed cache routes each key to the right node.

**Batch job**
- The whole input is processed; a run that stops halfway is visible as incomplete.
- Corrupt records (nulls, huge numbers, wrong types, missing keys) are flagged and quarantined.
- A rerun cleans up or overwrites the failed run's output.
- A new input format from a sender fails loudly.
- **Data skew** and the largest single item stay within the envelope.
- The job does not starve the online system of capacity.
- Two views of the same data (a count, a total, a status) are computed from one source and agree.

**Event stream**
- The event schema is a contract: a change retests producer and consumer together, with **backward and forward compatibility** (schema registry, **consumer-driven contract test**).
- Events that must be ordered are processed in order, also after a consumer restarts from its **offset**.
- A poison event lands in the **dead letter queue** with its error.
- The broker is down: producer and consumer retry, and nothing is lost or doubled.
- **Consumer lag**: consumers keep up with the producer at peak.

**Outside input** (forms, APIs, uploads)
- Every rule is enforced on the server, not only in the UI.
- Injection attempts (SQL, script, path, prompt) are stored or refused intact, never executed.
- Secrets and personal data stay out of logs, errors and traces.

**Deploy**
- A smoke test after the release reaches each entry point (CLI, web view, API), so a missing dependency or setting fails there and not in the first real run.

## Large tests and data

- Large tests create their data through the app's public API, never by inserting rows, so a schema change breaks no test. A downstream system with no API is the one exception.
- A real database or broker in a test is an integration test: use a throwaway container (Testcontainers) in the same clean state every run.
