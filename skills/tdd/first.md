# FIRST: causes and fixes

The usual ways a test breaks each letter of FIRST, and the fix for each. Measure before you fix: `pytest --durations=10` (it lists setup and call apart, so a slow setup points at a fixture), `vitest --slowTestThreshold=100`, `go test -v`.

## Fast

A unit test runs in under 100 ms, and the one-test command answers in seconds.

| Cause | Fix |
|---|---|
| `sleep`, a real timeout, a retry's backoff, polling until something happens | Pass the clock or the `sleep` in, and advance a fake one |
| The network, an HTTP API, a model | A fake at the seam, or a recorded response ([mocking.md](mocking.md)) |
| A database, a bucket, the file system | An in-memory fake of the port; a temp dir only for code whose job is files |
| A server, browser, container or subprocess started per test | Test the logic below it; one marked integration test covers the wiring |
| A large fixture: a real dataset, a full config, a model file | The smallest input that shows the behaviour, built inline in the test |
| Every combination parametrized | One case per behaviour: the typical case, each boundary, the failure |
| Heavy setup in an autouse fixture or a base class | Opt-in fixtures; read-only data built once per module |
| Slow startup: heavy imports at module level, coverage or parallel workers in the default options | Keep the core free of heavy imports; coverage and workers belong to the full-suite command |

## Isolated

| Cause | Fix |
|---|---|
| Module- or class-level state a test changes | Build the state inside the test |
| A test reads what another wrote: a row, a file, a cache | Each test arranges its own data, in a fresh temp dir or transaction |
| Env vars or global config set and never restored | `monkeypatch` (pytest), `vi.stubEnv` (Vitest), `t.Setenv` (Go) |
| It passes only in file order | Shuffle: pytest-randomly (on once installed), `vitest --sequence.shuffle`, `jest --randomize`, `go test -shuffle=on` |

## Repeatable

| Cause | Fix |
|---|---|
| `now()`, `today()`, the timezone, the locale | Inject the clock; pin the timezone and locale in the test |
| Randomness, generated IDs | A fixed seed or an injected generator |
| The order of a set, a dict, or rows read without `ORDER BY` | Sort, or compare contents |
| Real threads and timing | Test the logic on one thread; one marked test covers the race |
| The network or a live model | A recorded response ([mocking.md](mocking.md)) |

A flaky test is a bug: fix its cause, or delete it and say so. A retry only hides it.

## Self-validating

| Cause | Fix |
|---|---|
| It prints or writes output for a person to read | Assert the expected value |
| No assertion, or one that can't fail | Assert the behaviour the test is named after |
| A snapshot accepted without reading it | Read it once, or assert the few fields that matter |
| The expected value computed the way the code computes it | A known literal or a worked example ([tests.md](tests.md)) |

## Timely

One test at a time, each just before the code that makes it pass. Tests written after the code, or in bulk, check what was built instead of what was asked (horizontal slicing, in [SKILL.md](SKILL.md)).

## Sizes

| Size | Uses | Runs |
|---|---|---|
| Unit | One process, memory only | Every red → green cycle |
| Integration | This machine: a real database in a container, the file system, a local server | When a slice that touches that edge is done, and in the full suite |
| E2E | Real services, a browser, the deployed app | Once, before the merge request into the default branch is ready |
