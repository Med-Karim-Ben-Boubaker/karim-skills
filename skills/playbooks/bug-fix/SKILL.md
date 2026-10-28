---
name: bug-fix
description: "Playbook for something broken, throwing, failing, or newly slow: reproduce, find the root cause with evidence, fix it test-first. Use when the user reports a bug or a regression, or says 'debug' or 'diagnose'."
---

# Bug fix

**You own the root cause.** Every line you ship traces to runtime evidence. A change that "might help" is a hypothesis, not a fix. Redact secrets in every command and output you show.

1. **Build a feedback loop.** This is most of the work. Follow [references/feedback-loop.md](references/feedback-loop.md). *Done when:* you have one command, already run, that goes red on the user's exact symptom, fast and deterministic. No loop, no step 2: don't theorize from reading code.
2. **Reproduce and minimise.** Cut inputs, config, and steps one at a time until every remaining piece is load-bearing. *Done when:* the loop shows the user's symptom (not a nearby one) and removing any piece makes it go green.
3. **Rank 3–5 hypotheses.** Seed them with the "how" skill over the area and, for a regression, the "why" skill on what changed. Each states a prediction: "if X is the cause, changing Y makes it disappear". Show the list to the user and continue without waiting. *Done when:* the list is written.
4. **Test them, one variable at a time.** Debugger first, then targeted logs tagged `[DEBUG-xxxx]`. For perf regressions, measure and bisect instead of logging. *Done when:* one hypothesis survives with runtime evidence (**principle-fix-root-causes**). Two failed fixes on one premise: test the premise (**principle-attack-the-premise**).
5. **Fix test-first.** Turn the minimal repro into a failing test at a seam that reproduces the real pattern (the "tdd" skill). Watch it fail, fix at the root, watch it pass, rerun the original loop. *Done when:* the failing test lands before the fix in history. If no correct seam exists, say so: that is a finding.
6. **Clean up and review.** Remove every `[DEBUG-` line (grep for it) and throwaway harnesses. Run the **review** playbook. *Done when:* grep finds nothing and review returned a verdict.

**Reply:** what was broken, the root cause, the fix, and the failing-then-passing loop output, verbatim.
