# Subagent model

When you spawn a subagent with the Agent tool, run it on Haiku 5.5 (`model: "haiku"`) by default.

Use a different model only when one of these says so, in this order:

1. **The user** names a model for the subagent or the task.
2. **A skill** you are following names a model for the subagents it spawns.
3. **The agent definition** sets `model:` in its frontmatter (for example `.claude/agents/*.md`). Leave `model` unset so the definition's choice applies.

Forks (`subagent_type: "fork"`) always inherit your model; this rule does not apply to them.
