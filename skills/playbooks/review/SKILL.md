---
name: review
description: "Playbook for reviewing the changes since a fixed point (commit, branch, tag, PR): gates, then behaviour, tests, design, and style lanes in independent reviewers, then a judged verdict. Use to review a branch, a PR, or work in progress, or when another playbook hands off to review."
---

# Review

**You own the verdict, not the fix.** Each lane runs in a fresh `reviewer` agent that didn't write the code. You never fix anything during a review.

1. **Pin the inputs.** The fixed point (ask if not given); confirm it resolves. Capture `git diff <fixed-point>...HEAD`, the base SHA (`git merge-base`), and the head SHA. Find the spec or ticket (commit messages, the path given, `docs/`, `specs/`). Write one paragraph of intent. List the standards sources: `CODING_STANDARDS.md`, `CONTRIBUTING.md`, `AGENTS.md`, `CLAUDE.md`, `GLOSSARY.md`, ADRs and READMEs in touched folders. *Done when:* the diff is non-empty and every input is written down.
2. **Run the gates yourself.** Typecheck, lint, full tests, build. *Done when:* all pass. If any fails, stop: verdict `FAIL`, quote the failing command and output, spawn no lanes.
3. **Spawn the lanes in one message.** One `reviewer` agent per lane, each given its lane file and the inputs from step 1, never your opinion. *Done when:* every lane has reported; a lane that returns nothing is respawned once, and a second miss is a gap, not a pass.

   | Lane | File | Runs when |
   |---|---|---|
   | Behaviour | [references/behavior.md](references/behavior.md) | Always |
   | Tests | [references/tests.md](references/tests.md), `isolation: "worktree"` | Diff adds or changes tests |
   | Design | [references/design.md](references/design.md) | Always |
   | Style | [references/style.md](references/style.md), `isolation: "worktree"` | Always |

4. **Judge.** Read [references/judging.md](references/judging.md). Merge duplicates, check doubtful findings yourself, bucket each as **Act on**, **Consider**, **Noted**, or **Dismissed** with a one-line reason. *Done when:* every finding has a bucket.
5. **Give the verdict per level.** `FAIL` = any **Act on**, or a missing lane. `PASS+NOTES` = only **Consider**. `PASS` = nothing above **Noted**. Overall = the worst level, for the head SHA only.

**Reply:**

```
## Verdict: PASS | PASS+NOTES | FAIL  (head <sha>)
| Level | Verdict | Lanes |
### Intent
### Act on      (finding, location, lanes that raised it, why it matters)
### Consider
### Noted
### Dismissed   (with reason)
### Gaps
### Comment patch
```

Then offer to fix the **Act on** findings and apply the comment patch.
