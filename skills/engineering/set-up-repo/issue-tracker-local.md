# Issue tracker: Local Markdown

Issues and specs for this repo live as markdown files in `.scratch/`.

## Conventions

```
.scratch/
├── issues/<NNN>-<slug>.md        an issue on its own, numbered from 001
├── <feature-slug>/
│   ├── spec.md                   the feature's spec
│   └── issues/<NN>-<slug>.md     its tickets, numbered from 01, one file per ticket
└── templates/                    bug.md, feature.md, chore.md, for filing by hand
```
- Comments and conversation history append to the bottom of the file under a `## Comments` heading

## Children and dependencies

Big work is a feature folder: `spec.md` is the parent, and each file in its `issues/` folder is a child ticket. Dependencies are front matter in the child:

```markdown
---
kind: feature
stage: ready
blocked-by: [01, 02]
---
```

- **Create a child**: the next numbered file in `.scratch/<feature-slug>/issues/`. Number blockers first.
- **Frontier**: the children whose `stage:` is not `closed`, with no `assignee:` line, whose every `blocked-by` file is closed.
- **Claim**: add `assignee: <name>` to the front matter and save, before any work.
- **Finish**: close each child (see **Labels**); close `spec.md` the same way after its last child.

## Explore

- **Existing issues**: files under `.scratch/`; count them by `stage:` front matter, or by an older `Status:` line.
- **Other backlogs**: `TODO.md`, `BACKLOG.md`, `docs/backlog*`, `TODO` comments counted with `grep -rc TODO --include=*.<ext>`. Propose moving lasting ones into `.scratch/issues/`.

## Create

`mkdir -p .scratch/issues .scratch/templates`, then write the three templates.

## Labels

Kind and stage are **front matter** at the top of each issue file (the strings are under `### Issue labels` in `AGENTS.md` or `CLAUDE.md`):

```markdown
---
kind: bug
stage: needs-triage
---
```

- **Move an issue**: edit its `stage:` line.
- **Close an issue**: set `stage: closed` and add `closed: done`, `closed: not planned` or `closed: duplicate of <path>`, after a comment with the reason.
- **List by stage**: `grep -rl "^stage: ready" .scratch`.

## Issue templates

`.scratch/templates/bug.md`, `feature.md`, `chore.md`: each is the kind's template body under front matter with its `kind:` and `stage: needs-triage`. Copy one to file an issue by hand.

## Pull requests

None: work merges locally. After the merge, close each ticket it finished as done, with a comment naming the merge commit. Keep screenshots for the evidence in `.scratch/<feature-slug>/evidence/` and link them from the comment.

## When a skill says "publish to the issue tracker"

Create a new file under `.scratch/<feature-slug>/`, or `.scratch/issues/` for an issue outside any feature (creating the directory if needed).

## When a skill says "fetch the relevant ticket"

Read the file at the referenced path. The user will normally pass the path or the issue number directly.

## Wayfinding operations

Used by `/plan-large-work`. The **map** is a file with one **child** file per ticket.

- **Map**: `.scratch/<effort>/map.md` (the Notes / Decisions-so-far / Fog body).
- **Child ticket**: `.scratch/<effort>/issues/NN-<slug>.md`, numbered from `01`, with the question in the body. A `Type:` line records the ticket type (`research`/`prototype`/`grilling`/`task`); a `Status:` line records `claimed`/`resolved`.
- **Blocking**: a `Blocked by: NN, NN` line near the top. A ticket is unblocked when every file it lists is `resolved`.
- **Frontier**: scan `.scratch/<effort>/issues/` for files that are open, unblocked, and unclaimed; first by number wins.
- **Claim**: set `Status: claimed` and save before any work.
- **Resolve**: append the answer under an `## Answer` heading, set `Status: resolved`, then append a context pointer (gist + link) to the map's Decisions-so-far in `map.md`.
