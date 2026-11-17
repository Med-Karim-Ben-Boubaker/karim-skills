---
name: prove-change
description: "Proves a change works by running the software as it is meant to run (CLI, pages, API, or a deployed dev environment) for each acceptance criterion, capturing the output or a screenshot, and looking at it: Proven, Failed or Unproven. Use after building, before a merge request goes ready, or when asked to prove, show or demo that something works."
---

# Prove a change

A **proof** is one acceptance criterion shown holding by running the software the way it is meant to run, with what it printed or showed captured and looked at. A test run is never a proof: tests check code, a proof checks the software.

## Inputs

- **The criteria**: the `## Brief` checkboxes of the ticket (each child of a spec has its own), plus a bug's steps to reproduce from its `## Diagnosis`. Fetch the ticket with the command in `docs/agents/issue-tracker.md`.
- **The run recipe**: `### Run` in `AGENTS.md` or `CLAUDE.md` names it, usually `.claude/skills/run-<app>/SKILL.md`. It says how to start, use and stop the app, the **sandbox** every run writes to, and what is off limits. Without one, work the launch out from the README and build files, write nothing to shared state (a bucket, a database, a tracker, an outgoing message), and tell the user `/set-up-repo` records a recipe.
- **The commit**: `HEAD`'s short sha. Evidence goes to `.sandbox/proof-<sha>/`; when `git check-ignore -q .sandbox/` fails, add `.sandbox/` to `.git/info/exclude`.

## Steps

For each criterion:

1. **Pick where it can be seen, cheapest first.** Locally, in this worktree's sandbox, when the criterion is about what the code does. On a deployed dev environment, through the recipe's **Deployed** section, only when the criterion names one or the behaviour exists only deployed (infrastructure, an Image, a service on a VM). Nowhere, when it needs production data, a person's login or an off-limits output: mark it **Unproven** with the reason.
2. **Write down what a person should see** when it holds: the output line, the page, the rows a run writes.
3. **Run it** through the software's own entry point: the CLI on a small real input, the page in a browser, the request to the API. Command output goes through `tee` into the evidence folder; screenshots come from the recipe's capture commands. For a bug, run the steps that used to show it.
4. **Look at what you captured**: open each screenshot, read each output, and compare it with step 2. Mark the criterion:
   - **Proven**: what you saw matches, with the file path.
   - **Failed**: expected against seen, with the file path. It is a bug in the work: fix it and prove again.
   - **Unproven**: why it can't be shown here.

Done when every criterion is Proven, Failed or Unproven, each with its command and its captured file.

## Report

One entry per criterion, in the order of the `## Brief`: the criterion, the mark, the command that was run, and the captured file by full path. `write-pr` copies these into the merge request's `## Proof`. After a later push, rerun only the proofs the push touched, on the new `HEAD`.
