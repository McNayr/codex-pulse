#!/usr/bin/env python3
"""Write a compact, portable session context checkpoint for a Pulse workspace.

The checkpoint is intentionally agent-neutral: it writes only fields provided on
its command line or in a JSON file, emits workspace-relative/passed-through file
references, and has no private local-path, account, or runtime dependencies.
"""
from __future__ import annotations

import argparse
import json
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable

DEFAULT_CHECKPOINT_NAME = "SESSION_CONTEXT_CHECKPOINT.md"


def _list(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, str):
        return [value.strip()] if value.strip() else []
    if isinstance(value, Iterable):
        return [str(item).strip() for item in value if str(item).strip()]
    text = str(value).strip()
    return [text] if text else []


@dataclass
class Checkpoint:
    active_task: str = ""
    completed: list[str] = field(default_factory=list)
    modified_files: list[str] = field(default_factory=list)
    verification: list[str] = field(default_factory=list)
    blockers: list[str] = field(default_factory=list)
    next_files: list[str] = field(default_factory=list)
    next_step: str = ""
    created_at: str = ""

    @classmethod
    def from_mapping(cls, data: dict[str, Any]) -> "Checkpoint":
        return cls(
            active_task=str(data.get("active_task", "")).strip(),
            completed=_list(data.get("completed")),
            modified_files=_list(data.get("modified_files")),
            verification=_list(data.get("verification")),
            blockers=_list(data.get("blockers")),
            next_files=_list(data.get("next_files")),
            next_step=str(data.get("next_step", "")).strip(),
            created_at=str(data.get("created_at", "")).strip(),
        )


def _now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _section(title: str, items: list[str], empty: str = "None") -> list[str]:
    lines = [f"## {title}", ""]
    if items:
        lines.extend(f"- {item}" for item in items)
    else:
        lines.append(empty)
    lines.append("")
    return lines


def render_checkpoint(checkpoint: Checkpoint) -> str:
    created_at = checkpoint.created_at or _now()
    lines = [
        "# Codex Pulse Session Checkpoint",
        "",
        f"Created: `{created_at}`",
        "",
        "Purpose: compact file-backed handoff for agent sessions when chat context is risky, stale, or unavailable. Treat this as a pointer to durable source files, not a replacement for project docs.",
        "",
        "## Active Task",
        "",
        checkpoint.active_task or "None",
        "",
    ]
    lines.extend(_section("Completed", checkpoint.completed))
    lines.extend(_section("Modified Files", checkpoint.modified_files))
    lines.extend(_section("Verification", checkpoint.verification))
    lines.extend(_section("Blockers", checkpoint.blockers))
    lines.extend(_section("Next Files To Open", checkpoint.next_files))
    lines.extend(
        [
            "## Next Step",
            "",
            checkpoint.next_step or "None",
            "",
            "## Resume Rule",
            "",
            "Open the files above first, then continue from the next step. If this checkpoint conflicts with project source-of-truth files, prefer the source-of-truth files and refresh the checkpoint.",
            "",
        ]
    )
    return "\n".join(lines)


def write_checkpoint(target_dir: str | Path, checkpoint: Checkpoint, filename: str = DEFAULT_CHECKPOINT_NAME) -> Path:
    target = Path(target_dir).expanduser().resolve()
    target.mkdir(parents=True, exist_ok=True)
    out = target / filename
    out.write_text(render_checkpoint(checkpoint), encoding="utf-8")
    return out


def _load_checkpoint_args(args: argparse.Namespace) -> Checkpoint:
    if args.json:
        data = json.loads(Path(args.json).expanduser().read_text(encoding="utf-8"))
        return Checkpoint.from_mapping(data)
    return Checkpoint(
        active_task=args.active_task or "",
        completed=args.completed or [],
        modified_files=args.modified_file or [],
        verification=args.verification or [],
        blockers=args.blocker or [],
        next_files=args.next_file or [],
        next_step=args.next_step or "",
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Write a compact Codex Pulse session checkpoint")
    parser.add_argument("--target", default=".", help="Directory to receive the checkpoint file")
    parser.add_argument("--filename", default=DEFAULT_CHECKPOINT_NAME)
    parser.add_argument("--json", help="Read checkpoint fields from a JSON file")
    parser.add_argument("--active-task")
    parser.add_argument("--completed", action="append")
    parser.add_argument("--modified-file", action="append")
    parser.add_argument("--verification", action="append")
    parser.add_argument("--blocker", action="append")
    parser.add_argument("--next-file", action="append")
    parser.add_argument("--next-step")
    parser.add_argument("--format", choices=["markdown", "json"], default="markdown")
    args = parser.parse_args(argv)

    checkpoint = _load_checkpoint_args(args)
    out = write_checkpoint(args.target, checkpoint, filename=args.filename)
    summary = {"checkpoint": out.name, "target": ".", "written": True}
    if args.format == "json":
        print(json.dumps(summary, indent=2))
    else:
        print("# Codex Pulse Session Checkpoint")
        print("")
        print(f"Wrote: `{out.name}`")
        print("Target: `.`")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
