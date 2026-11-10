#!/usr/bin/env python3
"""Count skill loads, user commands, full test-suite runs and eval runs in Claude Code session logs."""
import argparse
import collections
import datetime
import glob
import json
import os
import re

FULL_SUITE = re.compile(r"(^|[;&|]\s*|\s)(make (test|check)\b|(uv run )?(python -m )?pytest(\s+-[a-zA-Z]+)*\s*($|[;&|>]))")
EVAL_RUN = re.compile(r"make (eval|eval-compare|e2e)\b|-m (tests\.e2e|evals?)\b|\be2e run\b|scripts/eval")
COMMAND = re.compile(r"<command-name>/?([^<]+)</command-name>")


def parse_time(value):
    try:
        return datetime.datetime.fromisoformat(value.replace("Z", "+00:00"))
    except (AttributeError, ValueError):
        return None


def short(name):
    return name.split(":", 1)[-1].lstrip("/")


def scan(projects_dir, since):
    loads, typed, runs, seconds = (collections.Counter() for _ in range(4))
    main = glob.glob(os.path.join(projects_dir, "*", "*.jsonl"))
    sub = glob.glob(os.path.join(projects_dir, "*", "*", "subagents", "*.jsonl"))
    for path in main + sub:
        where = "subagent" if "/subagents/" in path else "main"
        pending = {}
        for line in open(path, errors="replace"):
            try:
                entry = json.loads(line)
            except json.JSONDecodeError:
                continue
            when = parse_time(entry.get("timestamp") or "")
            if when is None or (since and when.date() < since):
                continue
            content = (entry.get("message") or {}).get("content")
            if entry.get("type") == "user" and isinstance(content, str):
                for name in COMMAND.findall(content):
                    typed[short(name)] += 1
            for block in content if isinstance(content, list) else []:
                if not isinstance(block, dict):
                    continue
                if block.get("type") == "text" and entry.get("type") == "user":
                    for name in COMMAND.findall(block.get("text", "")):
                        typed[short(name)] += 1
                elif block.get("type") == "tool_use" and block.get("name") == "Skill":
                    loads[(short(block["input"].get("skill", "")), where)] += 1
                elif block.get("type") == "tool_use" and block.get("name") == "Bash":
                    command = (block.get("input") or {}).get("command", "")
                    kind = "eval or e2e run" if EVAL_RUN.search(command) else "full test suite" if FULL_SUITE.search(command) else None
                    if kind:
                        pending[block["id"]] = (kind, when, (block.get("input") or {}).get("run_in_background"))
                elif block.get("type") == "tool_result" and block.get("tool_use_id") in pending:
                    kind, started, background = pending.pop(block["tool_use_id"])
                    runs[kind] += 1
                    if not background:
                        seconds[kind] += (when - started).total_seconds()
    return loads, typed, runs, seconds


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--since", type=datetime.date.fromisoformat, help="only count events on or after YYYY-MM-DD")
    parser.add_argument("--projects-dir", default=os.path.expanduser("~/.claude/projects"))
    parser.add_argument("--skills-dir", default=os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."),
                        help="the plugin's skills/ folder, to list skills never loaded")
    args = parser.parse_args()
    loads, typed, runs, seconds = scan(args.projects_dir, args.since)

    skills = sorted(d for d in os.listdir(args.skills_dir) if os.path.isfile(os.path.join(args.skills_dir, d, "SKILL.md")))
    print(f"{'skill':45} {'agent':>6} {'subagent':>9} {'typed':>6}")
    for name in skills:
        row = (loads[(name, "main")], loads[(name, "subagent")], typed[name])
        print(f"{name:45} {row[0]:>6} {row[1]:>9} {row[2]:>6}")
    unused = [n for n in skills if not (loads[(n, "main")] or loads[(n, "subagent")] or typed[n])]
    print(f"\nnever used: {len(unused)} of {len(skills)}: {', '.join(unused) or '-'}")
    for kind in ("full test suite", "eval or e2e run"):
        print(f"{kind}: {runs[kind]} runs, {seconds[kind] / 3600:.1f} h in the foreground")


if __name__ == "__main__":
    main()
