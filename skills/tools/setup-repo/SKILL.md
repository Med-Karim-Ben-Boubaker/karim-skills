---
name: setup-repo
description: "Configure a repo for these skills: its issue tracker, its domain doc layout, and README blueprint checks. Use when a skill needs the tracker or domain docs and the repo has no docs/agents/ yet."
user-invocable: false
---

# Setup repo

Write the per-repo config the other skills read. Explore first, then ask one section at a time, leading with the recommended answer.

1. **Explore.** `git remote -v`; `CLAUDE.md` / `AGENTS.md` and any `## Agent skills` block; `GLOSSARY.md`, `GLOSSARY-MAP.md`, `docs/adr/`; `docs/agents/`; `.scratch/`; monorepo signals (`pnpm-workspace.yaml`, `workspaces` in `package.json`, a populated `packages/*`).
2. **Issue tracker.** Propose GitHub or GitLab from the remote; otherwise offer local markdown (`.scratch/features/<feature>/`, wayfinder maps under `.scratch/maps/<effort>/`) or "other" (record the user's one-paragraph description). Seed `docs/agents/issue-tracker.md` from [issue-tracker-github.md](issue-tracker-github.md), [issue-tracker-gitlab.md](issue-tracker-gitlab.md), or [issue-tracker-local.md](issue-tracker-local.md).
3. **Domain docs.** Single-context (one `GLOSSARY.md` + `docs/adr/` at the root) without asking. Offer multi-context (`GLOSSARY-MAP.md` pointing to per-context glossaries) only when exploration found monorepo signals. Seed `docs/agents/domain.md` from [domain.md](domain.md).
4. **Blueprints.** If the repo has CI or a pre-commit config, offer to copy the "blueprint" skill's `scripts/check_readmes.py` into the repo's `scripts/` and run it there.
5. **Confirm, then write.** Show the drafts and let the user edit. Edit `CLAUDE.md` if it exists, else `AGENTS.md`; if neither, ask which to create. Add or update one block in place:

```markdown
## Agent skills

### Issue tracker
[one line]. See `docs/agents/issue-tracker.md`.

### Domain docs
[single-context or multi-context]. See `docs/agents/domain.md`.

### READMEs
Folder READMEs are blueprints linked into one tree; write and update them with the `blueprint` skill.
```

Tell the user they can edit `docs/agents/*.md` directly; rerun this skill only to switch trackers.
