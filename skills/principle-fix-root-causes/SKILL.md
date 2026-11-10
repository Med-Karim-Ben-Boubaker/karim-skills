---
name: principle-fix-root-causes
description: "Fixes wrong behaviour where it first went wrong (data model, schema, algorithm, prompt) instead of patching the symptom, lets failures surface as errors, and fixes the whole class, never one instance. Use when fixing a bug, failing test, error or wrong model answer, before adding a guard, fallback, default, retry or special case."
---

# Fix Root Causes

**Duct tape** (**symptom-fixing**, **special-case coding**) patches the place a failure showed up: an `if` for the input that broke, a null check, a fallback value, a magic number that makes one test pass, a `try/except` that swallows the error, a retry, a sleep, a prompt rule for one document. The fault stays in place, the code gains a path nobody can explain, and the next patch nests inside this one until the code becomes an **arrow anti-pattern** with a **combinatorial explosion** of paths. Fix the **root cause** instead: the first place the system went wrong, usually the data model, the schema, the algorithm or the prompt.

For the reproduce, hypothesise and instrument loop that finds a hard cause, use `diagnose-bug`.

## Find the cause

- **Name the fault before you write the fix.** Ask why until the answer is a wrong decision (**Five Whys**): a broken relation, a type that allows the bad value, an algorithm that only handles the cases its author pictured. A consequence of an earlier fault is not the answer yet.
- **Attack the premise.** When two fixes that share one assumption fail the same check, stop fixing. Write the assumption as one sentence and test it directly, with an observation that would come out differently if it were false (**falsifiability**; watch for **confirmation bias**, **sunk cost** and **shotgun debugging**).
- **Persisted state first** when something fails only after a restart: caches, config, lock files, serialised state, migrations.

## Fix the foundation

- **Correct the model, schema, algorithm or prompt** so the failing case follows the same rule as every other case. When the case is a real variant, model it: a sum type, a table (`principle-design-the-core`).
- **The class, not the instance.** A town, a layout, a fixture or one failing document is evidence, never a rule. Write the fix for the class it belongs to, with no names, words or structures from the one case in code, prompts or tickets, and prove it on cases beyond the one that failed. Search for every place with the same fault and fix them together.
- **A guard is a fix only for a legitimate state.** If the system may truly be in that state (an empty cart, a network timeout), handling it is the fix. If the state should never exist, the guard hides the bug; find what produced it.

## Fail loud

A failure surfaces as an error, with its context, and reaches the caller. Every step returns its real result or raises: never a default, placeholder or made-up value, a simpler stand-in algorithm, or a success status. Catch only a specific error you can truly recover from, and recover by doing the real work. A degraded result exists only when the user chose it: it comes from a real source (a cached copy with its age) and every caller can see it is degraded.

## Close the gap

- **Read your diff for tape.** A new branch that names the failing input, a fallback, a magic number, a swallowed error or a retry, with no legitimate state behind it, is duct tape. Replace it with the real fix.
- **Add the cheapest check against the whole class**: a test, a type, a lint rule, an assertion (**mistake-proofing**). Ask why the defect was written and why nothing caught it.
- **When the cause is out of reach** (a third-party bug, a production fire), make the workaround explicit: isolate it at the edge, link the real cause's issue, and tell the user it is a workaround.

## Example

```python
# Duct tape: the monthly report crashed on orders with no customer
name = order.customer.name if order.customer else "Unknown"
```

The root cause: the import job writes orders before their customers, and the schema lets `customer_id` be null. The fix: import customers first in the same transaction, and make `customer_id` NOT NULL with a foreign key, so the state cannot exist. The report needs no special case.

## Reporting a fix

```
Symptom: the monthly report crashes on orders with no customer.
Root cause: the import writes orders before customers; customer_id allows null.
Fix: import customers first, in one transaction; customer_id NOT NULL with a foreign key.
Why it slipped through: test fixtures always create customers first.
Check added: the constraint, and a test that imports orders listed before their customers.
```

**Terms:** root cause analysis, symptom-fixing, special-case coding, duct-tape fix, arrow anti-pattern, combinatorial explosion, magic numbers, Replace Conditional with Polymorphism, Five Whys, scientific debugging, falsifiability, confirmation bias, sunk cost fallacy, shotgun debugging, overfitting, error masking, fail fast, defect prevention, mistake-proofing (poka-yoke), regression test.
