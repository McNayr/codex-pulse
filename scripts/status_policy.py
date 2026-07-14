#!/usr/bin/env python3
"""Evaluate a portable, agent-neutral Pulse status policy.

This script intentionally does not read Hermes/Codex auth, logs, or private local
paths. Callers pass already-sanitized adapter signals on the command line or in a
small JSON fixture, and Pulse maps them into safe operating guidance.
"""
from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

USAGE_ORDER = {"normal": 0, "caution": 1, "conserve": 2, "critical": 3, "exhausted": 4}
LOG_ORDER = {"clean": 0, "watch": 1, "critical": 3}


@dataclass(frozen=True)
class StatusInputs:
    usage_mode: str = "normal"
    log_risk: str = "clean"

    @classmethod
    def from_mapping(cls, data: dict[str, Any]) -> "StatusInputs":
        return cls(
            usage_mode=str(data.get("usage_mode", data.get("usage", "normal"))).strip().lower(),
            log_risk=str(data.get("log_risk", data.get("logs", "clean"))).strip().lower(),
        )


def _normalize(value: str, allowed: dict[str, int], field: str) -> str:
    normalized = value.strip().lower()
    if normalized not in allowed:
        choices = ", ".join(sorted(allowed))
        raise ValueError(f"unknown {field}: {value!r}; expected one of: {choices}")
    return normalized


def evaluate_status(inputs: StatusInputs) -> dict[str, Any]:
    usage = _normalize(inputs.usage_mode, USAGE_ORDER, "usage_mode")
    logs = _normalize(inputs.log_risk, LOG_ORDER, "log_risk")
    usage_score = USAGE_ORDER[usage]
    log_score = LOG_ORDER[logs]

    if usage in {"conserve", "critical", "exhausted"} or logs == "critical":
        mode = "SAFE_HANDOFF"
        checkpoint_now = True
        max_parallel_agents = 0
        broad_research = False
        heavy_runtime_experiments = False
        recommendations = [
            "Refresh a compact checkpoint before additional work.",
            "Avoid broad research, agent fan-out, and runtime mutation.",
            "Do at most one tiny no-surprise safe-prep slice, then update durable handoff notes.",
        ]
    elif usage_score or log_score:
        mode = "CAUTION"
        checkpoint_now = False
        max_parallel_agents = 3
        broad_research = True
        heavy_runtime_experiments = True
        recommendations = [
            "Prefer compact packets and indexes before broad rereads.",
            "Batch tool calls and checkpoint before context-heavy work.",
            "Monitor watched signals before increasing task breadth.",
        ]
    else:
        mode = "NORMAL"
        checkpoint_now = False
        max_parallel_agents = 5
        broad_research = True
        heavy_runtime_experiments = True
        recommendations = [
            "Proceed with normal bounded work.",
            "Keep durable project files as the source of truth.",
        ]

    return {
        "mode": mode,
        "checkpoint_now": checkpoint_now,
        "max_parallel_agents": max_parallel_agents,
        "broad_research": broad_research,
        "heavy_runtime_experiments": heavy_runtime_experiments,
        "reasons": [f"usage:{usage}", f"logs:{logs}"],
        "recommendations": recommendations,
    }


def format_markdown(status: dict[str, Any]) -> str:
    lines = [
        "# Codex Pulse Status Policy",
        "",
        f"Mode: {status['mode']}",
        f"Checkpoint now: {'yes' if status['checkpoint_now'] else 'no'}",
        f"Max parallel agents: {status['max_parallel_agents']}",
        f"Broad research: {'yes' if status['broad_research'] else 'no'}",
        f"Heavy runtime experiments: {'yes' if status['heavy_runtime_experiments'] else 'no'}",
        f"Reasons: {', '.join(status['reasons'])}",
        "",
        "## Recommendations",
        "",
    ]
    lines.extend(f"- {item}" for item in status["recommendations"])
    return "\n".join(lines) + "\n"


def _load_inputs(args: argparse.Namespace) -> StatusInputs:
    if args.json:
        data = json.loads(Path(args.json).expanduser().read_text(encoding="utf-8"))
        return StatusInputs.from_mapping(data)
    return StatusInputs(usage_mode=args.usage_mode, log_risk=args.log_risk)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Evaluate portable Codex Pulse status policy from sanitized adapter signals")
    parser.add_argument("--usage-mode", default="normal", choices=sorted(USAGE_ORDER))
    parser.add_argument("--log-risk", default="clean", choices=sorted(LOG_ORDER))
    parser.add_argument("--json", help="Read sanitized status inputs from a JSON fixture")
    parser.add_argument("--format", choices=["markdown", "json"], default="markdown")
    args = parser.parse_args(argv)

    status = evaluate_status(_load_inputs(args))
    if args.format == "json":
        print(json.dumps(status, indent=2))
    else:
        print(format_markdown(status), end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
