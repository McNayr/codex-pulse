# Release Checklist

Use this before publishing a public release.

## v0.1.0 Status

Released: `v0.1.0`

- [x] README explains what Pulse is in the first screen.
- [x] `./bin/pulse` works from a fresh clone.
- [x] `projects/example-app.md` points only to files that exist.
- [x] `./scripts/new_project.sh test-project /tmp/test-project` works in a scratch path.
- [x] `./scripts/self_test.sh` passes.
- [x] GitHub Actions self-test passes after push.
- [x] project examples are fictional.
- [x] README credits external agent catalogs or tools that influenced the workflow.
- [x] contributor docs explain how to validate first-run onboarding.
- [x] scripts use relative paths derived from the repo root.
- [x] no private project names or local machine paths remain.
- [x] license exists.
- [x] contribution guide exists.
- [x] security/privacy guidance exists.

## Required For Future Releases

- [ ] README still explains what Pulse is in the first screen.
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
rg -n '/home/|/Users/|[A-Za-z]:\\\\Users|password|secret|token|credential|private key|customer|internal' .
```

Review matches manually. Guidance files may mention risky words; real private
material should not be present.

## Versioning

Use an annotated tag for future releases:

```bash
git tag -a v0.1.1 -m "Codex Pulse v0.1.1"
```
