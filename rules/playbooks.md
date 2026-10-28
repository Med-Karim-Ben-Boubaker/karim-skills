# Playbooks

Every task runs in exactly one playbook. Before any other work, name it in one line (`Playbook: bug-fix`), call the Skill tool with its name, and copy its numbered steps into your todo list verbatim. A step you skip stays in the list as `skip: <reason>`. A step is done only when its *Done when* holds, and the reply shows the evidence for each step.

| Playbook | When |
|---|---|
| investigation | Read-only question: how or why X works, what a change could break, which option to pick |
| discovery | Learning a new domain, client need, standard, or library landscape |
| planning | Turning an idea into decisions, a spec, and tickets |
| feature | New or changed behaviour |
| bug-fix | Something broken, throwing, failing, or newly slow |
| refactoring | Structure changes, behaviour doesn't |
| perf | One number must move against a baseline |
| prototype | Throwaway code to settle a design question |
| review | Reviewing a diff, branch, or PR |
| shipping | Commits, PR, push |
| authoring-a-skill | Writing or changing a skill, agent, rule, AGENTS.md, or CLAUDE.md |

If none fits, say so and use the closest one. If the task changes type midway (an investigation turns into a fix), finish the current playbook's reply, then name the next one. Conversation with no work to do (a quick fact, a yes/no) needs no playbook.

## Delegation

You are the lead; there is no separate orchestrator. You run the playbook, decide, and judge. Each action goes to a subagent, and only these three, all on Haiku:

| Action | Agent |
|---|---|
| Search, read, trace, gather facts | `explorer` |
| Write or change code, merge a branch | `implementer`, in its own worktree |
| Check work independently: a review lane, a synthesis, a design option | `reviewer` |

- Brief each one with pointers (paths, ticket, spec), the step's *Done when*, and the report format.
- Spawn independent agents in one message so they run in parallel.
- Read the diff or evidence yourself before marking a step done. A subagent's "done" is a claim, not evidence.
- Never spawn an agent to run a whole playbook. Act yourself only when the action is a few tool calls.
