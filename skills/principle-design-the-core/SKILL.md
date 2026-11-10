---
name: principle-design-the-core
description: "Encodes rules in the shape of the data and keeps them in a pure core: sum types, state machines, tables, value objects, parsing at the edge, I/O in thin adapters, ports only where something really varies. Use when choosing types, schemas or data structures, placing new logic, or wiring a database, API, CLI, queue or LLM client."
---

# Design the Core

Get the data right and the code follows (**data dominates**), and keep the rules away from I/O. Three known ideas make one design: **make illegal states unrepresentable**, **parse, don't validate**, and **functional core, imperative shell** (also called Clean Architecture, Hexagonal, Ports and Adapters).

For module depth and seam vocabulary, see `codebase-design`; for the pattern a shape has earned, see `design-patterns`.

## Rules live in the shape of the data

Encode each rule once, in the data, so the compiler or the structure enforces it instead of `if`s scattered across files.

- **Sum types over flag bags.** Model variants as discriminated unions or enums with payloads, not optional fields whose valid combinations live in a comment. `{ done: boolean; doneAt?: Date }` becomes `{ kind: "open" } | { kind: "done"; at: Date }`. Match **exhaustively**, so a new variant breaks the build everywhere it must be handled.
- **State machines over scattered booleans** for anything with a lifecycle: states, events and a transition table.
- **Tables over branches.** When logic is a mapping, write it as data: a lookup table, a registry, a config row. Tests become tables too.
- **Value objects for meaningful primitives.** `UserId`, `Money`, `Email` get their own type, validated once at creation (**Primitive Obsession** cured).
- **Aggregates own their invariants.** One module guards each consistency rule, and every change goes through it.
- **Define errors out of existence.** Shape the API so the error cannot arise or is handled in one place: total functions, sensible no-ops, low-level exceptions masked inside the module.
- **Derive from the source of truth.** Generate types from the schema (OpenAPI, protobuf, migrations) instead of copying them by hand.
- **Strengthen only where partiality appears.** A runtime assertion or "can't happen" throw marks a type that is too weak. Tighten that one; leave the rest plain.

## Rules live in a pure core

- **Pure core.** Business logic is pure functions over domain types: data in, decision out. The clock, randomness, I/O and config arrive as arguments, so the core tests without mocks.
- **Thin edges.** Adapters translate between the outside world and core types, and stay too simple to need much testing (**Humble Object**). A **service layer** orchestrates a use case: load, call the core, save.
- **Parse once, where input enters.** Turn every external input (HTTP body, CLI arguments, environment, files, database rows, model output) into a domain type that proves the check happened, then trust it inside. Handle and translate errors at the edge.
- **Domain types cross the surface.** ORM rows, HTTP payloads and SDK types stay inside their adapter.
- **A boundary pays rent.** Add a port (an interface) only where something really varies: production and a test fake, or two real implementations. **Dependency injection** is passing arguments; a container is optional.

## Example

```python
# Core: pure, rules held in data, tested with plain values
LIMITS = {"free": 10, "pro": 100, "team": 1000}   # a new plan is a new row

def quota(plan: Plan, used: int) -> Quota:
    return Quota(left=LIMITS[plan] - used)

# Edge: thin, does the I/O
def handle(request, db):
    account = Account.parse(request.json)          # parse once, here
    return quota(account.plan, db.usage(account.id)).to_json()
```

## When it bends

A short script or a plain CRUD endpoint with no business rules needs no core/edge split: keep it in one file until real rules appear.

**Terms:** algebraic data types, sum types, discriminated unions, exhaustive pattern matching, finite state machine, table-driven design, value object, newtype, Primitive Obsession, parse don't validate, aggregate, invariant, total function, define errors out of existence, Dependency Rule, Dependency Inversion Principle, hexagonal architecture, ports and adapters, functional core / imperative shell, Humble Object, service layer, anti-corruption layer.
