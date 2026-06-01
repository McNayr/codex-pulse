# Security And Privacy

Codex Pulse is a documentation workflow system. That means it can become very
useful and very leaky if you copy real operational notes into it without
thinking.

## Do Not Commit

- passwords
- API keys
- access tokens
- private keys
- customer names
- internal hostnames
- production URLs that should not be public
- incident details that identify private systems
- personal data

## Before Publishing

Run:

```bash
./scripts/self_test.sh
```

Then run your own secret scanner if you have one.

At minimum, inspect matches from:

```bash
rg -n "password|secret|token|credential|private key|customer|internal" .
```

The words themselves are allowed in guidance files. Real secrets are not.

## Reporting Issues

If you find a security issue in the project templates or scripts, open a GitHub
security advisory or contact the maintainer privately.

If you accidentally committed secrets to your own project while using Pulse,
rotate those secrets. Editing git history is not enough by itself.
