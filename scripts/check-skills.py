#!/usr/bin/env python3
"""Check that skills, playbooks, agents and rules form one connected, valid set.

Exits 1 and lists every problem when:
- a SKILL.md lacks a name or description, or its name differs from its folder;
- a skill sits in the wrong tier: skills/user/ must be user-only
  (`disable-model-invocation: true`), every other skill agent-only
  (`user-invocable: false`);
- a skill or agent named in any document does not exist;
- a document calls a user-only skill through the Skill tool;
- a relative Markdown link points to a missing file;
- a playbook step has no "Done when", or a playbook has no "Reply:" line;
- rules/playbooks.md and skills/playbooks/ list different playbooks;
- a playbook, tool, or principle is reachable from no user skill.
"""

import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
SKILLS = REPO / "skills"
AGENTS = REPO / "agents"
RULES = REPO / "rules"

SKILL_REF = [
    re.compile(r'Skill tool with "([a-z0-9-]+)"'),
    re.compile(r'Skill tool (?:twice|with), for "([a-z0-9-]+)"'),
    re.compile(r'the "([a-z0-9-]+)" skill'),
    re.compile(r'\*\*([a-z0-9-]+)\*\* playbook'),
    re.compile(r'\*\*(principle-[a-z0-9-]+)\*\*'),
    re.compile(r'"(feature|refactoring|perf)" for'),
    re.compile(r'\| \*\*([a-z-]+)\*\* \|$', re.M),
]
AGENT_REF = re.compile(r'`([a-z-]+)` agents?\b')
LINK = re.compile(r'\]\(([^)#\s]+)(?:#[^)]*)?\)')
PLACEHOLDERS = {"url", "link", "..."}
STEP = re.compile(r'^\s{0,3}\d+\. \*\*')


def frontmatter(text):
    m = re.match(r"---\n(.*?)\n---\n", text, re.S)
    if not m:
        return {}
    fields = {}
    for line in m.group(1).splitlines():
        if ":" in line and not line.startswith(" "):
            key, value = line.split(":", 1)
            fields[key.strip()] = value.strip().strip('"')
    return fields


def main():
    errors = []
    skills = {}
    for path in sorted(SKILLS.rglob("SKILL.md")):
        folder = path.parent
        meta = frontmatter(path.read_text())
        name = meta.get("name")
        if not name or not meta.get("description"):
            errors.append(f"{path.relative_to(REPO)}: missing name or description")
            continue
        if name != folder.name:
            errors.append(f"{path.relative_to(REPO)}: name '{name}' differs from folder '{folder.name}'")
        if name in skills:
            errors.append(f"duplicate skill name '{name}'")
        kind = folder.relative_to(SKILLS).parts[0]
        user_only = meta.get("disable-model-invocation") == "true"
        agent_only = meta.get("user-invocable") == "false"
        if kind == "user" and (not user_only or agent_only):
            errors.append(f"{path.relative_to(REPO)}: user skill must set only disable-model-invocation: true")
        if kind != "user" and (user_only or not agent_only):
            errors.append(f"{path.relative_to(REPO)}: {kind} skill must set only user-invocable: false")
        skills[name] = {"folder": folder, "kind": kind, "user_only": user_only}
    agents = {p.stem for p in AGENTS.glob("*.md")}

    docs = [p for p in REPO.glob("skills/**/*.md")] + list(AGENTS.glob("*.md")) + list(RULES.glob("*.md"))
    edges = {name: set() for name in skills}
    for doc in docs:
        text = doc.read_text()
        prose = re.sub(r"```.*?```", "", text, flags=re.S)
        prose = re.sub(r"`[^`\n]*`", "", prose)
        rel = doc.relative_to(REPO)
        owner = next((n for n, s in skills.items() if s["folder"] in doc.parents), None)
        for pattern in SKILL_REF:
            for ref in pattern.findall(text):
                if ref not in skills:
                    errors.append(f"{rel}: unknown skill '{ref}'")
                elif owner:
                    edges[owner].add(ref)
        for ref in AGENT_REF.findall(text):
            if ref not in agents and ref not in skills:
                errors.append(f"{rel}: unknown agent '{ref}'")
        for ref in SKILL_REF[0].findall(text):
            if ref in skills and skills[ref]["user_only"]:
                errors.append(f"{rel}: calls user-only skill '{ref}' (disable-model-invocation blocks it)")
        for target in LINK.findall(prose):
            if re.match(r"[a-z]+:", target) or target.startswith("<") or target in PLACEHOLDERS:
                continue
            if not (doc.parent / target).exists():
                errors.append(f"{rel}: broken link '{target}'")

    playbooks = {n for n, s in skills.items() if s["kind"] == "playbooks"}
    for name in sorted(playbooks):
        path = skills[name]["folder"] / "SKILL.md"
        lines = path.read_text().splitlines()
        if not any(line.startswith("**Reply:**") for line in lines):
            errors.append(f"{path.relative_to(REPO)}: no '**Reply:**' line")
        for i, line in enumerate(lines):
            if STEP.match(line) and "Done when" not in line:
                errors.append(f"{path.relative_to(REPO)}:{i + 1}: step has no 'Done when'")

    rule = (RULES / "playbooks.md").read_text()
    listed = set(re.findall(r"^\| ([a-z-]+) \|", rule, re.M)) - {"Playbook"}
    for name in sorted(playbooks - listed):
        errors.append(f"rules/playbooks.md: playbook '{name}' missing from the table")
    for name in sorted(listed - playbooks):
        errors.append(f"rules/playbooks.md: '{name}' is not a playbook")

    roots = {n for n, s in skills.items() if s["kind"] == "user"}
    reached, frontier = set(roots), list(roots)
    while frontier:
        for ref in edges[frontier.pop()]:
            if ref not in reached:
                reached.add(ref)
                frontier.append(ref)
    for name, skill in sorted(skills.items()):
        if name not in reached:
            errors.append(f"skill '{name}' is reachable from no user skill")

    for error in errors:
        print(error)
    print(f"{len(skills)} skills ({len(roots)} user, {len(playbooks)} playbooks), {len(agents)} agents: "
          f"{len(errors)} problem(s)")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
