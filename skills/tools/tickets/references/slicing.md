# Slicing children

- **Vertical, not horizontal.** Each child cuts a narrow but complete path through every layer (schema, API, UI, tests) and is verifiable on its own (**principle-sequence-verifiable-units**).
- **Subtract and prefactor first.** Removal and prefactor tickets come first; the rest are blocked by them (**principle-keep-it-simple**).
- **Walking skeleton.** If the repo has no test runner or CI, child 01 is the thinnest end-to-end path through real infrastructure, and blocks everything else (**principle-foundational-thinking**).
- **Shared seams.** Reuse the parent's seams; the fewer, the better.
- **No shared writes.** Two children that would write the same module either get split so they don't, or get a blocking edge (**principle-separate-before-serializing-shared-state**).
- **Wide refactors use expand–contract.** Expand (add the new form beside the old), migrate callers in batches sized by blast radius (each blocked by expand), then contract (delete the old form, blocked by every batch, never optional: **principle-migrate-callers-then-delete-legacy-apis**). If batches can't stay green alone, they share an integration branch and a final integrate-and-verify ticket; say where breakage is allowed (**principle-outcome-oriented-execution**).
