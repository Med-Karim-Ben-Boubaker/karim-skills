---
name: prototype
description: "Playbook for throwaway code that settles a design question: does this logic or state model hold up, what should this UI look like, will this library or approach work. Use for 'prototype', 'sketch it', 'spike', 'mock it up', or any fork running something would answer better than asking."
---

# Prototype

**You own the decision, not the code.** The prototype is thrown away. Speed beats polish: no tests, no abstractions, no persistence unless persistence is the question.

1. **Name the question.** One decision the prototype exists to make. *Done when:* the question is written. No question, no prototype: route to **feature**.
2. **Pick the branch.** Logic or state model → [references/logic.md](references/logic.md). Looks → [references/ui.md](references/ui.md). Library or approach → [references/spike.md](references/spike.md). If unclear, match the surrounding code and state the assumption. *Done when:* the branch is named.
3. **Build 2–3 real alternatives** (**principle-exhaust-the-design-space**), not flavours of one. Put it next to the code it's for, clearly named as a prototype, startable with one command. *Done when:* each variant runs and shows its full state.
4. **Observe** (**principle-prove-it-works**). *Done when:* the verdict comes from what you saw (output, screenshot, timing), not what you expected.
5. **Capture.** Commit to a throwaway `prototype/<question-slug>` branch, never merged; the message states the question and verdict. A hard-to-reverse choice gets an ADR via the "domain-modeling" skill. *Done when:* the branch exists and main holds only the decision.

**Reply:** the variants, the evidence, the tradeoffs, your recommendation, the branch name. Say plainly that it's throwaway.
