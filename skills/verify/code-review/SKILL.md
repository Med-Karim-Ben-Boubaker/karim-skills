---
name: code-review
description: "Review the changes since a fixed point (commit, branch, tag, or merge-base) at four levels: gates (typecheck, lint, tests, build), behaviour (acceptance criteria run for real, regressions against the base, blast radius, whether the tests can fail), design (correctness, structure, complexity, security against the principles), and style (documented standards, code smells, comments). Runs each lane in an independent subagent, then judges the findings and returns a verdict. Use when the user wants to review a branch, a PR, work-in-progress changes, or asks to \"review since X\"."
---

Review the diff between `HEAD` and a fixed point at four levels. Each lane runs in a fresh subagent that didn't write the code, so its context isn't polluted by the author's intent or by the other lanes. You are the coordinator and the lead judge: you gather inputs, spawn the lanes, judge what comes back, and give the verdict. You never fix anything during a review.

The issue tracker should have been provided to you. If not, tell the user to run `/setup-repo`.

## 1. Pin the inputs

**Fixed point.** Whatever the user said (a SHA, branch, tag, `main`, `HEAD~5`). If they didn't say, ask. Confirm it resolves (`git rev-parse <fixed-point>`), capture the diff command once as `git diff <fixed-point>...HEAD` (three-dot, against the merge-base), the base SHA (`git merge-base <fixed-point> HEAD`), the head SHA, and `git log <fixed-point>..HEAD --oneline`. A bad ref or empty diff fails here, not inside the lanes.

**Spec.** Look for the originating spec or ticket, in this order: issue references in commit messages (fetched via the tracker doc), a path the user passed, a spec file under `docs/`, `specs/`, or `.scratch/features/` matching the branch. If none, ask; if there isn't one, the behaviour lane checks regressions and scope only.

**Intent.** One paragraph stating what the change is for, from the spec, commits, and PR description. Every lane gets it.

**Seams.** The seams the ticket or spec names. If none are named, say so; the behaviour lane picks the highest interface where the change is observable.

**Standards sources.** Every file that documents how code should be written. When `CODING_STANDARDS.md` or `CONTRIBUTING.md` exists, it must be on the list. Also `GLOSSARY.md`, the ADRs in the touched area, and the README of each touched folder: a diff that changes a folder's modules, interface, or data flow without updating its README is a style finding.

## 2. Level 0: gates

Run the repo's typecheck, lint, full test suite, and build yourself. When the repo's READMEs are blueprints (a README opens with an `↑` up link), also run the `blueprint` skill's `scripts/check_readmes.py` on the repo root. If any fails, stop: report the failing command and its output, verdict `FAIL`, and spawn no lanes. Reviewing code that doesn't pass its own gates wastes every lane.

## 3. Levels 1 to 3: spawn the lanes

Spawn every lane in one message so they run in parallel. Each is a registered agent: pass the inputs from step 1, never your own opinion of the change.

| Level | Lane | Agent (`subagent_type`) | Runs when |
|---|---|---|---|
| 1. Behaviour | Acceptance criteria run for real, regressions vs base, scope | `behavior-verifier` | Always |
| 1. Behaviour | What breaks outside the diff, the one safety fact proven | `blast-radius-reviewer` | Always |
| 1. Behaviour | Whether each new or changed test can fail | `test-auditor`, with `isolation: "worktree"` | The diff adds or changes tests |
| 2. Design | Correctness, root cause, structure, complexity, security, against the principles | `design-reviewer` | Always |
| 3. Style | Documented standards and the code-smell baseline | `standards-reviewer` | Always |
| 3. Style | Narration comments, suppressions, workaround code | `comment-sicko`, with `isolation: "worktree"` | Always |

`comment-sicko` deletes comments in its worktree: its deletions come back as a proposed patch, and its `MUST KILL` flags join the findings. Nothing lands on the reviewed branch.

When tests change, give `test-auditor` [principle-first-tests](../../principles/principle-first-tests/SKILL.md) to assess test feedback reliability. Review timing from available evidence; mark unknown timing as unknown.

If the diff adds new code paths but no tests, that's a behaviour finding in itself; don't spawn `test-auditor` to say so.

If a lane fails or returns nothing, respawn it once. A second miss is a gap in the report, never a pass.

## 4. Judge

Read [references/lead-judgment.md](references/lead-judgment.md), then:

1. **Merge** findings that describe the same issue across lanes. Note which lanes raised each; two lanes independently is the strongest signal.
2. **Check the doubtful ones yourself.** A hypothetical ("this could be null") stays only if you can trace a caller that triggers it. A reading-only claim about behaviour that the behaviour lane ran and saw working is checked against that lane's output.
3. **Bucket** every finding: **Act on**, **Consider**, **Noted**, or **Dismissed**, each with a one-line reason.
4. **Verdict per level**, then overall. Each level gets its own verdict so one level can't mask another: code that passes every standard but implements the wrong thing fails Behaviour, and code that does exactly what was asked but tangles the design fails Design.
   - `FAIL`: any **Act on** finding in that level, or a lane that was blocked or missing.
   - `PASS+NOTES`: only **Consider** findings.
   - `PASS`: nothing above **Noted**.

   The overall verdict is the worst level. It covers the head SHA it ran on, and nothing after.

## Output

```
## Verdict: PASS | PASS+NOTES | FAIL  (head <sha>)

| Level | Verdict | Lanes |
|---|---|---|
| 0. Gates | ... | typecheck, lint, tests, build |
| 1. Behaviour | ... | behavior-verifier, blast-radius-reviewer, test-auditor |
| 2. Design | ... | design-reviewer |
| 3. Style | ... | standards-reviewer, comment-sicko |

### Intent
### Act on        (each: finding, location, level, lanes that raised it, why it matters)
### Consider
### Noted
### Dismissed     (each with its reason)
### Gaps          (lanes blocked or missing, and what that leaves unchecked)
### Comment patch (comment-sicko's proposed deletions, as a diff or its worktree path)
```

Don't fix anything. Offer to apply the comment patch and to fix the **Act on** findings once the user has read the verdict.
