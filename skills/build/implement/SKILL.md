---
name: implement
description: "Implement one ticket or piece of work in code: a new behaviour, a refactor that keeps behaviour fixed, or an optimization that moves a metric. Use when the user wants a ticket, spec slice, or described change built, or when an orchestrating skill hands a subagent one ticket to build."
---

# Implement

Build the work described by the user, the ticket, or the spec slice.

If the user passes a ticket reference, fetch it from the issue tracker and state its title before starting. If the reference is ambiguous, ask. Read `GLOSSARY.md` so names match the domain language, and respect ADRs in the area you're touching.

## Pick a branch

The branch is decided by **what the change is allowed to change**. Read it from the ticket; a prefactor or wide-refactor ticket from `to-tickets` is a refactor, a vertical slice is a feature.

- **Behaviour changes** (a new capability, a changed rule, the walking skeleton) → [FEATURE.md](FEATURE.md).
- **Structure changes, behaviour must not** (prefactor, deepening a module, renaming, migrating callers, porting to a new component) → [REFACTOR.md](REFACTOR.md).
- **A number must move** (latency, memory, bundle size, an eval score) and the behaviour must not → [OPTIMIZE.md](OPTIMIZE.md).

Something broken, throwing, or newly slow is not build work: call the Skill tool with "diagnosing-bugs". If the work mixes branches, split it: land the refactor first against the current behaviour, then the feature on top.

## Rules that apply to every branch

1. **Decide reversible things yourself.** Call the Skill tool with "principle-never-block-on-the-human": a naming, layout, or internal-shape choice that a later commit can undo gets made and noted in the report, not asked. Ask only about product calls and one-way doors.
2. **Check often.** Run typechecking and single test files after each step, the full test suite once at the end.
3. **Keep the blueprint current.** If the change altered a folder's modules, public interface, or data flow, call the Skill tool with "blueprint" to update that folder's README, and its parent's when the parent's diagram changed.
4. **Hand off to review.** Once done, call the Skill tool with "code-review" to review the work.
5. **Commit** to the current branch, in the small ordered commits the branch file describes.

Report what you built, which branch you followed, the choices you made on your own, and what you verified on the real surface.
