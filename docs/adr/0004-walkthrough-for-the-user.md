---
status: accepted
---

# A walkthrough for the user to check the work themselves

The Demo proves a change to the agent, but the user's trust comes from seeing it themselves: their own manual commands kept finding failures that tests and agent reports had missed. `write-walkthrough` gives them a few numbered steps in the chat, each a copyable command or UI clicks with what they should see, for the finished work's demo or any other demo they name. The agent runs every command first, so the user never gets a broken one. It is user-invoked and reuses the run recipe and the Demo's commands; `write-pr` doesn't call it, so a merge request doesn't pay for a second run.

The first version (2026-11-09) wrote a full document: setup, a sample-data table agreed with the user, one step per acceptance criterion, edge cases, cleanup and a checklist, saved as a Markdown file. In use it produced too much text and asked too many questions, so on 2026-11-10 it was cut to the steps alone: the agent looks inputs up or makes them, asks only for what only the user has, and saves no file.

**Revisit when:** the user runs it after most tasks (then `implement` should produce it), or its steps keep drifting from the Demo's (then one should be generated from the other).
