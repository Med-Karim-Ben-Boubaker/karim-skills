---
name: implement
description: "Implement a piece of work based on a spec or set of tickets."
disable-model-invocation: true
---

Implement the work described by the user in the spec or tickets.

If the user passes a ticket reference, fetch it from the issue tracker and state its title before starting. If the reference is ambiguous, ask.

Before the first change, call the Skill tool with "principle-keep-it-simple" and "principle-fix-root-causes", plus the principle the work needs: "principle-design-the-core" for types, data and where code lives; "principle-design-for-operations" for jobs, pipelines, config and deployment; "principle-let-models-judge" whenever the work touches code that calls an LLM (prompts, agents, tools, model settings, evals), because model behaviour is not fixed the way code is.

Call the Skill tool with "tdd" where possible, testing at the seams the spec names or the repo's test policy defines (`### Checks` in `AGENTS.md` or `CLAUDE.md`).

Test what changed, as `principle-take-small-verified-steps` says: the one test each red → green cycle; the tests of what the work touched, with typecheck and lint on changed files, once it is done and synced; and the full suite once, only on the way into the default branch. Evals are not checks: run one only when the work changed a prompt, model, model setting or tool and the user asked for a measurement. The commands are under `### Checks`.

Once done, call the Skill tool with "remove-comments" on the work, then with "review-code" to review it; its Demo runs the software against the ticket's acceptance criteria. A criterion the Demo saw fail is a bug in the work: fix it, then rerun the Demo's `demo.sh` until its output shows the criterion holding. When the review's findings are fixed, sync with the target branch (see **Commit**), then call the Skill tool with "write-pr" to write the merge request's body and evidence, and mark it ready. Then watch it and wait for the user's approval (see **Commit**).

## Commit

A **merge request** here is a GitHub pull request or a GitLab merge request; each tracker's commands are under **Pull requests** or **Merge requests** in `docs/agents/issue-tracker.md`. A repo whose tracker has neither merges locally, on the same approval.

- **Branch first.** Before the first change, branch off the **target branch**: the integration branch the work belongs to, or without one the default branch. Name the branch after the ticket, for example `123-export-streaming`. Never commit to the default branch or to an integration branch.
- **Follow the repo's commit rules** under `### Commits` in `AGENTS.md` or `CLAUDE.md`: message format, types, scopes. If there are none, write a short imperative title and a body that says why.
- **One commit per verified step**, with refactors and behaviour changes in separate commits.
- **Reference the ticket** in each commit (`Refs #123`), never `Closes`: the merge request closes it.
- **Open the merge request as a draft** into the target branch, never into another ticket branch, after the first push, with only the `Closes #123` line, so the ticket shows work in progress. Its body is written once the work is verified (see above).
- **Sync before ready.** Merge the latest target branch into the work branch, resolve the conflicts, rerun the tests the merge touched, and push. Mark the merge request ready once the tracker reports it free of conflicts. Into the default branch, the full suite and e2e run once here: in the merge request's pipeline where the repo has one, locally otherwise.
- **Watch it while it waits.** Run `python3 watch-merge-request.py <github|gitlab> <number>` (next to this file) in the background from the repo; it exits printing `conflict`, `merged` or `closed`. On `conflict`, sync again as above, unasked, and watch again; ask the user only when both sides' changes cannot both be kept. The tracker's status of your own merge request is the only coordination with other agents: their branches, worktrees and progress are theirs.
- **Merge on the user's approval, through the tracker.** The user approves one merge request by merging it on the tracker, or by a clear yes in the session that names it. After a yes, merge it with the tracker's command (`gh pr merge`, `glab mr merge`), never locally or by a push to the target branch. A conflict fix after the approval needs no second one.
- **Never skip hooks** (`--no-verify`). When a hook rejects a commit, fix what it found.

## Finish

Leave nothing open behind you:

- **Tickets.** Each ticket this work finished is closed, by its merge request (`Closes #123`) or, without one, as done with a comment linking the commits. After the merge, check each one's state on the tracker and close any the merge left open, as **After the merge** in `docs/agents/issue-tracker.md` says. When it was the last open child of its parent, close the parent too. A ticket you claimed and did not finish: unassign it and comment where it stands.
- **Branches and worktrees.** After the merge, delete the ticket branch, local and remote, and remove any worktree you created (`git worktree remove <path>`). `git worktree list` shows none of yours.
- **Report** what you closed and removed, and each acceptance criterion as Proven, Failed or Unproven with its evidence: the merge request, or without one, the full path of each screenshot and output. End by telling the user that `/write-walkthrough` gives them steps to check the work themselves.
