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
- Update examples when onboarding behavior changes.
- Keep scripts portable.

## What Good PRs Usually Include

- a clear workflow improvement
- matching template/example updates when behavior changes
- self-test coverage for new scripts or required files
- no private project details
- docs that explain the user outcome, not only the mechanism

## Validation

For onboarding changes, test the first-run path:

1. run `./bin/pulse`
2. inspect `MISSION_BOARD.md`
3. open `projects/example-app.md`
4. confirm every referenced example file exists
5. run `./scripts/new_project.sh scratch-project /tmp/scratch-project`
6. run `./scripts/self_test.sh`

## Before Opening A PR

Run:

```bash
./scripts/self_test.sh
```

Then check for private material:

```bash
rg -n "/home/|customer|secret|token|password|private|internal" .
```
