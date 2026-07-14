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

## Messenger-specific continuity check

If a messenger lane feels circular or expensive, compare recent sessions before changing project logic. Adapter-specific diagnostics should answer:

- which stable user, room, channel, or thread key was used;
- whether consecutive top-level messages updated the same recent session;
- whether the adapter accidentally keyed sessions by per-message event id;
- whether short turns used a small number of API calls.

Healthy behavior:

- consecutive top-level messages update the same recent session;
- batch/session keys are stable per user or room, not per event id;
- short turns use a small number of API calls.

## Runtime profile

Adapter implementations can stage equivalent local settings in their own config,
then reload the adapter service if needed. Public Pulse does not ship private
credentials, service files, local config paths, or platform-specific room ids;
treat this document as the agent-neutral behavior contract.
