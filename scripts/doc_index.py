#!/usr/bin/env python3
"""Build and query a small, deterministic markdown index for a Pulse workspace.

The index is intentionally portable: it reads only the workspace passed on the
command line, stores workspace-relative paths, and avoids private local-path,
agent-account, or runtime dependencies.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path
from typing import Any

CANONICAL_PATHS = {"MISSION_BOARD.md", "PROJECTS.md", "CURRENT_STATE.md", "START_HERE.md"}


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def _title(text: str, fallback: str) -> str:
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("#"):
            return stripped.lstrip("#").strip() or fallback
    return fallback


def _summary(text: str, *, max_lines: int = 4) -> str:
    useful: list[str] = []
    for raw in text.splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or line == "---":
            continue
        useful.append(line)
        if len(useful) >= max_lines:
            break
    return " ".join(useful)[:500]


def _terms(query: str) -> list[str]:
    return [term for term in re.split(r"[^a-z0-9]+", query.lower()) if term]


def build_index(workspace: str | Path) -> dict[str, Any]:
    root = Path(workspace).expanduser().resolve()
    files: list[dict[str, Any]] = []
    for path in sorted(root.rglob("*.md")):
        rel_path = path.relative_to(root)
        if any(part.startswith(".") for part in rel_path.parts):
            continue
        text = _read(path)
        rel = rel_path.as_posix()
        files.append(
            {
                "path": rel,
                "title": _title(text, path.stem),
                "summary": _summary(text),
                "size": path.stat().st_size,
                "sha256": hashlib.sha256(text.encode("utf-8", errors="replace")).hexdigest(),
                "canonical": rel in CANONICAL_PATHS or rel.startswith("projects/"),
                "project_brief": rel.startswith("projects/"),
            }
        )
    return {"workspace": ".", "files": files}


def query_index(index: dict[str, Any], query: str, *, limit: int = 10) -> list[dict[str, Any]]:
    terms = _terms(query)
    if not terms:
        return []
    scored: list[dict[str, Any]] = []
    for item in index.get("files", []):
        haystack = " ".join([item.get("path", ""), item.get("title", ""), item.get("summary", "")]).lower()
        score = sum(haystack.count(term) for term in terms)
        if score:
            result = dict(item)
            result["score"] = score
            scored.append(result)
    scored.sort(key=lambda row: (row["score"], row.get("project_brief", False), row.get("canonical", False), row.get("path", "")), reverse=True)
    return scored[:limit]


def format_markdown_index(index: dict[str, Any]) -> str:
    lines = ["# Codex Pulse Document Index", "", "Workspace: `.`", "", "## Files"]
    files = index.get("files", [])
    if not files:
        lines.append("- none found")
    for item in files:
        marker = " (canonical)" if item.get("canonical") else ""
        lines.append(f"- `{item['path']}`{marker}: {item['title']}")
        if item.get("summary"):
            lines.append(f"  - {item['summary']}")
    return "\n".join(lines) + "\n"


def format_markdown_results(results: list[dict[str, Any]], query: str) -> str:
    lines = ["# Codex Pulse Document Query", "", f"Query: `{query}`", "", "## Matches"]
    if not results:
        lines.append("- none found")
    for item in results:
        lines.append(f"- score {item['score']}: `{item['path']}` — {item['title']}")
        if item.get("summary"):
            lines.append(f"  - {item['summary']}")
    return "\n".join(lines) + "\n"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Build or query a portable Codex Pulse markdown index")
    parser.add_argument("query", nargs="?", help="Optional search query. If omitted, emit the index.")
    parser.add_argument("--workspace", default=".", help="Pulse workspace root; output remains workspace-relative")
    parser.add_argument("--index", help="Read/write this JSON index path instead of rebuilding every time")
    parser.add_argument("--limit", type=int, default=10, help="Maximum query results")
    parser.add_argument("--format", choices=["markdown", "json"], default="markdown")
    args = parser.parse_args(argv)

    if args.index and Path(args.index).is_file():
        index = json.loads(Path(args.index).read_text(encoding="utf-8"))
    else:
        index = build_index(args.workspace)
        if args.index:
            index_path = Path(args.index)
            index_path.parent.mkdir(parents=True, exist_ok=True)
            index_path.write_text(json.dumps(index, indent=2) + "\n", encoding="utf-8")

    if args.query:
        results = query_index(index, args.query, limit=args.limit)
        if args.format == "json":
            print(json.dumps({"query": args.query, "matches": results}, indent=2))
        else:
            print(format_markdown_results(results, args.query), end="")
    elif args.format == "json":
        print(json.dumps(index, indent=2))
    else:
        print(format_markdown_index(index), end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
