"""Extract redacted AI command usage facts from local Codex session JSONL."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from collections import Counter
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


TOKEN_FIELDS = (
    "input_tokens",
    "cached_input_tokens",
    "output_tokens",
    "reasoning_output_tokens",
    "total_tokens",
)

REQ_RE = re.compile(r"\bREQ-\d{4,}[A-Za-z0-9_-]*\b")
BUG_RE = re.compile(r"\bBUG-\d{4,}[A-Za-z0-9_-]*\b")
SPRINT_RE = re.compile(r"\bsprint-\d{3,}\b")
EVENT_RE = re.compile(r"--event\s+([a-z][a-z0-9_.-]*)|/(req|bug|opsx|sprint)-([a-z0-9-]+)")
SECRET_RE = re.compile(
    r"(authorization|bearer|cookie|secret|password|api[_-]?key|access[_-]?key|token\s*[:=]|\.env)",
    re.IGNORECASE,
)
ABS_PATH_RE = re.compile(r"(/Users/|/home/|/private/|[A-Za-z]:\\)")
CHANGE_RE = re.compile(r"\b(?:add|update|fix|build|archive|refine|implement|create)-[a-z0-9][a-z0-9-]{2,}\b")


@dataclass
class CommandRun:
    source_session_hash: str
    source_line_start: int
    source_line_end: int
    turn_hash: str
    started_at: str | None = None
    ended_at: str | None = None
    command: str = "unknown"
    workflow_event: str | None = None
    requirements: set[str] = field(default_factory=set)
    bugs: set[str] = field(default_factory=set)
    changes: set[str] = field(default_factory=set)
    sprint_id: str | None = None
    attribution_confidence: str = "low"
    model_call_count: int = 0
    input_tokens: int = 0
    cached_input_tokens: int = 0
    output_tokens: int = 0
    reasoning_output_tokens: int = 0
    total_tokens: int = 0
    tool_call_count: int = 0
    tool_output_chars: int = 0
    retry_count: int = 0
    retry_count_method: str = "tool_result_error_count"
    warnings: list[str] = field(default_factory=list)
    _tool_errors: int = 0

    def to_record(self) -> dict[str, Any]:
        return {
            "source_session_hash": self.source_session_hash,
            "source_line_start": self.source_line_start,
            "source_line_end": self.source_line_end,
            "turn_hash": self.turn_hash,
            "started_at": self.started_at,
            "ended_at": self.ended_at,
            "command": self.command,
            "workflow_event": self.workflow_event,
            "requirements": sorted(self.requirements),
            "bugs": sorted(self.bugs),
            "changes": sorted(self.changes),
            "sprint_id": self.sprint_id,
            "attribution_confidence": self.attribution_confidence,
            "model_call_count": self.model_call_count,
            "input_tokens": self.input_tokens,
            "cached_input_tokens": self.cached_input_tokens,
            "output_tokens": self.output_tokens,
            "reasoning_output_tokens": self.reasoning_output_tokens,
            "total_tokens": self.total_tokens,
            "tool_call_count": self.tool_call_count,
            "tool_output_chars": self.tool_output_chars,
            "retry_count": self.retry_count,
            "retry_count_method": self.retry_count_method,
            "warnings": self.warnings,
        }


def stable_hash(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:16]


def source_hash(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def event_type(row: dict[str, Any]) -> str:
    payload = row.get("payload") if isinstance(row.get("payload"), dict) else {}
    value = payload.get("type") or row.get("type") or row.get("event")
    return str(value or "unknown")


def timestamp(row: dict[str, Any]) -> str | None:
    for key in ("timestamp", "ts", "created_at", "time"):
        value = row.get(key)
        if isinstance(value, str) and value:
            return value
    payload = row.get("payload") if isinstance(row.get("payload"), dict) else {}
    value = payload.get("timestamp")
    return value if isinstance(value, str) and value else None


def safe_text(value: Any) -> str:
    if isinstance(value, str):
        return value
    if isinstance(value, dict):
        for key in ("text", "content", "message", "cmd", "command"):
            if isinstance(value.get(key), str):
                return value[key]
    return ""


def user_text(row: dict[str, Any]) -> str:
    payload = row.get("payload") if isinstance(row.get("payload"), dict) else {}
    message = row.get("message") if isinstance(row.get("message"), dict) else {}
    if row.get("role") == "user" or payload.get("role") == "user" or message.get("role") == "user":
        return safe_text(row) or safe_text(payload) or safe_text(message)
    if event_type(row) in {"user_message", "user_turn", "input"}:
        return safe_text(row) or safe_text(payload)
    return ""


def is_token_event(row: dict[str, Any]) -> bool:
    return event_type(row) == "token_count"


def token_usage(row: dict[str, Any]) -> dict[str, int]:
    payload = row.get("payload") if isinstance(row.get("payload"), dict) else {}
    usage = payload.get("last_token_usage") or row.get("last_token_usage") or payload.get("usage") or {}
    if not isinstance(usage, dict):
        return {field: 0 for field in TOKEN_FIELDS}
    return {field: int(usage.get(field) or 0) for field in TOKEN_FIELDS}


def is_tool_call(row: dict[str, Any]) -> bool:
    kind = event_type(row)
    if kind in {"tool_call", "function_call", "exec_command", "tool_use"}:
        return True
    payload = row.get("payload") if isinstance(row.get("payload"), dict) else {}
    return bool(payload.get("tool_name") or row.get("tool_name"))


def is_tool_result(row: dict[str, Any]) -> bool:
    return event_type(row) in {"tool_result", "function_result", "exec_result", "tool_output"}


def tool_output_length(row: dict[str, Any]) -> int:
    payload = row.get("payload") if isinstance(row.get("payload"), dict) else {}
    for key in ("output", "result", "stdout", "stderr", "content"):
        value = payload.get(key, row.get(key))
        if isinstance(value, str):
            return len(value)
    return 0


def tool_failed(row: dict[str, Any]) -> bool:
    payload = row.get("payload") if isinstance(row.get("payload"), dict) else {}
    status = payload.get("status") or row.get("status")
    if str(status).lower() in {"failed", "error", "timeout"}:
        return True
    exit_code = payload.get("exit_code", row.get("exit_code"))
    return isinstance(exit_code, int) and exit_code != 0


def classify_text(text: str) -> dict[str, Any]:
    reqs = set(REQ_RE.findall(text))
    bugs = set(BUG_RE.findall(text))
    sprints = set(SPRINT_RE.findall(text))
    changes = set(CHANGE_RE.findall(text))
    workflow_event = None
    event_match = EVENT_RE.search(text)
    if event_match:
        workflow_event = event_match.group(1) or f"{event_match.group(2)}.{event_match.group(3)}"
    command = workflow_event or ("multi-issue" if len(reqs | bugs) > 1 else "command")
    confidence = "high" if any((reqs, bugs, sprints, changes, workflow_event)) else "low"
    return {
        "requirements": reqs,
        "bugs": bugs,
        "changes": changes,
        "sprint_id": sorted(sprints)[0] if sprints else None,
        "workflow_event": workflow_event,
        "command": command,
        "attribution_confidence": confidence,
    }


def redaction_warnings(text: str) -> list[str]:
    warnings: list[str] = []
    if ABS_PATH_RE.search(text):
        warnings.append("redacted-local-absolute-path")
    if SECRET_RE.search(text):
        warnings.append("redacted-sensitive-text")
    return warnings


def apply_attribution(run: CommandRun, text: str) -> None:
    details = classify_text(text)
    run.requirements.update(details["requirements"])
    run.bugs.update(details["bugs"])
    run.changes.update(details["changes"])
    run.sprint_id = run.sprint_id or details["sprint_id"]
    run.workflow_event = run.workflow_event or details["workflow_event"]
    run.command = details["command"]
    run.attribution_confidence = details["attribution_confidence"]
    run.warnings.extend(redaction_warnings(text))


def parse_session_jsonl(path: Path, manual_map: dict[str, Any] | None = None) -> tuple[list[dict[str, Any]], list[str]]:
    raw = path.read_bytes()
    session_hash = source_hash(raw)
    runs: list[CommandRun] = []
    current: CommandRun | None = None
    warnings: list[str] = []

    for line_number, raw_line in enumerate(raw.splitlines(), start=1):
        if not raw_line.strip():
            continue
        try:
            row = json.loads(raw_line)
        except json.JSONDecodeError:
            warnings.append(f"line-{line_number}: malformed-json")
            if current:
                current.warnings.append("malformed-json-row-skipped")
            continue
        if not isinstance(row, dict):
            warnings.append(f"line-{line_number}: non-object-row")
            continue

        text = user_text(row)
        if text:
            if current:
                current.retry_count = current._tool_errors
                runs.append(current)
            current = CommandRun(
                source_session_hash=session_hash,
                source_line_start=line_number,
                source_line_end=line_number,
                turn_hash=stable_hash(f"{session_hash}:{line_number}:{text}"),
                started_at=timestamp(row),
                ended_at=timestamp(row),
            )
            apply_attribution(current, text)
            continue

        if current is None:
            continue
        current.source_line_end = line_number
        current.ended_at = timestamp(row) or current.ended_at
        kind = event_type(row)
        if is_token_event(row):
            current.model_call_count += 1
            usage = token_usage(row)
            for field in TOKEN_FIELDS:
                setattr(current, field, getattr(current, field) + usage[field])
            continue
        if is_tool_call(row):
            current.tool_call_count += 1
            continue
        if is_tool_result(row):
            current.tool_output_chars += tool_output_length(row)
            if tool_failed(row):
                current._tool_errors += 1
            continue
        if kind not in {"assistant_message", "message", "unknown"}:
            current.warnings.append(f"unknown-event:{kind}")

    if current:
        current.retry_count = current._tool_errors
        runs.append(current)

    records = [run.to_record() for run in runs]
    if manual_map:
        records = apply_manual_mapping(records, manual_map)
    return records, warnings


def apply_manual_mapping(records: list[dict[str, Any]], manual_map: dict[str, Any]) -> list[dict[str, Any]]:
    for record in records:
        mapping = manual_map.get(record["turn_hash"]) or manual_map.get(record["source_session_hash"])
        if not isinstance(mapping, dict):
            continue
        for key in ("requirements", "bugs", "changes"):
            if isinstance(mapping.get(key), list):
                record[key] = sorted(set(record[key]) | set(str(item) for item in mapping[key]))
        if isinstance(mapping.get("sprint_id"), str):
            record["sprint_id"] = mapping["sprint_id"]
        if isinstance(mapping.get("workflow_event"), str):
            record["workflow_event"] = mapping["workflow_event"]
        record["attribution_confidence"] = mapping.get("attribution_confidence", "medium")
    return records


def aggregate_sprint(records: list[dict[str, Any]], sprint_id: str) -> dict[str, Any]:
    unique: dict[str, dict[str, Any]] = {}
    for record in records:
        if record.get("sprint_id") == sprint_id or sprint_id in record.get("changes", []):
            unique[record["turn_hash"]] = record
    rows = list(unique.values())
    totals = {field: sum(int(row.get(field) or 0) for row in rows) for field in TOKEN_FIELDS}
    totals.update(
        {
            "command_run_count": len(rows),
            "model_call_count": sum(int(row.get("model_call_count") or 0) for row in rows),
            "tool_call_count": sum(int(row.get("tool_call_count") or 0) for row in rows),
            "tool_output_chars": sum(int(row.get("tool_output_chars") or 0) for row in rows),
            "retry_count": sum(int(row.get("retry_count") or 0) for row in rows),
        }
    )
    by_event: dict[str, Counter[str]] = {}
    for row in rows:
        event = row.get("workflow_event") or row.get("command") or "unknown"
        bucket = by_event.setdefault(event, Counter())
        bucket["command_run_count"] += 1
        bucket["model_call_count"] += int(row.get("model_call_count") or 0)
        bucket["tool_call_count"] += int(row.get("tool_call_count") or 0)
        bucket["retry_count"] += int(row.get("retry_count") or 0)
        for field in TOKEN_FIELDS:
            bucket[field] += int(row.get(field) or 0)
    warnings = sorted({warning for row in rows for warning in row.get("warnings", [])})
    if not rows:
        warnings.append("no-real-usage-snapshot")
    return {
        "sprint_id": sprint_id,
        "source": "data/ai-usage command-runs",
        "estimated": not bool(rows),
        "totals": totals,
        "by_workflow_event": {key: dict(value) for key, value in sorted(by_event.items())},
        "warnings": warnings,
    }


def assert_record_safe(record: dict[str, Any]) -> None:
    text = json.dumps(record, ensure_ascii=False)
    if ABS_PATH_RE.search(text) or SECRET_RE.search(text):
        raise ValueError("unsafe text detected in usage record")


def write_outputs(records: list[dict[str, Any]], out_dir: Path, sprint_id: str | None) -> dict[str, Path]:
    out_dir.mkdir(parents=True, exist_ok=True)
    command_dir = out_dir / "command-runs"
    sprint_dir = out_dir / "sprints"
    command_dir.mkdir(parents=True, exist_ok=True)
    sprint_dir.mkdir(parents=True, exist_ok=True)
    for record in records:
        assert_record_safe(record)
    output_paths: dict[str, Path] = {}
    if records:
        command_path = command_dir / f"{records[0]['source_session_hash'][:16]}.json"
        command_path.write_text(json.dumps({"command_runs": records}, ensure_ascii=False, indent=2) + "\n")
        output_paths["command_runs"] = command_path
    if sprint_id:
        snapshot = aggregate_sprint(records, sprint_id)
        assert_record_safe(snapshot)
        sprint_path = sprint_dir / f"{sprint_id}.json"
        sprint_path.write_text(json.dumps(snapshot, ensure_ascii=False, indent=2) + "\n")
        output_paths["sprint"] = sprint_path
    return output_paths


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--session-jsonl", type=Path, required=True)
    parser.add_argument("--out-dir", type=Path, default=Path("data/ai-usage"))
    parser.add_argument("--sprint")
    parser.add_argument("--manual-map", type=Path)
    parser.add_argument("--json", action="store_true")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    manual = json.loads(args.manual_map.read_text()) if args.manual_map else None
    records, warnings = parse_session_jsonl(args.session_jsonl, manual)
    paths = write_outputs(records, args.out_dir, args.sprint)
    payload = {"command_run_count": len(records), "warnings": warnings, "outputs": {k: str(v) for k, v in paths.items()}}
    print(json.dumps(payload, ensure_ascii=False, indent=2) if args.json else payload)
    return 0
