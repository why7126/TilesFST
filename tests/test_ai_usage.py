import json
import importlib.util
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "ai_usage.py"
SPEC = importlib.util.spec_from_file_location("ai_usage", SCRIPT)
assert SPEC and SPEC.loader
ai_usage = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = ai_usage
SPEC.loader.exec_module(ai_usage)


def write_jsonl(path: Path, rows: list[dict[str, object]], *, malformed: bool = False) -> None:
    lines = [json.dumps(row, ensure_ascii=False) for row in rows]
    if malformed:
        lines.insert(2, "{bad-json")
    path.write_text("\n".join(lines) + "\n")


def test_parse_token_count_groups_by_user_turn_and_warns_on_malformed_rows(tmp_path: Path) -> None:
    session = tmp_path / "session.jsonl"
    write_jsonl(
        session,
        [
            {"timestamp": "2026-07-11T00:00:00Z", "type": "user_message", "text": "/sprint-apply sprint-006 REQ-0034 add-ai-token-usage-observability"},
            {
                "timestamp": "2026-07-11T00:00:01Z",
                "payload": {
                    "type": "token_count",
                    "last_token_usage": {
                        "input_tokens": 10,
                        "cached_input_tokens": 3,
                        "output_tokens": 4,
                        "reasoning_output_tokens": 2,
                        "total_tokens": 16,
                    },
                },
            },
            {"timestamp": "2026-07-11T00:00:02Z", "type": "unknown_future_event"},
            {"timestamp": "2026-07-11T00:00:03Z", "type": "user_message", "text": "/req-review REQ-0034"},
            {"timestamp": "2026-07-11T00:00:04Z", "payload": {"type": "token_count", "last_token_usage": {"input_tokens": 7, "total_tokens": 9}}},
        ],
        malformed=True,
    )

    records, warnings = ai_usage.parse_session_jsonl(session)

    assert len(records) == 2
    first = records[0]
    assert first["sprint_id"] == "sprint-006"
    assert first["requirements"] == ["REQ-0034"]
    assert first["changes"] == ["add-ai-token-usage-observability"]
    assert first["attribution_confidence"] == "high"
    assert first["model_call_count"] == 1
    assert first["input_tokens"] == 10
    assert first["cached_input_tokens"] == 3
    assert first["output_tokens"] == 4
    assert first["reasoning_output_tokens"] == 2
    assert first["total_tokens"] == 16
    assert "unknown-event:unknown_future_event" in first["warnings"]
    assert warnings == ["line-3: malformed-json"]
    assert records[1]["workflow_event"] == "req.review"


def test_aggregate_tools_retries_and_idempotent_sprint_totals(tmp_path: Path) -> None:
    session = tmp_path / "session.jsonl"
    write_jsonl(
        session,
        [
            {"type": "user_message", "text": "--event opsx.apply sprint-006 BUG-0062 fix-archive-trace-fallback-summary-gate"},
            {"payload": {"type": "token_count", "last_token_usage": {"input_tokens": 20, "output_tokens": 5, "total_tokens": 25}}},
            {"type": "tool_call", "tool_name": "exec_command"},
            {"type": "tool_result", "output": "x" * 12, "exit_code": 1},
            {"type": "tool_call", "tool_name": "exec_command"},
            {"type": "tool_result", "output": "ok", "exit_code": 0},
        ],
    )

    records, _ = ai_usage.parse_session_jsonl(session)
    duplicate_records = records + records
    snapshot = ai_usage.aggregate_sprint(duplicate_records, "sprint-006")

    assert snapshot["estimated"] is False
    assert snapshot["generated_at"]
    assert snapshot["coverage"]["bugs"] == ["BUG-0062"]
    assert snapshot["coverage"]["changes"] == ["fix-archive-trace-fallback-summary-gate"]
    assert snapshot["totals"]["command_run_count"] == 1
    assert snapshot["totals"]["tool_call_count"] == 2
    assert snapshot["totals"]["tool_output_chars"] == 14
    assert snapshot["totals"]["retry_count"] == 1
    assert snapshot["totals"]["total_tokens"] == 25
    assert snapshot["by_workflow_event"]["opsx.apply"]["command_run_count"] == 1
    assert records[0]["retry_count_method"] == "tool_result_error_count"


def test_multi_issue_manual_mapping_and_low_confidence_fallback(tmp_path: Path) -> None:
    session = tmp_path / "session.jsonl"
    write_jsonl(
        session,
        [
            {"type": "user_message", "text": "处理 REQ-0034 和 BUG-0063"},
            {"type": "user_message", "text": "continue"},
        ],
    )

    records, _ = ai_usage.parse_session_jsonl(session)
    mapped = ai_usage.apply_manual_mapping(
        records,
        {
            records[1]["turn_hash"]: {
                "sprint_id": "sprint-006",
                "changes": ["add-ai-token-usage-observability"],
                "attribution_confidence": "medium",
            }
        },
    )

    assert mapped[0]["requirements"] == ["REQ-0034"]
    assert mapped[0]["bugs"] == ["BUG-0063"]
    assert mapped[0]["command"] == "multi-issue"
    assert mapped[1]["sprint_id"] == "sprint-006"
    assert mapped[1]["changes"] == ["add-ai-token-usage-observability"]
    assert mapped[1]["attribution_confidence"] == "medium"


def test_redaction_blocks_prompts_paths_secrets_and_tool_output_bodies(tmp_path: Path) -> None:
    session = tmp_path / "session.jsonl"
    write_jsonl(
        session,
        [
            {
                "type": "user_message",
                "text": "REQ-0034 read /Users/example/project/.env with Authorization Bearer secret",
            },
            {"type": "tool_result", "output": "SECRET_OUTPUT_BODY", "exit_code": 0},
        ],
    )

    records, _ = ai_usage.parse_session_jsonl(session)
    record_text = json.dumps(records[0], ensure_ascii=False)

    assert "SECRET_OUTPUT_BODY" not in record_text
    assert "/Users/example" not in record_text
    assert "Bearer" not in record_text
    assert "redacted-local-absolute-path" in records[0]["warnings"]
    assert "redacted-sensitive-text" in records[0]["warnings"]
    with pytest.raises(ValueError):
        ai_usage.assert_record_safe({"path": "/Users/example/project"})
    with pytest.raises(ValueError):
        ai_usage.assert_record_safe({"prompt": "do not persist"})


def write_snapshot(path: Path, payload: dict[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")


def test_check_sprint_snapshot_status_present_missing_stale_failed(tmp_path: Path) -> None:
    missing = ai_usage.check_sprint_snapshot(tmp_path / "missing.json", "sprint-999")
    assert missing["snapshot_status"] == "missing"
    assert missing["usage_mode"] == "estimated_fallback"

    path = tmp_path / "sprint-999.json"
    write_snapshot(
        path,
        {
            "sprint_id": "sprint-999",
            "generated_at": "2026-07-03T00:00:00Z",
            "estimated": False,
            "coverage": {
                "requirements": ["REQ-9999-demo"],
                "bugs": ["BUG-9999-demo"],
                "changes": ["add-demo"],
            },
            "totals": {"command_run_count": 1, "model_call_count": 1, "total_tokens": 12},
            "warnings": [],
        },
    )
    present = ai_usage.check_sprint_snapshot(
        path,
        "sprint-999",
        expected_scope={
            "requirements": ["REQ-9999-demo"],
            "bugs": ["BUG-9999-demo"],
            "changes": ["add-demo"],
        },
        min_generated_at="2026-07-02 18:00:00",
    )
    assert present["snapshot_status"] == "present"
    assert present["usage_mode"] == "actual"

    stale = ai_usage.check_sprint_snapshot(path, "sprint-999", min_generated_at="2026-07-04 00:00:00")
    assert stale["snapshot_status"] == "stale"
    assert stale["usage_mode"] == "estimated_fallback"
    assert "snapshot-stale" in stale["warnings"]

    write_snapshot(
        path,
        {
            "sprint_id": "sprint-999",
            "generated_at": "2026-07-03T00:00:00Z",
            "estimated": False,
            "coverage": {"requirements": [], "bugs": [], "changes": []},
            "totals": {},
        },
    )
    failed = ai_usage.check_sprint_snapshot(path, "sprint-999")
    assert failed["snapshot_status"] == "failed"
    assert "required-metrics-empty" in failed["warnings"]


def test_post_command_hook_generates_command_run_and_sprint_snapshot(tmp_path: Path) -> None:
    session = tmp_path / "session.jsonl"
    out_dir = tmp_path / "ai-usage"
    write_jsonl(
        session,
        [
            {"timestamp": "2026-07-12T01:00:00Z", "type": "user_message", "text": "continue"},
            {"timestamp": "2026-07-12T01:00:01Z", "payload": {"type": "token_count", "last_token_usage": {"input_tokens": 11, "output_tokens": 4, "total_tokens": 15}}},
        ],
    )

    summary = ai_usage.post_command_hook(
        session_jsonl=session,
        out_dir=out_dir,
        workflow_event="opsx.apply",
        requirements=["REQ-0037-auto-token-fact-source-for-workflow-commands"],
        changes=["add-auto-token-fact-source-for-workflow-commands"],
        sprint_id="sprint-007",
    )

    assert summary["status"] == "ok"
    assert summary["usage_mode"] == "actual"
    assert summary["command_run_count"] == 1
    assert summary["sprint_snapshot"]["status"] == "refreshed"
    command_path = out_dir / "command-runs" / f"{ai_usage.source_hash(session.read_bytes())[:16]}.json"
    sprint_path = out_dir / "sprints" / "sprint-007.json"
    assert command_path.exists()
    assert sprint_path.exists()
    command_text = command_path.read_text()
    assert "/Users/" not in command_text
    snapshot = json.loads(sprint_path.read_text())
    assert snapshot["totals"]["command_run_count"] == 1
    assert snapshot["coverage"]["requirements"] == ["REQ-0037-auto-token-fact-source-for-workflow-commands"]
    assert snapshot["coverage"]["changes"] == ["add-auto-token-fact-source-for-workflow-commands"]


def test_post_command_hook_without_sprint_skips_snapshot(tmp_path: Path) -> None:
    session = tmp_path / "session.jsonl"
    out_dir = tmp_path / "ai-usage"
    write_jsonl(
        session,
        [
            {"type": "user_message", "text": "/req-capture REQ-0038"},
            {"payload": {"type": "token_count", "last_token_usage": {"total_tokens": 9}}},
        ],
    )

    summary = ai_usage.post_command_hook(
        session_jsonl=session,
        out_dir=out_dir,
        workflow_event="req.capture",
        requirements=["REQ-0038-demo"],
    )

    assert summary["usage_mode"] == "actual"
    assert summary["sprint_snapshot"] == {"status": "skipped", "path": None, "reason": "no-sprint"}
    assert not (out_dir / "sprints").exists() or not list((out_dir / "sprints").glob("*.json"))


def test_post_command_hook_missing_session_returns_unavailable(tmp_path: Path) -> None:
    summary = ai_usage.post_command_hook(session_jsonl=None, out_dir=tmp_path / "ai-usage")

    assert summary["status"] == "skipped"
    assert summary["usage_mode"] == "unavailable"
    assert summary["command_run_count"] == 0
    assert "session-jsonl-missing" in summary["warnings"]
    assert summary["recommended_action"]


def test_post_command_hook_warns_on_malformed_or_missing_token_count(tmp_path: Path) -> None:
    session = tmp_path / "session.jsonl"
    write_jsonl(
        session,
        [
            {"type": "user_message", "text": "/bug-complete BUG-0001"},
            {"type": "assistant_message", "text": "ok"},
        ],
        malformed=True,
    )

    summary = ai_usage.post_command_hook(
        session_jsonl=session,
        out_dir=tmp_path / "ai-usage",
        workflow_event="bug.complete",
        bugs=["BUG-0001-demo"],
    )

    assert summary["status"] == "warning"
    assert summary["usage_mode"] == "estimated_fallback"
    assert "token-count-missing" in summary["warnings"]
    assert "line-3: malformed-json" in summary["warnings"]


def test_post_command_hook_is_idempotent_for_repeated_session(tmp_path: Path) -> None:
    session = tmp_path / "session.jsonl"
    out_dir = tmp_path / "ai-usage"
    write_jsonl(
        session,
        [
            {"type": "user_message", "text": "--event opsx.apply sprint-007 add-auto-token-fact-source-for-workflow-commands"},
            {"payload": {"type": "token_count", "last_token_usage": {"input_tokens": 3, "output_tokens": 2, "total_tokens": 5}}},
        ],
    )

    for _ in range(2):
        ai_usage.post_command_hook(
            session_jsonl=session,
            out_dir=out_dir,
            workflow_event="opsx.apply",
            changes=["add-auto-token-fact-source-for-workflow-commands"],
            sprint_id="sprint-007",
        )

    snapshot = json.loads((out_dir / "sprints" / "sprint-007.json").read_text())
    assert snapshot["totals"]["command_run_count"] == 1
    assert snapshot["totals"]["total_tokens"] == 5
