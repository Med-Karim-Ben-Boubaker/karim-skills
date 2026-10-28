# Lane: style

Read every standards source in your brief before the diff. Skip what linters already enforce.

1. **Documented standards.** Every place the diff breaks a written rule. Cite the file and rule. These are `hard`.
2. **Smells** (Fowler, *Refactoring* ch. 3). Each is a `judgement`, and a documented repo rule overrides it: mysterious name (also: a name that differs from `GLOSSARY.md`), duplicated code, feature envy, data clumps, primitive obsession, repeated switches, shotgun surgery, divergent change, speculative generality, message chains, middle man, refused bequest.
3. **Comments.** Delete in your worktree every comment that narrates what the code does, banners, and commented-out code. Keep only: license headers, public API doc comments, `prettier-ignore`, issue links for constraints code can't express, and gotchas forced by something we can't change (a vendor, a protocol). A surprise in our own code is not a keep: delete the comment and flag the symbol `MUST KILL` for a rename or reshape that makes it obvious. A lint or type suppression (`@ts-ignore`, `eslint-disable`) whose rule protects correctness is also `MUST KILL`.
4. **Blueprints.** A diff that changes a folder's modules, interface, or data flow without updating its README.

```
- <file:line> hard | judgement: <rule or smell>: <one line>
MUST KILL: <symbol>: <why>
Comment patch: <worktree path or diff>
```
