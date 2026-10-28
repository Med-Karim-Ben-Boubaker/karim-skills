---
name: explore
description: "Understand something before deciding or building: how or why code works, what a change could break, the cause of a bug without fixing it, a new domain or library, or a design question to settle with a prototype."
argument-hint: "The question, topic, or code to explore"
disable-model-invocation: true
---

# Explore

Read-only for the codebase: nothing lands on the working branch. Explain, don't interrogate: the user may not know the domain yet.

Write `Playbook: <name>` in one line, then call the Skill tool with it and follow its steps:

| The question | Playbook |
|---|---|
| How or why existing code works, what a change could break, the cause of a bug (no fix) | **investigation** |
| A new domain, client need, standard, or library landscape | **discovery** |
| A design fork that running something would settle better than asking | **prototype** |

End by naming the command that fits next, usually `/plan` or `/implement`.
