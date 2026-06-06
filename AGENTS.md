# Agent Instructions

Codex Pulse is a workflow/reference layer, not an app runtime.

## Core rules

- Start from `START_HERE.md`, `MISSION_BOARD.md`, and `WORKFLOW_RULES.md`.
- Project folders own project truth; Pulse points to that truth and should not duplicate it unnecessarily.
- Keep examples fictional and sanitized.
- Do not rename core files casually; startup depends on them.
- Keep adapter-specific guidance under `integrations/<agent>/`.
- Run `./scripts/self_test.sh` after structural changes.

## Memory and state

- Chat history is not durable state.
- Session state belongs in `SESSION_SAVE.md` or the relevant project handoff file.
- Reusable lessons belong in durable project docs, not only in an agent's private memory.

## Safety

- Do not commit private local paths, credentials, customer data, or internal project names.
- Treat `projects/example-app.md` and `examples/example-app/` as fictional examples.
