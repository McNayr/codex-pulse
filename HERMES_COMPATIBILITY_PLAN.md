# Hermes Compatibility Plan

Status: implemented v0.1 adapter

Goal: make Codex Pulse usable from Hermes without breaking the normal Codex workflow.

## Summary

The best compatibility path is not a fork and not a rewrite.

Keep Codex Pulse as the shared, file-based operating layer, then add thin runtime adapters for each agent interface:

- Codex continues to use `Open Codex Pulse`, `./bin/pulse`, and the existing markdown control files.
- Hermes gets a native skill that teaches Hermes how to open and follow Pulse.
- Optional wrappers such as `bin/hermes-pulse` may help onboarding, but should not become a separate source of truth.

The shared contract should remain: written files first, project docs own project truth, chat memory is not durable state.

## Why This Works

Codex Pulse is already mostly agent-neutral in architecture:

- shell startup command prints the recovery map
- markdown files define session flow
- project briefs point to durable project state
- templates scaffold handoff packs
- self-test verifies basic structure

Hermes can operate on those same files with its file, terminal, search, memory, skills, session search, cron, and delegation toolsets. The missing piece is not capability; it is a Hermes-native instruction layer so Hermes knows when and how to run the Pulse ritual.

## Compatibility Principle

Separate these layers:

1. Core Pulse files: shared by every agent.
2. Runtime adapters: small files that explain how a specific agent should use Pulse.
3. Agent-specific power features: optional, never required for baseline resume.

Do not let Hermes-specific memory, Codex subagents, or provider-specific features become required for basic Pulse operation.

## Recommended Repository Shape

Add:

```text
integrations/
  hermes/
    README.md
    skills/
      codex-pulse/
        SKILL.md
    install_hermes_skill.sh
AGENTS.md
```

Optional later:

```text
bin/hermes-pulse
RUNTIME_COMPATIBILITY.md
```

## Hermes Skill Contract

Create a Hermes skill named `codex-pulse` or `pulse-session`.

Trigger cases:

- user says `Open Codex Pulse`
- user says `Open Pulse`
- user asks to resume a Pulse-tracked project
- user is working in a repo containing Pulse control files

Skill behavior:

1. Run `./bin/pulse` when available.
2. Read `START_HERE.md`, `MISSION_BOARD.md`, `WORKFLOW_RULES.md`, and `SESSION_STARTUP.md`.
3. Inspect `projects/*.md` briefs.
4. Summarize resume candidates compactly.
5. If no project is named, ask which project to resume.
6. Open the chosen project's source-of-truth files in this order:
   - `README.md`
   - `CURRENT_STATE.md` or `RESUME.md`
   - `SESSION_SAVE.md`
   - `TODO.md`
   - `CHRONOLOGY.md`
   - active runbook or plan
7. Keep only minimal active context once the next action is clear.
8. Before ending, follow `SESSION_SHUTDOWN.md` and update durable state if the session changed anything.

Hermes-specific notes:

- Use file tools for reading and patching docs.
- Use terminal only for commands/scripts/tests.
- Use Hermes memory only for stable preferences or reusable environment facts, not project state.
- Use Hermes skills for reusable procedures discovered from Pulse work.
- Use Hermes `todo` for current-session execution tracking, but keep durable project TODOs in project files.
- Use Hermes `delegate_task` for bounded parallel work only when the main session can verify results.
- Use Hermes cron only for scheduled Pulse checks if the prompt is self-contained and writes/verifies durable output.

## AGENTS.md Contract

Add a short `AGENTS.md` at the repo root so Codex, Hermes, and other coding agents get the same baseline rules when they inspect the repo.

It should say:

- This repo is a workflow/reference layer, not an app runtime.
- Do not duplicate project truth into Pulse when a project file can be linked.
- Keep examples fictional and sanitized.
- Run `./scripts/self_test.sh` after structural changes.
- Do not rename core files casually; startup depends on them.
- Keep adapter-specific guidance under `integrations/<agent>/`.

## Naming Recommendation

For compatibility, keep the public project name `Codex Pulse` for now.

Inside docs, gradually describe the architecture as an "agent session operating layer" rather than Codex-only. That keeps existing Codex users oriented while making the Hermes path natural.

Avoid a sudden rename to `Agent Pulse` until there is a real second adapter. The first Hermes integration can prove the abstraction before changing the brand.

## Implementation Order

### Phase 1: Non-breaking Hermes adapter

- Add `integrations/hermes/README.md`.
- Add `integrations/hermes/skills/codex-pulse/SKILL.md`.
- Add `integrations/hermes/install_hermes_skill.sh` that copies or symlinks the skill into `~/.hermes/skills/workflow/codex-pulse`.
- Add self-test checks that the Hermes skill files exist and contain the core startup phrase.
- Do not change existing Codex startup behavior.

### Phase 2: Agent-neutral baseline docs

- Add root `AGENTS.md`.
- Update README language from "Codex only" to "Codex-first, agent-compatible" in a few places.
- Keep the command `./bin/pulse` unchanged.
- Keep `Open Codex Pulse` supported.
- Add `Open Pulse` as an additional generic phrase.

### Phase 3: Optional Hermes ergonomics

- Add `bin/hermes-pulse` only if it provides value beyond `bin/pulse`.
- Add a Hermes quickstart section to README.
- Add a small example: `hermes -s codex-pulse` from a workspace containing Pulse.

### Phase 4: Advanced Hermes features, gated

Only after the basic adapter works:

- optional cron health checks for stale `CURRENT_STATE.md` files
- optional Hermes skill for project adoption/extraction workflow
- optional MCP integration if Pulse grows executable project-management tools

Do not start here. Advanced features should not be required for clean resume.

## First Draft Hermes Skill Skeleton

```markdown
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

Use this skill when the user says `Open Codex Pulse`, `Open Pulse`, asks to resume a Pulse-tracked project, or the current workspace contains Pulse files.

## Startup

1. If `./bin/pulse` exists, run it.
2. Read `START_HERE.md`, `MISSION_BOARD.md`, `WORKFLOW_RULES.md`, and `SESSION_STARTUP.md`.
3. Inspect `projects/*.md`.
4. Summarize likely resume candidates.
5. If the user did not name a project, ask what to resume.

## Project Resume

Open the selected project's source-of-truth files in this order: README, CURRENT_STATE or RESUME, SESSION_SAVE, TODO, CHRONOLOGY, active runbook/plan.

## Shutdown

Before ending after meaningful work, follow `SESSION_SHUTDOWN.md` and update durable files.

## Hermes Rules

Use Hermes memory only for stable preferences, not project state. Use durable Pulse/project docs as the source of truth.
```

## Risks

- Over-Hermes-ifying Pulse could make it less useful for Codex users.
- Importing Codex agent TOMLs into Hermes directly is the wrong path; translate high-value workflows into Hermes skills instead.
- Hermes persistent memory is useful, but project state should stay in files so Codex and Hermes remain cross-compatible.
- A second command or renamed project could confuse existing users if introduced before the adapter proves itself.

## Definition Of Done For Hermes Compatibility v0.1

- A fresh Hermes session can be told `Open Codex Pulse` and correctly follows the Pulse startup path.
- Existing Codex instructions still work unchanged.
- `./scripts/self_test.sh` passes.
- The Hermes skill is installable without private paths.
- No project state is stored only in Hermes memory.
- README documents both Codex-first usage and Hermes adapter usage.
