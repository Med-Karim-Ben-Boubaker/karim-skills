---
name: refactoring
description: "Playbook for a change to structure while behaviour stays fixed: rename, extract, inline, dedupe, move, deepen a module, migrate callers, port to a new component. Use when the code should look different but do the same thing."
---

# Refactoring

**You own the contract.** The structure changes; the behaviour does not. A bug or missing feature found on the way is split out to **bug-fix** or **feature**.

1. **Pin the behaviour.** Call the Skill tool with "how" over the area, then capture what the code does now at its public interface: a characterization test, a snapshot, or a harness that diffs old against new output (**principle-test-behavior-not-implementation**). Typecheck and lint are not a pin. *Done when:* the pin runs green and is the first commit if it's new.
2. **Name the target shape.** The layout, types, and call graph as if built today (**principle-redesign-from-first-principles**, **principle-deep-modules**). *Done when:* the target is written and it deletes branches, layers, or invalid states rather than adding indirection.
3. **Subtract first.** Delete dead code, one-caller wrappers, and redundant guards (**principle-keep-it-simple**). Before deleting something odd-looking, call the Skill tool with "why" on it. *Done when:* the subtraction commit is green against the pin.
4. **Move in small green steps** (**principle-sequence-verifiable-units**). Wide mechanical edits get a codemod or script (**principle-build-the-lever**). API reshapes migrate every caller and delete the old API in the same wave, no shims (**principle-migrate-callers-then-delete-legacy-apis**). *Done when:* the pin is green after every step, and renames are spot-checked in strings and docs.
5. **Prove equivalence** (**principle-prove-it-works**). *Done when:* the pin passes and, for larger reshapes, the old-vs-new comparison shows no difference.
6. **Keep it only if it's better** (**principle-keep-it-simple**). *Done when:* you can name where reader load dropped. If you can't, revert.
7. **Review.** Commits in order: pin, subtraction, reshape. Update blueprints with the "blueprint" skill if structure changed. Run the **review** playbook. *Done when:* review returned a verdict.

Never edit the pin to make it pass: that means it pinned the implementation.

**Reply:** the structure that changed, the pin, the equivalence proof, the reader-load gain, what was reverted.
