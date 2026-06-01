# Contributing

Thanks for helping improve Codex Pulse.

Good contributions make sessions:

- easier to start
- easier to resume
- harder to drift
- safer around real systems
- clearer without getting bloated

## Rules

- Keep examples fictional.
- Do not add private customer or infrastructure details.
- Prefer small, readable docs over giant frameworks.
- Update templates when workflow expectations change.
- Keep scripts portable.

## Before Opening A PR

Run:

```bash
./scripts/self_test.sh
```

Then check for private material:

```bash
rg -n "/home/|customer|secret|token|password|private|internal" .
```
