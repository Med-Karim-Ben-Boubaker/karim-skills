---
name: principle-keep-it-simple
description: "KISS and YAGNI: decides whether a feature, command, flag, option, config key, dependency, abstraction, layer or design pattern should exist at all, using a need test, and presents the minimal version first with a list of what was cut. Use whenever proposing, designing, scoping, implementing or reviewing anything new, especially when a request asks for something flexible, complete, future-proof or 'best practice'. For how to write the code that stays, use principle-write-obvious-code."
---

# Keep It Simple

Every feature, command, flag, dependency, layer and pattern is a **liability**: someone must read, test, document and maintain it for as long as it exists. Build only what a named user needs now. The cheapest code is the code never written.

## The need test

Run it on every item before you propose or build it:

1. **Who needs it, for which task, now?** Name the person and the task. "Might be useful", "for flexibility" and "best practice" name no one.
2. **Is there a cheaper path?** Something that already exists covers it; it is rare enough for one README line; it composes from existing pieces; it is a field or a row of data instead of a new command or code path.
3. **Otherwise, cut it.**

For what survives, build **the simplest thing that could possibly work**: the simplest option that still meets the real constraints (security, reliability, what the team knows).

## Present less

- **Lead with the minimal version** that solves the stated problem. Follow it with a **Cut** list, one reason per item, so the user adds back only what they need.
- **Subtract before you add.** Delete dead code, unused options, one-caller wrappers and redundant guards first, then build on the smaller base. A diff that removes lines is a good diff.
- **Rule of Three.** Abstract on the third repetition, not the first. A design pattern (Strategy, Factory, Observer, Visitor…) earns its place only by solving a problem the code has today; otherwise it is **Speculative Generality**.
- **Pareto (80/20).** Find the few features that carry most of the value and make those excellent: an **MVP**, polished, beats a broad, rough tool. The user is whoever consumes the work: an end user, an API caller, the next maintainer.
- **Dependencies are features too.** Each library or framework brings its own weight, upgrades and failure modes. Prefer the standard library and a few lines of code over a package for a small job.

## Stay inside the task

- **Every changed line traces to the request.** A reasonable next step, a nearby refactor or an extra test is still unrequested: name it under **Noticed, not done** in the reply and keep it out of the diff.
- **Fix the shape first.** Before writing, name the files, functions and dependencies the change needs. A new file, layer or dependency needs its own reason.
- **Reuse before you write:** existing code, then the standard library, then an installed dependency, then new code.
- **Guard only states that can happen.** Unexpected failures surface loudly (**principle-design-for-crashes**) instead of being caught or silently replaced by a fallback.
- **Delete pass before handing back.** Reread the diff, remove every line the task does not need, and report the line count before and after.

## Why

The **Equation of Software Design**: a change is worth making in proportion to (value now + future value) ÷ (effort to build + effort to maintain). Maintenance never stops, so over a system's life it dominates the cost. Keep the system small. For an agent the bill comes sooner: every command, flag and option is more context the next agent and the user must read before they can act.

Writing code used to be expensive, and that cost kept human diffs small. For an agent writing is nearly free, so the cost moves to the reviewer: every line beyond the task is new logic a human must read and trust. The **Law of Defect Probability** says defects grow with the size of the change. A small diff that matches the request is a predictable diff; an agent's extras are the reviewer's **unknown unknowns**.

## What stays

Simplicity cuts scope, not quality. Whatever survives the need test gets finished: tests, error handling at the edges, security, data integrity and accessibility are part of the feature. **Essential complexity**, the part the problem itself demands, stays; only **accidental complexity** goes.

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

**Terms:** essential vs accidental complexity, KISS, YAGNI, simplest thing that could possibly work, Rule of Three, Speculative Generality, gold plating, feature creep, scope creep, additive bias, Law of Defect Probability, unknown unknowns, minimum viable product (MVP), Pareto principle (80/20), Equation of Software Design, dependency bloat, worse is better.
