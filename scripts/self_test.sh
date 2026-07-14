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
check_file "$ROOT/scripts/doc_index.py"
check_file "$ROOT/scripts/session_checkpoint.py"
check_file "$ROOT/scripts/status_policy.py"
check_file "$ROOT/scripts/log_cost_summary.py"
check_file "$ROOT/scripts/rate_limit_snapshot.py"
check_file "$ROOT/scripts/startup_audit.py"
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
check_file "$ROOT/integrations/adapters/TELEMETRY_FIXTURES.md"
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

index_output="$(python3 "$ROOT/scripts/doc_index.py" --workspace "$ROOT" --index "$ROOT/.pulse-test-index.json" "startup packet" --format markdown 2>/dev/null || true)"
rm -f "$ROOT/.pulse-test-index.json"
if printf '%s\n' "$index_output" | rg -q 'Codex Pulse Document Query'; then
  pass "document index query executed"
else
  fail "document index query failed"
fi
if printf '%s\n' "$index_output" | rg -q 'README.md|START_HERE.md|CHANGELOG.md'; then
  pass "document index query returned workspace-relative matches"
else
  fail "document index query missing expected matches"
fi
if printf '%s\n' "$index_output" | rg -q '/home/'; then
  fail "document index leaked private absolute path"
else
  pass "document index avoids private absolute paths"
fi

checkpoint_tmpdir="$(mktemp -d)"
checkpoint_output="$(python3 "$ROOT/scripts/session_checkpoint.py" \
  --target "$checkpoint_tmpdir" \
  --active-task "Self-test checkpoint" \
  --completed "Verified portable checkpoint writer" \
  --modified-file "scripts/session_checkpoint.py" \
  --verification "./scripts/self_test.sh" \
  --next-file "START_HERE.md" \
  --next-step "Open source-of-truth files before resuming" \
  --format markdown 2>/dev/null || true)"
checkpoint_file="$checkpoint_tmpdir/SESSION_CONTEXT_CHECKPOINT.md"
if [ -f "$checkpoint_file" ]; then
  pass "session checkpoint command wrote checkpoint"
else
  fail "session checkpoint command failed"
fi
if printf '%s\n' "$checkpoint_output" | rg -q 'Codex Pulse Session Checkpoint'; then
  pass "session checkpoint command emitted markdown summary"
else
  fail "session checkpoint command missing markdown summary"
fi
if [ -f "$checkpoint_file" ] && rg -q 'Self-test checkpoint' "$checkpoint_file" \
  && rg -q 'Verified portable checkpoint writer' "$checkpoint_file" \
  && rg -q 'Open source-of-truth files before resuming' "$checkpoint_file"; then
  pass "session checkpoint includes handoff fields"
else
  fail "session checkpoint missing handoff fields"
fi
if { printf '%s\n' "$checkpoint_output"; [ -f "$checkpoint_file" ] && cat "$checkpoint_file"; } | rg -q '/home/'; then
  fail "session checkpoint leaked private absolute path"
else
  pass "session checkpoint avoids private absolute paths"
fi
rm -rf "$checkpoint_tmpdir"

status_output="$(python3 "$ROOT/scripts/status_policy.py" --usage-mode normal --log-risk watch --format markdown 2>/dev/null || true)"
if printf '%s\n' "$status_output" | rg -q 'Codex Pulse Status Policy'; then
  pass "status policy command executed"
else
  fail "status policy command failed"
fi
if printf '%s\n' "$status_output" | rg -q 'Mode: CAUTION' \
  && printf '%s\n' "$status_output" | rg -q 'Max parallel agents: 3'; then
  pass "status policy maps normal usage and watched logs to caution"
else
  fail "status policy missing expected caution mapping"
fi
if printf '%s\n' "$status_output" | rg -q '/home/'; then
  fail "status policy leaked private absolute path"
else
  pass "status policy avoids private absolute paths"
fi

log_tmpdir="$(mktemp -d)"
log_fixture="$log_tmpdir/log-cost.jsonl"
printf '%s\n' \
  '{"key":"startup","input_tokens":100,"output_tokens":25,"duration_ms":1200}' \
  '{"key":"startup","tokens":75,"duration_ms":800}' \
  '{"key":"checkpoint","input_tokens":120,"output_tokens":30,"duration_ms":1500,"status":"timeout"}' \
  > "$log_fixture"
log_cost_output="$(python3 "$ROOT/scripts/log_cost_summary.py" --jsonl "$log_fixture" --format markdown 2>/dev/null || true)"
if printf '%s\n' "$log_cost_output" | rg -q 'Codex Pulse Log Cost Summary'; then
  pass "log cost summary command executed"
else
  fail "log cost summary command failed"
fi
if printf '%s\n' "$log_cost_output" | rg -q 'Total records: 3' \
  && printf '%s\n' "$log_cost_output" | rg -q 'Total tokens: 350' \
  && printf '%s\n' "$log_cost_output" | rg -q 'Timeout records: 1'; then
  pass "log cost summary totals sanitized fixture"
else
  fail "log cost summary missing expected totals"
fi
if printf '%s\n' "$log_cost_output" | rg -q 'startup: 2'; then
  pass "log cost summary reports repeated keys"
else
  fail "log cost summary missing repeated-key evidence"
fi
if printf '%s\n' "$log_cost_output" | rg -q '/home/'; then
  fail "log cost summary leaked private absolute path"
else
  pass "log cost summary avoids private absolute paths"
fi
rm -rf "$log_tmpdir"

rate_tmpdir="$(mktemp -d)"
rate_fixture="$rate_tmpdir/rate-events.sse"
printf '%s\n' \
  'event: codex.rate_limits' \
  'data: {"type":"codex.rate_limits","rate_limits":{"primary":{"used_percent":92,"window_minutes":300},"secondary":{"used_percent":25,"window_minutes":10080}},"info":{"plan_type":"plus"}}' \
  > "$rate_fixture"
rate_output="$(python3 "$ROOT/scripts/rate_limit_snapshot.py" --file "$rate_fixture" --format markdown 2>/dev/null || true)"
if printf '%s\n' "$rate_output" | rg -q 'Codex Pulse Rate Limit Snapshot'; then
  pass "rate limit snapshot command executed"
else
  fail "rate limit snapshot command failed"
fi
if printf '%s\n' "$rate_output" | rg -q 'Mode: CONSERVE' \
  && printf '%s\n' "$rate_output" | rg -q 'Most constrained remaining: 8.0%'; then
  pass "rate limit snapshot maps captured fixture to usage mode"
else
  fail "rate limit snapshot missing expected usage mapping"
fi
if printf '%s\n' "$rate_output" | rg -q '/home/'; then
  fail "rate limit snapshot leaked private absolute path"
else
  pass "rate limit snapshot avoids private absolute paths"
fi
rm -rf "$rate_tmpdir"

startup_audit_output="$(python3 "$ROOT/scripts/startup_audit.py" --workspace "$ROOT" --format markdown 2>/dev/null || true)"
if printf '%s\n' "$startup_audit_output" | rg -q 'Codex Pulse Startup Audit'; then
  pass "startup audit command executed"
else
  fail "startup audit command failed"
fi
if printf '%s\n' "$startup_audit_output" | rg -q 'START_HERE.md' \
  && printf '%s\n' "$startup_audit_output" | rg -q 'root-policy' \
  && printf '%s\n' "$startup_audit_output" | rg -q 'query-first'; then
  pass "startup audit reports source tiers"
else
  fail "startup audit missing source tier evidence"
fi
if printf '%s\n' "$startup_audit_output" | rg -q '/home/'; then
  fail "startup audit leaked private absolute path"
else
  pass "startup audit avoids private absolute paths"
fi

if rg -q 'Adapter Telemetry Fixtures' "$ROOT/integrations/adapters/TELEMETRY_FIXTURES.md" \
  && rg -q 'offline replay only' "$ROOT/integrations/adapters/TELEMETRY_FIXTURES.md" \
  && rg -q 'normalized modes' "$ROOT/integrations/adapters/TELEMETRY_FIXTURES.md"; then
  pass "adapter telemetry fixture contract documents safe exports"
else
  fail "adapter telemetry fixture contract missing safe-export guidance"
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
