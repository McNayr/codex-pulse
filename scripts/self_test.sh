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

if "$ROOT/bin/pulse" >/dev/null; then
  pass "pulse command executed"
else
  fail "pulse command failed"
fi

tmpdir="$(mktemp -d)"
self_test_name="pulse-self-test-$$"
self_test_brief="$ROOT/projects/$self_test_name.md"
if "$ROOT/scripts/new_project.sh" "$self_test_name" "$tmpdir/test-project" >/dev/null; then
  pass "new_project command executed"
else
  fail "new_project command failed"
fi

check_file "$self_test_brief"
check_file "$tmpdir/test-project/CURRENT_STATE.md"
check_file "$tmpdir/test-project/SESSION_SAVE.md"
check_file "$tmpdir/test-project/TODO.md"
check_file "$tmpdir/test-project/CHRONOLOGY.md"
rm -f "$self_test_brief"
rm -rf "$tmpdir"

overwrite_tmpdir="$(mktemp -d)"
printf 'do not overwrite\n' > "$overwrite_tmpdir/CURRENT_STATE.md"
if "$ROOT/scripts/new_project.sh" "pulse-overwrite-test-$$" "$overwrite_tmpdir" >/dev/null 2>&1; then
  fail "new_project allowed overwrite"
  rm -f "$ROOT/projects/pulse-overwrite-test-$$.md"
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
