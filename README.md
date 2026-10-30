# karim-skills

Agent skills and rules for Claude Code and Codex, shipped as one plugin.

## Structure

```
skills/<name>/          one folder per skill, directly under skills/
  SKILL.md              the skill: name, description, instructions
  agents/openai.yaml    Codex display name and invocation policy
  *.md                  reference files the skill loads when needed
rules/*.md              always-on instructions, installed by a script
scripts/install-rules.sh
.claude-plugin/         Claude Code plugin and marketplace manifests
.codex-plugin/          Codex plugin manifest
.agents/plugins/        Codex marketplace manifest
```

Skills are never nested in group folders, because Codex finds skills only one level deep. [`skills/README.md`](skills/README.md) lists them in three groups:

| Group | What |
|---|---|
| Engineering | Code work: issues, spec and tickets, implement, TDD, review, PRs, bug diagnosis, diagrams |
| Productivity | Grilling, hand-off, teaching, writing for agents, codebase design, design patterns |
| Principles (`principle-*`) | Rules of judgment the agent applies while it works, one question each |

A skill is either model-invoked (the agent picks it when the task matches its description) or user-only: `disable-model-invocation: true` in `SKILL.md` for Claude Code, `policy.allow_implicit_invocation: false` in `agents/openai.yaml` for Codex. Naming rules are in [`AGENTS.md`](AGENTS.md). Many skills are forked from [mattpocock/skills](https://github.com/mattpocock/skills) (MIT, see [`LICENSE-mattpocock`](LICENSE-mattpocock)); [`UPSTREAM.md`](UPSTREAM.md) maps their names.

## Install

### Skills

The repo is one plugin with a manifest for each tool: [`.claude-plugin/`](.claude-plugin) for Claude Code, [`.codex-plugin/`](.codex-plugin) and [`.agents/plugins/marketplace.json`](.agents/plugins/marketplace.json) for Codex.

Claude Code:

```bash
claude plugin marketplace add Med-Karim-Ben-Boubaker/karim-skills
claude plugin install karim-skills@karim-skills
```

Codex:

```bash
codex plugin marketplace add Med-Karim-Ben-Boubaker/karim-skills
codex plugin add karim-skills@karim-skills
```

Done when `claude plugin list` or `codex plugin list` shows `karim-skills`. The skills load in the next new session.

### Rules

Plugins can't install rules in either tool, so a script does it from a clone of this repo. Claude Code reads each rule from `~/.claude/rules/`; Codex reads them from one managed block in `~/.codex/AGENTS.md`, leaving the rest of that file alone. (Codex's own `~/.codex/rules/*.rules` files are command-approval policies, not instructions; the script doesn't touch them.)

```bash
git clone https://github.com/Med-Karim-Ben-Boubaker/karim-skills ~/karim-skills
~/karim-skills/scripts/install-rules.sh --dry-run
~/karim-skills/scripts/install-rules.sh
```

Run `--dry-run` first and show the user what would change. The script links Claude rules, so a `git pull` updates them; rerun it after a pull for Codex. It skips any rule file in `~/.claude/rules/` that isn't one of its links: report those to the user, and use `--force` only if they agree. `--claude` or `--codex` limits it to one tool; `--remove` uninstalls.

### Update

Claude Code:

```bash
claude plugin marketplace update karim-skills
claude plugin update karim-skills@karim-skills
```

Codex:

```bash
codex plugin marketplace upgrade karim-skills
```

Rules, from the clone the user installed them from (`~/karim-skills` above; find it with `readlink -f ~/.claude/rules/brief-replies.md` if unsure):

```bash
git -C <clone> pull
<clone>/scripts/install-rules.sh --dry-run
<clone>/scripts/install-rules.sh
```

- Claude Code reads rules through links into the clone, so the `pull` already updates changed rules; the script only links rules that are new.
- Codex holds a copy in `~/.codex/AGENTS.md`, so rerun the script after every pull, or Codex keeps the old text.
- When the user edits a rule in the clone without pulling, Claude sees it at once; rerun the script for Codex.
- When the dry run reports a rule as skipped, a file of that name in `~/.claude/rules/` is not one of the script's links, for example a link from an older setup. Tell the user which files, and rerun with `--force` only if they agree to replace them.

Start a new session after any update, so both tools load the new skills and rules.

## Release

Every skill is listed in [`.claude-plugin/plugin.json`](.claude-plugin/plugin.json) as `./skills/<name>`. To release, raise `version` to the same value in `.claude-plugin/plugin.json` and `.codex-plugin/plugin.json` in one commit, then push to `main`. Both tools cache by version, so a push without a new version doesn't reach installed copies.
