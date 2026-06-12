#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
FAIL=0

pass() { printf 'PASS: %s\n' "$1"; }
fail() { printf 'FAIL: %s\n' "$1"; FAIL=1; }

check_file() {
  if [ -f "$1" ]; then
    pass "file exists: $1"
  else
    fail "missing file: $1"
  fi
}

check_file "$ROOT/README.md"
check_file "$ROOT/START_HERE.md"
check_file "$ROOT/MISSION_BOARD.md"
check_file "$ROOT/WORKFLOW_RULES.md"
check_file "$ROOT/SESSION_STARTUP.md"
check_file "$ROOT/SESSION_SHUTDOWN.md"
check_file "$ROOT/DRIFT_DETECTION.md"
check_file "$ROOT/AGENT_GUIDE.md"
check_file "$ROOT/bin/pulse"
check_file "$ROOT/scripts/new_project.sh"
check_file "$ROOT/scripts/context_packet.py"
check_file "$ROOT/projects/example-app.md"
check_file "$ROOT/examples/example-app/README.md"
check_file "$ROOT/examples/example-app/CURRENT_STATE.md"
check_file "$ROOT/examples/example-app/SESSION_SAVE.md"
check_file "$ROOT/examples/example-app/TODO.md"
check_file "$ROOT/examples/example-app/CHRONOLOGY.md"
check_file "$ROOT/templates/PROJECT_BRIEF_TEMPLATE.md"
check_file "$ROOT/templates/CURRENT_STATE_TEMPLATE.md"
check_file "$ROOT/templates/SESSION_SAVE_TEMPLATE.md"
check_file "$ROOT/templates/TODO_TEMPLATE.md"
check_file "$ROOT/templates/CHRONOLOGY_TEMPLATE.md"
check_file "$ROOT/CONTRIBUTING.md"
check_file "$ROOT/SECURITY.md"
check_file "$ROOT/CHANGELOG.md"
check_file "$ROOT/RELEASE_CHECKLIST.md"
check_file "$ROOT/LICENSE"
check_file "$ROOT/AGENTS.md"
check_file "$ROOT/HERMES_COMPATIBILITY_PLAN.md"
check_file "$ROOT/integrations/hermes/README.md"
check_file "$ROOT/integrations/hermes/install_hermes_skill.sh"
check_file "$ROOT/integrations/hermes/skills/codex-pulse/SKILL.md"
check_file "$ROOT/integrations/messaging/SESSION_CONTINUITY.md"
check_file "$ROOT/integrations/messaging/CLI_LIKE_PROFILE.md"

if "$ROOT/bin/pulse" >/dev/null; then
  pass "pulse command executed"
else
  fail "pulse command failed"
fi

packet_output="$(python3 "$ROOT/scripts/context_packet.py" --workspace "$ROOT" --project example-app --format markdown 2>/dev/null || true)"
if printf '%s\n' "$packet_output" | rg -q 'Codex Pulse Context Packet'; then
  pass "context packet command executed"
else
  fail "context packet command failed"
fi
if printf '%s\n' "$packet_output" | rg -q 'projects/example-app.md'; then
  pass "context packet includes project brief pointer"
else
  fail "context packet missing project brief pointer"
fi
if printf '%s\n' "$packet_output" | rg -q '/home/'; then
  fail "context packet leaked private absolute path"
else
  pass "context packet avoids private absolute paths"
fi

if rg -q 'per-message event ids' "$ROOT/integrations/messaging/SESSION_CONTINUITY.md"; then
  pass "messaging continuity guide documents stable session keys"
else
  fail "messaging continuity guide missing stable session-key guidance"
fi
if rg -q 'Messenger CLI-like Profile' "$ROOT/integrations/messaging/CLI_LIKE_PROFILE.md" \
  && rg -q 'new topic' "$ROOT/integrations/messaging/CLI_LIKE_PROFILE.md" \
  && rg -q 'checkpoint' "$ROOT/integrations/messaging/CLI_LIKE_PROFILE.md"; then
  pass "messaging CLI-like profile documents mobile controls"
else
  fail "messaging CLI-like profile missing mobile controls"
fi

tmpdir="$(mktemp -d)"
self_test_name="pulse-self-test-$(basename "$tmpdir" | tr '[:upper:]' '[:lower:]' | tr -cd '[:alnum:]_-')"
self_test_brief="$ROOT/projects/$self_test_name.md"
created_self_test_brief=0
if [ -e "$self_test_brief" ]; then
  fail "self-test project brief collision: $self_test_brief"
fi
if "$ROOT/scripts/new_project.sh" "$self_test_name" "$tmpdir/test-project" >/dev/null; then
  created_self_test_brief=1
  pass "new_project command executed"
else
  fail "new_project command failed"
fi

check_file "$self_test_brief"
check_file "$tmpdir/test-project/CURRENT_STATE.md"
check_file "$tmpdir/test-project/SESSION_SAVE.md"
check_file "$tmpdir/test-project/TODO.md"
check_file "$tmpdir/test-project/CHRONOLOGY.md"
if [ "$created_self_test_brief" -eq 1 ]; then
  rm -f "$self_test_brief"
fi
rm -rf "$tmpdir"

overwrite_tmpdir="$(mktemp -d)"
overwrite_name="pulse-overwrite-test-$(basename "$overwrite_tmpdir" | tr '[:upper:]' '[:lower:]' | tr -cd '[:alnum:]_-')"
overwrite_brief="$ROOT/projects/$overwrite_name.md"
printf 'do not overwrite\n' > "$overwrite_tmpdir/CURRENT_STATE.md"
if [ -e "$overwrite_brief" ]; then
  fail "overwrite test project brief collision: $overwrite_brief"
elif "$ROOT/scripts/new_project.sh" "$overwrite_name" "$overwrite_tmpdir" >/dev/null 2>&1; then
  fail "new_project allowed overwrite"
  rm -f "$overwrite_brief"
else
  pass "new_project refuses to overwrite existing handoff files"
fi
if rg -q 'do not overwrite' "$overwrite_tmpdir/CURRENT_STATE.md"; then
  pass "overwrite guard preserved existing file"
else
  fail "overwrite guard did not preserve existing file"
fi
rm -rf "$overwrite_tmpdir"

if rg -n '/home/[[:alnum:]_-]+|/Users/[[:alnum:]_.-]+|C:\\Users\\[[:alnum:]_.-]+' "$ROOT" >/dev/null 2>&1; then
  fail "absolute user path scan matched"
else
  pass "absolute user path scan clean"
fi

if rg -n 'password|secret|credential|private key|access token' "$ROOT/projects" "$ROOT/templates" >/dev/null 2>&1; then
  fail "sensitive-word scan matched"
else
  pass "project/template sensitive-word scan clean"
fi

if [ "$FAIL" -ne 0 ]; then
  printf '\nCodex Pulse self-test: FAILED\n'
  exit 1
fi

printf '\nCodex Pulse self-test: PASSED\n'
