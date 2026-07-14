#!/usr/bin/env python3
"""Report startup/source tiers for a Codex Pulse workspace.

Portable by design: reads only the workspace passed on the command line and
emits workspace-relative paths. It does not inspect agent logs, auth files, or
machine-specific runtime state.
"""
from __future__ import annotations

import argparse
import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

ROOT_POLICY = {
    "START_HERE.md",
    "SESSION_STARTUP.md",
    "WORKFLOW_RULES.md",
    "SESSION_SHUTDOWN.md",
    "DRIFT_DETECTION.md",
    "AGENT_GUIDE.md",
}
REGISTRY = {"MISSION_BOARD.md", "PROJECTS.md"}


@dataclass(frozen=True)
class AuditRow:
    path: str
    tier: str
    bytes: int
    lines: int
    suggested_read: str
    warnings: list[str]


def tier_for(path: str) -> str:
    if path in ROOT_POLICY:
        return "root-policy"
    if path in REGISTRY:
        return "registry"
    if path.startswith("projects/"):
        return "project-brief"
    if path.startswith("examples/") or path.startswith("templates/"):
        return "template-example"
    return "reference"


def suggested_read(tier: str) -> str:
    return {
        "root-policy": "policy-only",
        "registry": "packet-input",
        "project-brief": "selected-brief",
        "template-example": "lookup-only",
    }.get(tier, "query-first")


def warnings_for(tier: str, size: int, warn_bytes: int) -> list[str]:
    warnings: list[str] = []
    if tier == "project-brief" and size > warn_bytes:
        warnings.append("brief-over-threshold")
    elif tier == "reference" and size > warn_bytes:
        warnings.append("reference-large")
    elif tier in {"root-policy", "registry"} and size > warn_bytes:
        warnings.append("startup-doc-large")
    return warnings


def audit_workspace(workspace: str | Path, *, warn_bytes: int = 12_000) -> dict[str, Any]:
    root = Path(workspace).expanduser().resolve()
    rows: list[AuditRow] = []
    for path in sorted(root.rglob("*.md")):
        rel_path = path.relative_to(root)
        if any(part.startswith(".") for part in rel_path.parts):
            continue
        rel = rel_path.as_posix()
        text = path.read_text(encoding="utf-8", errors="replace")
        tier = tier_for(rel)
        rows.append(
            AuditRow(
                path=rel,
                tier=tier,
                bytes=path.stat().st_size,
                lines=text.count("\n") + 1,
                suggested_read=suggested_read(tier),
                warnings=warnings_for(tier, path.stat().st_size, warn_bytes),
            )
        )
    rows.sort(key=lambda row: (bool(row.warnings), row.bytes, row.path), reverse=True)
    return {"workspace": ".", "files": [asdict(row) for row in rows]}


def format_markdown(report: dict[str, Any], *, limit: int = 40) -> str:
    lines = [
        "# Codex Pulse Startup Audit",
        "",
        "Workspace: `.`",
        "",
        "| Path | Tier | Bytes | Lines | Suggested read | Warnings |",
        "| --- | --- | ---: | ---: | --- | --- |",
    ]
    for row in report.get("files", [])[:limit]:
        warnings = ", ".join(row.get("warnings") or []) or "-"
        lines.append(
            f"| `{row['path']}` | {row['tier']} | {row['bytes']} | {row['lines']} | {row['suggested_read']} | {warnings} |"
        )
    lines.extend(
        [
            "",
            "## Policy",
            "",
            "- Use packet-input and selected-brief tiers before broad root-policy reads.",
            "- Use query-first for large reference docs and lookup-only for templates/examples.",
            "- Output stays workspace-relative for public, agent-neutral reuse.",
        ]
    )
    return "\n".join(lines) + "\n"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Report Codex Pulse startup/source tiers")
    parser.add_argument("--workspace", default=".", help="Pulse workspace root; output remains workspace-relative")
    parser.add_argument("--warn-bytes", type=int, default=12_000, help="Warn when selected docs exceed this size")
    parser.add_argument("--limit", type=int, default=40, help="Maximum markdown rows")
    parser.add_argument("--format", choices=["markdown", "json"], default="markdown")
    args = parser.parse_args(argv)

    report = audit_workspace(args.workspace, warn_bytes=args.warn_bytes)
    if args.format == "json":
        print(json.dumps(report, indent=2))
    else:
        print(format_markdown(report, limit=args.limit), end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
