---
name: implement
description: "Implement a piece of work based on a spec or set of tickets."
disable-model-invocation: true
---

Implement the work described by the user in the spec or tickets.

If the user passes a ticket reference, fetch it from the issue tracker and state its title before starting. If the reference is ambiguous, ask.

Before the first change, call the Skill tool with "principle-keep-it-simple" and "principle-fix-root-causes", plus the principle the work needs: "principle-design-the-core" for types, data and where code lives; "principle-design-for-operations" for jobs, pipelines, config and deployment; "principle-let-models-judge" for prompts, agents and evals.

Call the Skill tool with "tdd" where possible, testing at the seams the spec names or the repo's test policy defines (`### Checks` in `AGENTS.md` or `CLAUDE.md`).

Test what changed, as `principle-take-small-verified-steps` says: the one test each red → green cycle; the tests of what the work touched, with typecheck and lint on changed files, once it is done and synced; and the full suite once, only on the way into the default branch. Evals are not checks: run one only when the work changed a prompt, model, model setting or tool and the user asked for a measurement. The commands are under `### Checks`.

Once done, call the Skill tool with "remove-comments" on the work, then with "review-code" to review it; its Demo runs the software against the ticket's acceptance criteria. A criterion the Demo saw fail is a bug in the work: fix it, then rerun the Demo's `demo.sh` until its output shows the criterion holding. When the review's findings are fixed, sync with the target branch (see **Commit**), then call the Skill tool with "write-pr" to write the merge request's body and evidence, and mark it ready. Then watch it and wait for the user's approval (see **Commit**).

## Commit

- **Branch first.** Before the first change, branch off the **target branch**: the integration branch the work belongs to, or without one the default branch. Name the branch after the ticket, for example `123-export-streaming`. Never commit to the default branch or to an integration branch.
- **Follow the repo's commit rules** under `### Commits` in `AGENTS.md` or `CLAUDE.md`: message format, types, scopes. If there are none, write a short imperative title and a body that says why.
- **One commit per verified step**, with refactors and behaviour changes in separate commits.
- **Reference the ticket** in each commit (`Refs #123`), never `Closes`: the merge request closes it.
- **Open the merge request as a draft** into the target branch, never into another ticket branch, after the first push, with only the `Closes #123` line, so the ticket shows work in progress. Its body is written once the work is verified (see above).
- **Sync before ready.** Before marking the merge request ready, merge the latest target branch into the work branch, resolve the conflicts, and run the tests for the code the work and the merge touched, with typecheck and lint on changed files. Into an integration branch that is all: no full suite, no e2e, no pipeline. Into the default branch the full suite and e2e also run once: the merge request's pipeline is that run where the repo has one, so locally run only the checks under `### Checks` the pipeline leaves out; without a pipeline, run them all locally. Fix a failure with targeted reruns of the failing tests. If the target branch moves before the merge, sync and rerun only the tests the new merge touched.
- **No conflicts at ready.** After the sync, push and check that the tracker reports the merge request free of conflicts. One with conflicts is never marked ready and never handed to the user.
- **Coordinate through the tracker only.** Other agents merge into the same target branch. Never look at their branches, worktrees, merge requests or progress: all you need is whether your own merge request has a conflict, and the tracker tells you.
- **Watch it while it waits.** Once the merge request is ready, run `python3 watch-merge-request.py <iid>` (next to this file; GitLab, through `glab`) in the background from the repo. It exits printing `conflict`, `merged` or `closed`. On another tracker, poll the same three facts with its CLI. The user never has to tell you about a conflict.
- **Resolve a conflict unasked,** whenever the tracker reports one, before or after the approval: merge the latest target branch into the work branch, keep both sides' changes, rerun the tests the merge touched, push, and watch again. Ask the user only when both sides cannot be kept.
- **Merge on the user's approval only, through the tracker.** The user approves by merging the merge request on the tracker themselves, or by a clear yes in the session that names it; after a yes, merge it with the tracker's own merge (`glab mr merge`, `gh pr merge`). Never merge locally or push to the target branch: the tracker takes one merge at a time, and that is the only lock between agents. When the tracker refuses the merge for a conflict, resolve it as above and merge again without asking: the approval stands when the fix touched only the conflicting lines. An approval covers the one merge request it names, never the next. This holds for every merge into an integration branch and into the default branch.
- **Never skip hooks** (`--no-verify`). When a hook rejects a commit, fix what it found.

## Finish

Leave nothing open behind you:

- **Tickets.** Each ticket this work finished is closed, by its merge request (`Closes #123`) or, without one, as done with a comment linking the commits. After the merge, check each one's state on the tracker and close any the merge left open, as **After the merge** in `docs/agents/issue-tracker.md` says. When it was the last open child of its parent, close the parent too. A ticket you claimed and did not finish: unassign it and comment where it stands.
- **Branches and worktrees.** After the merge, delete the ticket branch, local and remote, and remove any worktree you created (`git worktree remove <path>`). `git worktree list` shows none of yours.
- **Report** what you closed and removed, and each acceptance criterion as Proven, Failed or Unproven with its evidence: the merge request, or without one, the full path of each screenshot and output. End by telling the user that `/write-walkthrough` gives them steps to check the work themselves.
