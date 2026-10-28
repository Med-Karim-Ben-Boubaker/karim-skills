#!/usr/bin/env python3
"""Check that the README.md files under a root form a connected blueprint tree.

Usage: check_readmes.py [ROOT] [--max-lines N]

Each README's parent is the README in its nearest ancestor folder, up to ROOT.
Errors (exit 1):
  - no Mermaid diagram
  - more than --max-lines lines outside Mermaid blocks
  - no up link to the parent README in the first 5 lines
  - a child README the parent does not link to
  - a child folder name missing from the parent's Mermaid diagrams
  - a relative link to a path that does not exist
Warnings: prose paragraphs longer than 3 sentences.

A README containing `<!-- blueprint: skip -->` is left out of the tree
(test fixtures, corpus notes, generated folders).
"""

import argparse
import re
import subprocess
import sys
from pathlib import Path

SKIP_DIRS = {"node_modules", "__pycache__", "venv", "dist", "build", "site-packages"}
SKIP_MARKER = "<!-- blueprint: skip -->"
LINK = re.compile(r"\[[^\]]*\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)")
SENTENCE_END = re.compile(r"[.!?](?:\s+(?=[A-Z0-9`*\[])|$)")


def find_readmes(root: Path) -> list[Path]:
    try:
        out = subprocess.run(
            ["git", "ls-files", "--cached", "--others", "--exclude-standard", "--", "*README.md"],
            cwd=root, capture_output=True, text=True, check=True,
        ).stdout
        paths = [root / p for p in out.splitlines()]
    except (subprocess.CalledProcessError, FileNotFoundError):
        paths = list(root.rglob("README.md"))
    return sorted(
        p.resolve() for p in paths
        if p.is_file()
        and not any(part.startswith(".") or part in SKIP_DIRS for part in p.relative_to(root).parts[:-1])
    )


def split_blocks(lines: list[str]) -> tuple[list[tuple[int, str]], list[str]]:
    """Return (prose lines with line numbers, Mermaid block texts); other code blocks are dropped."""
    prose, mermaid, block, fence = [], [], [], None
    for no, line in enumerate(lines, 1):
        stripped = line.strip()
        if fence is None and stripped.startswith("```"):
            fence = stripped[3:].strip() or "code"
            block = []
        elif fence is not None and stripped.startswith("```"):
            if fence == "mermaid":
                mermaid.append("\n".join(block))
            fence = None
        elif fence is not None:
            block.append(line)
        else:
            prose.append((no, line))
    return prose, mermaid


def paragraphs(prose: list[tuple[int, str]]):
    para, start = [], 0
    for no, line in prose + [(0, "")]:
        s = line.strip()
        is_text = s and not re.match(r"(#|[-*+] |\d+\. |\||>|<!--|↑)", s)
        if is_text:
            if not para:
                start = no
            para.append(s)
        elif para:
            yield start, " ".join(para)
            para = []


def links(prose: list[tuple[int, str]]):
    for no, line in prose:
        for target in LINK.findall(re.sub(r"`[^`]*`", "", line)):
            if not re.match(r"[a-z][a-z0-9+.-]*:|#", target):
                yield no, target.split("#")[0]


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("root", nargs="?", default=".")
    ap.add_argument("--max-lines", type=int, default=100)
    args = ap.parse_args()
    root = Path(args.root).resolve()

    docs = {}
    for path in find_readmes(root):
        text = path.read_text(encoding="utf-8")
        if SKIP_MARKER in text:
            continue
        lines = text.splitlines()
        prose, mermaid = split_blocks(lines)
        docs[path] = {"lines": lines, "prose": prose, "mermaid": mermaid}

    def parent_of(path: Path) -> Path | None:
        folder = path.parent
        while folder != root:
            folder = folder.parent
            if folder / "README.md" in docs:
                return folder / "README.md"
        return None

    errors, warnings = [], []

    def rel(p: Path) -> str:
        return str(p.relative_to(root))

    children: dict[Path, list[Path]] = {p: [] for p in docs}
    for path in docs:
        parent = parent_of(path)
        if parent:
            children[parent].append(path)

    for path, doc in docs.items():
        here = rel(path)
        linked = {(path.parent / t).resolve() for _, t in links(doc["prose"]) if t}

        if not doc["mermaid"]:
            errors.append(f"{here}:1: no Mermaid diagram")
        if len(doc["prose"]) > args.max_lines:
            errors.append(f"{here}:1: {len(doc['prose'])} lines outside diagrams (max {args.max_lines})")

        for no, target in links(doc["prose"]):
            if target and not (path.parent / target).exists():
                errors.append(f"{here}:{no}: broken link {target}")

        parent = parent_of(path)
        if parent:
            head = [(no, line) for no, line in doc["prose"] if no <= 5]
            if parent not in {(path.parent / t).resolve() for _, t in links(head) if t}:
                errors.append(f"{here}:1: no up link to {rel(parent)} in the first 5 lines")

        for child in children[path]:
            if child not in linked:
                errors.append(f"{here}:1: does not link child {rel(child)}")
            name = child.parent.name
            if not any(re.search(rf"\b{re.escape(name)}\b", m) for m in doc["mermaid"]):
                errors.append(f"{here}:1: child folder '{name}' missing from its diagrams")

        for start, para in paragraphs(doc["prose"]):
            count = len(SENTENCE_END.findall(para))
            if count > 3:
                warnings.append(f"{here}:{start}: paragraph has {count} sentences (max 3)")

    for line in errors:
        print(f"error: {line}")
    for line in warnings:
        print(f"warning: {line}")
    print(f"{len(docs)} READMEs, {len(errors)} errors, {len(warnings)} warnings")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
