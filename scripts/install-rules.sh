#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'USAGE'
Install the rules in rules/*.md for Claude Code and Codex.

  Claude Code: links each rule into ~/.claude/rules/ (or $CLAUDE_CONFIG_DIR/rules/).
  Codex:       writes all rules into one managed block in ~/.codex/AGENTS.md
               (or $CODEX_HOME/AGENTS.md); the rest of that file is left alone.

Rerun after pulling to pick up changed or new rules.

Usage: scripts/install-rules.sh [--claude] [--codex] [--remove] [--force] [--dry-run]

  --claude    only Claude Code
  --codex     only Codex
  --remove    uninstall: remove the links and the managed block
  --force     replace a rule file in ~/.claude/rules/ that is not one of our links
  --dry-run   print what would change, change nothing
USAGE
}

repo=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
rules_dir="$repo/rules"
claude_rules="${CLAUDE_CONFIG_DIR:-$HOME/.claude}/rules"
codex_agents="${CODEX_HOME:-$HOME/.codex}/AGENTS.md"
begin_marker="<!-- karim-skills rules: begin (managed by scripts/install-rules.sh; edits inside are overwritten) -->"
end_marker="<!-- karim-skills rules: end -->"

do_claude=0 do_codex=0 remove=0 force=0 dry_run=0
for arg in "$@"; do
  case "$arg" in
    --claude) do_claude=1 ;;
    --codex) do_codex=1 ;;
    --remove) remove=1 ;;
    --force) force=1 ;;
    --dry-run) dry_run=1 ;;
    -h|--help) usage; exit 0 ;;
    *) echo "unknown option: $arg" >&2; usage >&2; exit 2 ;;
  esac
done
if (( !do_claude && !do_codex )); then do_claude=1 do_codex=1; fi

run() {
  if (( dry_run )); then echo "would run: $*"; else "$@"; fi
}

shopt -s nullglob
rules=("$rules_dir"/*.md)
if (( ${#rules[@]} == 0 )); then echo "no rules in $rules_dir" >&2; exit 1; fi

install_claude() {
  run mkdir -p "$claude_rules"
  for rule in "${rules[@]}"; do
    target="$claude_rules/$(basename "$rule")"
    if [[ -L "$target" && "$(readlink -f "$target")" == "$(readlink -f "$rule")" ]]; then
      echo "claude: up to date  $target"
    elif [[ -e "$target" || -L "$target" ]] && (( !force )); then
      echo "claude: skipped     $target exists and is not ours (rerun with --force to replace)"
    else
      run ln -sfn "$rule" "$target"
      echo "claude: linked      $target"
    fi
  done
}

remove_claude() {
  for target in "$claude_rules"/*.md; do
    if [[ -L "$target" && "$(readlink -f "$target")" == "$rules_dir"/* ]]; then
      run rm "$target"
      echo "claude: removed     $target"
    fi
  done
}

strip_block() {
  awk -v b="$begin_marker" -v e="$end_marker" '
    $0 == b { skipping = 1; next }
    $0 == e { skipping = 0; next }
    !skipping { print }
  ' "$1"
}

write_codex() {
  local with_block=$1 tmp
  tmp=$(mktemp)
  if [[ -f "$codex_agents" ]]; then strip_block "$codex_agents" | sed -e :a -e '/^\n*$/{$d;N;ba' -e '}' > "$tmp"; fi
  if (( with_block )); then
    {
      [[ -s "$tmp" ]] && printf '\n'
      echo "$begin_marker"
      for rule in "${rules[@]}"; do printf '\n'; cat "$rule"; done
      printf '\n%s\n' "$end_marker"
    } >> "$tmp"
  fi
  if (( dry_run )); then
    echo "would write $codex_agents:"; diff -u "$codex_agents" "$tmp" 2>/dev/null || true
    rm "$tmp"
  else
    mkdir -p "$(dirname "$codex_agents")"
    mv "$tmp" "$codex_agents"
    echo "codex:  wrote       $codex_agents"
  fi
}

if (( do_claude )); then
  if (( remove )); then remove_claude; else install_claude; fi
fi
if (( do_codex )); then
  if (( remove )); then write_codex 0; else write_codex 1; fi
fi
