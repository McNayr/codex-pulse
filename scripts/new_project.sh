#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

usage() {
  printf 'Usage: %s <project-name> <project-root>\n' "$(basename "$0")"
  printf 'Example: %s my-app ../my-app\n' "$(basename "$0")"
}

if [ "$#" -ne 2 ]; then
  usage
  exit 1
fi

name="$1"
project_root="$2"
slug="$(printf '%s' "$name" | tr '[:upper:] ' '[:lower:]-' | tr -cd '[:alnum:]-_')"

if [ -z "$slug" ]; then
  printf 'Project name must contain at least one letter, number, dash, or underscore.\n' >&2
  exit 1
fi

brief="$ROOT/projects/$slug.md"

if [ -e "$brief" ]; then
  printf 'Project brief already exists: %s\n' "$brief" >&2
  exit 1
fi

mkdir -p "$project_root"

cp "$ROOT/templates/PROJECT_BRIEF_TEMPLATE.md" "$brief"
cp "$ROOT/templates/CURRENT_STATE_TEMPLATE.md" "$project_root/CURRENT_STATE.md"
cp "$ROOT/templates/SESSION_SAVE_TEMPLATE.md" "$project_root/SESSION_SAVE.md"
cp "$ROOT/templates/TODO_TEMPLATE.md" "$project_root/TODO.md"
cp "$ROOT/templates/CHRONOLOGY_TEMPLATE.md" "$project_root/CHRONOLOGY.md"

printf '\nCreated Codex Pulse project scaffold\n'
printf '====================================\n\n'
printf 'Project brief:\n'
printf '  %s\n\n' "$brief"
printf 'Project files:\n'
printf '  %s\n' "$project_root/CURRENT_STATE.md"
printf '  %s\n' "$project_root/SESSION_SAVE.md"
printf '  %s\n' "$project_root/TODO.md"
printf '  %s\n\n' "$project_root/CHRONOLOGY.md"
printf 'Next:\n'
printf '  1. Edit %s\n' "$brief"
printf '  2. Add the project to %s\n' "$ROOT/MISSION_BOARD.md"
printf '  3. Run %s\n' "$ROOT/bin/pulse"
