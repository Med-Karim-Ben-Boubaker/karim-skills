# Lane: behaviour

Check what the change does, by running it.

1. **Acceptance criteria.** For each criterion in the spec, drive the code through its seam the way a user would (endpoint, CLI, public function, page). Record the command and what it printed. A criterion that only looks implemented from reading is `UNVERIFIED`, never a pass.
2. **Regression against the base.** Pick the scenarios the diff could disturb, including ones the spec doesn't mention. Run each at the base (`git worktree add <scratch> <base-sha>`) and at the head, and compare. An unasked behaviour change is a finding, even if it looks like an improvement.
3. **Blast radius.** Call the Skill tool with "blast-radius" over the diff: what breaks outside it, and the one fact the change is safe because of, proven by running code.
4. **Scope.** Requirements missing or partial; behaviour nobody asked for. Quote the spec line for each.

Call the Skill tool with "how" first if you don't know the area well enough to pick scenarios.

```
Verdict: PASS | PASS+NOTES | FAIL | BLOCKED
Criteria:
- <criterion>: PASS | FAIL | UNVERIFIED | BLOCKED: <command> → <observed>
Regression: <scenario>: same | differs: <how>
Safety fact: <fact>: proven (<how>) | unproven
Risks: <risk> at file:line
Scope: missing: ... / unasked: ...
```
