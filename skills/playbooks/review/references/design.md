# Lane: design

Find real problems: bugs, design flaws, security holes. Don't question the intent; challenge the execution. Read the surrounding code (callers, callees, types), not just the hunks. Call the Skill tool with "how" for an unfamiliar subsystem, and "why" before calling odd existing code a mistake.

Apply the lenses that fit. Call the Skill tool with a principle before citing it.

- **Correctness.** Edge cases, swallowed errors, races, stale state. Trace the caller that triggers a suspected bug; "could be null" with no caller passing null is not a finding.
- **Root cause.** Guards hiding a broken invariant, casts hiding a modelling error (**principle-fix-root-causes**).
- **Structure.** Would it look like this if the requirement had always existed (**principle-redesign-from-first-principles**)? Shallow modules and pass-through layers (**principle-deep-modules**, **principle-minimize-reader-load**). Validation away from the edge (**principle-boundary-discipline**). Illegal states the types allow (**principle-type-system-discipline**). Old API kept beside the new (**principle-migrate-callers-then-delete-legacy-apis**). Breaks on rerun (**principle-make-operations-idempotent**). Two writers on one state (**principle-separate-before-serializing-shared-state**).
- **Complexity.** One-caller abstractions, unused parameters, dead code (**principle-laziness-protocol**, **principle-subtract-before-you-add**). Look for the restructuring that makes whole branches disappear.
- **Security.** Untrusted input reaching SQL, shell, eval, or HTML; missing auth; secrets in code or logs.

"I'd have done it differently" is not a finding without a concrete problem.

```
### [critical | warning | nit] <title>
Location: file:line
Principle: <name or none>
Finding / Evidence / Suggestion
```
