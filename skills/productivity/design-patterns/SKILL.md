---
name: design-patterns
description: "The 22 classic design patterns (creational, structural, behavioral) as a lookup from a signal in the code to the pattern it earns, with the simplest form first: a function, a dict, a generator or a module before a class hierarchy. Use when a design or refactor keeps hitting the same shape (a growing conditional, a constructor with many options, a tree, a tangle of objects calling each other), when review-code flags a smell such as Repeated Switches, or when someone asks which pattern fits."
---

# Design Patterns

A pattern is a named solution to a problem that keeps coming back. Use one only when the code shows its signal, and only in the smallest form that removes the problem: `principle-keep-it-simple` holds (Rule of Three: abstract on the third repetition). Most patterns have a plain-language form, a function, a dict, a generator or a module, that does the job without the class hierarchy; reach for the classes only when that form stops being enough.

Find the signal below, then read that pattern's file for its roles, a sketch, its costs and the patterns it gets confused with.

## Signal → pattern

| The code shows | Pattern | Simplest form |
|---|---|---|
| The same `if kind == ...: X()` construction in several places | [Factory Method](creational/factory-method.md) | dict from key to class |
| Several objects that must always come from the same variant | [Abstract Factory](creational/abstract-factory.md) | a module or dict per variant |
| A constructor with many optional parameters | [Builder](creational/builder.md) | keyword arguments, `dataclass` |
| Costly setup, copied from a few presets | [Prototype](creational/prototype.md) | `copy`, `dataclasses.replace` |
| One process-wide resource | [Singleton](creational/singleton.md) | create it at startup and pass it in |
| A library or legacy class with the wrong interface | [Adapter](structural/adapter.md) | a conversion function |
| Subclasses multiplying across two dimensions | [Bridge](structural/bridge.md) | pass the second dimension in |
| A tree, and `isinstance` checks for leaf vs group | [Composite](structural/composite.md) | a recursive function |
| Optional behaviours (retry, cache, log) combined in many ways | [Decorator](structural/decorator.md) | `@decorator` for functions, a wrapper class for objects |
| Callers repeating the setup and call order of a subsystem | [Facade](structural/facade.md) | a module with a few functions |
| Memory exhausted by many near-identical objects (measured) | [Flyweight](structural/flyweight.md) | `lru_cache`, `__slots__` |
| Work needed around every call to a service: lazy load, access check, cache | [Proxy](structural/proxy.md) | a forwarding wrapper, `functools.cache` |
| Ordered checks or steps that get added and reordered | [Chain of Responsibility](behavioral/chain-of-responsibility.md) | a list of functions |
| Actions to queue, retry, log or undo | [Command](behavioral/command.md) | a callable, `functools.partial` |
| Callers looping over a collection's internals | [Iterator](behavioral/iterator.md) | a generator |
| Objects calling each other in a tangle | [Mediator](behavioral/mediator.md) | an event bus or dict of callbacks |
| Undo or rollback without exposing fields | [Memento](behavioral/memento.md) | a frozen snapshot the object makes |
| A change that must trigger reactions in unknown others | [Observer](behavioral/observer.md) | a list of callables |
| The same `if self.status == ...` cascade in several methods | [State](behavioral/state.md) | `Enum` plus a transition table |
| A conditional choosing between variants of one algorithm | [Strategy](behavioral/strategy.md) | pass a function |
| Near-identical algorithms that differ in a few steps | [Template Method](behavioral/template-method.md) | a function taking the steps as arguments |
| Many operations over a stable set of node types | [Visitor](behavioral/visitor.md) | `singledispatch`, `match` |

## From review-code smells

| Smell | Look at |
|---|---|
| Repeated Switches | Strategy, State, or polymorphism |
| Message Chains | Facade |
| Middle Man | none: remove the layer |
| Speculative Generality | none: a pattern with one variant is speculative; inline it |
| Data Clumps, Primitive Obsession | none: a small type, not a pattern |

## When not to

- **One variant.** A Strategy with one strategy, a Factory for one class, an interface with one implementation: delete it until a second appears.
- **Named for the pattern.** `OrderStrategyFactory` names the mechanism, not the domain; name it for what it does.
- **The language already has it.** Iterators, decorators, first-class functions, modules and `copy` cover several patterns without any classes.
