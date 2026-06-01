# Drift Detection

Use this when implementation stops matching the expected source of truth.

## Trigger Conditions

Treat drift as real when:

- two changes in a row do not resolve the same issue
- visible behavior contradicts the current docs
- the session is still guessing after a second pass
- the same problem keeps reappearing under different fixes
- the live source of behavior is unclear

## Default Response

1. Stop making new changes.
2. Reopen the project brief and current-state file.
3. Reopen the exact code/config/docs path in question.
4. Map the real source of behavior.
5. Resume implementation only after the source and next action are clear.

## Practical Rule

Do not keep patching the symptom path.
