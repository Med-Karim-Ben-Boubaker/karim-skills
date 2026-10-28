---
name: grill-me
description: "Stress-test the user's plan, decision, or idea with rounds of questions until every branch is settled."
argument-hint: "The plan, decision, or idea to grill"
disable-model-invocation: true
---

Before the first round, read the repo's domain docs: `GLOSSARY.md` (or the one `GLOSSARY-MAP.md` points to) and the ADRs in `docs/adr/` that touch the topic. Ground every question in them, and flag where the plan contradicts a recorded decision.

Then call the Skill tool with "grilling" and follow it. As each term or decision settles, call the Skill tool with "domain-modeling" to update `GLOSSARY.md`, or record a new ADR when the decision is hard to reverse.
