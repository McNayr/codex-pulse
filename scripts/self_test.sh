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
check_file "$ROOT/projects/example-app.md"
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

if "$ROOT/bin/pulse" >/dev/null; then
  pass "pulse command executed"
else
  fail "pulse command failed"
fi

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
