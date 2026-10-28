---
name: research
description: Investigate a question against high-trust primary sources and capture the findings as a Markdown file in the repo. Use when the user wants a topic researched, a new domain explored (processes, legal or medical terminology, standards), libraries compared, docs or API facts gathered, client requirements traced through the team's records, or reading legwork delegated to a background agent.
---

Spin up a background `explorer` agent to do the research, so you keep working while it reads.

For a broad question (a whole domain, "how does e-invoicing work in the EU", a library landscape), split it into 2 to 4 distinct angles and spawn one `explorer` per angle in a single message, then one `analyst` agent to synthesize their findings into the file. For a narrow question, one `explorer` does both. If you can't spawn agents (you are already a subagent), do the job yourself.

Its job:

1. Investigate the question against **primary sources**: official docs, source code, specs, standards, regulations, first-party APIs. When the question is about what the client or team said or decided, the team's own records are the primary source: query whatever connected MCPs hold them (issue tracker, docs, chat, email). Not a secondary write-up of any of these. Follow every claim back to the source that owns it. Call the Skill tool with "principle-prove-it-works" for what counts as checking the real thing.
2. Label every claim with its confidence, per [EPISTEMICS.md](EPISTEMICS.md), and cite its source.
3. When a finding is a number (a benchmark, a statistic, a legal threshold), call the Skill tool with "principle-explain-the-number" before writing it down.
4. Write the findings to `research/<topic>.md`, or match the repo's existing convention for such notes if it has one, and say where. End the file with **What we don't know**: each open question, the sources searched, and who or what could answer it.

When the question is why our own code or system is shaped the way it is, call the Skill tool with "why" instead: it reads the team's history (commits, PRs, tickets, chat) behind the code rather than outside sources.

When the findings resolve a domain term or settle a hard-to-reverse decision, call the Skill tool with "domain-modeling" to update `GLOSSARY.md` or record an ADR.
