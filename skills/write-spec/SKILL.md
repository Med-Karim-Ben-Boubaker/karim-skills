---
name: write-spec
description: "Turn the current conversation into a spec and publish it to the project issue tracker: no interview, just synthesis of what you've already discussed."
disable-model-invocation: true
---

This skill takes the current conversation context and codebase understanding and produces a spec. Do NOT interview the user; just synthesize what you already know.

The issue tracker (`docs/agents/issue-tracker.md`) and the repo's issue labels (`### Issue labels` in `AGENTS.md` or `CLAUDE.md`) should have been provided to you. If not, tell the user to run `/set-up-repo`.

## Process

1. Explore the repo to understand the current state of the codebase, if you haven't already. Use the project's domain glossary vocabulary throughout the spec, and respect any ADRs in the area you're touching.

2. Sketch out the seams at which you're going to test the feature. Use the test policy the repo already defines (`### Checks` in `AGENTS.md` or `CLAUDE.md`, and `CODING_STANDARDS.md`): its seams, fakes and fixtures. Existing seams should be preferred to new ones. Use the highest seam possible. If new seams are needed, propose them at the highest point you can. The fewer seams across the codebase, the better - the ideal number is one. Ask the user about seams only when the repo defines none.

   Code tests never call a model. Plan an eval only when the spec changes a prompt, model, model setting or tool, and say so in **Testing Decisions** (`principle-let-models-judge`).

3. Write the spec using the template below, then publish it to the project issue tracker. Label it with its kind (`feature`, or `bug` for a diagnosed bug) and the `ready` stage; it needs no triage. If the work started from an existing issue, link it from the spec and close it as a duplicate of the spec, so one open issue carries the work.

<spec-template>

## Problem Statement

The problem that the user is facing, from the user's perspective.

## Solution

The solution to the problem, from the user's perspective.

## User Stories

A LONG, numbered list of user stories. Each user story should be in the format of:

1. As an <actor>, I want a <feature>, so that <benefit>

Where the outcome could be read two ways, add one to three **declarative** Given / When / Then scenarios (BDD) in the user's words: the final picture, with no commands or UI steps.

<user-story-example>
1. As a mobile bank customer, I want to see balance on my accounts, so that I can make better informed decisions about my spending
   - Given a pending card payment, when I open my accounts, then I see the balance after it and the payment marked pending.
</user-story-example>

This list of user stories should be extremely extensive and cover all aspects of the feature.

## Implementation Decisions

A list of implementation decisions that were made. This can include:

- The modules that will be built/modified
- The interfaces of those modules that will be modified
- Technical clarifications from the developer
- Architectural decisions
- Schema changes
- API contracts
- Specific interactions
- The path to the default branch: each ticket on its own (the default), or one feature branch because the tickets are correct only together, and why

Do NOT include specific file paths or code snippets. They may end up being outdated very quickly.

Exception: if a prototype produced a snippet that encodes a decision more precisely than prose can (state machine, reducer, schema, type shape), inline it within the relevant decision and note briefly that it came from a prototype. Trim to the decision-rich parts, not a working demo, just the important bits.

## Limits and Failure Modes

What breaks, named before building (`principle-test-what-breaks`, **Spec**):

- **Operating envelope**: each limit with its number (input size, external caps, resource caps, time caps against the longest step), and the back-of-the-envelope estimate behind the concurrency
- **Worst real inputs**: the largest, strangest and most broken samples, and where they come from
- **Bad input**: the stated outcome for each kind (refused, scaled, quarantined, degraded)
- **Dependencies**: what the system does when each one refuses, hangs, answers garbage or slows down
- **Timing risks**: races and lag, and the design's answer to each
- **Abuser stories**, when the change takes outside input or touches auth, money or secrets

Take the numbers from the code, config, provider docs and the data itself. Write "none" under a heading that doesn't apply, with the reason; a limit you could not find is an open question in **Further Notes**, never "none".

## Testing Decisions

A list of testing decisions that were made. Include:

- A description of what makes a good test (only test external behavior, not implementation details)
- Which modules will be tested
- The robustness cases each limit and failure mode above gets, and whether a scale test runs before the first real run
- Prior art for the tests (i.e. similar types of tests in the codebase)
- Whether any eval runs at all: only if the spec changes a prompt, model, model setting or tool, with the smallest case set that answers the question

## Out of Scope

A description of the things that are out of scope for this spec.

## Further Notes

Any further notes about the feature.

</spec-template>
