---
name: implement
description: "Implement an issue, a ticket, a spec, or a described change: classify it, run the matching playbook, end with a review verdict."
argument-hint: "A ticket or issue reference, a spec, or a description of the change"
disable-model-invocation: true
---

# Implement

If given a reference, fetch it and state its title. If the tracker isn't configured, call the Skill tool with "setup-repo".

**A ticket with child tickets** (a spec split into slices) → follow [references/ticket-graph.md](references/ticket-graph.md); it runs one playbook per child.

**Anything else** → classify it by intent, write `Playbook: <name>` in one line, then call the Skill tool with that playbook and follow its steps:

| The work | Playbook |
|---|---|
| New or changed behaviour | **feature** |
| Something broken, throwing, failing, or newly slow | **bug-fix** |
| Structure changes, behaviour doesn't | **refactoring** |
| A number must move against a baseline | **perf** |
| A skill, agent, rule, AGENTS.md, or CLAUDE.md | **authoring-a-skill** |

Work that mixes kinds is split: the refactoring lands first, then the behaviour change on top.

Every playbook ends in the **reviewing** playbook. Stop at its verdict; shipping is the user's call (`/ship`).
