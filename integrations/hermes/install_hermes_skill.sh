#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
SRC="$ROOT/integrations/hermes/skills/codex-pulse"
DEST="${HERMES_SKILLS_DIR:-$HOME/.hermes/skills/workflow}/codex-pulse"

if [ ! -f "$SRC/SKILL.md" ]; then
  printf 'ERROR: missing skill source: %s\n' "$SRC/SKILL.md" >&2
  exit 1
fi

mkdir -p "$(dirname "$DEST")"
rm -rf "$DEST"
cp -R "$SRC" "$DEST"

printf 'Installed Codex Pulse Hermes skill to %s\n' "$DEST"
printf 'In Hermes, load skill: codex-pulse\n'
