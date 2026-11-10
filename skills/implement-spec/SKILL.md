---
name: implement-spec
description: "Implement a spec from /write-spec and its child tickets in code, on one integration branch."
disable-model-invocation: true
---

You have been provided a spec: a parent issue whose children are the tickets that implement it (see **Children and dependencies** in `docs/agents/issue-tracker.md`).

The issue tracker should have been provided to you. If not, tell the user to run `/set-up-repo`.

The goal is the entire spec implemented on a single **integration branch**, with every ticket resolved the way the issue tracker closes work.

The tickets are not a list of steps. They are a **task graph** with blocking relationships between them. This means there is always a **frontier** of tickets which are ready to be grabbed.

Start every subagent with a fresh context window.

Communication to and from subagents should be sparse. Communicate primarily through **context pointers**: to the spec, tickets, research notes, and previous commits. Don't duplicate information already available via pointers.

**Implementer subagents** should be run in the background where possible for maximum concurrency. Give each one a time budget and track it in a progress file, as the `watchable-commands` rule says for background agents; one that passes its budget gets stopped, its worktree checked, and the user told.

**Checks.** Each ticket runs only the tests for what it changed. The full suite, e2e and CI run once, in step 8: before that, start or wait for no pipeline.

## Steps

1. Read the spec, list its children, and read their blocking edges to build the task graph. The **frontier** is the open children with no assignee and no open blocker.

2. (optional) Use an **exploration subagent** to conduct any exploration required by the tickets - relevant codebase files or external documentation. Ensure the exploration subagent can save files - it should save its markdown notes in a directory outside the repo, accessible by all future subagents. This lets **implementer subagents** focus on implementation rather than exploration.

3. Create the integration branch. If the issue tracker closes work through PRs, or the user asks for one, open a draft PR into the default branch after the first merge in step 5 (a branch with no commits ahead of main can't open one), with only `Closes #<parent>` in its body.

4. Claim each frontier ticket on the tracker (assign it) before starting its subagent, so no other run takes it. Use a fresh **implementer subagent** for each ticket, always in its **own git worktree** on its own branch off the integration branch, never in the main checkout: start it with worktree isolation, or create one with `git worktree add <path> -b <ticket-branch> <integration-branch>`. Record each worktree's path and branch. Each implementer subagent:
   - confirms its worktree is based on the integration branch before starting, and resets onto it if not;
   - calls the Skill tool with `principle-keep-it-simple`, `principle-fix-root-causes` and any principle the ticket's work needs (as the `implement` skill lists them), then with `tdd` to build the ticket;
   - commits as the **Commit** section of the `implement` skill says, referencing its ticket;
   - opens a PR from its branch into the integration branch after its first push, with `Refs #<ticket>` in its body;
   - before reporting done, syncs with the integration branch as **Sync before ready** in the `implement` skill says, and writes the PR's **Evidence** in the `write-pr` format from its own run of the software: the command and its real output, or a screenshot (the run's one Demo comes in step 7)

5. Once an **implementer subagent** completes, check on the tracker that its PR has no conflicts, mark it ready, give the user its link, and start one background watcher for it, as **Watch it while it waits** in the `implement` skill says. The tracker is the only coordination between tickets: no subagent is told about another's work. Other tickets keep running meanwhile.
   - **`conflict`**: send a fresh implementer subagent into that worktree to sync it, unasked, then watch again.
   - **Approval**: each PR merges only on the user's approval of it, as **Merge on the user's approval** in the `implement` skill says.
   - **`merged`**: clean up that ticket at once: `git worktree remove <path>` and `git branch -D <ticket-branch>` (a squash merge on the tracker makes `-d` refuse).

6. Close the merged ticket as done, with a comment naming the integration branch: it merged there, not into the default branch, so no keyword closes it, and its blocked tickets wait for it to close. Then re-read the frontier from the tracker. Kick off more **implementer subagents** for any new tickets on it. This allows for maximum concurrency.

7. Once all tickets are complete, call the Skill tool with `remove-comments` on the integration branch's diff, then with `review-code` on the integration branch. Fix all issues raised by the code review in a single fresh **implementer subagent**.

8. When the review's findings are fixed, sync the integration branch with the default branch as **Sync before ready** in the `implement` skill says; the full suite and e2e run here, once. Then call the Skill tool with `write-pr` to write the draft PR's body, with evidence for every child's acceptance criteria, and mark it ready for review; its merge, which also waits for the user's approval, closes the parent. Without a PR, close the parent once every child is closed. After the merge, check the parent and every child are closed, and report the integration branch.

9. If the run stops before every ticket is done, unassign each claimed ticket that did not merge and comment where it stands, so the next run can take it.

10. Final sweep: `git worktree list` shows only the main checkout and the integration branch's, `git worktree prune` clears stale entries, and `git branch --merged <integration-branch>` lists no ticket branches. Remove any left over, delete merged ticket branches on the remote too, and check the parent and every merged child are closed. Report what you closed and removed, and tell the user that `/write-walkthrough` gives them steps to check the work themselves.
