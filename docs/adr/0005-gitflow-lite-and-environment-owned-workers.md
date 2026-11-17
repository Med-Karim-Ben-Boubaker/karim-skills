---
status: accepted
---

# GitFlow-lite branches, and workers run the environment's way

Agents now run in parallel through an environment that starts, messages and cleans up agents in their own worktrees, as well as through subagents. `implement-spec` and `implement` prescribed the mechanics themselves: make the worker's checkout, poll it against a time budget, send a fresh subagent into a conflicting worktree, and remove every worktree after the merge, including the one a worker was given. Each of these contradicts an environment that owns its workers. The branch a spec's children merged into was called an "integration branch", a word no branching model uses, and ticket branches had no naming rule.

**Decision.** A new rule, `rules/workers.md`: the environment's own worker rules win over the skills' defaults, and whoever creates a workspace removes it with the same tool. The skills say *what* goes to a worker and *when*, and name no environment. Branches follow GitFlow-lite with Conventional Branch names, stated once under **Branch first** in `implement`: `<kind>/<issue>-<slug>` for a ticket, `feature/<spec>-<slug>` for a spec whose children are correct only together, `hotfix/<issue>-<slug>` from the release tag; no `develop` or `release/*`. A ticket goes straight to the default branch unless the spec says why it needs a feature branch.

**Considered options:** naming the environment in one adapter rule ties the plugin to it and is wrong where it runs without it; naming it in each skill ties ten skills to it; full GitFlow adds `develop` and `release/*`, worth it only when several released versions are supported at once.

**Revisit when:** a second environment with its own worker mechanics behaves differently enough that "its rules win" leaves a skill step undefined, or a repo needs to support two released versions at once.
