---
name: principle-point-dependencies-inward
description: "Decides where code lives and which way dependencies point: business rules in a pure core; databases, HTTP, CLIs, queues, LLM clients and frameworks in thin adapters at the edge; external input parsed once where it enters; interfaces only where something real varies. Use when placing new logic, wiring an external system or framework, adding validation or error handling, or adding a port, interface or wrapper. For the shape of domain types, use principle-make-illegal-states-unrepresentable."
---

# Dependency Rule

Source-code dependencies point inward, toward the business rules (**policy**). The database, web framework, CLI, queues, LLM clients and third-party APIs are **details** at the edge: they depend on the core, never the reverse. Same idea under three names: **Clean Architecture**, **Hexagonal / Ports and Adapters**, **Functional Core, Imperative Shell**.

- **Pure core.** Business logic is pure functions over domain types: data in, decision out. The clock, randomness, I/O and config arrive as arguments. The core tests without mocks.
- **Thin edges.** Adapters translate between the outside world and core types, and stay too simple to need much testing (**Humble Object**). A **service layer** orchestrates a use case: load, call the core, save.
- **Validate once, at the edge.** Parse every external input (HTTP body, CLI args, env, config, files, DB rows, model output) into domain types where it enters, then trust it inside. Handle and translate errors at the edge; the core reports them as values or typed errors.
- **Domain types cross the surface.** ORM rows, HTTP payloads and SDK types stay inside their adapter. Wrap a third-party API when its types would otherwise spread through the code.
- **A boundary must pay rent.** Add a port (an interface) when something real varies across it: production vs test, or two real implementations. One adapter is a hypothetical seam; start with a **partial boundary** or none. **Dependency injection** is passing arguments; a container is optional.

## Why

Business rules change for business reasons; databases, frameworks and APIs change for technical ones. Keeping them apart lets each change alone, and keeps the rules testable in milliseconds with plain values instead of a database, a network or mocks.

## Example

```python
# Core: pure, tested with plain values
def price(order: Order, rates: TaxRates, today: date) -> Invoice: ...

# Edge: thin, does the I/O
def checkout(request, db, clock):
    order = Order.parse(request.json)   # validate once, here
    invoice = price(order, db.tax_rates(), clock.today())
    db.save(invoice)
    return invoice.to_json()
```

## When it bends

A short script or a plain CRUD endpoint with no business rules needs no core/edge split: keep it in one file until real rules appear.

**Terms:** Dependency Rule, Dependency Inversion Principle (DIP), Stable Dependencies Principle (SDP), hexagonal architecture, ports and adapters, functional core / imperative shell, Humble Object, service layer, Repository pattern, partial boundary, dependency injection, composition root, anti-corruption layer, Adapter pattern, Facade pattern.
