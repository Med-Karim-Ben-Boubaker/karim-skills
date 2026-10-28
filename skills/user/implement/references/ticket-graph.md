# Building a spec's ticket graph

The spec's tickets are a **task graph** with blocking edges, not a list. The **frontier** is every ticket whose blockers are done. The tracker should be configured; if not, tell the user to run the "setup-repo" skill.

Talk to subagents through pointers (spec, ticket, notes, commits), not pasted content (**principle-guard-the-context-window**).

1. **Read the spec and tickets.** *Done when:* you can name the frontier.
2. **Explore once, if needed.** One `explorer` agent saves notes outside the repo for every implementer to read. *Done when:* the notes path exists, or `skip: tickets are self-contained`.
3. **Create the integration branch.** If the tracker closes work through PRs, open a draft PR after the first merge.
4. **Build the frontier in parallel.** One `implementer` agent per ticket, in the background, each in its own worktree based on the integration branch. Each runs the playbook the ticket calls for (see the table in [the implement skill](../SKILL.md)) and merges the integration tip into its branch before reporting.
5. **Merge as each finishes.** An `implementer` agent merges the branch into the integration branch and runs the full suite. Spawn implementers for any newly unblocked tickets.
6. **Prove the whole** (**principle-prove-it-works**). Run the full suite and exercise the spec's user stories on the real surface: tickets passing alone don't prove they work together. Run the **reviewing** playbook on the integration branch; one `implementer` fixes the **Act on** findings.
7. **Close out.** Mark the PR ready, or resolve each ticket the way the tracker closes work. Remove the worktrees.
