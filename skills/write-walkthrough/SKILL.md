---
name: write-walkthrough
description: "Guide you through running a demo yourself that shows a fix or a new feature working: a few numbered steps in the chat, each a command to copy or a click to make, with what you should see."
disable-model-invocation: true
---

# Walkthrough

A **walkthrough** is a short numbered guide, given in the chat, that the user follows to see with their own hands that a bug is fixed or a new feature works, in the software as it runs now: a command to copy or a click to make, then what they should see.

**What to demo.** The fix or feature the user names, whether or not an agent built it; when they name nothing, the work just finished, against its acceptance criteria. For a fix, the steps are the ones that used to show the bug. For a feature, they are a person using it, through the software's own CLI, pages or API. Reuse the commands and inputs of `.sandbox/demo-<short sha>/demo.sh` where `review-code` ran a Demo.

**Look it up instead of asking.** How to start the app and where runs may write is under `### Run` in `AGENTS.md` or `CLAUDE.md`. Inputs come from the Demo, a sample already in the repo, or a few made-up lines in a heredoc. Ask only for what only the user has: a login, their own file.

**Write the guide in the chat**, short enough to fit one screen:

1. One line saying what the demo shows and the folder to run it from.
2. A few numbered steps, in the order the user does them. Each step is one thing to do, then **See:** with the output line or what the screen shows.
   - A command step is one copyable block calling the app's real entry point.
   - A UI step names the URL, each element by its visible label, and the text to type: "Click **Export** in the top bar".
3. When the guide started something that keeps running, a last step with the command that stops it.

The guide is the steps alone: it is a chat reply, never a saved file, and the user asks for more (an edge case, the reason behind a step) when they want it.

**Run each command once before you give it**, in order in one shell, writing only to the sandbox. A command taken from a `demo.sh` that ran on this commit counts as run. Mark a step you could not run (their login, a device) as not run. When a step shows the software itself is wrong, report that as a bug.
