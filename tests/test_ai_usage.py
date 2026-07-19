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
    assert first["source_data_file"].endswith("session.jsonl")
    assert not first["source_data_file"].startswith("/Users/")
    assert first["sprint_id"] == "sprint-006"
    assert first["requirements"] == ["REQ-0034-ai-token-usage-observability"]
    assert first["changes"] == ["add-ai-token-usage-observability"]
    assert first["attribution_confidence"] == "high"
    assert first["model_call_count"] == 1
    assert first["input_tokens"] == 10
    assert first["cached_input_tokens"] == 3
    assert first["output_tokens"] == 4
    assert first["reasoning_output_tokens"] == 2
    assert first["total_tokens"] == 16
    assert "warnings" not in first
    assert warnings == ["line-3: malformed-json"]
    assert records[1]["workflow_event"] == "req.review"


def test_parse_token_count_supports_payload_info_last_token_usage(tmp_path: Path) -> None:
    session = tmp_path / "session.jsonl"
    write_jsonl(
        session,
        [
            {"timestamp": "2026-07-12T02:15:47Z", "type": "user_message", "text": "/opsx-apply add-auto-token-fact-source-for-workflow-commands"},
            {
                "timestamp": "2026-07-12T02:16:01Z",
                "type": "token_count",
                "payload": {
                    "type": "token_count",
                    "info": {
                        "last_token_usage": {
                            "input_tokens": 101,
                            "cached_input_tokens": 40,
                            "output_tokens": 12,
                            "reasoning_output_tokens": 7,
                            "total_tokens": 120,
                        }
                    },
                },
            },
        ],
    )

    records, warnings = ai_usage.parse_session_jsonl(session)

    assert warnings == []
    assert records[0]["input_tokens"] == 101
    assert records[0]["cached_input_tokens"] == 40
    assert records[0]["output_tokens"] == 12
    assert records[0]["reasoning_output_tokens"] == 7
    assert records[0]["total_tokens"] == 120


def test_parse_session_attaches_model_metadata_to_command_run(tmp_path: Path) -> None:
    session = tmp_path / "session.jsonl"
    write_jsonl(
        session,
        [
            {
                "type": "turn_context",
                "payload": {
                    "model": "gpt-5.5",
                    "effort": "medium",
                    "summary": "auto",
                    "collaboration_mode": {"settings": {"model": "gpt-5.5", "reasoning_effort": "medium"}},
                },
            },
            {"type": "user_message", "text": "/opsx-apply add-brand-certificate-management"},
            {
                "payload": {
                    "type": "token_count",
                    "info": {
                        "last_token_usage": {"total_tokens": 12},
                        "model_context_window": 258400,
                    },
                },
                "rate_limits": {
                    "limit_id": "codex_bengalfox",
                    "limit_name": "GPT-5.3-Codex-Spark",
                },
            },
        ],
    )

    records, _ = ai_usage.parse_session_jsonl(session)
    record = records[0]

    assert record["model_name"] == "gpt-5.5"
    assert record["reasoning_effort"] == "medium"
    assert record["reasoning_summary"] == "auto"
    assert record["model_rate_limit_name"] == "GPT-5.3-Codex-Spark"
    assert record["model_speed_tier"] == "frontier"
    assert record["model_context_window"] == 258400


def test_turn_hash_stays_stable_when_session_file_grows(tmp_path: Path) -> None:
    session = tmp_path / "rollout-stable.jsonl"
    write_jsonl(
        session,
        [
            {"type": "user_message", "text": "/sprint-propose REQ-0038 sprint-007"},
            {"payload": {"type": "token_count", "last_token_usage": {"total_tokens": 10}}},
        ],
    )
    first_records, _ = ai_usage.parse_session_jsonl(session)

    with session.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps({"type": "user_message", "text": "later follow-up"}, ensure_ascii=False) + "\n")
        handle.write(json.dumps({"payload": {"type": "token_count", "last_token_usage": {"total_tokens": 3}}}, ensure_ascii=False) + "\n")

    second_records, _ = ai_usage.parse_session_jsonl(session)

    assert second_records[0]["source_session_hash"] == first_records[0]["source_session_hash"]
    assert second_records[0]["turn_hash"] == first_records[0]["turn_hash"]
    assert len(second_records) == 2


def test_classify_text_only_treats_command_position_skill_links_as_workflow_events() -> None:
    invoked = ai_usage.classify_text("[$sprint-propose](/project/.agents/skills/sprint-propose/SKILL.md) REQ-0038 sprint-007")
    mentioned = ai_usage.classify_text("这个命令[$sprint-propose](/project/.agents/skills/sprint-propose/SKILL.md) REQ-0038 没有生成 usage")
    release_invoked = ai_usage.classify_text("/release-prepare v0.1.0 sprint-007 add-brand-certificate-management")

    assert invoked["workflow_event"] == "sprint.propose"
    assert mentioned["workflow_event"] is None
    assert release_invoked["workflow_event"] == "release.prepare"
    assert release_invoked["release_version"] == "v0.1.0"


def test_canonicalize_issue_ids_collapses_short_requirement_alias() -> None:
    values = ["REQ-0038", "REQ-0038-brand-certificate-management"]

    assert ai_usage.canonicalize_issue_ids(values, canonical_map={}) == ["REQ-0038-brand-certificate-management"]


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
    assert snapshot["coverage"]["bugs"] == [
        "BUG-0062-archive-issue-subdoc-status-consistency",
        "BUG-0063-archived-change-trace-fallback-summary",
    ]
    assert snapshot["coverage"]["changes"] == ["fix-archive-trace-fallback-summary-gate"]
    assert snapshot["totals"]["command_run_count"] == 1
    assert snapshot["totals"]["tool_call_count"] == 2
    assert snapshot["totals"]["tool_output_chars"] == 14
    assert snapshot["totals"]["retry_count"] == 1
    assert snapshot["totals"]["total_tokens"] == 25
    assert snapshot["by_workflow_event"]["opsx.apply"]["command_run_count"] == 1
    assert records[0]["retry_count_method"] == "tool_result_error_count"


def test_aggregate_sprint_normalizes_requirement_coverage_aliases() -> None:
    snapshot = ai_usage.aggregate_sprint(
        [
            {
                "turn_hash": "a",
                "sprint_id": "sprint-007",
                "workflow_event": "sprint.propose",
                "source_data_file": "~/.codex/sessions/2026/07/14/session.jsonl",
                "requirements": ["REQ-0038", "REQ-0038-brand-certificate-management"],
                "bugs": [],
                "changes": ["add-brand-certificate-management"],
                "total_tokens": 1,
            }
        ],
        "sprint-007",
    )

    assert snapshot["coverage"]["requirements"] == ["REQ-0038-brand-certificate-management"]
    assert snapshot["source_data_files"] == ["~/.codex/sessions/2026/07/14/session.jsonl"]


def test_aggregate_sprint_groups_model_metadata() -> None:
    snapshot = ai_usage.aggregate_sprint(
        [
            {
                "turn_hash": "a",
                "sprint_id": "sprint-007",
                "workflow_event": "sprint.propose",
                "source_data_file": "~/.codex/sessions/2026/07/14/session.jsonl",
                "requirements": ["REQ-0038-brand-certificate-management"],
                "bugs": [],
                "changes": ["add-brand-certificate-management"],
                "model_name": "gpt-5.5",
                "model_provider": "openai",
                "reasoning_effort": "medium",
                "reasoning_summary": "auto",
                "model_speed_tier": "frontier",
                "model_rate_limit_name": "GPT-5.5",
                "model_context_window": 258400,
                "model_call_count": 2,
                "total_tokens": 30,
            }
        ],
        "sprint-007",
    )

    assert snapshot["models"] == [
        {
            "model_name": "gpt-5.5",
            "model_provider": "openai",
            "reasoning_effort": "medium",
            "reasoning_summary": "auto",
            "model_speed_tier": "frontier",
            "model_rate_limit_name": "GPT-5.5",
            "model_context_window": 258400,
        }
    ]
    assert snapshot["source_data_files"] == ["~/.codex/sessions/2026/07/14/session.jsonl"]
    assert snapshot["by_model"]["gpt-5.5|medium|frontier"]["total_tokens"] == 30
    assert snapshot["by_model"]["gpt-5.5|medium|frontier"]["model_call_count"] == 2


def test_opsx_records_infer_linked_requirement_from_change(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.chdir(tmp_path)
    req_dir = tmp_path / "issues" / "requirements" / "review" / "REQ-0038-brand-certificate-management"
    req_dir.mkdir(parents=True)
    (req_dir / "trace.md").write_text(
        "openspec_changes:\n  - change_id: add-brand-certificate-management\n",
        encoding="utf-8",
    )
    change_dir = tmp_path / "openspec" / "changes" / "add-brand-certificate-management"
    change_dir.mkdir(parents=True)
    (change_dir / "trace.md").write_text(
        "source_requirement: REQ-0038-brand-certificate-management\n",
        encoding="utf-8",
    )

    record = ai_usage.normalize_record_issues(
        {
            "workflow_event": "opsx.apply",
            "requirements": [],
            "bugs": [],
            "changes": ["add-brand-certificate-management"],
        }
    )

    assert record["requirements"] == ["REQ-0038-brand-certificate-management"]
    assert record["bugs"] == []


def test_opsx_records_infer_linked_requirement_from_archived_change(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.chdir(tmp_path)
    req_dir = tmp_path / "issues" / "requirements" / "review" / "REQ-0038-brand-certificate-management"
    req_dir.mkdir(parents=True)
    archived_change_dir = tmp_path / "openspec" / "changes" / "archive" / "2026-07-15-add-brand-certificate-management"
    archived_change_dir.mkdir(parents=True)
    (archived_change_dir / "trace.md").write_text(
        "change_id: add-brand-certificate-management\nsource_requirement: REQ-0038-brand-certificate-management\n",
        encoding="utf-8",
    )

    record = ai_usage.normalize_record_issues(
        {
            "workflow_event": "opsx.archive",
            "requirements": [],
            "bugs": [],
            "changes": ["add-brand-certificate-management"],
        }
    )

    assert record["requirements"] == ["REQ-0038-brand-certificate-management"]
    assert record["bugs"] == []


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

    assert mapped[0]["requirements"] == ["REQ-0034-ai-token-usage-observability"]
    assert mapped[0]["bugs"] == ["BUG-0063-archived-change-trace-fallback-summary"]
    assert mapped[0]["command"] == "multi-issue"
    assert mapped[1]["sprint_id"] == "sprint-006"
    assert mapped[1]["changes"] == ["add-ai-token-usage-observability"]
    assert mapped[1]["attribution_confidence"] == "medium"


def test_manual_mapping_can_mark_post_command_target(tmp_path: Path) -> None:
    session = tmp_path / "session.jsonl"
    write_jsonl(
        session,
        [
            {"type": "user_message", "text": "/sprint-propose REQ-0038 sprint-007 add-brand-certificate-management"},
            {"payload": {"type": "token_count", "last_token_usage": {"total_tokens": 34}}},
            {"type": "user_message", "text": "后续排查 REQ-0038 sprint-007 add-brand-certificate-management"},
            {"payload": {"type": "token_count", "last_token_usage": {"total_tokens": 999}}},
        ],
    )
    records, _ = ai_usage.parse_session_jsonl(session)

    mapped = ai_usage.apply_manual_mapping(
        records,
        {
            records[0]["turn_hash"]: {
                "post_command_target": True,
                "workflow_event": "sprint.propose",
            }
        },
    )
    target = ai_usage.select_workflow_context_record(
        mapped,
        workflow_event="sprint.propose",
        requirements=["REQ-0038"],
        changes=["add-brand-certificate-management"],
        sprint_id="sprint-007",
    )

    assert target == mapped[0]


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
    assert "warnings" not in records[0]
    with pytest.raises(ValueError):
        ai_usage.assert_record_safe({"path": "/Users/example/project"})
    with pytest.raises(ValueError):
        ai_usage.assert_record_safe({"prompt": "do not persist"})


def test_safety_allows_workflow_ids_containing_password_or_token() -> None:
    ai_usage.assert_record_safe(
        {
            "turn_hash": "abc",
            "workflow_event": "release.prepare",
            "bugs": ["BUG-0061-change-password-policy-error-message-unclear"],
            "changes": [
                "fix-change-password-policy-error-message",
                "add-auto-token-fact-source-for-workflow-commands",
            ],
        }
    )


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
    command_files = list((out_dir / "command-runs").rglob("*.json"))
    assert len(command_files) == 1
    command_path = command_files[0]
    sprint_path = out_dir / "sprints" / "sprint-007.json"
    assert command_path.exists()
    assert command_path.relative_to(out_dir / "command-runs").parts[:2] == (
        "issues",
        "REQ-0037-auto-token-fact-source-for-workflow-commands",
    )
    assert command_path.name.startswith("2026-07-12--opsx.apply--")
    assert command_path.name.endswith(f"{ai_usage.session_source_hash(session, session.read_bytes())[:16]}.json")
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
    assert summary["session_input"] == "unavailable"
    assert "session-jsonl-missing" in summary["warnings"]
    assert summary["recommended_action"]


def test_compact_post_command_summary_uses_standard_field_allowlist() -> None:
    summary = ai_usage.compact_post_command_summary(
        {
            "status": "ok",
            "usage_mode": "actual",
            "command_run_count": 1,
            "session_input": "auto",
            "outputs": {"command_runs": "local.json"},
            "sprint_snapshot": {"status": "skipped", "path": None, "reason": "no-sprint"},
            "release_artifact": {"status": "skipped", "path": None, "reason": "no-release"},
            "warnings": ["unsafe-records-skipped:1"],
            "warning_count": 1,
            "recommended_action": None,
        }
    )

    assert list(summary) == [
        "status",
        "usage_mode",
        "command_run_count",
        "sprint_snapshot",
        "warning_count",
        "recommended_action",
    ]
    assert "outputs" not in summary
    assert "warnings" not in summary
    assert "session_input" not in summary
    assert "release_artifact" not in summary


def test_compact_post_command_summary_preserves_release_contract() -> None:
    summary = ai_usage.compact_post_command_summary(
        {
            "status": "ok",
            "usage_mode": "actual",
            "command_run_count": 1,
            "session_input": "auto",
            "sprint_snapshot": {"status": "skipped", "path": None, "reason": "no-sprint"},
            "release_artifact": {"status": "refreshed", "path": "release.publish.json", "reason": None},
            "warning_count": 0,
            "recommended_action": None,
        },
        include_release=True,
    )

    assert summary["session_input"] == "auto"
    assert summary["release_artifact"]["status"] == "refreshed"


def test_post_command_hook_cli_json_prints_compact_summary(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    session = tmp_path / "session.jsonl"
    out_dir = tmp_path / "ai-usage"
    write_jsonl(
        session,
        [
            {"type": "user_message", "text": "/opsx-propose compact-workflow-hook-summary"},
            {"payload": {"type": "token_count", "last_token_usage": {"total_tokens": 9}}},
        ],
    )

    exit_code = ai_usage.main(
        [
            "--post-command-hook",
            "--workflow-event",
            "opsx.propose",
            "--change",
            "compact-workflow-hook-summary",
            "--session-jsonl",
            str(session),
            "--out-dir",
            str(out_dir),
            "--json",
        ]
    )

    payload = json.loads(capsys.readouterr().out)
    assert exit_code == 0
    assert list(payload) == [
        "status",
        "usage_mode",
        "command_run_count",
        "sprint_snapshot",
        "warning_count",
        "recommended_action",
    ]
    assert "outputs" not in payload
    assert "warnings" not in payload
    assert "session_input" not in payload
    assert payload["sprint_snapshot"]["status"] == "skipped"


def test_post_command_hook_auto_discovers_session_by_workflow_context(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    sessions_dir = tmp_path / "sessions"
    sessions_dir.mkdir()
    unrelated = sessions_dir / "unrelated.jsonl"
    write_jsonl(
        unrelated,
        [
            {"type": "user_message", "text": "/req-capture REQ-0001"},
            {"payload": {"type": "token_count", "last_token_usage": {"total_tokens": 1}}},
        ],
    )
    session = sessions_dir / "rollout.jsonl"
    write_jsonl(
        session,
        [
            {"type": "user_message", "text": "/sprint-propose REQ-0038 sprint-007"},
            {"payload": {"type": "token_count", "last_token_usage": {"input_tokens": 30, "output_tokens": 4, "total_tokens": 34}}},
            {"type": "user_message", "text": "follow-up"},
            {"payload": {"type": "token_count", "last_token_usage": {"input_tokens": 3, "output_tokens": 2, "total_tokens": 5}}},
        ],
    )
    monkeypatch.setenv("AI_USAGE_SESSIONS_DIR", str(sessions_dir))

    out_dir = tmp_path / "ai-usage"
    summary = ai_usage.post_command_hook(
        session_jsonl=None,
        out_dir=out_dir,
        workflow_event="sprint.propose",
        requirements=["REQ-0038-brand-certificate-management"],
        changes=["add-brand-certificate-management"],
        sprint_id="sprint-007",
    )

    assert summary["status"] == "ok"
    assert summary["usage_mode"] == "actual"
    assert summary["command_run_count"] == 1
    assert summary["session_input"] == "auto"
    assert summary["sprint_snapshot"]["status"] == "refreshed"
    command_files = list((out_dir / "command-runs").rglob("*.json"))
    assert len(command_files) == 1
    command_path = command_files[0]
    payload = json.loads(command_path.read_text())
    sprint_run = payload["command_runs"][0]
    assert len(payload["command_runs"]) == 1
    assert sprint_run["workflow_event"] == "sprint.propose"
    assert sprint_run["sprint_id"] == "sprint-007"
    assert "REQ-0038-brand-certificate-management" in sprint_run["requirements"]
    assert "add-brand-certificate-management" in sprint_run["changes"]
    assert str(tmp_path) not in json.dumps(summary)


def test_post_command_hook_merges_multiple_target_runs_from_same_session(tmp_path: Path) -> None:
    session = tmp_path / "session.jsonl"
    out_dir = tmp_path / "ai-usage"
    write_jsonl(
        session,
        [
            {"type": "user_message", "text": "/req-opsx REQ-0038 add-brand-certificate-management"},
            {"payload": {"type": "token_count", "last_token_usage": {"total_tokens": 21}}},
            {"type": "user_message", "text": "/sprint-propose REQ-0038 sprint-007 add-brand-certificate-management"},
            {"payload": {"type": "token_count", "last_token_usage": {"total_tokens": 34}}},
        ],
    )

    ai_usage.post_command_hook(
        session_jsonl=session,
        out_dir=out_dir,
        workflow_event="req.opsx",
        requirements=["REQ-0038-brand-certificate-management"],
        changes=["add-brand-certificate-management"],
    )
    ai_usage.post_command_hook(
        session_jsonl=session,
        out_dir=out_dir,
        workflow_event="sprint.propose",
        requirements=["REQ-0038-brand-certificate-management"],
        changes=["add-brand-certificate-management"],
        sprint_id="sprint-007",
    )

    command_files = list((out_dir / "command-runs").rglob("*.json"))
    assert len(command_files) == 1
    command_path = command_files[0]
    payload = json.loads(command_path.read_text())
    events = sorted(record["workflow_event"] for record in payload["command_runs"])
    snapshot = json.loads((out_dir / "sprints" / "sprint-007.json").read_text())

    assert events == ["req.opsx", "sprint.propose"]
    assert snapshot["totals"]["command_run_count"] == 1
    assert snapshot["totals"]["total_tokens"] == 34


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


def test_command_run_without_issue_uses_change_scope_directory(tmp_path: Path) -> None:
    session = tmp_path / "session.jsonl"
    out_dir = tmp_path / "ai-usage"
    write_jsonl(
        session,
        [
            {"type": "user_message", "text": "/opsx-explore standalone-change"},
            {"payload": {"type": "token_count", "last_token_usage": {"total_tokens": 8}}},
        ],
    )

    ai_usage.post_command_hook(
        session_jsonl=session,
        out_dir=out_dir,
        workflow_event="opsx.explore",
        changes=["standalone-change"],
    )

    command_files = list((out_dir / "command-runs").rglob("*.json"))
    assert len(command_files) == 1
    assert command_files[0].relative_to(out_dir / "command-runs").parts[:2] == ("opsxs", "standalone-change")
    assert command_files[0].name.startswith("unknown-date--opsx.explore--")


def test_post_command_hook_supports_release_events_without_sprint_snapshot(tmp_path: Path) -> None:
    session = tmp_path / "session.jsonl"
    out_dir = tmp_path / "ai-usage"
    write_jsonl(
        session,
        [
            {"type": "user_message", "text": "/release-publish v0.1.0 add-brand-certificate-management"},
            {"payload": {"type": "token_count", "last_token_usage": {"input_tokens": 8, "output_tokens": 2, "total_tokens": 10}}},
        ],
    )

    summary = ai_usage.post_command_hook(
        session_jsonl=session,
        out_dir=out_dir,
        workflow_event="release.publish",
        release_version="v0.1.0",
        release_sprints=["sprint-005", "sprint-006"],
        changes=["add-brand-certificate-management"],
    )

    command_files = [
        path
        for path in (out_dir / "command-runs").rglob("*.json")
        if path.name.startswith("2026-") or path.name.startswith("unknown-date--")
    ]
    assert len(command_files) == 1
    assert command_files[0].relative_to(out_dir / "command-runs").parts[:2] == ("releases", "v0.1.0")
    payload = json.loads(command_files[0].read_text())
    release_path = out_dir / "command-runs" / "releases" / "v0.1.0" / "release.publish.json"
    release_payload = json.loads(release_path.read_text())

    assert summary["status"] == "ok"
    assert summary["usage_mode"] == "actual"
    assert summary["outputs"]["release"] == "release.publish.json"
    assert summary["release_artifact"]["status"] == "refreshed"
    assert summary["release_artifact"]["path"] == "release.publish.json"
    assert summary["sprint_snapshot"]["status"] == "skipped"
    assert summary["sprint_snapshot"]["reason"] == "no-sprint"
    assert payload["command_runs"][0]["workflow_event"] == "release.publish"
    assert payload["command_runs"][0]["release_version"] == "v0.1.0"
    assert payload["command_runs"][0]["release_sprints"] == ["sprint-005", "sprint-006"]
    assert release_payload["release_version"] == "v0.1.0"
    assert release_payload["workflow_event"] == "release.publish"
    assert release_payload["totals"]["command_run_count"] == 1
    assert release_payload["coverage"]["changes"] == ["add-brand-certificate-management"]
    assert release_payload["coverage"]["sprints"] == ["sprint-005", "sprint-006"]


def test_post_command_hook_skips_unsafe_records_without_crashing(tmp_path: Path) -> None:
    session = tmp_path / "session.jsonl"
    out_dir = tmp_path / "ai-usage"
    write_jsonl(
        session,
        [
            {"type": "user_message", "text": "/release-prepare v0.0.3"},
            {"payload": {"type": "token_count", "last_token_usage": {"total_tokens": 10}}},
        ],
    )

    summary = ai_usage.post_command_hook(
        session_jsonl=session,
        out_dir=out_dir,
        workflow_event="release.prepare",
        changes=["/Users/example/unsafe-change"],
        sprint_id="sprint-007",
    )

    assert summary["status"] == "warning"
    assert summary["usage_mode"] == "unavailable"
    assert summary["command_run_count"] == 0
    assert "unsafe-records-skipped:1" in summary["warnings"]
    assert "no-safe-command-runs" in summary["warnings"]
    assert summary["sprint_snapshot"]["status"] == "skipped"
    assert not list((out_dir / "command-runs").rglob("*.json"))
