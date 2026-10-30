---
name: principle-make-illegal-states-unrepresentable
description: "Encodes domain rules in types and data structures so wrong states cannot be built: sum types instead of flag bags, state machines, lookup tables instead of branches, value objects, parse-don't-validate, aggregates guarding invariants, errors defined out of existence. Use when choosing core types, data structures or schemas, writing stateful or branch-heavy logic, adding a boolean or optional field, or handling errors and special cases. For names and readability, use principle-write-obvious-code; for project vocabulary, use model-domain."
---

# Make Illegal States Unrepresentable

Get the data structures right and the code follows (**data dominates**). Encode each rule once, in the shape of the data, so the compiler or the structure enforces it instead of `if`s scattered across files.

- **Sum types over flag bags.** Model variants as discriminated unions or enums with payloads, not optional fields whose valid combinations live in a comment. `{ done: boolean; doneAt?: Date }` becomes `{ kind: "open" } | { kind: "done"; at: Date }`. Match **exhaustively**, so a new variant breaks the build everywhere it must be handled.
- **State machines over scattered booleans** for anything with a lifecycle: states, events and a transition table. Reach for the GoF **State** or **Strategy** pattern only when each case carries real behaviour; a map of functions usually does.
- **Tables over branches.** When logic is a mapping, write it as data: a lookup table, a registry, a config row. Tests become tables too (**table-driven tests**).
- **Value objects for meaningful primitives.** `UserId`, `Money`, `Email` get their own type (newtype or branded type), validated once at creation. This cures **Primitive Obsession**.
- **Parse, don't validate.** Turn untyped input into a type that proves the check happened, so downstream code never re-checks. Where parsing happens is **principle-point-dependencies-inward**.
- **Aggregates own their invariants.** One entity or module guards each consistency rule, and every change goes through it.
- **Define errors out of existence.** Shape the API so the error cannot arise or is handled in one place: total functions, sensible defaults (removing a missing key is a no-op), low-level exceptions masked inside the module. Each special case removed is code that cannot run wrong.
- **Derive from the source of truth.** Generate types from the schema (OpenAPI, protobuf, DB migrations) instead of hand-copying them.
- **Strengthen only where partiality appears.** A runtime assertion, null check or "can't happen" throw marks a type that is too weak. Tighten that one; leave the rest plain.

## Why

A rule held in the shape of the data is enforced everywhere the data goes, by the compiler or the lookup. A rule held in scattered `if`s is enforced only where someone remembered it, and forgotten in the next file.

## Example: a table instead of branches

```python
# Grows a branch per plan, repeated wherever limits matter
if plan == "free":
    limit = 10
elif plan == "pro":
    limit = 100

# One row per plan: a new plan is a new row, and an unknown plan fails at the lookup
LIMITS = {"free": 10, "pro": 100, "team": 1000}
limit = LIMITS[plan]
```

**Terms:** algebraic data types, sum types, Replace Conditional with Polymorphism, discriminated unions, exhaustive pattern matching, finite state machine, table-driven design, value object, newtype, branded type, Primitive Obsession, parse don't validate, aggregate, invariant, total function, define errors out of existence, single source of truth, schema-first code generation, State pattern, Strategy pattern.
