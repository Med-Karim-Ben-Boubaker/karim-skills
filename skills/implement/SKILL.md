---
name: implement
description: "Implement a piece of work based on a spec or set of tickets."
disable-model-invocation: true
---

Implement the work described by the user in the spec or tickets.

If the user passes a ticket reference, fetch it from the issue tracker and state its title before starting. If the reference is ambiguous, ask.

Before the first change, call the Skill tool with "principle-keep-it-simple" and "principle-fix-root-causes", plus the principle the work needs: "principle-design-the-core" for types, data and where code lives; "principle-design-for-operations" for jobs, pipelines, config and deployment; "principle-let-models-judge" for prompts, agents and evals.

Call the Skill tool with "tdd" where possible, testing at the seams the spec names or the repo's test policy defines (`### Checks` in `AGENTS.md` or `CLAUDE.md`).

Test what changed, as `principle-take-small-verified-steps` says: the one test each red → green cycle, the tests of what a step touched when it's done, typecheck and lint on changed files, and the full suite once, at the end. Evals are not checks: run one only when the work changed a prompt, model, model setting or tool and the user asked for a measurement. The commands are under `### Checks`.

Once done, call the Skill tool with "remove-comments" on the work, then with "review-code" to review it; its Demo runs the software against the ticket's acceptance criteria. A criterion the Demo saw fail is a bug in the work: fix it, then rerun the Demo's `demo.sh` until its output shows the criterion holding. When the review's findings are fixed, sync with the default branch (see **Commit**), then call the Skill tool with "write-pr" to write the merge request's body and evidence, and mark it ready.

## Commit

- **Branch first.** Before the first change, branch off the default branch (named after the ticket, for example `123-export-streaming`). Never commit to the default branch.
- **Follow the repo's commit rules** under `### Commits` in `AGENTS.md` or `CLAUDE.md`: message format, types, scopes. If there are none, write a short imperative title and a body that says why.
- **One commit per verified step**, with refactors and behaviour changes in separate commits.
- **Reference the ticket** in each commit (`Refs #123`), never `Closes`: the merge request closes it.
- **Open the merge request as a draft** after the first push, with only the `Closes #123` line, so the ticket shows work in progress. Its body is written once the work is verified (see above).
- **Sync before ready.** Before marking the merge request ready, merge the latest default branch into the work branch, resolve the conflicts, and run every check under `### Checks` once, full suite and e2e included. Fix a failure with targeted reruns of the failing tests, then run the full suite one last time. If the default branch moves before the merge, sync and run the full suite again.
- **Never skip hooks** (`--no-verify`). When a hook rejects a commit, fix what it found.

## Finish

Leave nothing open behind you:

- **Tickets.** Each ticket this work finished is closed, by its merge request (`Closes #123`) or, without one, as done with a comment linking the commits. After the merge, check each one's state on the tracker and close any the merge left open, as **After the merge** in `docs/agents/issue-tracker.md` says. When it was the last open child of its parent, close the parent too. A ticket you claimed and did not finish: unassign it and comment where it stands.
- **Branches and worktrees.** After the merge, delete the ticket branch, local and remote, and remove any worktree you created (`git worktree remove <path>`). `git worktree list` shows none of yours.
- **Report** what you closed and removed, and each acceptance criterion as Proven, Failed or Unproven with its evidence: the merge request, or without one, the full path of each screenshot and output. End by telling the user that `/write-walkthrough` gives them steps to check the work themselves.
