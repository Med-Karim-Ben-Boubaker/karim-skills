---
name: principle-first-tests
description: "Apply when writing or changing unit tests, or investigating slow or flaky tests. Use FIRST to keep test feedback fast, independent, repeatable, self-validating, and timely."
user-invocable: false
---

# FIRST Tests

Apply FIRST to each unit test:

- **Fast:** Keep tests quick enough to run during development. Keep network calls outside the unit suite.
- **Independent:** Each test owns its setup and cleanup. Tests pass alone and in any order.
- **Repeatable:** Control time, randomness, environment, and external dependencies. Identical inputs give identical results locally and in CI.
- **Self-validating:** Assertions decide pass or fail automatically. Logs explain failures; reading logs never decides the result.
- **Timely:** In TDD, write the failing test immediately before its implementation. Follow the `tdd` skill's sequencing rules.

Keep slower integration and end-to-end checks in their appropriate suites. Preserve isolation, repeatability, and automatic results there.
FIRST does not require every task to use TDD.

When choosing assertions, apply [principle-test-behavior-not-implementation](../principle-test-behavior-not-implementation/SKILL.md).

For slow or flaky tests, reproduce the issue with a focused run. Fix its cause, then rerun the affected checks.

Sources: Tim Ottinger and Brett Schuchert created FIRST; see [Ottinger's account](https://agileinaflash.blogspot.com/2009/02/first.html).
Robert C. Martin presents it in *Clean Code* (2008), Chapter 9, page 132.
