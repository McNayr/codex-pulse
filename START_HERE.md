# Start Here

Use this order at the beginning of a Codex session:

1. Run `./bin/pulse`.
2. For a compact resume packet before broad reading, run:
   ```bash
   python3 ./scripts/context_packet.py --workspace . --format markdown
   ```
   Use `--project <brief-name>` when the user already named the project.
3. When you need deterministic local lookup before opening broad docs, run:
   ```bash
   python3 ./scripts/doc_index.py --workspace . --index .pulse-index.json "search terms" --format markdown
   ```
4. If an adapter has sanitized usage/log-risk signals, evaluate safe operating breadth:
   ```bash
   python3 ./scripts/status_policy.py --usage-mode normal --log-risk watch --format markdown
   ```
   Use the result to decide whether to checkpoint, avoid agent fan-out, or keep work normal.
5. If an adapter exported a sanitized cost fixture, summarize repeated operations and timeout/failure counts without reading private logs:
   ```bash
   python3 ./scripts/log_cost_summary.py --jsonl sanitized-log-cost.jsonl --format markdown
   ```
6. If an adapter exported captured/sanitized rate-limit events, summarize the latest offline snapshot without opening live streams:
   ```bash
   python3 ./scripts/rate_limit_snapshot.py --file sanitized-rate-events.sse --format markdown
   ```
7. To classify startup/source tiers before broad root-doc reads, run:
   ```bash
   python3 ./scripts/startup_audit.py --workspace . --format markdown
   ```
   Treat `root-policy` as policy-only, `registry` as packet input, `project-brief` as selected-brief, and `reference` as query-first.
8. For adapter fixture safety rules, open [`integrations/adapters/TELEMETRY_FIXTURES.md`](./integrations/adapters/TELEMETRY_FIXTURES.md) before adding new telemetry exports or examples.
9. If the session is near a risky context window, reboot, handoff, or AFK closeout, refresh a compact checkpoint:
   ```bash
   python3 ./scripts/session_checkpoint.py --target . --active-task "Current task" --next-step "Exact next action" --format markdown
   ```
   Add `--completed`, `--modified-file`, `--verification`, and `--next-file` flags when work changed durable state.
9. Open [MISSION_BOARD.md](./MISSION_BOARD.md).
10. Open [WORKFLOW_RULES.md](./WORKFLOW_RULES.md).
11. Inspect active project briefs under [`projects/`](./projects/).
12. Summarize likely resume candidates.
13. Ask what to resume, or whether to start something new, if the user did not
   already specify.
14. Open the chosen project's source-of-truth files:
   - `README.md`
   - `CURRENT_STATE.md` or `RESUME.md`
   - `SESSION_SAVE.md`
   - `TODO.md`
   - `CHRONOLOGY.md`
   - any active runbook
15. Before ending, follow [SESSION_SHUTDOWN.md](./SESSION_SHUTDOWN.md).

## Default Prompt

Tell Codex:

```text
Open Codex Pulse
```

Codex should orient from written files first, not chat memory.

## Add A Project

Use:

```bash
./scripts/new_project.sh my-app ../my-app
```

Then edit the generated brief and add the project to `MISSION_BOARD.md`.
