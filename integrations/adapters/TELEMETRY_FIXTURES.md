# Adapter Telemetry Fixtures

Codex Pulse can read compact telemetry fixtures, but it should not read live agent
accounts, private runtime logs, or machine-specific paths directly. Agent-specific
adapters are responsible for collecting their own runtime facts, removing local
identifiers, and writing replay-safe fixture files for Pulse scripts.

## Contract

Adapters may provide three fixture families:

1. **Status modes** for `scripts/status_policy.py`
   - Pass only normalized modes:
     - usage: `normal`, `caution`, `conserve`, `critical`, or `exhausted`
     - logs: `clean`, `watch`, or `critical`
   - Do not pass raw provider responses or local log excerpts.

2. **Cost summaries** for `scripts/log_cost_summary.py`
   - Write JSONL records with generic fields such as `key`, `input_tokens`,
     `output_tokens`, `tokens`, `duration_ms`, and `status`.
   - Keep `key` values generic, for example `startup`, `checkpoint`, or
     `index-query`.
   - Remove account ids, usernames, exact local paths, customer names, and raw
     prompts before handing fixtures to Pulse.

3. **Rate-limit snapshots** for `scripts/rate_limit_snapshot.py`
   - Write captured/sanitized `codex.rate_limits` SSE or JSONL events.
   - Use offline replay only. Pulse should not open live streams or require
     provider authentication for this helper.

## Example: status modes

```bash
python3 ./scripts/status_policy.py \
  --usage-mode normal \
  --log-risk watch \
  --format markdown
```

## Example: cost fixture

```jsonl
{"key":"startup","input_tokens":100,"output_tokens":25,"duration_ms":1200}
{"key":"startup","tokens":75,"duration_ms":800}
{"key":"checkpoint","input_tokens":120,"output_tokens":30,"duration_ms":1500,"status":"timeout"}
```

```bash
python3 ./scripts/log_cost_summary.py --jsonl sanitized-log-cost.jsonl --format markdown
```

## Example: rate-limit fixture

```text
event: codex.rate_limits
data: {"type":"codex.rate_limits","rate_limits":{"primary":{"used_percent":92,"window_minutes":300}}}
```

```bash
python3 ./scripts/rate_limit_snapshot.py --file sanitized-rate-events.sse --format markdown
```

## Safety checklist

Before committing or sharing adapter fixtures:

- Use workspace-relative or synthetic labels only.
- Remove raw prompts, user content, local absolute paths, and provider account
  identifiers.
- Prefer tiny fixtures that exercise behavior over large exported logs.
- Keep live collection code in the adapter, not in Pulse core scripts.
- Run `./scripts/self_test.sh` after changing fixture docs or helper scripts.
