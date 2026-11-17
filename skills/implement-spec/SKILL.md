---
name: implement-spec
description: "Implement a spec from /write-spec through its child tickets, running /implement's ticket states for each child in its own worktree, straight to the default branch or through one feature branch."
disable-model-invocation: true
---

Build a whole spec: a parent issue whose children are the tickets that implement it (**Children and dependencies** in `docs/agents/issue-tracker.md`). Each child runs the **ticket states** of the `implement` skill, in a worker of its own; this skill runs the **spec states** around them. Read the `implement` skill first: its two guards, its intent table and its states apply to every child.

The issue tracker should have been provided to you. If not, tell the user to run `/set-up-repo`.

## The spec's path

The spec says which path it takes (`write-spec`, **Implementation Decisions**):

- **Straight to the default branch** (the default): each child merges into the default branch on its own and leaves it working.
- **Feature branch**, only when the children are correct only together: `feature/<spec>-<slug>` from the default branch, in its own worktree at `../<repo>-<spec>`. Children branch from it and merge into it; it merges once into the default branch.

A spec that names no path goes straight to the default branch.

## Spec states

```
Open → Running → (feature branch only: Integrating → Waiting) → Closed
```

| State | Do | Leave when |
|---|---|---|
| **Open** | Read the spec, list its children and their blocking edges: a **task graph**. For a feature branch, create it and its worktree, push it, and open a draft merge request into the default branch with only `Closes #<spec>` once it has a commit | The graph is known and, for a feature branch, its worktree exists |
| **Running** | Work the **frontier**: the open children with no assignee and no open blocker. For each, a fresh worker runs the `implement` ticket states from Ready to Waiting, in its own worktree, on the row the path decides. Give the user each merge request's link as it reaches Waiting. When one merges, close its ticket (into a feature branch, by hand with a note naming the branch, since no keyword closes it there), pull it into the feature branch's worktree, and re-read the frontier | Every child is closed |
| **Integrating** | On the feature branch: `remove-comments` on its diff, `review-code` against the default branch, fixes in one fresh worker. Sync with the default branch; the full suite and e2e run here, once. `write-pr` writes the body with every child's proofs; mark it ready | The merge request is ready and free of conflicts |
| **Waiting** | Watch it as the `implement` skill says. Offer `/prove-change` on the merged whole, once, in one line | The user approves it, and it merges with a merge commit |
| **Closed** | Check the parent and every child are closed; close any still open. Remove each worktree and branch you created, the feature branch's last. Report what you closed and removed, and tell the user `/write-walkthrough` gives them steps to check the work themselves | `git worktree list` and `git branch` show nothing of the spec's |

**Stopping early**: unassign each claimed child that did not merge and comment where it stands, so the next run can pick it up.

## Workers

- **One child, one worker, one worktree.** Claim the child (assign it) before its worker starts. Start each worker with a fresh context window and only **context pointers**: the spec, its ticket, research notes, earlier commits. How a worker is started, messaged, waited for and cleaned up follows the environment's own rules where it has them (the `workers` rule); otherwise, a subagent with worktree isolation, run in the background with a time budget tracked in a progress file (the `watchable-commands` rule).
- **The tracker is the only coordination.** No worker is told about another's work. On `conflict`, send the sync to that child's worker, or a fresh one in its worktree.
- **Exploration first, optionally.** One exploration subagent may read the code and docs the tickets need and save its notes outside the repo, for every worker to read.
- **Merges wait for the user's approval**, each one, as the `implement` skill says.
- **Checks.** Each child runs only the tests of what it changed. The full suite, e2e and CI run once per merge into the default branch.
