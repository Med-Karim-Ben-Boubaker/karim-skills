---
status: accepted
---

# A walkthrough for the user to check the work themselves

The Demo proves a change to the agent, but the user's trust comes from seeing it themselves: their own manual commands kept finding failures that tests and agent reports had missed. `write-walkthrough` gives them the steps: setup from a fresh terminal, one step per acceptance criterion with a copyable command or UI clicks and an expected result written from the criterion, edge cases, and cleanup, all writing to the sandbox. The agent runs every step first, so the user never gets a broken one. It is user-invoked and reuses the run recipe and the Demo's commands and screenshots; `write-pr` doesn't call it, so a merge request doesn't pay for a second run. A step with nothing to run on proves nothing, so the agent agrees the **sample data** with the user before writing: reused from the repo or the Demo, generated, or supplied by the user.

**Revisit when:** the user runs it after most tasks (then `implement` should produce it), or its steps keep drifting from the Demo's (then one should be generated from the other).
