# Messenger CLI-like Profile

Use this profile when Hermes is reachable from Matrix/Telegram/Discord/SMS or any chat surface where short mobile messages should behave like a durable CLI session.

## Goals

- Stable conversation lane: normal top-level messages continue the current work lane instead of accidentally creating a fresh agent/session.
- Concise mobile output: result first, short bullets, expand only when asked.
- Explicit controls: make reset/checkpoint/status behavior intentional rather than implicit.
- Runaway prevention: tool-heavy phone turns should checkpoint or ask to continue before burning a large session budget.

## Recommended controls

- `continue`: keep working in the current durable messenger lane.
- `new topic`: intentionally start/reset a separate work lane.
- `checkpoint`: write a durable handoff before the thread gets large or the operator goes AFK.
- `status`: report compact session/usage state before broad rereads.

## Matrix-specific continuity check

If Matrix feels circular or expensive, compare recent sessions before changing project logic:

```bash
python -m hermes_bag.cli matrix-sessions --limit 8 --format markdown
```

Healthy behavior after the stable-lane fix:

- consecutive top-level Matrix messages update the same recent session
- batch/session keys are stable per user or room, not per event id
- short turns use a small number of API calls

## Runtime profile

The private Hermes bag implementation can stage the local profile with:

```bash
python -m hermes_bag.cli messenger-profile --env ~/.hermes/.env --apply --format markdown
```

Then restart the gateway so the environment is reloaded.

Public Pulse does not ship private credentials, service files, or platform-specific room ids; treat this document as the agent-neutral behavior contract.
