---
status: accepted
---

# Six principles, core always on, wired into implement and review

Ten principle skills overlapped (the no-fallback rule lived in three of them, the no-comments keep-list in three) and no workflow skill or reviewer referenced them, so they loaded mostly when the user named them: 42% of skill loads followed the user typing the skill's name, three principles never loaded after the 10-30 rebuild, and over-engineering stayed the most repeated complaint (about 120 messages in 18 days). We merged them into six, put their core into the always-loaded `rules/engineering-defaults.md`, had `implement` and `implement-spec` load them before building, and turned them into `review-code`'s baseline checks.

**Considered Options:** keep ten and sharpen the descriptions (cheap, but descriptions were already the only route and didn't fire); the old playbook router that cited principles in every step (high usage, but heavy and dropped on 10-30 for complexity); merge and wire (chosen: one always-on core, depth loaded at fixed steps).

**Revisit when:** a retro (`skills/run-retro/skill-usage.py`) shows a principle unused for 30 days, or the same correction recurring in two sessions despite the rule.
