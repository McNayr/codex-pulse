# Release Checklist

Use this before publishing a public release.

## Required

- [ ] README explains what Pulse is in the first screen.
- [ ] `./bin/pulse` works from a fresh clone.
- [ ] `projects/example-app.md` points only to files that exist.
- [ ] `./scripts/new_project.sh test-project /tmp/test-project` works in a scratch path.
- [ ] `./scripts/self_test.sh` passes.
- [ ] GitHub Actions self-test passes after push.
- [ ] project examples are fictional.
- [ ] README credits external agent catalogs or tools that influenced the workflow.
- [ ] contributor docs explain how to validate first-run onboarding.
- [ ] scripts use relative paths derived from the repo root.
- [ ] no private project names or local machine paths remain.
- [ ] license exists.
- [ ] contribution guide exists.
- [ ] security/privacy guidance exists.

## Suggested Scan

```bash
rg -n "/home/|/Users/|C:\\\\Users|password|secret|token|credential|private key|customer|internal" .
```

Review matches manually. Guidance files may mention risky words; real private
material should not be present.

## Version

Recommended first tag:

```bash
git tag v0.1.0
```
