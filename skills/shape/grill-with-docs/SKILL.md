---
name: grill-with-docs
description: A relentless interview to sharpen a plan or design, which also creates docs (ADR's and glossary) as we go.
disable-model-invocation: true
---

Call the Skill tool twice, for "grilling" and "domain-modeling".

Grill against the code, not just the idea. Before the first round, call the Skill tool with "how" over the area being touched. When the user's design contradicts what the code does, surface it, and call the Skill tool with "why" on that code before proposing to override it.

When the tree reaches system design, shape those branches with:

- **Module boundaries and interfaces**: call the Skill tool with "principle-deep-modules" to decide where the seam goes and keep modules deep.
- **Core types and data shapes**: call the Skill tool with "principle-foundational-thinking" to settle the data structures before any logic.
- **Fitting the change into what exists**: call the Skill tool with "principle-redesign-from-first-principles" to ask what you'd build if the requirement had always been there.
- **What crosses the edge of the system** (external APIs, config, user input): call the Skill tool with "principle-boundary-discipline" to decide where parsing and validation live.
- **Crashes, retries, and concurrent writers**: call the Skill tool with "principle-make-operations-idempotent" and "principle-separate-before-serializing-shared-state" to ask what happens on a rerun or a second writer.
- **An architecture with no precedent in the codebase**: call the Skill tool with "principle-exhaust-the-design-space", then "prototype" to compare 2 to 3 structurally different options.

Record each settled structural decision that passes the ADR bar inline, through domain-modeling, as it lands.
