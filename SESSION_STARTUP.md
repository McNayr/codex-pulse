# Session Startup

Use this flow whenever you tell Codex to open Codex Pulse.

## Default Intake

If the user does not name a specific project, Codex should:

1. run `./bin/pulse` or read its output
2. open [MISSION_BOARD.md](./MISSION_BOARD.md)
3. open [WORKFLOW_RULES.md](./WORKFLOW_RULES.md)
4. inspect active project briefs
5. summarize likely resume candidates
6. ask which project to resume or whether to start something new

## Resume Existing Work

1. Open the chosen project brief in [`projects/`](./projects/).
2. Open the project's durable docs:
   - `CURRENT_STATE.md` or `RESUME.md`
   - `SESSION_SAVE.md`
   - `TODO.md`
   - `CHRONOLOGY.md`
   - active runbook or plan
3. State the current objective, blocker, and exact next action.
4. Then execute.

## Startup Rule

Never begin important work from chat memory alone.

Pulse first. Project state second. Execution third.
