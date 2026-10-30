# Skills

Every skill sits directly under `skills/<name>/`, so Claude Code and Codex both find it. The groups below are for reading only.

## Engineering

Skills I use daily for code work.

### User-invoked

Reachable only when you type them (Claude Code: `disable-model-invocation: true`; Codex: `policy.allow_implicit_invocation: false` in `agents/openai.yaml`).

- **[pick-skill](./pick-skill/SKILL.md)**: Ask which skill or flow fits your situation. A router over the user-invoked skills in this repo.
- **[grill-with-docs](./grill-with-docs/SKILL.md)**: Grilling session that also builds your project's domain model, sharpening terminology and updating `GLOSSARY.md` and ADRs inline.
- **[triage](./triage/SKILL.md)**: Sort issues: give each a kind (bug, feature) and a stage that says what it needs next.
- **[improve-codebase-architecture](./improve-codebase-architecture/SKILL.md)**: Scan a codebase for deepening opportunities, present them as a visual HTML report, then grill through whichever one you pick.
- **[set-up-repo](./set-up-repo/SKILL.md)**: Configure this repo for the engineering skills (issue tracker, issue labels, domain doc layout). Run once per repo.
- **[write-spec](./write-spec/SKILL.md)**: Turn the current conversation into a spec and publish it to the issue tracker.
- **[write-tickets](./write-tickets/SKILL.md)**: Break any plan, spec, or conversation into a set of tracer-bullet tickets, each declaring its blocking edges, whether as text in a local file or as native blocking links on a real tracker.
- **[implement](./implement/SKILL.md)**: Build the work described by a spec or set of tickets, driving `/tdd` at pre-agreed seams and closing out with `/review-code` before committing.
- **[implement-spec](./implement-spec/SKILL.md)**: Implement a whole spec on one integration branch. Works the tickets as a task graph, running implementer subagents across the ready frontier for maximum concurrency, then closes out with `/review-code`.
- **[plan-large-work](./plan-large-work/SKILL.md)**: Plan a huge chunk of work (more than one agent session can hold) as a shared map of decision tickets on the issue tracker, resolved one at a time until the way to the destination is clear.
- **[diagram-code](./diagram-code/SKILL.md)**: Turn code into technical diagrams (architecture, data flow, sequence, state, ER, and more) as a self-contained HTML page in Eraser's style, every box linked back to its source line.
- **[run-retro](./run-retro/SKILL.md)**: Suggest improvements to the coding agent's environment (navigation, automated checks, coding standards, steering files, tooling) after a session, most severe first.

### Model-invoked

Model- or user-reachable (rich trigger phrasing so the model can reach for them).

- **[prototype](./prototype/SKILL.md)**: Build a throwaway prototype to answer a design question: a single shareable HTML file for state/logic, or several toggleable UI variations.

- **[diagnose-bug](./diagnose-bug/SKILL.md)**: Disciplined diagnosis loop for hard bugs and performance regressions: build a feedback loop that goes red on this bug → minimise → hypothesise → instrument → fix → regression-test.
- **[research](./research/SKILL.md)**: Investigate a question against high-trust primary sources and capture the findings as a cited Markdown file in the repo, run as a background agent.
- **[tdd](./tdd/SKILL.md)**: Test-driven development with a red-green-refactor loop. Builds features or fixes bugs one vertical slice at a time.
- **[model-domain](./model-domain/SKILL.md)**: Actively build and sharpen a project's domain model by challenging terms, stress-testing with scenarios, and updating `GLOSSARY.md` and ADRs inline.
- **[review-code](./review-code/SKILL.md)**: Two-axis review of the diff since a fixed point: **Standards** (does it follow the repo's coding standards, plus a Fowler smell baseline?) and **Spec** (does it faithfully implement the originating issue/spec?), run as parallel sub-agents.
- **[remove-comments](./remove-comments/SKILL.md)**: Delete the comments in a diff, keeping only license headers, public API docstrings, outside constraints and tool directives, and fix the code each comment was covering for. Runs before review.
- **[write-pr](./write-pr/SKILL.md)**: The shape a pull request body should take: a summary as the smallest visual that makes the change clear, before/after evidence that it works, and a merge-danger call (one-way or two-way door, plus blast radius).
- **[write-issue](./write-issue/SKILL.md)**: File and move issues on GitLab, GitHub or local files: one kind (bug, feature, chore) and one stage each, a title that names the problem, and a description that grows a section per stage.
- **[write-wizard](./write-wizard/SKILL.md)**: Generate an interactive bash wizard that walks a human through steps only they can perform: provisioning infrastructure, setting up credentials or CI secrets, walking an unfamiliar third-party dashboard, or running a one-off migration or cutover.

## Productivity

General workflow tools, not code-specific.

### User-invoked

Reachable only when you type them (Claude Code: `disable-model-invocation: true`; Codex: `policy.allow_implicit_invocation: false` in `agents/openai.yaml`).

- **[grill-me](./grill-me/SKILL.md)**: Get relentlessly interviewed about a plan or design until every branch of the design tree is resolved.
- **[hand-off](./hand-off/SKILL.md)**: Compact the current conversation into a handoff document so another agent can continue the work.
- **[teach](./teach/SKILL.md)**: Teach the user a new skill or concept over multiple sessions, using the current directory as a stateful teaching workspace.
- **[write-questionnaire](./write-questionnaire/SKILL.md)**: Turn a decision you can't answer alone into a Markdown questionnaire for the one person who can (filled in async, or together over a meeting).
- **[wait-what](./wait-what/SKILL.md)**: Fire this the moment a message doesn't land. The agent re-pitches it with the context you're missing, in plain English, using your `GLOSSARY.md` vocabulary.

### Model-invoked

Model- or user-reachable (rich trigger phrasing so the model can reach for them).

- **[grill](./grill/SKILL.md)**: Interview the user relentlessly about a plan, decision, or idea until every branch of the design tree is resolved.
- **[write-for-agents](./write-for-agents/SKILL.md)**: Writing documents for agents: skills, AGENTS.md/CLAUDE.md, and any doc an agent reaches by a pointer.
- **[design-patterns](./design-patterns/SKILL.md)**: The 22 classic design patterns as a lookup from a signal in the code to the pattern it earns, simplest form first (a function, dict, generator or module before a class hierarchy).
- **[codebase-design](./codebase-design/SKILL.md)**: Shared discipline and vocabulary for designing deep modules: small interfaces, clean seams, testable through the interface.

## Principles

Rules of judgment the agent applies while it works. Each answers one question, so no two overlap. You can run one by name (`/principle-keep-it-simple`), and the agent loads one when its description matches the task.

| Principle | The question it answers |
|---|---|
| [`keep-it-simple`](principle-keep-it-simple/SKILL.md) | Should this exist at all? |
| [`write-obvious-code`](principle-write-obvious-code/SKILL.md) | Can a reader understand this and change it alone? |
| [`take-small-verified-steps`](principle-take-small-verified-steps/SKILL.md) | How big is this step, and how do I know it worked? |
| [`name-the-trade-off`](principle-name-the-trade-off/SKILL.md) | What are we optimising for, and what do we give up? |
| [`point-dependencies-inward`](principle-point-dependencies-inward/SKILL.md) | Where does this code live, and which way do dependencies point? |
| [`make-illegal-states-unrepresentable`](principle-make-illegal-states-unrepresentable/SKILL.md) | Can this data hold a wrong state? |
| [`program-strategically`](principle-program-strategically/SKILL.md) | After this change, does the code look designed for it? |
| [`design-for-crashes`](principle-design-for-crashes/SKILL.md) | What if it fails, stops halfway, runs twice, or runs concurrently? |
| [`measure-before-optimizing`](principle-measure-before-optimizing/SKILL.md) | Is it actually slow, and what limits it? |
| [`fix-root-causes`](principle-fix-root-causes/SKILL.md) | Where did it first go wrong? |

Covered by other skills, so no principle: deep modules and seams (`codebase-design`), design patterns (`design-patterns`), testing behaviour through interfaces (`tdd`), the project's vocabulary (`model-domain`), the debugging loop (`diagnose-bug`), turning recurring corrections into checks (`run-retro`).
