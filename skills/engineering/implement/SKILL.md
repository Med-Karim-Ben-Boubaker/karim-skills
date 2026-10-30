---
name: implement
description: "Implement a piece of work based on a spec or set of tickets."
disable-model-invocation: true
---

Implement the work described by the user in the spec or tickets.

If the user passes a ticket reference, fetch it from the issue tracker and state its title before starting. If the reference is ambiguous, ask.

Call the Skill tool with "tdd" where possible, at pre-agreed seams.

Run typechecking regularly, single test files regularly, and the full test suite once at the end. The commands are under `### Checks` in `AGENTS.md` or `CLAUDE.md`.

Once done, call the Skill tool with "remove-comments" on the work, then with "review-code" to review it. When the review's findings are fixed, sync with the default branch (see **Commit**), then call the Skill tool with "write-pr" to write the merge request's body and evidence, and mark it ready.

## Commit

- **Branch first.** Before the first change, branch off the default branch (named after the ticket, for example `123-export-streaming`). Never commit to the default branch.
- **Follow the repo's commit rules** under `### Commits` in `AGENTS.md` or `CLAUDE.md`: message format, types, scopes. If there are none, write a short imperative title and a body that says why.
- **One commit per verified step**, with refactors and behaviour changes in separate commits.
- **Reference the ticket** in each commit (`Refs #123`), never `Closes`: the merge request closes it.
- **Open the merge request as a draft** after the first push, with only the `Closes #123` line, so the ticket shows work in progress. Its body is written once the work is verified (see above).
- **Sync before ready.** Before marking the merge request ready, merge the latest default branch into the work branch, resolve the conflicts, and run every check under `### Checks`, unit and e2e included, until all pass. If the default branch moves before the merge, sync and run them again.
- **Never skip hooks** (`--no-verify`). When a hook rejects a commit, fix what it found.

## Finish

Leave nothing open behind you:

- **Tickets.** Each ticket this work finished is closed, by its merge request (`Closes #123`) or, without one, as done with a comment linking the commits. After the merge, check each one's state on the tracker and close any the merge left open, as **After the merge** in `docs/agents/issue-tracker.md` says. When it was the last open child of its parent, close the parent too. A ticket you claimed and did not finish: unassign it and comment where it stands.
- **Branches and worktrees.** After the merge, delete the ticket branch, local and remote, and remove any worktree you created (`git worktree remove <path>`). `git worktree list` shows none of yours.
- **Report** what you closed and removed.
