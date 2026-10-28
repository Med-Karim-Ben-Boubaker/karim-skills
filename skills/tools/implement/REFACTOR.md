# Refactor

The **structure** changes; the **behaviour** does not. You own the contract.

If the work reveals a missing feature or a real bug, split it out: land the structural change against the current behaviour first, then route the rest to [FEATURE.md](FEATURE.md) or diagnosing-bugs.

## Process

### 1. Pin the behaviour

Call the Skill tool with "how" over the affected subsystem to learn the contract you're about to pin.

Before any structure moves, capture what the code does now at its public interface: a characterization test, a snapshot, or an equivalence harness that diffs old against new output. Call the Skill tool with "principle-test-behavior-not-implementation": the pin must fail when behaviour breaks and survive the reshape. If the area has no coverage, the pin is the first commit. Typechecking and linting are not a pin.

When porting to a new component or implementation, the old output is the spec: freeze it as a baseline (golden files, screenshots compared by image diff) and never edit the baseline to make a diff pass.

### 2. Name the target shape

State the module layout, types, and call graph as if built today. Call the Skill tool with "principle-redesign-from-first-principles" for the target, and "principle-deep-modules" for where the seams go. The target must delete branches, layers, or invalid states, not add indirection.

### 3. Subtract first

Call the Skill tool with "principle-subtract-before-you-add": delete dead code, one-caller wrappers, redundant validators, and orphan references before introducing the new shape. Before deleting code that looks defensive or odd for no visible reason (a guard, a retry, a magic number), call the Skill tool with "why" on it: delete it once you know what it was for. Call the Skill tool with "principle-laziness-protocol": the smallest change that reaches the target ships.

### 4. Move in small green steps

Call the Skill tool with "principle-sequence-verifiable-units": one behaviour-preserving step at a time, the pin green after each.

- **Wide or mechanical changes** (renames, signature changes across many files): call the Skill tool with "principle-build-the-lever" and write the codemod or script, then spot-check what it touched, including strings and docs.
- **API reshapes**: call the Skill tool with "principle-migrate-callers-then-delete-legacy-apis": migrate every caller and delete the old API in the same wave, no shims.
- **Planned breakage** (a ticket that says green is promised only at integration): call the Skill tool with "principle-outcome-oriented-execution" and keep the breakage inside the declared scope.

### 5. Prove equivalence

Call the Skill tool with "principle-prove-it-works": the pin passes, and for larger reshapes the equivalence check (old vs new output, a replayed baseline, a smoke run on the real surface) shows no difference.

### 6. Keep it only if it's better

Call the Skill tool with "principle-minimize-reader-load": name where reader load dropped (fewer layers to trace, less state to hold). If you can't, revert.

Land as small ordered commits: the pin, then the subtraction, then the reshape.

## Anti-patterns

- **Moving before pinning.** Without a pin, "no behaviour changed" is a guess.
- **Editing the pin to pass.** A pin that changes with the refactor pinned the implementation, not the behaviour.
- **Compatibility shims "for now".** Old and new paths side by side become permanent.
