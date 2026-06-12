# Messaging Session Continuity

Use this note when an agent is reached through chat, SMS, Matrix, Discord, Slack, or another messenger and the conversation feels worse than the CLI: circular replies, repeated orientation, high token use, or separate answers that do not remember the prior phone message.

## Principle

Messenger adapters should preserve one durable conversation lane for the human unless the human explicitly opens a new thread/topic.

A mobile chat is not the same UX as a terminal, but it should not force a fresh agent session for every top-level message.

## Symptoms

- Short messages cause long re-orientation responses.
- The agent repeatedly asks what was already established.
- Usage/API calls climb faster over chat than over CLI.
- Each message appears as a separate thread, topic, or session in the adapter logs.
- A follow-up like "do that" does not refer to the previous chat turn.

## Checks

1. Identify the adapter's conversation key.
   - Prefer stable keys such as user id, room id, channel id, or explicit thread id.
   - Avoid per-message event ids as the default key.
2. Compare recent chat sessions.
   - A healthy follow-up should append to the same session or explicit thread.
   - A suspicious follow-up creates a new session with a new title for every short message.
3. Compare API/token shape.
   - Look for many small sessions with repeated startup/context costs.
   - Look for repeated project-doc reads that would be unnecessary inside one CLI session.
4. Keep encryption/privacy separate from continuity.
   - End-to-end encryption can work while session continuity is still broken.
   - Verify both independently.

## Recommended adapter defaults

- Use one stable conversation key per human+room/channel by default.
- Enable explicit thread/topic routing only when the user deliberately replies inside a thread/topic.
- Keep status pings and smoke tests quiet by default.
- Add a compact context/status command that shows session id, API calls, message count, and token totals for recent chat sessions.
- Document how to reset the chat session intentionally.

## Promotion boundary

This guidance is agent-neutral and contains no private paths, credentials, room ids, or provider-specific secrets. Project-specific diagnostics belong in the private project that discovered them; public Pulse should keep only the reusable pattern.
