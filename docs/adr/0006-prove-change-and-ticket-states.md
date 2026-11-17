---
status: accepted
---

# The author proves each change; implement runs as ticket states

ADR 0003's Demo ran a fresh, blind sub-agent inside every `review-code`, with a `demo.sh` and a before and after run on two checkouts, and once more over every finished spec. It cost more than it caught, and it split one idea, "run the software and look at what it does", into two words (Demo and evidence). `implement` and `implement-spec` spread the process across prose steps, so an agent could not tell where it stood, and nothing stopped work without a ticket or in the main checkout.

**Decision.**

- **One proof.** A new skill, `prove-change`: for each acceptance criterion, the author runs the software as it is meant to run (locally, or on a dev environment the run recipe's **Deployed** section names), captures the output or a screenshot, looks at it, and marks it Proven, Failed or Unproven. A test run is never a proof. It runs in every ticket's Proving state; `write-pr` copies it into `## Proof`. `review-code` keeps two axes, Standards and Spec.
- **Ticket states.** `implement` is a state machine: Ready → Claimed → Building ⇄ Reviewing → Proving → Waiting → Merged → Done, each with what to do and when to leave. `implement-spec` runs those states per child inside spec states (Open → Running → Integrating → Waiting → Closed), straight to the default branch by default, through one feature branch when the spec says why.
- **Two guards, the rest guidance.** No implement without a ticket; never build in the main checkout: each ticket in its own worktree, from the base its intent decides (ADR 0005's GitFlow-lite table).

**Considered options:** keeping the blind checker as an on-request `demo` skill keeps two words for one idea; the author's own proof misses inputs the author never thought of, so a person who wants that check runs `/prove-change` from a fresh session.

**Revisit when:** a defect that running the software would have shown reaches the default branch with a Proven proof, or Proving takes longer than Building.
