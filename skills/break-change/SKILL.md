---
name: break-change
description: "QA pass that tries to make finished work fail: walks the fault checklist at each agreed seam, attacks it with worst-case, generated and oversized input and injected faults, and turns every break into a failing test. Use after building and before review, or when asked to QA, harden or break a change."
---

# Break Change

The author tested the user flow; this pass assumes the work breaks and finds where. It is QA, run like `diagnose-bug` without a bug to start from: each attack is a test that tries to go **red**. Whoever owns the work fixes each break through `tdd` (**After the report**).

## Steps

1. **Load the principle.** Call the Skill tool with `principle-test-what-breaks`, and read its `fault-checklist.md`. Done when both are in context.

2. **Read the work.** The diff since its base, the ticket's `## Brief` or the spec (its **Limits and Failure Modes** above all), and the tests that already exist for it. Done when you can list each seam the work touches, the input each seam receives, and the dependencies behind it.

3. **List the attacks.** For each seam, collect:
   - every applicable item of the fault checklist,
   - each limit of the **operating envelope**, at its boundary,
   - each failure mode the spec names, and each one it should have named,
   - **error guessing** from this code's past bugs: closed bug issues on the tracker that touch the same module, and `git log` of its fixes.

   Order the list the way exploratory testing walks it: functional flows first (the single flow, the **repeat flow** with the same input again, the **multi-user flow** with two at once), then failures and error handling, then cross-functional aspects (security, performance, privacy).

   Keep an attack only when the seam can really receive that input or meet that fault in production; an input no caller can produce is noise. Done when every checklist item is on the list or marked not applicable with its reason.

4. **Attack.** Write each attack as a test at its seam, FIRST (`tdd`): a fixture from the worst-case corpus, a synthetic input built at the boundary, a property-based test, a fake dependency that refuses or hangs, a fake clock, a count of calls through a fake. A property-based or fuzz test runs with a fixed seed and a bounded number of examples, so it stays repeatable. An attack that needs a real database or broker is a marked integration test. Run each one. Done when every attack has run.

5. **Sort each result.**
   - **Held**: it passes. Keep the test only when no existing test covers that case.
   - **Broke**: it fails. Keep the test red, and name the stated outcome it should reach. When the spec states none, the break is a question for the user, not a fix.
   - **Not run**: it needs full size or real infrastructure (a scale, soak or load test). Name the command or run-recipe step that would run it, and when.

   A break outside the work's scope is filed with `write-issue`.

6. **Report.** One table, one row per attack: seam, attack, result, and the test name or the reason. Then the breaks, each with its red test command and the outcome the fix must reach. Done when every attack from step 3 has a row.

## After the report

Run on your own work, fix each break now, red → green through `tdd`, fixing where it first went wrong (`principle-fix-root-causes`). Run as a subagent for `implement`, stop at the report: the author takes each break back to Building.
