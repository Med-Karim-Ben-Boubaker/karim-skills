---
name: investigation
description: "Playbook for a read-only question about existing code or decisions: how does X work, why is Y built this way, what could this change break, what causes this bug, should we do X or Y. Produces a cited answer, not a code change."
user-invocable: false
---

# Investigation

**You own the answer.** Read-only: no code changes. If the answer leads to a change, finish here and name the playbook that should follow.

1. **Pick the question type.** How it works → the "how" skill. Why it's shaped this way → the "why" skill. What a change could break → the "blast-radius" skill. Which option to choose → "how" over each option's area. The cause of a bug, without fixing it → steps 1–4 of the **bug-fix** playbook, then stop. *Done when:* the question and its type are written in one line.
2. **Run the skill.** *Done when:* every claim in the answer cites a `file:line`, a commit, a PR, or a doc. An empty search is reported as a finding.
3. **Separate fact from inference.** Mark each claim as read, measured, or inferred. *Done when:* nothing inferred is stated as fact.
4. **Judge.** For "should we" or "are we sure", give your real recommendation, and push back if the premise is wrong. *Done when:* the answer ends in a recommendation or `n/a: purely explanatory`.

**Reply:** the answer from the skill's output, with citations. For a decision, a tradeoffs table and your recommendation.
