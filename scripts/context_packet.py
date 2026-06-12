#!/usr/bin/env python3
"""Generate a compact, sanitized Codex Pulse startup/resume packet.

This is intentionally agent-neutral: it reads only the workspace passed on the
command line, emits workspace-relative paths, and has no Hermes/Codex auth or
private local-path dependencies.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

OPEN_FIRST = ["START_HERE.md", "MISSION_BOARD.md", "WORKFLOW_RULES.md", "SESSION_STARTUP.md"]
PROJECT_SECTIONS = ["Brief", "Where To Work", "Current Source Of Truth", "Current Situation", "Resume Cue"]


def _read(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return ""


def _title(text: str, fallback: str) -> str:
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("#"):
            return stripped.lstrip("#").strip() or fallback
    return fallback


def _section_lines(text: str, section: str, *, max_lines: int = 4) -> list[str]:
    lines = text.splitlines()
    wanted = "## " + section
    capture = False
    result: list[str] = []
    for line in lines:
        stripped = line.strip()
        if stripped == wanted:
            capture = True
            continue
        if capture and stripped.startswith("## "):
            break
        if capture and stripped:
            result.append(stripped)
        if len(result) >= max_lines:
            break
    return result


def _project_briefs(workspace: Path, selected: str | None) -> list[dict[str, Any]]:
    projects_dir = workspace / "projects"
    if not projects_dir.exists():
        return []
    briefs = sorted(projects_dir.glob("*.md"))
    if selected:
        selected_file = selected if selected.endswith(".md") else selected + ".md"
        briefs = [path for path in briefs if path.name == selected_file or path.stem == selected]
    packets: list[dict[str, Any]] = []
    for path in briefs:
        text = _read(path)
        rel = path.relative_to(workspace).as_posix()
        packets.append(
            {
                "name": _title(text, path.stem),
                "path": rel,
                "brief": _section_lines(text, "Brief", max_lines=3),
                "source_of_truth": _section_lines(text, "Current Source Of Truth", max_lines=6),
                "situation": _section_lines(text, "Current Situation", max_lines=4),
                "resume": _section_lines(text, "Resume Cue", max_lines=4),
            }
        )
    return packets


def build_packet(workspace: str | Path, *, project: str | None = None) -> dict[str, Any]:
    root = Path(workspace).expanduser().resolve()
    open_first = [name for name in OPEN_FIRST if (root / name).is_file()]
    projects = _project_briefs(root, project)
    return {
        "workspace": ".",
        "open_first": open_first,
        "projects": projects,
        "notes": [
            "Paths are workspace-relative to avoid private local path leakage.",
            "Open only named source-of-truth files unless deeper detail is needed.",
        ],
    }


def format_markdown(packet: dict[str, Any]) -> str:
    lines = ["# Codex Pulse Context Packet", "", "Workspace: `.`", "", "## Open first"]
    for path in packet["open_first"]:
        lines.append(f"- `{path}`")
    if not packet["open_first"]:
        lines.append("- none found")
    lines.extend(["", "## Resume candidates"])
    if not packet["projects"]:
        lines.append("- none found")
    for project in packet["projects"]:
        lines.append(f"- {project['name']} (`{project['path']}`)")
        for label, key in (("Brief", "brief"), ("State", "situation"), ("Resume", "resume")):
            values = project.get(key) or []
            if values:
                lines.append(f"  - {label}: " + " / ".join(values))
        source = project.get("source_of_truth") or []
        if source:
            lines.append("  - Source: " + " / ".join(source))
    lines.extend(["", "## Operating notes"])
    for note in packet["notes"]:
        lines.append(f"- {note}")
    return "\n".join(lines) + "\n"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Generate a compact Codex Pulse context packet")
    parser.add_argument("--workspace", default=".", help="Pulse workspace root; output remains workspace-relative")
    parser.add_argument("--project", help="Optional project brief name/stem to focus on")
    parser.add_argument("--format", choices=["markdown", "json"], default="markdown")
    args = parser.parse_args(argv)
    packet = build_packet(args.workspace, project=args.project)
    if args.format == "json":
        print(json.dumps(packet, indent=2))
    else:
        print(format_markdown(packet), end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
