#!/usr/bin/env bash
set -euo pipefail

# Links every skill in skills/<group>/<name>/ into the local skill directories:
#   - ~/.claude/skills: Claude Code
#   - ~/.agents/skills: Codex and other Agent Skills-compatible harnesses
# Also links every subagent in agents/<name>.md into ~/.claude/agents, and
# every rule in rules/<name>.md into ~/.claude/rules.
# Each entry is a symlink into this repo, so edits here are live everywhere.
# Group folders are flattened, so skill names must be unique across the repo.

REPO="$(cd "$(dirname "$0")/.." && pwd)"
DESTS=("$HOME/.claude/skills" "$HOME/.agents/skills")

names=()
srcs=()
while IFS= read -r -d '' skill_md; do
  src="$(dirname "$skill_md")"
  names+=("$(basename "$src")")
  srcs+=("$src")
done < <(find "$REPO/skills" -name SKILL.md -not -path '*/deprecated/*' -print0)

dupes="$(printf '%s\n' "${names[@]}" | sort | uniq -d)"
if [ -n "$dupes" ]; then
  echo "error: duplicate skill names: $dupes" >&2
  exit 1
fi

for DEST in "${DESTS[@]}"; do
  # A DEST that resolves into this repo would write links back into skills/.
  if [ -L "$DEST" ]; then
    case "$(readlink -f "$DEST")" in
      "$REPO"|"$REPO"/*)
        echo "error: $DEST is a symlink into this repo. Remove it and re-run." >&2
        exit 1
        ;;
    esac
  fi

  mkdir -pv "$DEST"

  # Drop links into this repo whose skill was renamed or deleted.
  for link in "$DEST"/*; do
    if [ -L "$link" ] && [ ! -e "$link" ]; then
      case "$(readlink "$link")" in
        "$REPO"/*) rm -v "$link" ;;
      esac
    fi
  done

  for i in "${!names[@]}"; do
    target="$DEST/${names[$i]}"
    # Never delete a real skill folder installed by something else.
    if [ -e "$target" ] && [ ! -L "$target" ]; then
      echo "skip ${names[$i]}: $target is a real folder, not a link. Remove it yourself." >&2
      continue
    fi
    ln -sfnv "${srcs[$i]}" "$target"
  done
done

# Subagents and rules: Claude Code only. Each file in agents/ and rules/ is
# linked into ~/.claude/agents and ~/.claude/rules. Other harnesses get an
# agent's prompt from the skill that spawns it (see that skill's references/).
link_files() {
  local src_dir="$1" dest="$2" file target link
  mkdir -pv "$dest"
  for link in "$dest"/*; do
    if [ -L "$link" ] && [ ! -e "$link" ]; then
      case "$(readlink "$link")" in
        "$REPO"/*) rm -v "$link" ;;
      esac
    fi
  done
  for file in "$src_dir"/*.md; do
    [ -e "$file" ] || continue
    target="$dest/$(basename "$file")"
    if [ -e "$target" ] && [ ! -L "$target" ]; then
      echo "skip $(basename "$file"): $target is a real file, not a link. Remove it yourself." >&2
      continue
    fi
    ln -sfnv "$file" "$target"
  done
}

link_files "$REPO/agents" "$HOME/.claude/agents"
link_files "$REPO/rules" "$HOME/.claude/rules"
