# Issue tracker: GitHub

Issues and specs for this repo live as GitHub issues. Use the `gh` CLI for all operations.

## Conventions

- **Create an issue**: `gh issue create --title "..." --body "..."`. Use a heredoc for multi-line bodies.
- **Read an issue**: `gh issue view <number> --json number,title,body,labels,comments`.
- **List issues**: `gh issue list --state open --json number,title,body,labels,comments --jq '[.[] | {number, title, body, labels: [.labels[].name], comments: [.comments[].body]}]'` with appropriate `--label` and `--state` filters.
- **Comment on an issue**: `gh issue comment <number> --body "..."`
- **Apply / remove labels**: `gh issue edit <number> --add-label "..."` / `--remove-label "..."`
- **Close**: post the explanation with `gh issue comment <number> --body "..."`, then `gh issue close <number> --reason completed` (done) or `--reason "not planned"`. For a duplicate, comment `Duplicate of #<original>` (GitHub marks the link), then close as not planned. On an already-closed issue, `gh issue close --comment` drops the comment and still exits 0.

Infer the repo from `git remote -v`; `gh` does this automatically when run inside a clone.

## Children and dependencies

Big work is one **parent** issue, the spec, with **sub-issues** as its tickets and native **issue dependencies** between them, so the ticket graph lives in GitHub and shows in its UI. Keep one level: parent → tickets.

- **Create a child**: `gh issue create --parent <parent> --blocked-by <n>,<n> --title "..." --body "..." --label "..."`. Create blockers first, so their numbers exist.
- **Attach an existing issue**: `gh issue edit <parent> --add-sub-issue <child>`.
- **Add a dependency later**: `gh issue edit <child> --add-blocked-by <blocker>`.
- **List the children**: `gh api repos/{owner}/{repo}/issues/<parent>/sub_issues --jq '.[] | {number, state, assignees: [.assignees[].login]}'`.
- **Open blockers of a child**: `gh api repos/{owner}/{repo}/issues/<child> --jq .issue_dependencies_summary.blocked_by` (open blockers only; 0 means startable).
- **Frontier**: the open children with no assignee and 0 open blockers.
- **Claim**: `gh issue edit <child> --add-assignee @me`, before any work.
- **Finish**: each child closes through its PR (`Closes #<child>`); close the parent as done after its last child.

## Explore

- **Repo and issues enabled**: `gh repo view --json nameWithOwner,hasIssuesEnabled`.
- **Labels**: `gh label list --limit 200 --json name,description`.
- **Open issues and their labels**: `gh issue list --state open --limit 500 --json number,labels` (count by label). Organisation issue types, if any: `gh api orgs/<org>/issue-types`.
- **Templates**: `.github/ISSUE_TEMPLATE/`, `.github/pull_request_template.md`.
- **Planning**: milestones `gh api repos/{owner}/{repo}/milestones`, projects `gh project list --owner <owner>`.

## Create

- **New repo**: `gh repo create <name> --private --source . --push`.
- **Issues off**: `gh repo edit --enable-issues`.

## Labels

GitHub has no scoped labels, so kind and stage are plain labels with a prefix (`kind: bug`, `stage: ready`; the strings are under `### Issue labels` in `AGENTS.md` or `CLAUDE.md`). GitHub allows several at once, so remove the old stage in the same command that adds the new one: `gh issue edit <n> --add-label "stage: ready" --remove-label "stage: needs-investigation"`.

- **Create a label**: `gh label create "kind: bug" --color d73a4a --description "Something works wrong" --force` (`--force` updates one that exists).
- **File an issue with its labels**: `gh issue create --title "..." --body "..." --label "kind: bug" --label "stage: needs-triage"`.
- **List by stage**: `gh issue list --label "stage: ready"`.

## Issue templates

One Markdown file per kind in `.github/ISSUE_TEMPLATE/`: `bug.md`, `feature.md`, `chore.md`. GitHub offers them when someone opens a new issue. Each holds the kind's template body under front matter that names it and sets the labels:

```markdown
---
name: Bug
about: Something works wrong
labels: ["kind: bug", "stage: needs-triage"]
---
```

`gh issue create --body` does not apply templates: write the body from `/write-issue` and pass `--label`.

File issues only into the user's own repo. Never file into the repo these skills come from unless the user owns it. In a fork, `gh` can default to the upstream parent, so before the first `gh issue create` of a session, check the target with `gh repo view --json nameWithOwner` and confirm it with the user if it is not their repo.

## Pull requests as a triage surface

**PRs as a request surface: no.** _(Set to `yes` if this repo treats external PRs as feature requests; `/triage` reads this flag.)_

When set to `yes`, PRs run through the same labels and states as issues, using the `gh pr` equivalents:

- **Read a PR**: `gh pr view <number>`, then `gh pr view <number> --comments` (off a TTY, `--comments` prints only the comments, not the body), and `gh pr diff <number>` for the diff.
- **List external PRs for triage**: `gh api --paginate 'repos/{owner}/{repo}/pulls?state=open' --jq '.[] | select(.author_association | IN("OWNER","MEMBER","COLLABORATOR") | not) | {number, title, author: .user.login, author_association, labels: [.labels[].name]}'`.
- **Comment / label / close**: `gh pr comment`, `gh pr edit --add-label`/`--remove-label`, `gh pr close`.

GitHub shares one number space across issues and PRs, so a bare `#42` may be either: resolve with `gh pr view 42` and fall back to `gh issue view 42`.

## When a skill says "publish to the issue tracker"

Create a GitHub issue.

## When a skill says "fetch the relevant ticket"

Read it as in **Read an issue** above.

## Wayfinding operations

Used by `/plan-large-work`. The **map** is a single issue with **child** issues as tickets.

- **Map**: a single issue labelled `wayfinder:map`, holding the Notes / Decisions-so-far / Fog body. `gh issue create --label wayfinder:map`.
- **Child ticket**: a sub-issue of the map (see **Children and dependencies**). Where sub-issues aren't enabled, add the child to a task list in the map body and put `Part of #<map>` at the top of the child body. Labels: `wayfinder:<type>` (`research`/`prototype`/`grilling`/`task`). Once claimed, the ticket is assigned to the driving dev.
- **Blocking**: see **Blocking** under Conventions.
- **Frontier query**: list the map's open children (`gh issue list --state open`, scoped to the map's sub-issues / task list), drop any with an open blocker (see **Children and dependencies**, or an open issue in the `Blocked by` line) or an assignee; first in map order wins.
- **Claim**: `gh issue edit <n> --add-assignee @me`, the session's first write.
- **Resolve**: `gh issue comment <n> --body "<answer>"`, then `gh issue close <n>`, then append a context pointer (gist + link) to the map's Decisions-so-far.
