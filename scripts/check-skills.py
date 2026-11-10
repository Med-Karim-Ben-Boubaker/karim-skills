#!/usr/bin/env python3
"""Check the skills repo: frontmatter, manifest, skill references, relative links and description budgets."""
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKILLS = os.path.join(ROOT, "skills")
MODEL_DESCRIPTION_MAX = 60
USER_DESCRIPTION_MAX = 45
MODEL_DESCRIPTION_TOTAL_MAX = 1200
REFERENCE = re.compile(r'Skill tool with [`"]([a-z0-9:-]+)[`"]|\b(principle-[a-z0-9-]+)\b')
LINK = re.compile(r"\]\(((?!https?:|#|mailto:)[^)\s]+)\)")
CODE = re.compile(r"```.*?```|`[^`\n]*`", re.S)


def frontmatter(text):
    if not text.startswith("---\n"):
        return None
    end = text.find("\n---", 4)
    return text[4:end] if end != -1 else None


def field(block, name):
    match = re.search(rf"^{name}:\s*(.*)$", block, re.M)
    return match.group(1).strip().strip('"') if match else None


def main():
    errors = []
    names = sorted(d for d in os.listdir(SKILLS) if os.path.isdir(os.path.join(SKILLS, d)))
    total_model_words = 0
    for name in names:
        path = os.path.join(SKILLS, name, "SKILL.md")
        if not os.path.isfile(path):
            errors.append(f"skills/{name}: no SKILL.md")
            continue
        block = frontmatter(open(path).read())
        if block is None:
            errors.append(f"skills/{name}/SKILL.md: no frontmatter")
            continue
        if field(block, "name") != name:
            errors.append(f"skills/{name}/SKILL.md: name is {field(block, 'name')!r}, folder is {name!r}")
        description = field(block, "description") or ""
        words = len(description.split())
        user_only = field(block, "disable-model-invocation") == "true"
        limit = USER_DESCRIPTION_MAX if user_only else MODEL_DESCRIPTION_MAX
        if not description:
            errors.append(f"skills/{name}/SKILL.md: no description")
        elif words > limit:
            errors.append(f"skills/{name}/SKILL.md: description has {words} words, budget {limit}")
        if not user_only:
            total_model_words += words
    if total_model_words > MODEL_DESCRIPTION_TOTAL_MAX:
        errors.append(f"model-invoked descriptions total {total_model_words} words, budget {MODEL_DESCRIPTION_TOTAL_MAX}")

    manifest = json.load(open(os.path.join(ROOT, ".claude-plugin", "plugin.json")))
    listed = {entry.rstrip("/").split("/")[-1] for entry in manifest.get("skills", [])}
    for name in sorted(set(names) - listed):
        errors.append(f".claude-plugin/plugin.json: skills/{name} is not listed")
    for name in sorted(listed - set(names)):
        errors.append(f".claude-plugin/plugin.json: lists missing skill {name}")
    codex = json.load(open(os.path.join(ROOT, ".codex-plugin", "plugin.json")))
    if codex.get("version") != manifest.get("version"):
        errors.append("plugin versions differ between .claude-plugin and .codex-plugin")

    for folder, _, files in os.walk(ROOT):
        if any(part in folder for part in ("/.git", "/resources", "/node_modules")):
            continue
        for file in files:
            if not file.endswith(".md"):
                continue
            path = os.path.join(folder, file)
            rel = os.path.relpath(path, ROOT)
            text = open(path, errors="replace").read()
            for match in REFERENCE.finditer(text):
                ref = (match.group(1) or match.group(2)).split(":")[-1]
                if ref.startswith("principle-") and ref not in names:
                    errors.append(f"{rel}: references missing skill {ref}")
                elif match.group(1) and ref not in names and ":" not in match.group(1):
                    errors.append(f"{rel}: calls missing skill {ref}")
            for target in LINK.findall(CODE.sub("", text)):
                target = target.split("#")[0]
                if target and not os.path.exists(os.path.normpath(os.path.join(folder, target))):
                    errors.append(f"{rel}: broken link {target}")

    for error in errors:
        print(f"error: {error}")
    print(f"{len(names)} skills, {total_model_words} model-invoked description words, {len(errors)} errors")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
