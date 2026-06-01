# Codex Pulse

A tiny operating system for Codex sessions that forget less and drift less.

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

## Repository Layout

- `bin/pulse`: portable startup command
- `scripts/new_project.sh`: project scaffold helper
- `START_HERE.md`: default session entry
- `MISSION_BOARD.md`: active project registry
- `WORKFLOW_RULES.md`: core operating rules
- `SESSION_STARTUP.md`: startup flow
- `SESSION_SHUTDOWN.md`: shutdown flow
- `DRIFT_DETECTION.md`: stop-and-realign rules
- `AGENT_GUIDE.md`: simple agent usage policy
- `projects/`: project briefs
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
