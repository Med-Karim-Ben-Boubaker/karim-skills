---
name: principle-deep-modules
description: "Apply when designing or reviewing a module's interface, deciding where a seam goes, or about to add a layer, wrapper, or port. Put a lot of behaviour behind a small interface; test through that interface."
user-invocable: false
---

# Deep Modules

Design **deep modules**: a lot of behaviour behind a small interface, placed at a clean seam, testable through that interface.

**Why:** Depth gives callers **leverage** (more capability per thing they must learn) and maintainers **locality** (change, bugs, and verification concentrate in one place). A shallow module makes callers learn both the surface and the implementation, and spreads every fix across its callers.

## Vocabulary

Use these terms exactly. Consistent language is the point.

- **Module**: anything with an interface and an implementation, at any scale: a function, class, package, or tier-spanning slice. _Avoid_: unit, component, service.
- **Interface**: everything a caller must know to use the module correctly: the type signature, plus invariants, ordering constraints, error modes, required configuration, and performance characteristics. _Avoid_: API, signature.
- **Depth**: leverage at the interface: how much behaviour a caller or test can exercise per unit of interface they learn. Not a ratio of implementation lines to interface lines, which rewards padding.
- **Seam**: the place where a module's interface lives, where behaviour can be altered without editing in that place. Where the seam goes is its own decision, distinct from what goes behind it. _Avoid_: boundary.
- **Adapter**: a concrete thing that satisfies an interface at a seam. It names a role, not a size.
- **Leverage**: what callers get from depth. **Locality**: what maintainers get from depth.

## The tests

- **The deletion test.** Imagine deleting the module. If complexity vanishes, it was a pass-through: inline it. If complexity reappears across N callers, it earns its keep.
- **The interface is the test surface.** Callers and tests cross the same seam. If you want to test past the interface, the module is the wrong shape.
- **One adapter means a hypothetical seam; two adapters means a real one.** Don't introduce a port unless something actually varies across it (typically production and test).
- **Internal seams stay internal.** A deep module can be built from small, swappable parts with seams its own tests use. Don't expose them through the interface because a test wants them.

How a deep module is tested across its seam depends on what it depends on: see [DEEPENING.md](DEEPENING.md).

## Designing for testability

- **Accept dependencies, don't create them.** `processOrder(order, paymentGateway)`, not a `new StripeGateway()` inside.
- **Return results, don't produce side effects.** `calculateDiscount(cart): Discount`, not `applyDiscount(cart): void` mutating the cart.
- **Small surface.** Fewer entry points and parameters mean fewer tests and simpler setup.

The reader-side view of the same rule is the **principle-keep-it-simple** principle skill: collapse shallow layers. Tests at the seam follow the **test-behavior-not-implementation** principle skill.
