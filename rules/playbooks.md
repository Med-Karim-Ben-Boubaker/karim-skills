# Playbooks

The user drives work with commands (`/explore`, `/plan`, `/implement`, `/review`, `/ship`, `/grill-me`); each one picks a playbook. For a free-form request with no command, pick the playbook the matching command would pick, and write it in one line (`Playbook: bug-fix`) before any other work.

| Playbook | When |
|---|---|
| investigation | How or why code works, what a change could break, a bug's cause without a fix, which option to pick |
| discovery | Learning a new domain, client need, standard, or library landscape |
| prototype | Throwaway code to settle a design question |
| planning | Turning an idea into decisions and tickets |
| feature | New or changed behaviour |
| bug-fix | Something broken, throwing, failing, or newly slow |
| refactoring | Structure changes, behaviour doesn't |
| perf | One number must move against a baseline |
| authoring-a-skill | Writing or changing a skill, agent, rule, AGENTS.md, or CLAUDE.md |
| reviewing | Reviewing a diff, branch, or PR |
| shipping | Commits, PR, push |

Copy the playbook's numbered steps into your todo list verbatim. A skipped step stays as `skip: <reason>`. A step is done only when its *Done when* holds, and the reply shows each step's evidence. If none fits, say so and use the closest. A quick fact or yes/no needs no playbook.

## Delegation

You are the lead; there is no orchestrator agent. You run the playbook, decide, and judge. Each action goes to one of three subagents:

| Action | Agent |
|---|---|
| Search, read, trace, gather facts | `explorer` |
| Write or change code, merge a branch | `implementer`, in its own worktree |
| Check work independently: a review lane, a synthesis, a design option | `reviewer` |

- Brief each with pointers (paths, ticket, spec), the step's *Done when*, and the report format.
- Spawn independent agents in one message so they run in parallel.
- Read the diff or evidence yourself before marking a step done. A subagent's "done" is a claim, not evidence.
- Never spawn an agent to run a whole playbook. Act yourself only when the action is a few tool calls.
