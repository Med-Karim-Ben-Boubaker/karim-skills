# Issue tracker: GitLab

Issues and specs for this repo live as GitLab issues. Use the [`glab`](https://gitlab.com/gitlab-org/cli) CLI for all operations.

## Conventions

- **Create an issue**: `glab issue create --title "..." --description "..."`. Use a heredoc for multi-line descriptions. Pass `--description -` to open an editor.
- **Read an issue**: `glab issue view <number> --comments`. Use `-F json` for machine-readable output.
- **List issues**: `glab issue list -O json` with appropriate `--label` filters.
- **Comment on an issue**: `glab issue note <number> --message "..."`. GitLab calls comments "notes".
- **Apply / remove labels**: `glab issue update <number> --label "..."` / `--unlabel "..."`. Multiple labels can be comma-separated or by repeating the flag.
- **Close**: `glab issue close <number>`. `glab issue close` does not accept a closing comment or reason, so post the explanation first (done or not planned, and why) with `glab issue note <number> --message "..."`, then close. For a duplicate, post `/duplicate #<original>` as a note instead: it links the original and closes the issue.
- **Merge requests**: GitLab calls PRs "merge requests". Use `glab mr create`, `glab mr view`, `glab mr note`, etc., the same shape as `gh pr ...` with `mr` in place of `pr` and `note`/`--message` in place of `comment`/`--body`.

Infer the repo from `git remote -v`; `glab` does this automatically when run inside a clone.

## Children and dependencies

GitLab issues can't have child issues; an issue's native children are **tasks**. Big work is one **parent** issue, the spec, with child tasks as its tickets and **blocking links** between them, so the ticket graph lives in GitLab and shows under the issue's Child items. Epics stay free for roadmap work.

- **Create a child**: create the task, then attach it to the parent with a quick action. `glab` has no flag for either. Create blockers first, so their numbers exist.

  ```bash
  iid=$(glab api -X POST "projects/:id/issues" -f title="..." -f description="..." -f issue_type=task -f labels="<kind>,<stage>" | jq .iid)
  glab issue note <parent> --message "/add_child #$iid"
  ```

- **Block**: `glab api -X POST "projects/:id/issues/<child>/links" -f target_project_id=<project id> -f target_issue_iid=<blocker> -f link_type=is_blocked_by`. Blocking links need Premium; on Free, start the child's description with `Blocked by: #<n>, #<n>`. The first time in a project, check the link shows under the task's Linked items.
- **List the children** (GraphQL only):

  ```bash
  glab api graphql -f query='query { project(fullPath: "<group>/<project>") { workItems(iids: ["<parent>"]) { nodes { widgets { ... on WorkItemWidgetHierarchy { children { nodes { iid state title assignees { nodes { username } } } } } } } } } }'
  ```

- **Open blockers of a child**: `glab api "projects/:id/issues/<child>/links" | jq '[.[] | select(.link_type == "is_blocked_by" and .state == "opened")] | length'` (0 means startable), or the open issues in its `Blocked by` line.
- **Frontier**: the open children with no assignee and 0 open blockers.
- **Claim**: `glab issue update <child> --assignee @me`, before any work.
- **Finish**: each child closes through the MR that merges it into the default branch (see **Merge requests**); close the parent as done after its last child.

## Explore

- **Project and issues enabled**: `glab api "projects/:id"` (`issues_enabled`).
- **Labels**: `glab api "projects/:id/labels?per_page=100"`, and the group's: `glab api "groups/<group>/labels?per_page=100"`.
- **Open issues and their labels**: `glab issue list -O json --per-page 100` (count by label; also work items of type task: `glab api "projects/:id/issues?issue_type=task&state=opened"`).
- **Templates**: `.gitlab/issue_templates/`, `.gitlab/merge_request_templates/`.
- **Planning**: milestones `glab api "groups/<group>/milestones?state=active"`, epics `glab api "groups/<group>/epics?state=opened"`, boards `glab api "projects/:id/boards"`.

## Create

- **New project**: `glab repo create <name> --private`, then `git remote add origin <url>` if it isn't set.
- **Issues off**: `glab api -X PUT "projects/:id" -f issues_enabled=true`.

## Labels

Kind and stage are **scoped labels** (`kind::bug`, `stage::ready`; the strings are under `### Issue labels` in `AGENTS.md` or `CLAUDE.md`). GitLab keeps one label per scope, so adding a stage replaces the old one: `glab issue update <n> --label "stage::ready"`. Scoped labels need GitLab Premium; on Free, remove the old stage in the same command with `--unlabel`.

- **Create a label**: `glab label create --name "kind::bug" --color "#d73a4a" --description "Something works wrong"`. When several projects in a group share the labels, create them on the group instead: `glab api -X POST groups/<group>/labels -f name="kind::bug" -f color="#d73a4a"`.
- **File an issue with its labels**: `glab issue create --title "..." --description "..." --label "kind::bug,stage::needs-triage"`.
- **List by stage**: `glab issue list --label "stage::ready"`.

## Issue templates

One Markdown file per kind in `.gitlab/issue_templates/`: `Bug.md`, `Feature.md`, `Chore.md`. GitLab offers them in the issue form's template menu. Each holds the kind's template body, then quick actions that set the labels when the issue is created:

```markdown
/label ~"kind::bug" ~"stage::needs-triage"
```

`glab issue create` does not apply templates: write the body from `/write-issue` and pass `--label`.

## Merge requests

- **Open**: `glab mr create --draft --title "..." --description "..." --target-branch <branch> --remove-source-branch --yes`, after the first push. The description starts with `Closes #<ticket>` lines (`Closes #12, #13` works); `/write-pr` writes the rest.
- **Ready**: `glab mr update <mr> --ready` once the evidence is in.
- **Upload a screenshot**: `glab api` can't send files, so use the API directly; the response's `markdown` field is the embed:

  ```bash
  curl -s --header "PRIVATE-TOKEN: $(glab config get token --host <host>)" --form "file=@after.png" "https://<host>/api/v4/projects/<url-encoded path>/uploads" | jq -r .markdown
  ```

- **Auto-close**: always write `Closes`, never `Fixes`, `Resolves` or `Implements`. GitLab closes every `Closes` ticket when the MR merges into the **default branch**, if the project setting *Auto-close referenced issues on default branch* is on (`glab api "projects/:id" | jq .autoclose_referenced_issues`). Merging into another branch, or closing the MR unmerged, closes nothing. Commits say `Refs #<n>`, so nothing closes early.
- **After the merge**: check each ticket with `glab issue view <n> -F json | jq .state`. Close any still `opened` as done with a note linking the MR (child tasks may not auto-close); close the parent after its last child.

## Merge requests as a triage surface

**MRs as a request surface: no.** _(Set to `yes` if this repo treats external merge requests as feature requests; `/triage` reads this flag.)_

When set to `yes`, MRs run through the same labels and states as issues, using the `glab mr` equivalents:

- **Read an MR**: `glab mr view <number> --comments` and `glab mr diff <number>` for the diff.
- **List external MRs for triage**: `glab mr list -O json`, then keep only MRs whose author is not a project member/owner (a contributor's MR, not a maintainer's in-flight work).
- **Comment / label / close**: `glab mr note`, `glab mr update --label`/`--unlabel`, `glab mr close`.

Unlike GitHub, GitLab numbers issues and MRs separately, so `#42` is unambiguous once you know which surface the maintainer means.

## When a skill says "publish to the issue tracker"

Create a GitLab issue.

## When a skill says "fetch the relevant ticket"

Run `glab issue view <number> --comments`.

## Wayfinding operations

Used by `/plan-large-work`. The **map** is a single issue with **child** issues as tickets.

- **Map**: a single issue labelled `wayfinder:map`, holding the Notes / Decisions-so-far / Fog body. `glab issue create --label wayfinder:map`. (On GitLab tiers with native epics, an epic may hold the map instead; a labelled issue works everywhere.)
- **Child ticket**: a child task of the map (see **Children and dependencies**), labelled `wayfinder:<type>` (`research`/`prototype`/`grilling`/`task`). Once claimed, the ticket is assigned to the driving dev.
- **Blocking**: see **Block** under **Children and dependencies**. A ticket is unblocked when every blocker is closed.
- **Frontier query**: list the map's children (see **List the children**), keep the open ones carrying a `wayfinder:<type>` label, and drop any with an open blocker or an assignee; first in map order wins.
- **Claim**: `glab issue update <n> --assignee @me`, the session's first write.
- **Resolve**: `glab issue note <n> --message "<answer>"`, then `glab issue close <n>`, then append a context pointer (gist + link) to the map's Decisions-so-far.
