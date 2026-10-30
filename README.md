# karim-skills

My agent skills for Claude Code, shipped as one plugin.

| Folder | What | Source |
|---|---|---|
| [`skills/engineering/`](skills/engineering) | Code work: grilling, spec and tickets, implement, TDD, code review, diagnosing bugs | Forked from [mattpocock/skills](https://github.com/mattpocock/skills) at `a496f55` |
| [`skills/productivity/`](skills/productivity) | Grill-me, handoff, wait-what, teach, writing-for-agents | Forked from mattpocock/skills at `a496f55` |
| [`skills/principles/`](skills/principles) | 10 rules of judgment the agent applies while it works, one question each | Mine, distilled from the books in `resources/` |

The forked skills keep upstream names and layout so upstream changes merge cleanly, except `ask-matt` (now `which-skill`) and `setup-matt-pocock-skills` (now `setup-repo`). They are MIT-licensed by Matt Pocock: see [`LICENSE-mattpocock`](LICENSE-mattpocock).

## Where to start

Run `/which-skill` to find the skill or flow that fits. The main flow is `/grill-with-docs` → `/to-spec` → `/to-tickets` → `/implement` or `/implement-spec`, with `/code-review` at the end. Run `/setup-repo` once per repo first.

## Install

```bash
claude plugin marketplace add Med-Karim-Ben-Boubaker/karim-skills
claude plugin install karim-skills@karim-skills
```

Every skill must be listed in [`.claude-plugin/plugin.json`](.claude-plugin/plugin.json); bump its `version` so installs pick up changes.
