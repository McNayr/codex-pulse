# Codex Pulse

A tiny operating system for Codex sessions that forget less and drift less.

If you use Codex across multiple projects, Pulse gives each session a written
startup path, a current-state map, and a shutdown ritual. After five minutes,
you should be able to answer: what exists, what is true now, what should happen
next, and what should not be assumed.

Codex is very good at working. Humans are very good at saying, "quick thing,"
then opening seventeen tabs, changing three services, and trusting vibes as a
state-management strategy.

`Codex Pulse` is the small set of docs and scripts that keeps that from turning
into archaeology with a shell prompt.

## What It Is

`Codex Pulse` is a project-memory and workflow layer for Codex.

It gives each session a front door:

```bash
./bin/pulse
```

That command tells Codex what to open first, what projects exist, and how to
recover if the session falls out a window and comes back wearing a fake
mustache.

It is not magic. It is not a second brain. It is a clipboard with rules, a map,
and enough manners to write down what happened before leaving.

## What It Helps With

- starting a Codex session without inventing a perfect prompt
- resuming a project after a reboot, rate limit, nap, or existential snack
- keeping current state separate from history
- stopping implementation drift before it becomes folklore
- deciding when to use agents and when to keep things simple
- leaving shutdown notes that future-you will not resent
- turning repeated lessons into durable project knowledge

## The Core Idea

Every active project should have a small handoff pack:

- `README.md`: what this project is
- `CURRENT_STATE.md`: what is true now
- `SESSION_SAVE.md` or `RESUME.md`: where to restart
- `TODO.md`: what to do next
- `CHRONOLOGY.md`: what happened, append-only
- runbooks: how to repeat risky or manual operations

Pulse is the front desk. Projects own the truth.

## Start Here

Clone the repo into your workspace:

```bash
git clone https://github.com/McNayr/codex-pulse.git
cd codex-pulse
./bin/pulse
```

Then tell Codex:

```text
Open Codex Pulse
```

Codex should read:

1. `START_HERE.md`
2. `MISSION_BOARD.md`
3. `WORKFLOW_RULES.md`
4. one project brief under `projects/`

Then it should ask what to resume, unless you already named the project.

For a compact, agent-neutral orientation before opening broader files, run:

```bash
python3 ./scripts/context_packet.py --workspace . --format markdown
```

The packet uses workspace-relative paths and accepts `--project <brief-name>`
for focused resumes.

For deterministic local lookup across Pulse markdown, build or query the portable
workspace-relative index:

```bash
python3 ./scripts/doc_index.py --workspace . --index .pulse-index.json "startup packet" --format markdown
```

To classify startup/source tiers before opening broad docs, run the portable
audit helper:

```bash
python3 ./scripts/startup_audit.py --workspace . --format markdown
```

Use the report as a read policy: `root-policy` is policy-only, `registry` is
packet input, `project-brief` is selected-brief, and `reference` is query-first.
The helper emits workspace-relative paths only and does not read agent logs,
private auth, or machine-specific runtime state.

When a session is heading into a risky context window, handoff, reboot, or AFK
closeout, write a compact file-backed checkpoint without requiring any agent-
specific runtime:

```bash
python3 ./scripts/session_checkpoint.py \
  --target . \
  --active-task "Current task" \
  --completed "What changed" \
  --modified-file "relative/path.md" \
  --verification "Command output summary" \
  --next-file "START_HERE.md" \
  --next-step "Exact next action" \
  --format markdown
```

The checkpoint writer emits `SESSION_CONTEXT_CHECKPOINT.md` and keeps summary
output workspace-relative.

For adapter-provided usage/log signals, evaluate a portable no-auth status policy
before deciding whether to fan out agents or checkpoint first:

```bash
python3 ./scripts/status_policy.py --usage-mode normal --log-risk watch --format markdown
```

Adapters should pass sanitized modes only (`normal|caution|conserve|critical|exhausted`
for usage and `clean|watch|critical` for logs). Pulse does not read private auth,
agent logs, or machine-specific paths.

For sanitized cost fixtures exported by an adapter, summarize repeated operations,
token totals, timeout counts, and failure counts without reading private runtime
logs directly:

```bash
python3 ./scripts/log_cost_summary.py --jsonl sanitized-log-cost.jsonl --format markdown
```

Fixture records are JSON objects such as `{ "key": "startup", "input_tokens": 100,
"output_tokens": 25, "duration_ms": 1200 }`; adapter-specific log paths and
secrets should be removed before they reach Pulse.

For captured/sanitized rate-limit event fixtures, summarize the latest
`codex.rate_limits` snapshot offline without opening live streams or reading
private auth files:

```bash
python3 ./scripts/rate_limit_snapshot.py --file sanitized-rate-events.sse --format markdown
```

Adapters should export only replay-safe SSE/JSONL fixture data. Pulse reports the
most constrained remaining window and maps it to `NORMAL`, `CAUTION`,
`CONSERVE`, or `CRITICAL` guidance.

Adapter authors should follow the fixture contract in
[`integrations/adapters/TELEMETRY_FIXTURES.md`](./integrations/adapters/TELEMETRY_FIXTURES.md):
collect live runtime facts in the adapter, sanitize them into tiny replay-safe
fixtures or normalized modes, and keep Pulse core scripts independent from
provider auth, private logs, and machine-specific paths.

## Hermes Adapter

Pulse also ships a small Hermes adapter that keeps the Codex-first workflow unchanged.

Install it from the repository root:

```bash
./integrations/hermes/install_hermes_skill.sh
```

Then ask Hermes:

```text
Open Codex Pulse
```

The adapter lives under `integrations/hermes/` and teaches Hermes to follow the same Pulse startup, resume, and shutdown files. It does not make Hermes required for baseline Pulse usage.

Pulse also keeps agent-neutral notes for messaging adapters under `integrations/messaging/`. Start with [`SESSION_CONTINUITY.md`](./integrations/messaging/SESSION_CONTINUITY.md) when chat/mobile access feels more circular or expensive than the CLI; the key pattern is to keep one stable conversation lane unless the human explicitly opens a new thread or topic.

## Prerequisites

- Codex CLI, Hermes Agent, or another coding-agent environment that can read
  local files and run shell commands.
- A Unix-like shell for the included scripts.
- `rg` is recommended for the self-test and release scans.
- Git is recommended if you want Pulse to act as a clean reference baseline.

Pulse is just files and small shell scripts. There is no daemon, database, or
ritual sacrifice. If `./bin/pulse` prints the startup files and project briefs,
the basic setup works.

## Use It In Your Own Project

The simplest setup is to keep Pulse next to the projects it tracks:

```text
workspace/
  codex-pulse/
  my-app/
  my-infra/
```

Then scaffold a project:

```bash
./scripts/new_project.sh my-app ../my-app
```

That creates a project brief under `projects/` and handoff files in your
project folder. Fill in the brief, then add the project to `MISSION_BOARD.md`.

Now future Codex sessions have a map instead of a haunted attic.

## Adopt It In An Existing Project

Minimum viable adoption:

1. create `CURRENT_STATE.md`
2. create `SESSION_SAVE.md` or `RESUME.md`
3. create `TODO.md`
4. create `CHRONOLOGY.md`
5. add a Pulse project brief under `projects/`
6. add the project to `MISSION_BOARD.md`

Use `SESSION_SAVE.md` when you want a per-session handoff. Use `RESUME.md` when
the project already has one durable restart file and you want to keep that
convention.

See [projects/example-app.md](./projects/example-app.md) and
[examples/example-app](./examples/example-app) for a complete fictional example.

## What Makes It Useful

### Startup

Pulse gives Codex a consistent opening ritual. Not a ceremony. More like
checking your pockets before leaving the house.

### Resume

Pulse makes the next session start from written state instead of chat memory.
Chat memory is a fog machine with opinions.

### Shutdown

Pulse asks every session to leave:

- what changed
- what was verified
- what is blocked
- the exact next step
- which files to open first next time

### Drift Detection

If two fixes in a row do not solve the same problem, Pulse tells the session to
stop patching symptoms and reopen the source of truth.

### Agent Discipline

Pulse likes agents. Pulse does not like summoning a conference room because one
button is misaligned.

Use specialists when they reduce risk or rework. Keep the main session
responsible for integration.

Pulse does not ship agent definitions. The Codex subagent catalog used while
developing Pulse came from
[VoltAgent/awesome-codex-subagents](https://github.com/VoltAgent/awesome-codex-subagents).
If you want a broad specialist-agent library, start there and follow that
project's installation instructions. Credit to the VoltAgent contributors for
the catalog.

## Repository Layout

- `bin/pulse`: portable startup command
- `scripts/new_project.sh`: project scaffold helper
- `integrations/hermes/`: optional Hermes skill adapter
- `AGENTS.md`: baseline instructions for coding agents
- `START_HERE.md`: default session entry
- `MISSION_BOARD.md`: active project registry
- `WORKFLOW_RULES.md`: core operating rules
- `SESSION_STARTUP.md`: startup flow
- `SESSION_SHUTDOWN.md`: shutdown flow
- `DRIFT_DETECTION.md`: stop-and-realign rules
- `AGENT_GUIDE.md`: simple agent usage policy
- `projects/`: project briefs
- `examples/`: fictional complete example projects
- `templates/`: starter docs for projects

## Who This Is For

Use Pulse if you:

- work on multiple projects with Codex
- lose context between sessions
- do production or operational work where notes matter
- want repeatable handoffs
- want a clean project-memory system without installing a giant platform

Do not use Pulse if you want:

- automatic project management magic
- a replacement for source control
- a reason to avoid writing tests
- a sentient intern named Kevin

## Contributing

Contributions are welcome if they make Pulse:

- easier to start
- easier to resume
- harder to drift
- safer around live systems
- clearer without becoming a bureaucracy wearing a tiny hat

Good contributions include:

- better templates
- better startup scripts
- cleaner eval scenarios
- sharper shutdown rules
- examples from real workflows with private details removed

Before opening a PR, run:

```bash
./scripts/self_test.sh
```

And read [SECURITY.md](./SECURITY.md), because nobody wants to accidentally
publish the secret sauce, the secret token, or the secret third thing that
definitely should not be in git.

## Status

Early but usable.

This project came from a real working Codex operating system. This public
version is the clean-room edition: same useful bones, fewer private project
crumbs.

## License

MIT. Use it, fork it, improve it, and leave better notes than you found.
