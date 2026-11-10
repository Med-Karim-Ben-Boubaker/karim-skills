---
name: grill
description: "Interviews the user about a plan, decision or idea in short rounds over a design tree, with a recommended answer for every question, until every branch is settled; reads the glossary and ADRs first and records what settles. Use when the user wants to stress-test their thinking, settle a design before building, or uses any 'grill' phrasing."
---

Interview the user until you reach a shared understanding. Map it as a **design tree**: every decision branches into the decisions that hang off it.

## Before the first round

- If the repo has a `GLOSSARY.md` or `docs/adr/`, read them (and `docs/agents/domain.md` when it exists), and use the glossary's words.
- When the user doesn't know the domain yet, explore and explain first: read the code, the docs, the data or the law, or call the Skill tool with "research", then ask about what is left.

## Rounds

The **frontier** is every decision whose prerequisites are already settled: the questions you can ask _now_ without guessing at answers you haven't heard yet. Ask at most three frontier questions per round, the most decisive first, and wait for the answers before the next round.

Format a round like so:

```
❓ **Q1** - **<question title>**: <the question, in one or two lines>

➡️ <your recommended answer, in one line, with what it costs: what we give up, and whether it's easy to undo>

---

❓ **Q2** - …
```

Word each question so "yes" accepts your recommended answer. No tables, no background paragraphs: give detail when the user asks for it.

Ask only about taste, priorities and trade-offs. Implementation details you decide yourself: list them at the end of the round under **Decided without asking**, one line each, so the user can overrule any of them.

Each round the user answers reshapes the tree: settled decisions push the frontier outward and unblock questions that depended on them. Recompute the frontier and ask the next round. A question whose answer depends on another question still open in this round belongs to a later round.

## Facts are yours, decisions are theirs

Finding _facts_ is your job, never the user's. When a frontier question needs a fact from the environment (the codebase, data, docs, a CLI), dispatch a sub-agent with a fresh context window to find it; don't ask the user for anything you could look up yourself. Don't block on it: a running exploration is an unsettled prerequisite, so only the questions downstream of it wait; ask the rest of the frontier now. The _decisions_ are the user's: put each to them and wait.

## Record what settles

When a term settles, add it to `GLOSSARY.md`; when a decision settles that is hard to reverse, surprising without context and the result of a real trade-off, record it as an ADR. Call the Skill tool with "model-domain" for both.

## Done

The session is done when the frontier is empty: every branch of the design tree visited, nothing left silently assumed. Do not act on it until the user confirms you have reached a shared understanding.
