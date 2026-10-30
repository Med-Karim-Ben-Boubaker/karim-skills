---
name: principle-fix-root-causes
description: "Fixes wrong behaviour at its cause instead of duct-taping the symptom (symptom-fixing, special-case coding): corrects the data model, schema or algorithm where the system first went wrong, rather than adding an if for the failing input, a null check, a fallback value, a hardcoded number, a swallowed exception or a retry where the failure showed. Use when fixing a bug, failing test, error, regression or an edge case the code gets wrong, before adding any guard, special case or fallback, and after two fixes in a row fail the same check. For the reproduce-hypothesise-instrument loop, use diagnose-bug."
---

# Fix Root Causes

**Duct tape** (**symptom-fixing**, **special-case coding**) patches the place a failure showed up: an `if` for the input that broke, a null check, a fallback value, a magic number that makes one test pass, a `try/except` that swallows the error, a retry, a sleep. The fault stays in place, the code gains a path nobody can explain, and the next patch nests inside this one until the code becomes an **arrow anti-pattern** with a **combinatorial explosion** of paths. Fix the **root cause** instead: the first place the system went wrong, usually the data model, the schema or the algorithm.

- **Name the fault before you write the fix.** Ask why until the answer is a wrong decision in code (**Five Whys**): a broken relation, a type that allows the bad value, an algorithm that only handles the cases its author pictured. A consequence of an earlier fault is not the answer yet.
- **Fix the foundation.** Correct the model, schema or algorithm so the failing case follows the same rule as every other case. When the case is a real variant, model it: a sum type, a table, **Replace Conditional with Polymorphism**, **Strategy** (**principle-make-illegal-states-unrepresentable**).
- **A guard is a fix only for a legitimate state.** If the system may truly be in that state (an empty cart, a network timeout), handling it is the fix. If the state should never exist, the guard hides the bug; find what produced it.
- **Read your diff for tape.** A new branch that names the failing input, a fallback, a magic number, a swallowed error or a retry, with no legitimate state behind it, is duct tape. Replace it with the real fix.
- **Fix the pattern, not the instance.** Search for every place with the same fault and fix them together.
- **Attack the premise.** When two fixes that share one assumption fail the same check, stop fixing. Write the assumption as one sentence and test it directly, with an observation that would come out differently if it were false (**falsifiability**; watch for **confirmation bias**, **sunk cost** and **shotgun debugging**).
- **Persisted state first** when something fails only after a restart: caches, config, lock files, serialised state, migrations.
- **Close the gap.** Ask why the defect was written and why nothing caught it, then add the cheapest check against the whole class: a test, a type, a lint rule, an assertion (**mistake-proofing**).
- **When the cause is out of reach** (a third-party bug, a production fire), make the workaround explicit: isolate it at the edge, comment the real cause with a link to the issue, and tell the user it is a workaround.

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

**Terms:** root cause analysis, symptom-fixing, special-case coding, duct-tape fix, arrow anti-pattern (pyramid of doom), combinatorial explosion, magic numbers, Replace Conditional with Polymorphism, Strategy pattern, Five Whys, scientific debugging, falsifiability, confirmation bias, sunk cost fallacy, shotgun debugging, error masking, fail fast, defect prevention, mistake-proofing (poka-yoke), regression test.
