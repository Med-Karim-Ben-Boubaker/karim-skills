---
name: write-walkthrough
description: "Write the steps for you to check finished work yourself: setup with agreed sample data, copyable commands, UI clicks and what each should show, edge cases and cleanup, every step run by the agent first."
disable-model-invocation: true
---

# Write Walkthrough

A **walkthrough** is what the user follows to see with their own eyes that the work does what its acceptance criteria say: copyable commands, UI actions, and what each one should show. It reproduces results the way a person uses the software, through the app's CLI, its pages and its API; the test suite stays out of it.

## 1. Gather

- **The work**: the branch, the commit (`git rev-parse --short HEAD`), and the folder it is checked out in (`git worktree list`).
- **The criteria**: the `## Brief` acceptance criteria of the tickets the work finishes (fetch them as `docs/agents/issue-tracker.md` says), or the spec. Without either, ask the user what the work should do.
- **The run recipe**, under `### Run` in `AGENTS.md` or `CLAUDE.md`: how to start the app, the sandbox, and what is off limits.
- **The Demo**, if `review-code` ran one on this commit: `.sandbox/demo-<short sha>/` holds `demo.sh` and the screenshots and outputs it captured. Reuse its commands, inputs and screenshots.

## 2. Agree on the sample data

**Sample data** is what must exist before a step can run: an input file, rows in a database, an object in a bucket, a user with records to show, a request body. List what each criterion's step and edge case needs; when none needs anything, go on to step 3.

Each input comes from one source:

- **Reuse**: a sample file already in the repo, or an input the Demo's `demo.sh` made, when it covers the criterion.
- **Generate**: data you make for this walkthrough.
- **From the user**: what only they have: a real document, licensed or production data, their login.

Fill the **Sample data** table in [template.md](template.md) with a recommended source for each input: reuse what covers the criterion, generate the rest, and ask the user only for what you can't make. Show it to the user and wait for their answer. Done when every input has a source the user agreed to.

Generated data:

- has the real input's shape: the file type, columns, value types and encoding the app reads in use, taken from a real example or the code that parses it;
- is small, each record there for one criterion or edge case;
- is made up: invented names, `example.com` addresses, placeholder keys, so no real person's data or secret ends up in it;
- is created by a Setup command, a heredoc for text and an inline script with a fixed seed for anything else, so the walkthrough alone recreates it;
- lives in the sandbox: files in `.sandbox/walkthrough/input/`, records and objects where the recipe's sandbox says, each named with a `walkthrough-` prefix so cleanup deletes exactly those. Create records through the app's own entry point (its CLI, API or admin command) when it has one.

The user's files are copied into `.sandbox/walkthrough/input/`. The walkthrough names them by path and leaves their contents out, since it may go into a merge request.

## 3. Write

Fill [template.md](template.md). Write each **Expect:** line from the criterion before you run anything: it says what should happen, never what the code happens to do.

- **Setup** starts from a fresh terminal: `cd` into the folder the work is checked out in, check the commit, load the env file from the main checkout, point every output at the sandbox, install, then create the sample data.
- **One step per acceptance criterion**, named after it, ending in **Expect:** the exact output line, what the screen shows, or the Demo's screenshot to compare with, and the sample record it comes from. When the Demo captured a before, add what the same step showed before the change.
  - A command step is a block the user can copy, calling the app's real entry points.
  - A UI step starts the app in the background of the same shell, logging to the sandbox, then gives numbered actions naming the URL, each element by its visible label, and the text to type: "Click **Export** in the top bar".
  - A pipeline step runs on the sample data, then compares the output with the default branch's output on the same data.
- **Edge cases**: at least one per criterion where input can go wrong (empty, too large, illegal, missing), each with its own sample record, and what should happen instead of a crash.
- **Cleanup** stops what the walkthrough started, deletes the `walkthrough-` records and objects, and empties its sandbox folder.

Every command writes only to the sandbox. A step the recipe puts off limits stays out, and the walkthrough says why.

## 4. Run it yourself

Follow the walkthrough exactly as written, on the same commit:

- Run the command blocks in order in one fresh shell, so `cd` and `export` carry over as they will for the user.
- Do the UI steps in a browser you can drive (Playwright, Claude in Chrome), with the walkthrough's own server running, using the labels as written.

Fix every step whose command fails or whose wording misleads, and run it again. When a step fails on the sample data, compare the data with the real input's shape: a mismatch is the walkthrough's to fix, and data that matches but still fails is a bug in the work. A step only a person can do (their login, a device, production data) stays in, marked **Not run by me** with the reason. When a step shows the work itself is wrong, stop and report it as a bug: the walkthrough says what the criteria promise, and the code has to meet it.

Done when every step has run and shown what its **Expect:** line says, or is marked **Not run by me**.

## 5. Hand it over

Save it to `.sandbox/walkthrough-<short sha>.md`, print it in full, and give the file's full path. When a merge request is open for the branch, offer to add it to the description under **How to verify**, collapsed.
