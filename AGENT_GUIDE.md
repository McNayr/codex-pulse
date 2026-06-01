# Agent Guide

Use agents deliberately.

## Default Pattern

1. Map the path.
2. Make the change.
3. Review the risk.
4. Update durable docs.

Not every task needs every phase.

## Good Uses

- one read-only mapper for unclear ownership
- one implementer for a bounded change
- one reviewer for risky or user-facing changes
- one documentation pass after settled work

## Anti-Patterns

- multiple agents answering the same question
- reviewers before there is something concrete to review
- broad vague prompts
- letting agent output replace project docs
- using a team when the main thread can safely do the work

## Integration Rule

The main Codex session owns final judgment.
