---
name: principle-keep-it-simple
description: "KISS, YAGNI and obvious code: decides whether a feature, option, flag, layer, dependency or abstraction should exist, presents the minimal version first, keeps what stays readable, and lands each change as if the design had planned for it. Use when proposing, designing, scoping, writing, changing or reviewing code, plans or specs."
---

# Keep It Simple

Every feature, command, flag, dependency, layer and pattern is a **liability**: someone must read, test and maintain it for as long as it exists. Build the least that solves the stated problem, write it so a new reader can change it alone, and land each change as if the design had planned for it.

## Should it exist? The need test

Run it on every item before you propose or build it:

1. **Who needs it, for which task, now?** Name the person and the task. "Might be useful", "for flexibility" and "best practice" name no one.
2. **Is there a cheaper path?** Something that already exists covers it; one README line covers it; it composes from existing pieces; it is a field or a row of data instead of a new command or code path.
3. **Otherwise, cut it.**

What survives gets **the simplest thing that could possibly work** that still meets the real constraints.

## Present less

- **Lead with the minimal version** that solves the stated problem, then a **Cut** list with one reason per item, so the user adds back only what they need.
- **Every changed line traces to the request.** A nearby refactor, an extra test or a "while I'm here" is still unrequested: name it under **Noticed, not done** and keep it out of the diff.
- **Reuse before you write:** existing code, then the standard library, then an installed dependency, then new code. Dependencies are features too.
- **Rule of Three.** Abstract on the third repetition, not the first. A design pattern earns its place by solving a problem the code has today; otherwise it is **Speculative Generality**.
- **Specialise only for a different mechanism.** A new branch, type or component per case needs a genuinely different way of parsing, modelling or processing, not just a different name.
- **Subtract before you add,** and finish with a **delete pass**: reread the diff and remove every line the task doesn't need.

## Keep what stays obvious

**Complexity** is anything that makes code hard to understand or change. It shows as **change amplification** (one change, many edits), **cognitive load** (what a reader must hold in mind) and **unknown unknowns** (what a reader can't tell they need to know).

- **Names** say what a thing is, in the domain's words (`GLOSSARY.md` when the repo has one). One concept, one name, everywhere. When no precise name comes, the design is murky: fix the design.
- **Functions** do one thing at one level of abstraction. Extract a piece only when it is simpler to use than what it hides; a chain of pass-through functions raises cognitive load.
- **No comments.** Say it in a name, a type or a test. The few comments that stay are listed in `remove-comments`.
- **Locality.** What changes together lives together. Each piece of knowledge has one source of truth (**DRY** is about knowledge, not identical lines).
- **Consistency.** Do things the way the codebase already does them. A second way to do the same thing is complexity.
- **Smallest state scope.** Pure functions over mutation, locals over fields, derived values over copies kept in sync.

## Land the change as if designed for it

- **Redesign, then deliver.** Ask: if this requirement had existed on day one, what would the code look like? Move there in small verified steps. Often the right shape is smaller than the current one.
- **One path.** When you replace an internal API, migrate every caller and delete the old one in the same change. Callers you control need no shims, aliases, flags or deprecation periods.
- **Expand, migrate, contract** across a deploy boundary (public APIs, stored data, wire formats): add the new form, move readers and writers, then remove the old form. The removal is part of the task.
- **Boy Scout Rule, scoped.** Tidy the lines the task already changes; anything further goes under **Noticed, not done**.

## What stays

Simplicity cuts scope, not quality. Whatever survives the need test gets finished: tests, error handling at the edges, security and data integrity are part of the feature. **Essential complexity**, the part the problem demands, stays; **accidental complexity** goes.

## Example

A request for a test-runner CLI "as flexible as possible" first produced eight commands (`list`, `run`, `show`, `add`, `gold`, `review`, `sign`, `check`), each with flags. After the need test:

```
Proposal
  e2e run [--set core|optional|all] [--case NAME]
  e2e check SHA [BASE]

Cut
  list, show   `ls` and the case files already answer them
  add          rare; one README line covers it
  gold, sign   a field in the case file, not a command
  review       `run` followed by `check` composes it
```

**Terms:** KISS, YAGNI, essential vs accidental complexity, simplest thing that could possibly work, Rule of Three, Speculative Generality, gold plating, scope creep, change amplification, cognitive load, unknown unknowns, Four Rules of Simple Design, ubiquitous language, DRY, Common Closure Principle, principle of least astonishment, strategic vs tactical programming, tactical tornado, parallel change, expand–migrate–contract, strangler fig, Boy Scout Rule, Shotgun Surgery, Divergent Change.
