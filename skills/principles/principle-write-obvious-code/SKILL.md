---
name: principle-write-obvious-code
description: "Keeps code readable and changeable in one place: names, function size, comments, consistency, locality, coupling and state scope, judged by change amplification, cognitive load and unknown unknowns. Use when writing or reviewing code, or when code is hard to follow, one change needs edits in many places, or special cases pile up. For whether code should exist, use principle-keep-it-simple; for module interfaces and seams, use codebase-design."
---

# Obvious Code

**Complexity** is anything that makes code hard to understand or change. It shows as **change amplification** (one change, many edits), **cognitive load** (what a reader must hold in mind) and **unknown unknowns** (what a reader cannot tell they need to know). It comes from two causes: **dependencies** and **obscurity**. Simple means untangled, not short and not familiar (**simple vs easy**).

- **Four Rules of Simple Design**, in priority order: fits the people who will maintain it, communicates every idea the code needs, holds no duplication, has the fewest elements. Cut elements only within the first three.
- **Names.** A name says what a thing is or holds, in the domain's words (**ubiquitous language**: the repo's `GLOSSARY.md` when it has one). When no precise name comes, the design is murky: fix the design. One concept, one name, everywhere.
- **Functions.** Each does one thing at one level of abstraction. Extract a piece only when it is simpler to use than what it hides; a chain of tiny pass-through functions raises cognitive load.
- **Comments.** Explain *why*, and what an interface promises: units, preconditions, invariants, side effects. The code already says *what*.
- **Locality.** Keep what changes together in one place (**cohesion**, the **Common Closure Principle**). Each piece of knowledge has one source of truth (**DRY** is about knowledge, not identical lines: two identical lines that encode different rules stay separate, because the rules change for different reasons). Keep a definition next to its use.
- **Consistency.** Do things the way the codebase already does them. A second way to do the same thing is complexity.
- **Smallest state scope.** Pure functions over mutation, locals over fields, fields over globals. Derive values instead of keeping two copies in sync.
- **Explicit over clever.** Straight-line code with plain control flow; the **principle of least astonishment** for every caller.

**The test:** a new reader can answer "where does X come from?" and "what can change X?" quickly, and can change one piece without touching another.

## Why

Code is read far more often than it is written, and every reader, human or agent, pays the cognitive load again. Obscure code makes an agent open more files, guess more, and copy the confusion into the next change.

## Example

```python
# Repeats what the code says:
# add one to retries
retries += 1

# Says why, which the code cannot:
# The provider limits calls per minute, so wait for the next window
# instead of retrying at once and burning the quota.
sleep(seconds_until_next_minute())
```

**Terms:** Four Rules of Simple Design, intention-revealing code, change amplification, cognitive load, unknown unknowns, coupling, cohesion, Single Responsibility Principle (SRP), Common Closure Principle (CCP), DRY, ubiquitous language, levels of abstraction, principle of least astonishment, simple vs easy, Unix philosophy.
