---
name: implement
description: "Implement one ticket from the issue tracker in its own worktree, moving it through the ticket states from Ready to Done."
disable-model-invocation: true
---

Build one ticket. The work moves through the **ticket states** below; at each step, know which state you are in, do what it says, and leave it when its exit holds. Say the state to the user as you enter it ("Building #123").

## Two guards

These two always hold; everything else is guidance.

1. **A ticket first.** The work is a ticket on the issue tracker (`docs/agents/issue-tracker.md`; on a local tracker, a ticket file). Without one, stop and offer `/write-issue`. If the reference is ambiguous, ask.
2. **Its own worktree.** The work is built in a git worktree of its own, never in the main checkout (the first line of `git worktree list`). Use the worktree the environment gave you, or create one at `../<repo>-<issue>` with `git worktree add ../<repo>-<issue> -b <branch> <base>`. The worktree, the branch and the issue number agree.

## Where the work starts and lands

Branches follow **GitFlow-lite**: GitFlow's feature and hotfix branches, no `develop` or `release/*`, and a tag is a release. Names are **Conventional Branch** names, lowercase. The ticket's intent decides the row; the repo's own docs win where they name things otherwise.

| Intent | Base | Branch | Merge request into | Merge |
|---|---|---|---|---|
| A ticket that stands alone, or a child of a spec that goes straight to the default branch (the default) | default branch | `<kind>/<issue>-<slug>` | default branch | squash |
| A child of a spec with a **feature branch** | the feature branch | `<kind>/<issue>-<slug>` | the feature branch | squash |
| A spec whose children are correct only together (`implement-spec` makes it) | default branch | `feature/<spec>-<slug>` | default branch, after its last child | merge commit |
| A **hotfix** to what production runs | the release tag production runs | `hotfix/<issue>-<slug>` | default branch, once the fix is tagged | merge commit |

`<kind>` is the ticket's kind: `feature`, `bugfix` or `chore`, as in `chore/123-export-streaming`. Each merge into the default branch leaves it working: new code lands unused or behind a setting that is off until the last ticket wires it in.

## Ticket states

```
Ready → Claimed → Building ⇄ Reviewing → Proving → Waiting → Merged → Done
                     ↑                       │          │
                     └──── Failed proof ─────┘          └ conflict: sync, stay Waiting
```

| State | Do | Leave when |
|---|---|---|
| **Ready** | Fetch the ticket, state its title, read its `## Brief`, and pick its row above | Guard 1 holds and the row is known |
| **Claimed** | Assign the ticket to yourself. Create or enter the worktree from the row's base, on the row's branch | Guard 2 holds and `git merge-base HEAD <base>` is the base's tip |
| **Building** | Load the principles (below), then `tdd`: one red → green cycle at a time, one commit per verified step. After the first push, open a draft merge request into the row's target with only the `Closes #<issue>` line (`Refs #<issue>` into a feature branch) | Every criterion is built and the tests of what changed pass |
| **Reviewing** | `remove-comments` on the work, then `review-code` against the base | Every finding is fixed or answered; a fix goes back to Building |
| **Proving** | Sync with the target (below), then `prove-change` on every criterion of the `## Brief` | Each criterion is Proven or Unproven with its reason; a Failed one goes back to Building |
| **Waiting** | `write-pr` writes the body from the proofs; mark the merge request ready; watch it (below) | The user approves it |
| **Merged** | Merge through the tracker (below); close the ticket as **After the merge** in `docs/agents/issue-tracker.md` says, and the parent after its last child | The ticket is closed on the tracker |
| **Done** | Delete the branch, local and remote. Remove the worktree if you created it, with the tool you created it with; one you were given stays for its owner (the `workers` rule). Report | `git worktree list` and `git branch` show nothing of yours |

**Stopping early**, from any state: unassign the ticket and comment where it stands, so the next run can pick it up.

**The report** names the merge request, what you closed and removed, and each criterion with its proof mark. End by telling the user `/write-walkthrough` gives them steps to check the work themselves.

## Reference

**Principles.** Before the first change, call the Skill tool with `principle-keep-it-simple` and `principle-fix-root-causes`, plus what the work needs: `principle-design-the-core` for types, data and where code lives; `principle-design-for-operations` for jobs, pipelines, config and deployment; `principle-let-models-judge` whenever the work touches code that calls an LLM.

**Checks**, as `principle-take-small-verified-steps` says, with the commands under `### Checks` in `AGENTS.md` or `CLAUDE.md`: the one test each red → green cycle; the tests of what changed, with typecheck and lint on changed files, once the work is synced; the checks its pipeline runs (the full suite, lint, typecheck), never evals, once, locally, before a merge request into the default branch is opened. Evals run only when the work changed a prompt, model, model setting or tool and the user asked for a measurement.

**Commits.** Follow `### Commits` in `AGENTS.md` or `CLAUDE.md`; without one, a short imperative title and a body that says why. Refactors and behaviour changes go in separate commits. Each commit says `Refs #<issue>`, never `Closes`. Hooks always run: when one rejects a commit, fix what it found.

**Merge requests.** A GitHub pull request or a GitLab merge request; the commands are under **Pull requests** or **Merge requests** in `docs/agents/issue-tracker.md`. A tracker with neither merges locally, on the same approval.

- **Sync**: merge the latest target into the branch, resolve the conflicts, rerun the tests the merge touched, and push. Into the default branch, the checks its pipeline runs (the full suite, lint, typecheck), never evals, run once here, locally; open the merge request only when they pass.
- **Watch**: run `python3 watch-merge-request.py <github|gitlab> <number>` (next to this file) in the background; it exits printing `conflict`, `merged` or `closed`. On `conflict`, sync unasked and watch again; ask the user only when both sides' changes cannot both be kept. The tracker's state of your own merge request is your only coordination with other agents.
- **Merge on the user's approval**: they merge it on the tracker, or say a clear yes naming it. Then merge with the tracker's command and the row's merge style (`gh pr merge`, `glab mr merge`), never locally or by a push to the target. A conflict fix after the approval needs no second one.
