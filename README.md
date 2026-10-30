# karim-skills

My agent skills for Claude Code, shipped as one plugin.

| Folder | What | Source |
|---|---|---|
| [`skills/engineering/`](skills/engineering) | Code work: grilling, spec and tickets, implement, TDD, code review, bug diagnosis, diagrams | Forked from [mattpocock/skills](https://github.com/mattpocock/skills) at `a496f55` |
| [`skills/productivity/`](skills/productivity) | Grill-me, hand-off, wait-what, teach, write-for-agents | Forked from mattpocock/skills at `a496f55` |
| [`skills/principles/`](skills/principles) | 10 rules of judgment the agent applies while it works, one question each | Mine, distilled from the books in `resources/` |

Forked skills are renamed verb-first (see [`AGENTS.md`](AGENTS.md)). Their upstream names, for merging upstream changes:

| Here | Upstream |
|---|---|
| `pick-skill` | `ask-matt` |
| `set-up-repo` | `setup-matt-pocock-skills` |
| `review-code` | `code-review` |
| `diagnose-bug` | `diagnosing-bugs` |
| `model-domain` | `domain-modeling` |
| `write-pr` | `pr` |
| `run-retro` | `retro` |
| `write-spec` | `to-spec` |
| `write-tickets` | `to-tickets` |
| `plan-large-work` | `wayfinder` |
| `write-wizard` | `wizard` |
| `grill` | `grilling` |
| `hand-off` | `handoff` |
| `write-questionnaire` | `to-questionnaire` |
| `write-for-agents` | `writing-for-agents` |

They are MIT-licensed by Matt Pocock: see [`LICENSE-mattpocock`](LICENSE-mattpocock).

## Where to start

Run `/pick-skill` to find the skill or flow that fits. The main flow is `/grill-with-docs` → `/write-spec` → `/write-tickets` → `/implement` or `/implement-spec`, with `/review-code` at the end. Run `/set-up-repo` once per repo first.

## Install

```bash
claude plugin marketplace add Med-Karim-Ben-Boubaker/karim-skills
claude plugin install karim-skills@karim-skills
```

Every skill must be listed in [`.claude-plugin/plugin.json`](.claude-plugin/plugin.json); bump its `version` so installs pick up changes.
