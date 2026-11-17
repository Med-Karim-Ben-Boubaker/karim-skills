---
name: review-code
description: "Reviews the changes since a fixed point (commit, branch, tag, merge-base) in two parallel sub-agents: Standards (coding standards and principle checks) and Spec (what the issue asked for). Use when reviewing a branch, a PR or work in progress, or asked to 'review since X'."
---

Two-axis review of the change between `HEAD` and a fixed point the user supplies:

- **Standards**: does the code conform to this repo's documented coding standards?
- **Spec**: does the code faithfully implement the originating issue / spec?

Both run as **parallel sub-agents** so they don't pollute each other's context, then this skill aggregates their findings. Start every sub-agent with a fresh context window.

The issue tracker should have been provided to you (`### Issue tracker` in `AGENTS.md` or `CLAUDE.md`). If not, tell the user to run `/set-up-repo`.

## Process

### 1. Pin the fixed point

Whatever the user said is the fixed point (a commit SHA, branch name, tag, `main`, `HEAD~5`, etc.). If they didn't specify one, ask for it.

Capture the diff command once: `git diff <fixed-point>...HEAD` (three-dot, so the comparison is against the merge-base). Also note the list of commits via `git log <fixed-point>..HEAD --oneline`.

Before going further, confirm the fixed point resolves (`git rev-parse <fixed-point>`) and the diff is non-empty. A bad ref or empty diff should fail here, not inside two parallel sub-agents.

### 2. Identify the spec source

Look for the originating spec, in this order:

1. Issue references in the commit messages (`#123`, `Closes #45`, GitLab `!67`, etc.), fetched via the workflow in the tracker doc.
2. A path the user passed as an argument.
3. A spec file under `docs/`, `specs/`, or `.scratch/` matching the branch name or feature.
4. If nothing is found, ask the user where the spec is. If they say there isn't one, the **Spec** sub-agent skips and report "no spec available".

### 3. Identify the standards sources

Search the repo for every file that documents how code should be written. When `CODING_STANDARDS.md` or `CONTRIBUTING.md` exists, it must be on the list.

On top of whatever the repo documents, the Standards axis always carries the **baseline** below: the checks that follow from the principle skills and `tdd`'s FIRST tests, plus three Fowler smells (_Refactoring_, ch.3) no principle covers. It applies even when a repo documents nothing. Two rules bind it:

- **The repo overrides.** A documented repo standard always wins; where it endorses something the baseline would flag, suppress the check.
- **Always a judgement call.** Each check is a labelled heuristic ("possible duct tape"), never a hard violation. Like any standard here, skip anything tooling already enforces.

Each check reads *signal* → *fix*; match it against the diff. The skill named in each heading holds the reasoning; where a fix names a pattern, the `design-patterns` skill says which one the code has earned and its simplest form.

**Keep it simple** (`principle-keep-it-simple`)
- **Unrequested**: code, options, files or tests the request didn't ask for. → cut, or list under "Noticed, not done".
- **Speculative Generality**: an abstraction, parameter, hook or interface with one user. → inline it until a real need shows.
- **Shotgun Surgery / Divergent Change**: one change edits many files, or one module changes for unrelated reasons. → put what changes together in one place.
- **Second path**: a shim, alias, flag or old code path kept for callers we control. → migrate the callers, delete the old path.
- **Mysterious Name**: a name that doesn't say what the thing is, or two names for one concept. → rename to the glossary's term; if no honest name comes, the design is murky.
- **Duplicated knowledge**: the same rule encoded in two places. → one source of truth.
- **Middle Man**: a function or class that only delegates. → call the real target.
- **Comments**: any comment, docstring or commented-out code outside the keep-list of `remove-comments`. → run `remove-comments`; it deletes them and fixes what they covered for.

**Fix root causes** (`principle-fix-root-causes`)
- **Duct tape**: a new branch, fallback, default, retry, broad `except` or magic number with no state that can really happen behind it. → find and fix the cause.
- **Masked failure**: a caught error turned into a default, a placeholder or a success status. → let it raise.
- **One instance as a rule**: a town, file, layout or fixture named as a rule in code, prompts or tests. → write the general case.
- **No guard against recurrence**: a fix with no test, type or lint that goes red without it. → add one.

**Design the core** (`principle-design-the-core`)
- **Flag bag / Primitive Obsession / Data Clumps**: booleans or optionals whose valid combinations live in a comment, a string standing in for a concept, fields that always travel together. → a sum type, a value object, one type.
- **Repeated Switches**: the same `if`/`match` on a type in several places. → one table or one exhaustive match.
- **Re-validation**: input checked again inside the core. → parse once where it enters.
- **I/O in the core**: core code importing a database, HTTP, SDK or LLM client, or reading the environment or the clock. → pass it in.
- **Rent-free port**: an interface with one implementation and no test fake. → remove it.

**Design for operations** (`principle-design-for-operations`)
- **Non-idempotent rerun**: a rerun duplicates rows, files or messages. → upsert, key or completion marker.
- **Shared writer**: two writers on one file, key or partition. → one each.
- **Unbounded wait**: a remote call with no timeout, or a retry on a non-idempotent call. → bound it, or don't retry.
- **Config in code**: a deploy-specific value with a default in code, an `export` in a script, or config passed as a flag. → read it from the environment.
- **Exposed secret**: a secret printed, logged or committed. → remove it and tell the user to rotate it.

**Let models judge** (`principle-let-models-judge`)
- **Rule doing a model's job**: a regex, word list or layout check for fuzzy input. → put it in the prompt or the model's answer.
- **Patch prompt**: a prompt line naming one case, town, file or fixture. → state the concept.
- **Verbatim check**: code requiring quoted text to match exactly. → check pointers and structure.

**FIRST tests** (`tdd`)
- **Slow test**: a unit test that sleeps, waits on a real clock or timeout, calls the network, a model or a GPU, touches a database or a bucket, starts a server, browser or container, or loads a large fixture. → inject the clock, fake the I/O or replay a recorded response, and shrink the input; a test that needs the real thing is a marked integration test, and model behaviour belongs in evals.
- **Order-dependent or flaky test**: state shared between tests, or a reliance on run order, `now()`, randomness or timing. → each test arranges its own state; inject the clock and the seed.
- **Test that can't fail**: tautological, asserts nothing, or mocks the thing under test. → rewrite against the public interface.

**Small verified steps** (`principle-take-small-verified-steps`)
- **Unproven claim**: a number or a "works" with no command and output behind it. → measure or drop.
- **Mixed commit**: a refactor and a behaviour change in one commit. → split.

**Other smells**
- **Feature Envy**: a method that reaches into another object's data more than its own. → move it onto the data it envies.
- **Message Chains**: long `a.b().c().d()` navigation the caller shouldn't depend on. → hide the walk behind one method.
- **Refused Bequest**: a subclass that ignores or overrides most of what it inherits. → drop the inheritance, use composition.

### 4. Spawn the two sub-agents in parallel

Issue both sub-agent calls together, in the foreground, and aggregate the reports they return.

**Standards sub-agent prompt** should include:

- The full diff command and commit list.
- The list of standards-source files you found in step 3, **plus the baseline from step 3** pasted in full (the sub-agent has no other access to it).
- The brief: "Report, per file/hunk where relevant, (a) every place the diff violates a documented standard: cite the standard (file + the rule); and (b) any baseline check that fires: name it and quote the hunk. Distinguish hard violations from judgement calls: documented-standard breaches can be hard, but baseline checks are always judgement calls, and a documented repo standard overrides the baseline. Skip anything tooling enforces. Under 400 words."

**Spec sub-agent prompt** should include:

- The diff command and commit list.
- The path or fetched contents of the spec.
- The brief: "Report: (a) requirements the spec asked for that are missing or partial; (b) behaviour in the diff that wasn't asked for (scope creep); (c) requirements that look implemented but where the implementation looks wrong. Quote the spec line for each finding. Under 400 words."

If the spec is missing, skip the Spec sub-agent and note this in the final report.

### 5. Aggregate

Present the two reports under `## Standards` and `## Spec` headings, verbatim or lightly cleaned. Do **not** merge or rerank findings, because the axes are deliberately separate (see _Why two axes_).

End with a one-line summary: total findings per axis and the worst issue _within each axis_ (if any). Don't pick a single winner across axes: that's the reranking the separation exists to prevent.

## Why two axes

A change can pass one axis and fail another:

- Code that follows every standard but implements the wrong thing → **Standards pass, Spec fail.**
- Code that does exactly what the issue asked but breaks the project's conventions → **Spec pass, Standards fail.**
Reporting them separately stops one axis from masking another. Whether the software works when run is not a review axis: `prove-change` runs it.
