---
status: accepted
---

# Demo every change: run it, look at it, show the evidence

Agents claimed work done without running it (about 75 times in the 2026-11-09 retro), and the user's own manual commands kept finding failures that passing tests had missed. Every change now gets a Demo, a third axis of `review-code`: a fresh sub-agent given only the acceptance criteria and the repo's run recipe, never the diff or the author's account, uses the software as a person would, writes only to a sandbox, captures before and after evidence with a script (`demo.sh`), and looks at it; `write-pr` embeds that evidence, captured on the commit the PR points at. `set-up-repo` records the run recipe as a project skill at `.claude/skills/run-<app>/`, so Claude Code's `/run` and `/verify` follow it too.

**Considered options:** a new `demo` skill duplicates what Claude Code's `/run` and `/verify` already do; a demo by the implementer shares the blind spots that produced the bug, and a checker told what to expect tends to see it.

**Revisit when:** a defect a Demo should have caught reaches the default branch, a Demo takes longer than the work it checks, or the agent can call `/verify` with its own acceptance criteria.
