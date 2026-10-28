---
name: principle-keep-it-simple
description: "Apply when writing, refactoring, sizing a diff, or tempted to add an abstraction, layer, option, guard, or piece of state. Simple means untangled, not short or familiar: subtract first, build only what's needed now, and judge the whole system, not the diff."
user-invocable: false
---

**Simple** means each piece does one thing and isn't tangled with another, so it can be understood and changed alone. It is not "short" and not "familiar". Only accidental complexity can be removed; essential complexity gets hidden behind a deep module (**principle-deep-modules**), never pushed onto callers.

- **Subtract before you add.** Delete dead code, one-caller wrappers, redundant guards, and stub references first, then build on the smaller base.
- **Build only what's needed now.** No options, validators, parsers, or extension points for needs that haven't shown up. This doesn't forbid making code easy to change.
- **Smallest change for the whole system.** Fewer lines beat elegant boilerplate, but a small diff that adds work to every caller is not simpler.
- **Collapse layers that don't pay.** Wrappers with one caller, adapters with one implementation, layers that repeat the same methods: inline them. Question any task that threads a new signal through many layers.
- **One decision, one place.** Don't repeat a choice across files; put it behind one source of truth.
- **Smallest state scope.** Pure functions over mutation, locals over fields, fields over module state. Derive instead of syncing.
- **Explicit over clever.** Three similar statements beat a premature abstraction.
- **Grow from something simple that works** (**principle-sequence-verifiable-units**).

**The test:** can a new reader answer "where does X come from?" and "what can change X?" in under 30 seconds, and change one piece without touching another? If not, cut layers, state, or tangles.
