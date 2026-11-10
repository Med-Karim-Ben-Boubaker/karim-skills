---
status: accepted
---

# Targeted tests while working, the full suite once, evals rarely

Agents ran the full test suite 622 times in 18 days (about 12 hours of waiting in the foreground, several runs per task) and ran 410 eval or e2e jobs, many with no prompt or model change behind them, while the user asked again and again for fewer, faster runs. We now run the narrowest test that can catch a change while working, the full suite and e2e once before a merge request is ready, and evals only when a person changed a prompt, model, model setting or tool and wants it measured. Code tests never call a model; evals are not tests. The rule lives in `principle-take-small-verified-steps`, `principle-let-models-judge`, `rules/engineering-defaults.md`, and in each repo's `### Checks` table written by `set-up-repo`.

Since 2026-11-10 the full suite runs only on the way into the default branch, in the merge request's pipeline where the repo has one. Work merged into an integration branch runs the tests of what it changed, once, and its merge requests start no pipeline: a pipeline on every merge queued parallel agents behind CI, and the branches that waited drifted into conflicts. Each merge request still carries its evidence and waits for the user's approval.

**Revisit when:** a defect reaches the default branch that only a full-suite run during the work would have caught, or a repo's full suite runs in under 30 seconds.
