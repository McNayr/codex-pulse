#!/usr/bin/env python3
"""Summarize sanitized agent log-cost fixtures without reading private logs.

This is an adapter-neutral Pulse helper: callers provide JSONL records that have
already been collected and sanitized by their runtime adapter. The script never
opens agent auth files, runtime logs, or machine-specific default paths.
"""
from __future__ import annotations

import argparse
import json
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable

TIMEOUT_MARKERS = {"timeout", "timed_out", "deadline_exceeded"}
FAILURE_MARKERS = {"error", "failed", "failure", "exception"}


@dataclass(frozen=True)
class CostRecord:
    key: str
    tokens: int
    duration_ms: int
    status: str


def _as_int(value: Any) -> int:
    if value is None or value == "":
        return 0
    try:
        return max(0, int(value))
    except (TypeError, ValueError):
        return 0


def _record_key(data: dict[str, Any], fallback_index: int) -> str:
    raw = data.get("key") or data.get("operation") or data.get("label") or data.get("name")
    key = str(raw or f"record-{fallback_index}").strip()
    if not key:
        return f"record-{fallback_index}"
    # Keep output compact and avoid echoing long/path-like adapter details.
    return key.replace("\n", " ")[:80]


def _record_tokens(data: dict[str, Any]) -> int:
    explicit = _as_int(data.get("tokens") or data.get("total_tokens"))
    if explicit:
        return explicit
    return _as_int(data.get("input_tokens")) + _as_int(data.get("output_tokens"))


def parse_jsonl(lines: Iterable[str]) -> list[CostRecord]:
    records: list[CostRecord] = []
    for index, line in enumerate(lines, start=1):
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        data = json.loads(stripped)
        if not isinstance(data, dict):
            raise ValueError(f"line {index}: expected JSON object")
        records.append(
            CostRecord(
                key=_record_key(data, index),
                tokens=_record_tokens(data),
                duration_ms=_as_int(data.get("duration_ms") or data.get("elapsed_ms")),
                status=str(data.get("status") or data.get("result") or "ok").strip().lower(),
            )
        )
    return records


def summarize(records: list[CostRecord]) -> dict[str, Any]:
    key_counts = Counter(record.key for record in records)
    repeated = {key: count for key, count in key_counts.items() if count > 1}
    timeout_count = sum(1 for record in records if record.status in TIMEOUT_MARKERS)
    failure_count = sum(1 for record in records if record.status in FAILURE_MARKERS)
    return {
        "records": len(records),
        "total_tokens": sum(record.tokens for record in records),
        "max_tokens": max((record.tokens for record in records), default=0),
        "total_duration_ms": sum(record.duration_ms for record in records),
        "timeout_records": timeout_count,
        "failure_records": failure_count,
        "repeated_keys": repeated,
    }


def format_markdown(summary: dict[str, Any]) -> str:
    lines = [
        "# Codex Pulse Log Cost Summary",
        "",
        f"Total records: {summary['records']}",
        f"Total tokens: {summary['total_tokens']}",
        f"Max tokens in one record: {summary['max_tokens']}",
        f"Total duration ms: {summary['total_duration_ms']}",
        f"Timeout records: {summary['timeout_records']}",
        f"Failure records: {summary['failure_records']}",
        "",
        "## Repeated Keys",
        "",
    ]
    repeated = summary["repeated_keys"]
    if repeated:
        lines.extend(f"- {key}: {count}" for key, count in sorted(repeated.items()))
    else:
        lines.append("- None")
    return "\n".join(lines) + "\n"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Summarize sanitized JSONL log-cost fixtures")
    parser.add_argument("--jsonl", required=True, help="Path to a sanitized JSONL fixture")
    parser.add_argument("--format", choices=["markdown", "json"], default="markdown")
    args = parser.parse_args(argv)

    lines = Path(args.jsonl).expanduser().read_text(encoding="utf-8").splitlines()
    summary = summarize(parse_jsonl(lines))
    if args.format == "json":
        print(json.dumps(summary, indent=2))
    else:
        print(format_markdown(summary), end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
