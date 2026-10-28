---
name: authoring-a-skill
description: "Playbook for writing or changing a skill, playbook, agent, or rule in this repo, or an AGENTS.md / CLAUDE.md. Use when the user wants a new skill, a skill changed, or a recurring correction turned into instructions."
---

# Authoring a skill

**You own the agent's next run.** Keep it simple: every line must change what the agent does. When in doubt, delete.

1. **Find its place.** A situation the agent works in → a playbook in `skills/playbooks/`. A capability playbooks call → a tool in `skills/tools/`. A rule of judgment → a principle. A subagent role → `agents/`. Always-on behaviour → `rules/`. Prefer changing an existing skill over adding one. *Done when:* the place is named and no existing skill already covers it.
2. **Write it.** Call the Skill tool with "writing-for-agents". Playbooks use numbered steps, each ending in *Done when:*, and a **Reply:** line. Point at other skills by name; don't restate them. A rule you're writing for the second time becomes a script or check instead (**principle-encode-lessons-in-structure**). *Done when:* the file is under about 25 lines, or the rest sits in `references/`.
3. **Check the links.** Run `python3 scripts/check-skills.py`. *Done when:* it exits 0.
4. **Install it.** Run `scripts/link-skills.sh`. *Done when:* the new name appears in `~/.claude/skills`.
5. **Try it.** For a structural change, run the skill once on a real task and read what the agent did. *Done when:* the run followed the steps, or `skip: wording-only change`.

**Reply:** what the skill does, where it lives, its key decisions, and the check output.
