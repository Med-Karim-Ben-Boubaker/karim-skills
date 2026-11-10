# Split into child tickets

Break a spec, a plan or the conversation into **child tickets** of one parent: tracer-bullet vertical slices, each declaring the tickets that **block** it.

The issue tracker (`docs/agents/issue-tracker.md`) and the repo's issue labels (`### Issue labels` in `AGENTS.md` or `CLAUDE.md`) should have been provided to you. If not, tell the user to run `/set-up-repo`.

## 1. Gather context

Work from what is already in the conversation. If the user passes a reference (a spec path, an issue number or URL), fetch it and read its full body and comments.

If you have not explored the codebase yet, do so. Ticket titles and descriptions use the project's glossary vocabulary and respect ADRs in the area. Look for prefactoring that makes the implementation easier: "Make the change easy, then make the easy change."

## 2. Draft vertical slices

<vertical-slice-rules>

- Each slice cuts a narrow but COMPLETE path through every layer (schema, API, UI, tests): vertical, NOT a horizontal slice of one layer
- A completed slice is demoable or verifiable on its own
- Each slice fits one agent session in a fresh context window
- Any prefactoring comes first

</vertical-slice-rules>

**Use the fewest tickets that each verify on their own**: usually one per component or slice, listing its work as ordered, independently checkable items. Over-split work costs more coordination than it saves; one ticket for everything can't be verified step by step.

Give each ticket its **blocking edges**: the other tickets that must complete before it can start. A ticket with no blockers can start immediately.

**Wide refactors are the exception to vertical slicing.** A **wide refactor** is one mechanical change (rename a column, retype a shared symbol) whose **blast radius** fans across the whole codebase, so no vertical slice can land green. Sequence it as **expand–contract**: first expand, adding the new form beside the old so nothing breaks; then migrate the call sites in batches sized by blast radius (per package, per directory), each batch its own ticket blocked by the expand; finally contract, deleting the old form in a ticket blocked by every batch. When even the batches can't stay green alone, let them share an integration branch that all block a final integrate-and-verify ticket.

## 3. Show the breakdown once

Present the breakdown as a numbered list. For each ticket: **title**, **blocked by**, and **what it delivers** (the end-to-end behaviour it makes work). Ask one question: merge or split anything? Publish when the user agrees.

## 4. Publish as children of one parent

Publish the tickets as **children of one parent**, never as loose issues: the parent is the spec issue (or `spec.md` locally). If the source is not on the tracker yet, publish the spec as the parent first. Then follow **Children and dependencies** in `docs/agents/issue-tracker.md`:

- **GitHub**: each ticket a sub-issue of the parent, with native "blocked by" dependencies.
- **GitLab**: each ticket a child task of the parent, with blocking links (or a `Blocked by` line on Free).
- **Local files**: one file per ticket under `.scratch/<feature-slug>/issues/<NN>-<slug>.md`, with `blocked-by` in its front matter, from the template below.

Publish in dependency order (blockers first), so each blocking edge can reference a real identifier. Label each ticket with the parent's kind and the `ready` stage unless told otherwise. Don't close the parent or edit its description; only attach children to it.

<local-ticket-template>

---
kind: bug, feature or chore, from the parent
stage: ready
blocked-by: [the numbers of the tickets that gate this one, or empty]
---

# <NN>: <Ticket title>

## Brief

The end-to-end behaviour this ticket makes work, from the user's perspective, not a layer-by-layer implementation list.

- [ ] Acceptance criterion 1, as something a person can see by running the software
- [ ] Acceptance criterion 2

</local-ticket-template>

<issue-template>

## Brief

The end-to-end behaviour this ticket makes work, from the user's perspective, not layer-by-layer implementation.

- [ ] Criterion 1, as something a person can see by running the software
- [ ] Criterion 2

## Blocked by

- A reference to each blocking ticket, or "None (can start immediately)". Omit this section when blockers were set as native edges.

</issue-template>

In either form, avoid file paths and code snippets: they go stale fast. Exception: if a prototype produced a snippet that encodes a decision more precisely than prose can (state machine, reducer, schema, type shape), inline it and note that it came from a prototype.
