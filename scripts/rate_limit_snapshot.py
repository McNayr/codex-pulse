#!/usr/bin/env python3
"""Summarize captured rate-limit events from sanitized/offline fixtures.

This is intentionally offline-only: it reads caller-provided SSE/JSONL files and
never opens live streams, reads private auth files, or uses runtime log paths.
Adapters may export sanitized `codex.rate_limits`-style events for replay here.
"""
from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable, Iterator


@dataclass(frozen=True)
class RateWindow:
    name: str
    used_percent: float
    remaining_percent: float
    window_minutes: int | None


@dataclass(frozen=True)
class RateSnapshot:
    source: str
    provider: str
    plan_type: str
    windows: list[RateWindow]

    @property
    def most_constrained_remaining(self) -> float:
        if not self.windows:
            return 100.0
        return min(window.remaining_percent for window in self.windows)


def _as_float(value: Any, default: float = 0.0) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def _as_int(value: Any) -> int | None:
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def _window_name(name: str, window_minutes: int | None) -> str:
    if name in {"primary", "secondary"}:
        if window_minutes == 300:
            return "5h"
        if window_minutes == 10080:
            return "weekly"
    return name


def _looks_like_rate_limits(value: dict[str, Any]) -> bool:
    return any(isinstance(value.get(key), dict) for key in ("primary", "secondary"))


def _extract_rate_limits(event: dict[str, Any]) -> dict[str, Any] | None:
    for candidate in (event.get("rate_limits"), event.get("data"), event):
        if isinstance(candidate, dict) and _looks_like_rate_limits(candidate):
            return candidate
    return None


def _extract_info(event: dict[str, Any], rate_limits: dict[str, Any]) -> dict[str, Any]:
    info = event.get("info")
    if isinstance(info, dict):
        return info
    data = event.get("data")
    if isinstance(data, dict) and isinstance(data.get("info"), dict):
        return data["info"]
    return rate_limits


def parse_rate_limit_event(event: dict[str, Any]) -> RateSnapshot | None:
    event_type = str(event.get("type") or event.get("event") or "")
    if event_type != "codex.rate_limits":
        return None
    rate_limits = _extract_rate_limits(event)
    if not rate_limits:
        return None
    info = _extract_info(event, rate_limits)
    windows: list[RateWindow] = []
    for raw_name, value in rate_limits.items():
        if not isinstance(value, dict):
            continue
        used = max(0.0, min(100.0, _as_float(value.get("used_percent"))))
        window_minutes = _as_int(value.get("window_minutes"))
        windows.append(
            RateWindow(
                name=_window_name(str(raw_name), window_minutes),
                used_percent=used,
                remaining_percent=round(100.0 - used, 1),
                window_minutes=window_minutes,
            )
        )
    if not windows:
        return None
    return RateSnapshot(
        source="captured_fixture",
        provider=str(rate_limits.get("limit_id") or info.get("limit_id") or "unknown"),
        plan_type=str(info.get("plan_type") or rate_limits.get("plan_type") or "unknown"),
        windows=windows,
    )


def _iter_json_payloads(text: str) -> Iterator[dict[str, Any]]:
    pending_event_type: str | None = None
    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line:
            pending_event_type = None
            continue
        if line.startswith("event:"):
            pending_event_type = line.split(":", 1)[1].strip()
            continue
        payload_text = line.split(":", 1)[1].strip() if line.startswith("data:") else line
        if not payload_text or payload_text == "[DONE]":
            continue
        try:
            payload = json.loads(payload_text)
        except json.JSONDecodeError:
            continue
        if not isinstance(payload, dict):
            continue
        if pending_event_type and "type" not in payload and "event" not in payload:
            payload = {"type": pending_event_type, **payload}
        yield payload


def iter_snapshots(paths: Iterable[str | Path]) -> Iterator[RateSnapshot]:
    file_paths = [Path(path).expanduser() for path in paths]
    existing = [path for path in file_paths if path.exists() and path.is_file()]
    for path in sorted(existing, key=lambda item: (item.stat().st_mtime, str(item))):
        text = path.read_text(encoding="utf-8", errors="replace")
        for payload in _iter_json_payloads(text):
            snapshot = parse_rate_limit_event(payload)
            if snapshot is not None:
                yield snapshot


def find_latest_snapshot(paths: Iterable[str | Path]) -> RateSnapshot | None:
    latest: RateSnapshot | None = None
    for latest in iter_snapshots(paths):
        pass
    return latest


def usage_mode(remaining: float) -> str:
    if remaining <= 5.0:
        return "CRITICAL"
    if remaining <= 10.0:
        return "CONSERVE"
    if remaining <= 25.0:
        return "CAUTION"
    return "NORMAL"


def snapshot_to_dict(snapshot: RateSnapshot) -> dict[str, Any]:
    return {
        "source": snapshot.source,
        "provider": snapshot.provider,
        "plan_type": snapshot.plan_type,
        "mode": usage_mode(snapshot.most_constrained_remaining),
        "most_constrained_remaining": snapshot.most_constrained_remaining,
        "windows": [window.__dict__ for window in snapshot.windows],
    }


def format_markdown(snapshot: RateSnapshot) -> str:
    data = snapshot_to_dict(snapshot)
    lines = [
        "# Codex Pulse Rate Limit Snapshot",
        "",
        f"Mode: {data['mode']}",
        f"Most constrained remaining: {data['most_constrained_remaining']:.1f}%",
        f"Source: {data['source']}",
        f"Provider: {data['provider']}",
        f"Plan type: {data['plan_type']}",
        "",
        "## Windows",
        "",
    ]
    for window in snapshot.windows:
        minutes = "unknown" if window.window_minutes is None else str(window.window_minutes)
        lines.append(
            f"- {window.name}: used {window.used_percent:.1f}%, remaining {window.remaining_percent:.1f}%, window minutes {minutes}"
        )
    return "\n".join(lines) + "\n"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Offline-only parser for captured/sanitized codex.rate_limits SSE or JSONL fixtures"
    )
    parser.add_argument("--file", action="append", required=True, help="Captured SSE or JSONL fixture to parse")
    parser.add_argument("--format", choices=["markdown", "json"], default="markdown")
    args = parser.parse_args(argv)

    snapshot = find_latest_snapshot(args.file)
    if snapshot is None:
        raise SystemExit("no codex.rate_limits events found in provided fixture files")
    if args.format == "json":
        print(json.dumps(snapshot_to_dict(snapshot), indent=2))
    else:
        print(format_markdown(snapshot), end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
