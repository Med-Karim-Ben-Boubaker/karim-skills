---
name: tickets
description: "Write work to the issue tracker as one parent ticket (the spec) and, when it needs more than one slice, child tickets with blocking edges. Use when a plan, conversation, or settled design must become buildable tickets."
user-invocable: false
---

# Tickets

A spec is just the **parent ticket**. Small work is one ticket; bigger work is a parent plus child tickets. The tracker is configured in `docs/agents/issue-tracker.md`; if not, call the Skill tool with "setup-repo" first. Use `GLOSSARY.md` terms and respect ADRs. No file paths or code snippets, except a prototype snippet that states a decision more precisely than prose.

1. **Write the parent** from [references/parent.md](references/parent.md). Don't interview: synthesize what's already settled. Every feature must earn its place, the rest goes to Out of Scope (**principle-experience-first**). Name the seams where the behaviour is tested, as few and as high as possible (**principle-test-behavior-not-implementation**). For changes to existing code, describe the design as if the requirement had always existed (**principle-redesign-from-first-principles**).
2. **Decide if it needs children.** One fresh agent session can build and verify it → publish the parent alone, with acceptance criteria. Otherwise continue.
3. **Cut tracer-bullet children** per [references/slicing.md](references/slicing.md): each a complete, verifiable path through every layer, sized for one session, with its seam and its blocking edges.
4. **Show the breakdown** as a numbered list (title, blocked by, what it delivers, seam) and ask: right granularity, right edges, merge or split anything? Iterate until approved.
5. **Publish** blockers first. Local tracker: one file per ticket under `.scratch/features/<slug>/issues/<NN>-<slug>.md`. Real tracker: one issue per child, as a sub-issue of the parent, with native blocking links where the tracker has them. Use [references/child.md](references/child.md). Never close or modify the parent after publishing.

Acceptance criteria are behaviour observable at the seam, never "function X exists".
