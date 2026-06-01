# Workflow Rules

This is the short version of how Codex Pulse sessions should operate.

## Core Separation

- Pulse owns workflow.
- Project folders own project truth.
- Chat is execution, not durable memory.

## Session Rules

- Start from Pulse.
- Resume from project docs, not memory.
- Keep one clear current-state file per active project.
- Keep chronology append-only.
- End with a save/update pass.
- Re-check Pulse at decision points, not continuously.
- If drift triggers fire, stop implementing and realign before more changes.

## Documentation Rules

- README is the entrypoint, not the diary.
- Current state is present tense.
- Save files are exact restart instructions.
- TODO files hold next actions.
- Runbooks hold repeatable procedures.
- Decisions and lessons hold reusable project intelligence.
- Link instead of duplicating.

## Agent Rules

- Use agents for bounded parallel work.
- Keep the main thread responsible for integration.
- Map first, build second, review third.
- One agent per question.
- Use specialists for risk or depth, not because they exist.
- Promote important findings into durable docs.
