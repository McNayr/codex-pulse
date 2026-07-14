# Changelog

## Unreleased

- Added portable `scripts/startup_audit.py` for workspace-relative startup/source tier classification before broad root-doc reads.
- Added `integrations/adapters/TELEMETRY_FIXTURES.md` to document the sanitized adapter fixture contract for status modes, log-cost fixtures, and offline rate-limit snapshots.
- Added portable offline-only `scripts/rate_limit_snapshot.py` for captured/sanitized `codex.rate_limits` SSE/JSONL fixtures and usage-mode mapping without live stream capture or private auth reads.
- Added portable `scripts/log_cost_summary.py` for sanitized JSONL cost fixtures, repeated-operation evidence, timeout/failure counts, and token totals without reading private runtime logs.
- Added portable `scripts/status_policy.py` for adapter-provided usage/log signals without reading private auth, agent logs, or local machine paths.
- Added portable `scripts/session_checkpoint.py` for compact file-backed session handoffs during risky context windows or AFK closeout.
- Added portable `scripts/doc_index.py` for deterministic, workspace-relative markdown indexing/querying before broad document reads.
- Documented the portable `scripts/context_packet.py` startup packet in `README.md` and `START_HERE.md` so agents can orient compactly before broad file reads.

## 0.1.0

- Initial clean public scaffold.
- Added portable `./bin/pulse` startup command.
- Added `./scripts/new_project.sh` scaffold helper.
- Added startup, shutdown, workflow, drift, and agent guidance docs.
- Added fictional example project brief.
- Added complete fictional `examples/example-app` handoff pack.
- Added credit for the VoltAgent Codex subagent catalog.
- Added project handoff templates.
- Added self-test with portability and safety checks.
