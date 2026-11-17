# Workers

A **worker** is another agent that takes one task, such as one ticket, and reports back: a subagent, or an agent the environment runs beside you. The skills say *what* goes to a worker and *when*; how a worker runs belongs to the environment.

1. **The environment's own worker rules win.** When the environment you run in has its own skill or rule for starting, messaging, waiting for, stopping or cleaning up agents, follow it over the defaults in these skills. The defaults (a subagent with its own worktree, a time budget and a progress file, a background watcher) apply only where the environment has none. Never steer a worker through its terminal, and never poll for a report the environment will deliver.
2. **Whoever creates a workspace removes it, with the same tool.** You remove a worktree or branch you created, after its work merged, with the command you created it with. A worktree you were given, including the one you run in as a worker, is not yours to remove: report that its work is done and leave it to its owner.

## Examples

| Situation | Do |
|---|---|
| `implement-spec` needs a worker per ticket, and the environment offers its own way to start agents in new workspaces | Start them that way; skip `git worktree add` |
| Plain Claude Code, no such mechanism | Start a subagent with worktree isolation, give it a time budget, track it in a progress file |
| A worker's merge request has a conflict | Send the fix to that same worker through the environment, or to a fresh subagent where there is no way to message one |
| You ran `/implement` as a worker and the merge request merged | Delete the ticket branch; leave the worktree to whoever created it |
