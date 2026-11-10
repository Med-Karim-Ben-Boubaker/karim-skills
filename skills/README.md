# Skills

Every skill sits directly under `skills/<name>/`, so Claude Code and Codex both find it. The groups below are for reading only.

## Engineering

Skills I use daily for code work.

### User-invoked

Reachable only when you type them (Claude Code: `disable-model-invocation: true`; Codex: `policy.allow_implicit_invocation: false` in `agents/openai.yaml`).

- **[pick-skill](./pick-skill/SKILL.md)**: Ask which skill or flow fits your situation. A router over the user-invoked skills in this repo.
- **[set-up-repo](./set-up-repo/SKILL.md)**: Configure this repo for the engineering skills (issue tracker, issue labels, checks and test policy, domain doc layout, run recipe and sandbox). Run once per repo.
- **[write-spec](./write-spec/SKILL.md)**: Turn the current conversation into a spec and publish it to the issue tracker.
- **[implement](./implement/SKILL.md)**: Build the work described by a spec or set of tickets, driving `/tdd` at the agreed seams and closing out with `/review-code` before committing.
- **[implement-spec](./implement-spec/SKILL.md)**: Implement a whole spec on one integration branch. Works the child tickets as a task graph, running implementer subagents across the ready frontier, then closes out with `/review-code`.
- **[write-walkthrough](./write-walkthrough/SKILL.md)**: Write the steps for you to check finished work yourself: setup from a fresh terminal with sample data agreed with you, copyable commands and UI clicks with what each should show, edge cases and cleanup, every step run by the agent first.
- **[plan-large-work](./plan-large-work/SKILL.md)**: Plan a huge chunk of work (more than one agent session can hold) as a shared map of decision tickets on the issue tracker, resolved one at a time until the way to the destination is clear.
- **[diagram-code](./diagram-code/SKILL.md)**: Turn code into technical diagrams (architecture, data flow, sequence, state, ER, and more) as a self-contained HTML page in Eraser's style, every box linked back to its source line.
- **[run-retro](./run-retro/SKILL.md)**: Suggest improvements to the coding agent's environment (navigation, automated checks, coding standards, steering files, tooling) after a session, most severe first.
- **[write-wizard](./write-wizard/SKILL.md)**: Generate an interactive bash wizard for steps only a human can perform: provisioning infrastructure, credentials or CI secrets, an unfamiliar dashboard, a one-off cutover.

### Model-invoked

Model- or user-reachable (rich trigger phrasing so the model can reach for them).

- **[prototype](./prototype/SKILL.md)**: Build a throwaway prototype to answer a design question: a single shareable HTML file for state/logic, or several toggleable UI variations.
- **[diagnose-bug](./diagnose-bug/SKILL.md)**: Disciplined diagnosis loop for hard bugs and performance regressions: build a feedback loop that goes red on this bug → minimise → hypothesise → instrument → fix → regression-test.
- **[research](./research/SKILL.md)**: Investigate a question against high-trust primary sources and capture the findings as a cited Markdown file in the repo, run as a background agent.
- **[tdd](./tdd/SKILL.md)**: Test-driven development with a red-green-refactor loop. Builds features or fixes bugs one vertical slice at a time, running the narrowest test each cycle, with FIRST tests (fast, isolated, repeatable, self-validating, timely).
- **[model-domain](./model-domain/SKILL.md)**: Actively build and sharpen a project's domain model by challenging terms, stress-testing with scenarios, and updating `GLOSSARY.md` and ADRs inline.
- **[review-code](./review-code/SKILL.md)**: Three-axis review of the change since a fixed point: **Standards** (the repo's coding standards, plus a baseline of checks drawn from the principles), **Spec** (does it faithfully implement the originating issue/spec?) and **Demo** (a fresh agent runs the app in a sandbox against the acceptance criteria and captures before-and-after evidence), run as parallel sub-agents.
- **[remove-comments](./remove-comments/SKILL.md)**: Delete the comments in a diff, keeping only license headers, public API docstrings, outside constraints and tool directives, and fix the code each comment was covering for. Runs before review.
- **[write-pr](./write-pr/SKILL.md)**: The shape a pull request body should take: a summary as the smallest visual that makes the change clear, before/after evidence that it works, and a merge-danger call (one-way or two-way door, plus blast radius).
- **[write-issue](./write-issue/SKILL.md)**: File and move issues on GitLab, GitHub or local files: one kind (bug, feature, chore) and one stage each, a title that names the problem, a description that grows a section per stage, and big work split into child tickets.

## Productivity

General workflow tools, not code-specific.

### User-invoked

Reachable only when you type them (Claude Code: `disable-model-invocation: true`; Codex: `policy.allow_implicit_invocation: false` in `agents/openai.yaml`).

- **[hand-off](./hand-off/SKILL.md)**: Compact the current conversation into a handoff document so another agent can continue the work.
- **[write-questionnaire](./write-questionnaire/SKILL.md)**: Turn a decision you can't answer alone into a Markdown questionnaire for the one person who can (filled in async, or together over a meeting).
- **[wait-what](./wait-what/SKILL.md)**: Fire this the moment a message doesn't land. The agent re-pitches it with the context you're missing, in plain English, using your `GLOSSARY.md` vocabulary.

### Model-invoked

Model- or user-reachable (rich trigger phrasing so the model can reach for them).

- **[grill](./grill/SKILL.md)**: Interview the user in short rounds about a plan, decision or idea until every branch of the design tree is settled; reads the glossary and ADRs first and records what settles.
- **[write-for-agents](./write-for-agents/SKILL.md)**: Writing documents for agents: skills, AGENTS.md/CLAUDE.md, and any doc an agent reaches by a pointer.
- **[design-patterns](./design-patterns/SKILL.md)**: The 22 classic design patterns as a lookup from a signal in the code to the pattern it earns, simplest form first (a function, dict, generator or module before a class hierarchy).
- **[codebase-design](./codebase-design/SKILL.md)**: Shared discipline and vocabulary for designing deep modules: small interfaces, clean seams, testable through the interface.

## Principles

Rules of judgement the agent applies while it works, one question each. The core of all six is always loaded through [`rules/engineering-defaults.md`](../rules/engineering-defaults.md); `/implement` and `/implement-spec` load the full principles before building, and `/review-code` checks a diff against them. You can also run one by name (`/principle-keep-it-simple`).

| Principle | The question it answers |
|---|---|
| [`keep-it-simple`](principle-keep-it-simple/SKILL.md) | Is this the least code that does the job, obvious to read, and shaped as if designed for the requirement? |
| [`fix-root-causes`](principle-fix-root-causes/SKILL.md) | Where did it first go wrong, and does the fix cover the whole class? |
| [`take-small-verified-steps`](principle-take-small-verified-steps/SKILL.md) | What did I run, what did I see, and which checks does this change need? |
| [`design-the-core`](principle-design-the-core/SKILL.md) | Do the types forbid wrong states, and does I/O stay at a thin edge? |
| [`design-for-operations`](principle-design-for-operations/SKILL.md) | Will it run, crash, rerun, configure and deploy the same way everywhere? |
| [`let-models-judge`](principle-let-models-judge/SKILL.md) | Which part needs a model's judgement, which needs a code check, and when does an eval run? |

Covered by other skills, so no principle: deep modules and seams (`codebase-design`), design patterns (`design-patterns`), testing behaviour through interfaces (`tdd`), the project's vocabulary and ADRs (`model-domain`), the debugging loop (`diagnose-bug`), turning recurring corrections into checks (`run-retro`). Trade-offs are named where decisions are made: in `grill`'s recommendations and in ADRs.
