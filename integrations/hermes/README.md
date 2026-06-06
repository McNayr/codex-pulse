# Hermes Integration

This adapter makes Codex Pulse usable from Hermes without changing the Codex-first startup path.

Pulse remains the shared source of truth:

- core workflow files stay at the repository root
- project briefs stay under `projects/`
- project folders own their own state
- Hermes-specific behavior stays in `integrations/hermes/`

## Install the Hermes skill

From a clone of Codex Pulse:

```bash
./integrations/hermes/install_hermes_skill.sh
```

The installer copies the skill to:

```text
~/.hermes/skills/workflow/codex-pulse
```

Then a Hermes session can load the skill when the user says:

```text
Open Codex Pulse
```

or:

```text
Open Pulse
```

## What the skill does

The skill teaches Hermes to:

1. run `./bin/pulse` when available
2. read `START_HERE.md`, `MISSION_BOARD.md`, `WORKFLOW_RULES.md`, and `SESSION_STARTUP.md`
3. inspect `projects/*.md`
4. summarize resume candidates compactly
5. ask what to resume when no project is named
6. open the selected project's source-of-truth files in the normal Pulse order
7. update durable state before shutdown after meaningful work

## Compatibility rules

- Do not require Hermes for baseline Pulse usage.
- Do not store project state only in Hermes memory.
- Do not make private local paths part of public Pulse docs.
- Keep advanced Hermes features optional.
