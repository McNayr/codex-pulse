---
name: codex-pulse
description: Open and operate a Codex Pulse workspace from Hermes; follow Pulse startup, resume, and shutdown rules.
version: 0.1.0
author: Codex Pulse contributors
license: MIT
metadata:
  hermes:
    tags: [workflow, pulse, resume, project-state, codex-compatible]
---

# Codex Pulse for Hermes

Use this skill when the user says `Open Codex Pulse`, `Open Pulse`, asks to resume a Pulse-tracked project, or the current workspace contains Pulse control files.

Codex Pulse is a file-based session operating layer. Project truth belongs in project files, not chat memory and not Hermes memory.

## Startup

1. If `./bin/pulse` exists in the current Pulse repo, run it.
2. Read `START_HERE.md`, `MISSION_BOARD.md`, `WORKFLOW_RULES.md`, and `SESSION_STARTUP.md`.
3. Inspect `projects/*.md` for active project briefs.
4. Summarize likely resume candidates compactly.
5. If the user did not name a project, ask what to resume or whether to start something new.

## Project Resume

Open the selected project's source-of-truth files in this order:

1. `README.md`
2. `CURRENT_STATE.md` or `RESUME.md`
3. `SESSION_SAVE.md`
4. `TODO.md`
5. `CHRONOLOGY.md`
6. active runbook or plan, if referenced

Keep only the smallest useful active context once the next action is clear.

## Shutdown

Before ending after meaningful work:

1. follow `SESSION_SHUTDOWN.md`
2. update durable project/Pulse docs with changed state
3. record verification, blockers, changed files, and the exact next step

## Hermes Rules

- Use file tools for reading and patching docs.
- Use terminal only for commands, scripts, tests, git, and verification.
- Use Hermes memory only for stable preferences or reusable environment facts, not project state.
- Use Hermes skills for reusable procedures discovered from Pulse work.
- Use Hermes `todo` for current-session execution tracking, but keep durable TODOs in project files.
- Use Hermes `delegate_task` only for bounded parallel work whose output the main session can verify.
- Use Hermes cron only for scheduled Pulse checks when the prompt is self-contained and writes/verifies durable output.

## Safety

- Keep examples fictional and sanitized.
- Do not commit private local paths, credentials, customer data, or internal project names.
- Keep adapter-specific guidance under `integrations/hermes/`.
