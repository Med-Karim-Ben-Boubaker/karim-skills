---
name: write-issue
description: "Files and moves issues on the repo's tracker (GitLab, GitHub or local files): picks the kind (bug, feature, chore) and the stage (needs-triage, parked, needs-investigation, needs-input, ready), titles it, writes the kind's template, and appends what each later stage needs, with evidence that fits the problem. Use when filing, relabelling, moving or closing an issue, or when a bug, idea or chore should be recorded instead of done now. For sorting a backlog, use triage; for a full spec, write-spec; for splitting big work into child tickets, write-tickets."
---

# Write Issue

Every issue carries one **kind**, what it is, and one **stage**, what it needs next. The label strings are in the repo's `AGENTS.md` or `CLAUDE.md` under `### Issue labels`; the commands for this tracker (GitLab, GitHub or local files) are in `docs/agents/issue-tracker.md`. If either is missing, tell the user to run `/set-up-repo`.

## Kinds and stages

| Kind | Means |
|---|---|
| `bug` | Something works wrong |
| `feature` | New or changed behaviour |
| `chore` | Work with no change in behaviour: a refactor, infra, docs, a data run |

| Stage | Needs next |
|---|---|
| `needs-triage` | Someone to decide its kind and stage |
| `parked` | Nothing until it becomes a priority |
| `needs-investigation` | The cause (bug) or the design (feature, chore) |
| `needs-input` | An answer from a person outside the work: the reporter, a client, an expert |
| `ready` | Building. The fix or design is written down with acceptance criteria |

Closing is not a stage. Close as **done** (link the change, or where the behaviour already lives), **not planned** (say why), or **duplicate** (link the original). Work in progress shows as an assignee and a linked merge request, not a label. If only a human can build a `ready` issue, assign that person and say why in the brief.

## Choose the stage

Set the furthest stage you know is true. Use `needs-triage` only when you don't know, usually for an outside report or a quick capture.

| Situation | Kind | Stage |
|---|---|---|
| "A user says the export crashes; nobody has looked yet." | bug | `needs-triage` |
| "The export crashes on large files; I can reproduce it but don't know why." | bug | `needs-investigation` |
| "It crashes because the writer loads every row into memory; we'll stream it." | bug | `ready` |
| "Someone reports wrong dates, with no file attached." | bug | `needs-input`, waiting on the reporter |
| "We can't set the retention period until legal answers." | feature | `needs-input`, waiting on legal |
| "Dark mode would be nice someday." | feature | `parked` |
| "We need SSO this quarter but haven't designed it." | feature | `needs-investigation` |
| "SSO is specified." | feature | `ready` |
| "The staging database must move to the new server; it needs admin access." | chore | `ready`, assigned to the admin |
| "This is the crash reported in #42." | | Close as a duplicate of #42 |

## Title

- Bug: the symptom and where it shows. "Export crashes on files over 50 MB."
- Feature: what is true when it's done. "Enterprise customers sign in with SSO."
- Chore: the result, as a fact. "Staging runs on the new database server."

Never the fix, the issue number or a label: the tracker shows those beside the title.

## The description grows

File the issue with its kind's template: [bug](templates/bug.md), [feature](templates/feature.md), [chore](templates/chore.md). Fill what you know, and delete a section you have nothing for. A `needs-triage` issue may be free text.

Each later stage **appends** sections to the description and never rewrites earlier ones, so the description reads as what was known at each point. Discussion goes in comments.

| Moving to | Append |
|---|---|
| `parked` | `## Parked`: why not now, and what would make it a priority |
| `needs-input` | A **comment**, not the description: who it waits on, the stage to return to, what is settled so far, and specific questions. If it waits on someone other than the reporter, offer the user `/write-questionnaire` and link its file |
| `ready`, bug | `## Diagnosis`: the root cause, where it first goes wrong, and the check that goes red without the fix. Then `## Brief` |
| `ready`, feature | `## Plan`: the chosen approach, or a link to the spec. Then `## Brief` |
| `ready`, chore | `## Brief` |
| closed | A comment with the reason, then close it as `docs/agents/issue-tracker.md` says |

`## Brief` is the contract the builder works from: the desired behaviour, acceptance criteria as checkboxes, and what is out of scope. Describe behaviour and interfaces, not file paths, which go stale.

Change the stage label in the same step as the text, so the two always agree.

## Split into children

When a `ready` issue is too big for one change, keep it as the **parent** and split the work into child tickets with `/write-tickets`: native children of the parent (GitHub sub-issues, GitLab child tasks, files in the feature's `issues/` folder) with blocking links between them, never loose issues. Each child gets the parent's kind and `ready`. The parent stays open until its last child closes. `/implement-spec` then works the open, unblocked children in parallel.
