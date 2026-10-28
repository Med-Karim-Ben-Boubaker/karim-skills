# Feature

New or changed **behaviour**. You own the design: shape first, then fill it in test by test.

## Process

### 1. Shape before logic

When the ticket touches a subsystem you haven't traced in this session, call the Skill tool with "how" over it first: naming a file isn't grounding.

Sketch the types, signatures, and module layout the ticket needs before writing any logic. Call the Skill tool with "principle-foundational-thinking": the data structures come first, and the dominant access paths decide them. Call the Skill tool with "principle-model-the-domain" for anything stateful: a state machine over scattered booleans, a table over branching. Call the Skill tool with "principle-type-system-discipline" so the compiler rejects the states the domain forbids.

If the repo has no build, test runner, or CI yet (the walking-skeleton ticket), that scaffold is this ticket's first commit.

### 2. Confirm the seam

Take the seam from the ticket. If the ticket has none, or the shape from step 1 doesn't fit it, call the Skill tool with "principle-deep-modules" and pick the highest interface where the behaviour is observable. State it before the first test.

### 3. Red → green at the seam

Call the Skill tool with "tdd" and build one vertical slice per cycle through that seam, driven by the ticket's acceptance criteria.

While filling in, call the Skill tool with "principle-boundary-discipline": parse external input into domain types at the edge and trust them inside. If the work adds a job, command, migration, or anything retried, call the Skill tool with "principle-make-operations-idempotent" and give it a test that runs it twice.

### 4. Verify on the real surface

Call the Skill tool with "principle-prove-it-works": run the feature the way its user would (the endpoint, the CLI, the page), read the actual output, and check every acceptance criterion against what you saw. Passing tests are evidence, not the verdict.

### 5. Land in small commits

Call the Skill tool with "principle-sequence-verifiable-units": scaffold or types, then each slice with its test, each commit green on its own.

## Anti-patterns

- **Logic before shape.** Writing branches before the types exist bakes the wrong shape in.
- **A seam chosen by the tests.** Reaching past the interface to make a test easy means the module is the wrong shape; fix the shape.
- **Speculative surface.** Options, flags, and extension points no acceptance criterion asks for.
