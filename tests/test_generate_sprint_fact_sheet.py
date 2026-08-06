from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "generate-sprint-fact-sheet.py"
sys.path.insert(0, str(ROOT / "scripts"))
SPEC = importlib.util.spec_from_file_location("generate_sprint_fact_sheet", SCRIPT)
assert SPEC and SPEC.loader
generate_sprint_fact_sheet = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = generate_sprint_fact_sheet
SPEC.loader.exec_module(generate_sprint_fact_sheet)


def write_sprint(root: Path) -> None:
    sprint_dir = root / "iterations" / "archive" / "sprint-999"
    sprint_dir.mkdir(parents=True)
    (sprint_dir / "sprint.yaml").write_text(
        "\n".join(
            [
                "sprint_id: sprint-999",
                "status: completed",
                "lifecycle_stage: archive",
                "start_date: 2026-07-01 09:00:00",
                "end_date: 2026-07-02 18:00:00",
                "capacity:",
                "  developers: 1",
                "  testers: 1",
                "requirements:",
                "  - REQ-9999-demo",
                "bugs:",
                "  - BUG-9999-demo",
                "changes:",
                "  - add-demo",
                "estimated_story_points: 3",
                "estimated_person_days: 1.5",
                "",
            ]
        ),
        encoding="utf-8",
    )
    (sprint_dir / "sprint.md").write_text("# Sprint\n", encoding="utf-8")
    (sprint_dir / "release-note.md").write_text("# Release\n", encoding="utf-8")
    (sprint_dir / "acceptance-report.md").write_text(
        "# Acceptance\n\n**Verdict:** PASS\n",
        encoding="utf-8",
    )


def write_issue(root: Path, base: str, issue_id: str, trace: str) -> None:
    issue_dir = root / base / "archive" / issue_id
    issue_dir.mkdir(parents=True)
    (issue_dir / "trace.md").write_text(trace, encoding="utf-8")


def write_change(root: Path) -> None:
    change_dir = root / "openspec" / "archive" / "2026-07-02-add-demo"
    change_dir.mkdir(parents=True)
    (change_dir / "tasks.md").write_text("- [x] implement\n- [x] test\n", encoding="utf-8")
    (change_dir / "trace.md").write_text("---\nstatus: done\n---\n", encoding="utf-8")
    (change_dir / "proposal.md").write_text("REQ-9999 BUG-9999\n", encoding="utf-8")


def write_large_sprint(root: Path, change_count: int = 11) -> list[str]:
    change_ids = [f"add-batch-{index:02d}" for index in range(1, change_count + 1)]
    sprint_dir = root / "iterations" / "change" / "sprint-998"
    sprint_dir.mkdir(parents=True)
    (sprint_dir / "sprint.yaml").write_text(
        "\n".join(
            [
                "sprint_id: sprint-998",
                "status: in_progress",
                "lifecycle_stage: change",
                "start_date: 2026-07-01 09:00:00",
                "end_date: 2026-07-02 18:00:00",
                "requirements: []",
                "bugs: []",
                "changes:",
                *[f"  - {change_id}" for change_id in change_ids],
                "",
            ]
        ),
        encoding="utf-8",
    )
    (sprint_dir / "sprint.md").write_text("# Sprint\n", encoding="utf-8")
    (sprint_dir / "release-note.md").write_text("# Release\n", encoding="utf-8")
    (sprint_dir / "acceptance-report.md").write_text("# Acceptance\n\n**Verdict:** PASS\n", encoding="utf-8")
    for index, change_id in enumerate(change_ids, start=1):
        change_dir = root / "openspec" / "changes" / change_id
        change_dir.mkdir(parents=True)
        task_lines = ["- [x] implement", "- [x] test"]
        if index == 6:
            task_lines[-1] = "- [ ] test"
        (change_dir / "tasks.md").write_text("\n".join(task_lines) + "\n", encoding="utf-8")
        if index != 7:
            (change_dir / "trace.md").write_text("---\nstatus: applied\n---\n", encoding="utf-8")
    return change_ids


def seed_project(root: Path) -> None:
    write_sprint(root)
    write_issue(
        root,
        "issues/requirements",
        "REQ-9999-demo",
        "---\nstatus: done\n---\n```yaml\nstatus: done\nopenspec_changes:\n  - change_id: add-demo\n    status: archived\n```\n",
    )
    write_issue(
        root,
        "issues/bugs",
        "BUG-9999-demo",
        "---\nstatus: done\n---\n```yaml\nstatus: done\nrelated_change: add-demo\n```\n",
    )
    write_change(root)


def test_build_fact_sheet_collects_scope_and_tasks(tmp_path: Path) -> None:
    seed_project(tmp_path)

    fact_sheet = generate_sprint_fact_sheet.build_fact_sheet("sprint-999", root=tmp_path)

    assert fact_sheet["sprint"]["sprint_id"] == "sprint-999"
    assert fact_sheet["sprint"]["capacity"] == {"developers": "1", "testers": "1"}
    assert fact_sheet["scope"]["counts"]["requirements"] == 1
    assert fact_sheet["scope"]["counts"]["bugs"] == 1
    assert fact_sheet["scope"]["counts"]["changes"] == 1
    assert fact_sheet["scope"]["counts"]["tasks_done"] == 2
    assert fact_sheet["scope"]["counts"]["tasks_total"] == 2
    assert fact_sheet["changes"][0]["trace_exists"] is True
    assert fact_sheet["acceptance"]["signals"] == ["**Verdict:** PASS"]
    assert fact_sheet["change_batches"]["applicable"] is False
    assert fact_sheet["change_batches"]["reason"] == "not_applicable"


def test_fact_sheet_builds_change_batches_for_large_sprint(tmp_path: Path) -> None:
    change_ids = write_large_sprint(tmp_path)

    fact_sheet = generate_sprint_fact_sheet.build_fact_sheet("sprint-998", root=tmp_path)
    batches = fact_sheet["change_batches"]

    assert batches["applicable"] is True
    assert batches["total_changes"] == 11
    assert batches["batch_count"] == 3
    assert batches["batches"][0]["change_ids"] == change_ids[:5]
    assert batches["batches"][1]["counts"]["tasks_done"] == 9
    assert batches["batches"][1]["counts"]["tasks_total"] == 10
    assert batches["batches"][1]["counts"]["trace_missing"] == 1
    assert batches["batches"][1]["warning_labels"]["change-tasks-incomplete"] == 1
    assert batches["batches"][1]["warning_labels"]["change-trace-missing"] == 1


def test_fact_sheet_summary_includes_compact_change_batches(tmp_path: Path) -> None:
    write_large_sprint(tmp_path)

    fact_sheet = generate_sprint_fact_sheet.build_fact_sheet("sprint-998", root=tmp_path)
    summary = generate_sprint_fact_sheet.build_summary(fact_sheet)

    assert summary["change_batches"]["applicable"] is True
    assert summary["change_batches"]["batch_count"] == 3
    assert "evidence_hints" not in summary["change_batches"]["batches"][0]


def test_acceptance_summary_prioritizes_final_sections_over_raw_ac(tmp_path: Path) -> None:
    seed_project(tmp_path)
    report = tmp_path / "iterations" / "archive" / "sprint-999" / "acceptance-report.md"
    report.write_text(
        """# Acceptance

## 最终验收摘要

| 项 | 当前状态 | 说明 |
|---|---|---|
| 最终结论 | PASS | 通过归档判断 |

## 最终归档检查

| Gate | 当前结论 |
|---|---|
| Readiness | PASS |

## 原始 AC 引用

- [ ] 历史追溯：未完成的旧 AC，不作为最终归档判断。
""",
        encoding="utf-8",
    )

    summary = generate_sprint_fact_sheet.acceptance_summary(report.parent, tmp_path)

    assert any("PASS" in signal for signal in summary["signals"])
    assert not any("未完成的旧 AC" in signal for signal in summary["signals"])


def test_build_fact_sheet_handles_missing_acceptance_report(tmp_path: Path) -> None:
    seed_project(tmp_path)
    report = tmp_path / "iterations" / "archive" / "sprint-999" / "acceptance-report.md"
    report.unlink()

    fact_sheet = generate_sprint_fact_sheet.build_fact_sheet("sprint-999", root=tmp_path)

    assert fact_sheet["acceptance"]["exists"] is False
    assert fact_sheet["acceptance"]["signals"] == []
    assert "change_batches" in fact_sheet


def test_render_markdown_includes_evidence_hints(tmp_path: Path) -> None:
    seed_project(tmp_path)
    fact_sheet = generate_sprint_fact_sheet.build_fact_sheet("sprint-999", root=tmp_path)

    markdown = generate_sprint_fact_sheet.render_markdown(fact_sheet)

    assert "# Sprint Fact Sheet: sprint-999" in markdown
    assert "## Evidence Hints" in markdown
    assert "openspec/archive/2026-07-02-add-demo/tasks.md" in markdown


def test_fact_sheet_exposes_archived_path_residual_warnings(tmp_path: Path) -> None:
    seed_project(tmp_path)
    trace = tmp_path / "issues" / "requirements" / "archive" / "REQ-9999-demo" / "trace.md"
    trace.write_text("Old link: iterations/change/sprint-999/sprint.md\n", encoding="utf-8")

    fact_sheet = generate_sprint_fact_sheet.build_fact_sheet("sprint-999", root=tmp_path)

    residuals = fact_sheet["archived_path_residuals"]
    assert residuals["ok"] is False
    assert residuals["residual_count"] == 1
    assert any(warning["kind"] == "archived-path-residual" for warning in fact_sheet["warnings"])
    assert any("Archived path residual" in hint["reason"] for hint in fact_sheet["evidence_hints"])


def test_summary_exposes_compact_detail_signals_without_evidence_hints(tmp_path: Path) -> None:
    seed_project(tmp_path)
    trace = tmp_path / "issues" / "requirements" / "archive" / "REQ-9999-demo" / "trace.md"
    trace.write_text("Old link: iterations/change/sprint-999/sprint.md\n", encoding="utf-8")

    fact_sheet = generate_sprint_fact_sheet.build_fact_sheet("sprint-999", root=tmp_path)
    summary = generate_sprint_fact_sheet.build_summary(fact_sheet)

    assert summary["sprint"]["sprint_id"] == "sprint-999"
    assert summary["scope"]["counts"]["changes"] == 1
    assert summary["tasks"] == {"done": 2, "total": 2}
    assert summary["needs_detail"] is True
    assert summary["warnings"]["count"] == 1
    assert summary["detail_triggers"]["evidence_hint_count"] == len(fact_sheet["evidence_hints"])
    assert "evidence_hints" not in summary


def test_select_fields_can_return_evidence_hints_and_nested_values(tmp_path: Path) -> None:
    seed_project(tmp_path)
    fact_sheet = generate_sprint_fact_sheet.build_fact_sheet("sprint-999", root=tmp_path)

    selected = generate_sprint_fact_sheet.select_fields(
        fact_sheet,
        ["evidence_hints", "ai_usage_snapshot.snapshot_status"],
    )

    assert selected["evidence_hints"] == fact_sheet["evidence_hints"]
    assert selected["ai_usage_snapshot.snapshot_status"] == "missing"


def test_select_fields_can_return_full_ai_usage_matrices(tmp_path: Path) -> None:
    seed_project(tmp_path)
    snapshot_dir = tmp_path / "data" / "ai-usage" / "sprints"
    snapshot_dir.mkdir(parents=True)
    usage_matrices = {
        "metrics": ["total_tokens"],
        "columns": [{"key": "opsx.apply", "label": "Opsx-Apply"}],
        "rows": [
            {
                "object_id": "Total",
                "metrics": {"total_tokens": {"Opsx-Apply": 123}},
            }
        ],
    }
    (snapshot_dir / "sprint-999.json").write_text(
        json.dumps(
            {
                "sprint_id": "sprint-999",
                "generated_at": "2026-07-03T00:00:00Z",
                "estimated": False,
                "coverage": {
                    "requirements": ["REQ-9999-demo"],
                    "bugs": ["BUG-9999-demo"],
                    "changes": ["add-demo"],
                },
                "totals": {"command_run_count": 1, "model_call_count": 1, "total_tokens": 123},
                "usage_matrices": usage_matrices,
                "warnings": [],
            }
        ),
        encoding="utf-8",
    )

    fact_sheet = generate_sprint_fact_sheet.build_fact_sheet("sprint-999", root=tmp_path)
    selected = generate_sprint_fact_sheet.select_fields(
        fact_sheet,
        ["ai_usage_snapshot.usage_matrices"],
    )

    assert selected["ai_usage_snapshot.usage_matrices"] == usage_matrices


def test_render_ai_usage_retrospective_section_outputs_sprint_015_style_tables(tmp_path: Path) -> None:
    seed_project(tmp_path)
    snapshot_dir = tmp_path / "data" / "ai-usage" / "sprints"
    snapshot_dir.mkdir(parents=True)
    (snapshot_dir / "sprint-999.json").write_text(
        json.dumps(
            {
                "sprint_id": "sprint-999",
                "generated_at": "2026-07-03T00:00:00Z",
                "estimated": False,
                "coverage": {
                    "requirements": ["REQ-9999-demo"],
                    "bugs": ["BUG-9999-demo"],
                    "changes": ["add-demo"],
                },
                "totals": {
                    "command_run_count": 2,
                    "model_call_count": 3,
                    "tool_call_count": 4,
                    "input_tokens": 1000,
                    "cached_input_tokens": 800,
                    "output_tokens": 50,
                    "reasoning_output_tokens": 5,
                    "total_tokens": 1055,
                    "retry_count": 0,
                },
                "usage_matrices": {
                    "metrics": ["total_tokens", "input_tokens", "output_tokens", "model_call_count"],
                    "columns": [{"key": "opsx.apply", "label": "Opsx-Apply"}],
                    "rows": [
                        {
                            "object_id": "Total",
                            "metrics": {
                                "total_tokens": {"Opsx-Apply": 1055},
                                "input_tokens": {"Opsx-Apply": 1000},
                                "output_tokens": {"Opsx-Apply": 50},
                                "model_call_count": {"Opsx-Apply": 3},
                            },
                        },
                        {
                            "object_id": "sprint-999",
                            "metrics": {
                                "total_tokens": {"Opsx-Apply": 1055},
                                "input_tokens": {"Opsx-Apply": 1000},
                                "output_tokens": {"Opsx-Apply": 50},
                                "model_call_count": {"Opsx-Apply": 3},
                            },
                        },
                    ],
                },
                "warnings": [],
            }
        ),
        encoding="utf-8",
    )

    fact_sheet = generate_sprint_fact_sheet.build_fact_sheet("sprint-999", root=tmp_path)
    markdown = generate_sprint_fact_sheet.render_ai_usage_retrospective_section(fact_sheet)

    assert markdown.startswith("## 模型 Token 使用分析")
    assert "### Token Usage Fact Sheet" in markdown
    assert "| 精确 token 统计 | 有 | 来源：`data/ai-usage/sprints/sprint-999.json` |" in markdown
    assert "| total_tokens | 1,055 | snapshot totals |" in markdown
    assert "### total_tokens 矩阵" in markdown
    assert "### input_tokens 矩阵" in markdown
    assert "### output_tokens 矩阵" in markdown
    assert "### model_call_count 矩阵" in markdown
    assert "| 对象 | Opsx-Apply |" in markdown
    assert "| Total | 1055 |" in markdown
    assert "矩阵口径" in markdown


def test_fact_sheet_reads_ai_usage_snapshot(tmp_path: Path) -> None:
    seed_project(tmp_path)
    snapshot_dir = tmp_path / "data" / "ai-usage" / "sprints"
    snapshot_dir.mkdir(parents=True)
    (snapshot_dir / "sprint-999.json").write_text(
        json.dumps(
            {
                "sprint_id": "sprint-999",
                "generated_at": "2026-07-03T00:00:00Z",
                "estimated": False,
                "coverage": {
                    "requirements": ["REQ-9999-demo"],
                    "bugs": ["BUG-9999-demo"],
                    "changes": ["add-demo"],
                },
                "totals": {
                    "command_run_count": 2,
                    "model_call_count": 3,
                    "total_tokens": 123,
                },
                "usage_matrices": {"by_issue": [], "by_change": []},
                "by_workflow_event": {"sprint.apply": {"command_run_count": 2}},
                "warnings": [],
            }
        ),
        encoding="utf-8",
    )

    fact_sheet = generate_sprint_fact_sheet.build_fact_sheet("sprint-999", root=tmp_path)
    markdown = generate_sprint_fact_sheet.render_markdown(fact_sheet)

    assert fact_sheet["ai_usage_snapshot"]["exists"] is True
    assert fact_sheet["ai_usage_snapshot"]["estimated"] is False
    assert fact_sheet["ai_usage_snapshot"]["ai_usage_mode"] == "actual"
    assert fact_sheet["ai_usage_snapshot"]["snapshot_status"] == "present"
    assert fact_sheet["ai_usage_snapshot"]["fresh_gate"]["status"] == "pass"
    assert fact_sheet["ai_usage_snapshot"]["totals"]["total_tokens"] == 123
    assert "## AI Usage Snapshot" in markdown
    assert "| Mode | actual |" in markdown
    assert "| Fresh Gate | pass |" in markdown
    assert "| total_tokens | 123 |" in markdown


def test_fact_sheet_marks_missing_ai_usage_as_estimated_fallback(tmp_path: Path) -> None:
    seed_project(tmp_path)

    fact_sheet = generate_sprint_fact_sheet.build_fact_sheet("sprint-999", root=tmp_path)
    markdown = generate_sprint_fact_sheet.render_markdown(fact_sheet)

    ai_usage = fact_sheet["ai_usage_snapshot"]
    assert ai_usage["exists"] is False
    assert ai_usage["ai_usage_mode"] == "estimated_fallback"
    assert ai_usage["snapshot_status"] == "missing"
    assert ai_usage["fresh_gate"]["status"] == "blocker"
    assert "snapshot-missing" in ai_usage["warnings"]
    assert "estimated_fallback" in markdown


def test_fact_sheet_does_not_treat_stale_snapshot_as_actual(tmp_path: Path) -> None:
    seed_project(tmp_path)
    snapshot_dir = tmp_path / "data" / "ai-usage" / "sprints"
    snapshot_dir.mkdir(parents=True)
    (snapshot_dir / "sprint-999.json").write_text(
        json.dumps(
            {
                "sprint_id": "sprint-999",
                "generated_at": "2026-07-01T00:00:00Z",
                "estimated": False,
                "coverage": {
                    "requirements": ["REQ-9999-demo"],
                    "bugs": ["BUG-9999-demo"],
                    "changes": ["add-demo"],
                },
                "totals": {"command_run_count": 1, "total_tokens": 100},
                "usage_matrices": {"by_issue": [], "by_change": []},
                "warnings": [],
            }
        ),
        encoding="utf-8",
    )

    fact_sheet = generate_sprint_fact_sheet.build_fact_sheet("sprint-999", root=tmp_path)

    ai_usage = fact_sheet["ai_usage_snapshot"]
    assert ai_usage["exists"] is True
    assert ai_usage["ai_usage_mode"] == "estimated_fallback"
    assert ai_usage["snapshot_status"] == "stale"
    assert ai_usage["fresh_gate"]["status"] == "blocker"
    assert "snapshot-stale" in ai_usage["warnings"]


def test_fact_sheet_interprets_sprint_dates_as_project_timezone(tmp_path: Path) -> None:
    seed_project(tmp_path)
    snapshot_dir = tmp_path / "data" / "ai-usage" / "sprints"
    snapshot_dir.mkdir(parents=True)
    (snapshot_dir / "sprint-999.json").write_text(
        json.dumps(
            {
                "sprint_id": "sprint-999",
                "generated_at": "2026-07-02T10:30:00Z",
                "estimated": False,
                "coverage": {
                    "requirements": ["REQ-9999-demo"],
                    "bugs": ["BUG-9999-demo"],
                    "changes": ["add-demo"],
                },
                "totals": {"command_run_count": 1, "total_tokens": 100},
                "usage_matrices": {"by_issue": [], "by_change": []},
                "warnings": [],
            }
        ),
        encoding="utf-8",
    )

    fact_sheet = generate_sprint_fact_sheet.build_fact_sheet("sprint-999", root=tmp_path)

    ai_usage = fact_sheet["ai_usage_snapshot"]
    assert ai_usage["ai_usage_mode"] == "actual"
    assert ai_usage["snapshot_status"] == "present"
    assert ai_usage["fresh_gate"]["status"] == "pass"


def test_fact_sheet_ignores_future_planned_end_date_for_ai_usage_freshness(tmp_path: Path) -> None:
    seed_project(tmp_path)
    sprint_dir = tmp_path / "iterations" / "archive" / "sprint-999"
    (sprint_dir / "sprint.yaml").write_text(
        "\n".join(
            [
                "sprint_id: sprint-999",
                "status: completed",
                "lifecycle_stage: archive",
                "start_date: 2026-07-01 09:00:00",
                "end_date: 2026-08-18 18:00:00",
                "requirements:",
                "  - REQ-9999-demo",
                "bugs:",
                "  - BUG-9999-demo",
                "changes:",
                "  - add-demo",
                "",
            ]
        ),
        encoding="utf-8",
    )
    (sprint_dir / "sprint.md").write_text(
        "---\nupdated_at: 2026-08-04 23:15:03\n---\n# Sprint\n",
        encoding="utf-8",
    )
    (sprint_dir / "release-note.md").write_text(
        "---\nupdated_at: 2026-08-04 23:15:03\n---\n# Release\n",
        encoding="utf-8",
    )
    (sprint_dir / "acceptance-report.md").write_text(
        "---\nupdated_at: 2026-08-04 23:15:03\n---\n# Acceptance\n\n**Verdict:** PASS\n",
        encoding="utf-8",
    )
    snapshot_dir = tmp_path / "data" / "ai-usage" / "sprints"
    snapshot_dir.mkdir(parents=True)
    (snapshot_dir / "sprint-999.json").write_text(
        json.dumps(
            {
                "sprint_id": "sprint-999",
                "generated_at": "2026-08-04T15:30:08Z",
                "estimated": False,
                "coverage": {
                    "requirements": ["REQ-9999-demo"],
                    "bugs": ["BUG-9999-demo"],
                    "changes": ["add-demo"],
                },
                "totals": {"command_run_count": 1, "model_call_count": 1, "total_tokens": 100},
                "usage_matrices": {"metrics": ["total_tokens"], "columns": [], "rows": []},
                "warnings": [],
            }
        ),
        encoding="utf-8",
    )

    fact_sheet = generate_sprint_fact_sheet.build_fact_sheet("sprint-999", root=tmp_path)
    summary = generate_sprint_fact_sheet.build_summary(fact_sheet)

    ai_usage = fact_sheet["ai_usage_snapshot"]
    baseline = summary["ai_usage_snapshot"]["freshness_baseline"]
    assert ai_usage["snapshot_status"] == "present"
    assert ai_usage["ai_usage_mode"] == "actual"
    assert ai_usage["fresh_gate"]["status"] == "pass"
    assert baseline["source"] == "sprint.md:updated_at"
    assert baseline["min_generated_at"] == "2026-08-04T15:15:03Z"
    assert baseline["skipped"] == [
        {
            "source": "sprint.yaml:end_date",
            "value": "2026-08-18 18:00:00",
            "reason": "future-planned-time",
        }
    ]


def test_fact_sheet_ignores_future_planned_start_date_for_ai_usage_freshness(tmp_path: Path) -> None:
    seed_project(tmp_path)
    sprint_dir = tmp_path / "iterations" / "archive" / "sprint-999"
    (sprint_dir / "sprint.yaml").write_text(
        "\n".join(
            [
                "sprint_id: sprint-999",
                "status: completed",
                "lifecycle_stage: archive",
                "start_date: 2026-08-19 09:00:00",
                "end_date: 2026-08-20 18:00:00",
                "requirements:",
                "  - REQ-9999-demo",
                "bugs:",
                "  - BUG-9999-demo",
                "changes:",
                "  - add-demo",
                "",
            ]
        ),
        encoding="utf-8",
    )
    for name in ("sprint.md", "release-note.md", "acceptance-report.md"):
        (sprint_dir / name).write_text(
            "---\nupdated_at: 2026-08-04 23:15:03\n---\n# Doc\n",
            encoding="utf-8",
        )
    snapshot_dir = tmp_path / "data" / "ai-usage" / "sprints"
    snapshot_dir.mkdir(parents=True)
    (snapshot_dir / "sprint-999.json").write_text(
        json.dumps(
            {
                "sprint_id": "sprint-999",
                "generated_at": "2026-08-04T15:30:08Z",
                "estimated": False,
                "coverage": {
                    "requirements": ["REQ-9999-demo"],
                    "bugs": ["BUG-9999-demo"],
                    "changes": ["add-demo"],
                },
                "totals": {"command_run_count": 1, "model_call_count": 1, "total_tokens": 100},
                "usage_matrices": {"metrics": ["total_tokens"], "columns": [], "rows": []},
                "warnings": [],
            }
        ),
        encoding="utf-8",
    )

    fact_sheet = generate_sprint_fact_sheet.build_fact_sheet("sprint-999", root=tmp_path)
    summary = generate_sprint_fact_sheet.build_summary(fact_sheet)

    ai_usage = fact_sheet["ai_usage_snapshot"]
    baseline = summary["ai_usage_snapshot"]["freshness_baseline"]
    assert ai_usage["snapshot_status"] == "present"
    assert ai_usage["ai_usage_mode"] == "actual"
    assert ai_usage["fresh_gate"]["status"] == "pass"
    assert baseline["source"] == "sprint.md:updated_at"
    assert baseline["min_generated_at"] == "2026-08-04T15:15:03Z"
    assert baseline["skipped"] == [
        {
            "source": "sprint.yaml:start_date",
            "value": "2026-08-19 09:00:00",
            "reason": "future-planned-time",
        },
        {
            "source": "sprint.yaml:end_date",
            "value": "2026-08-20 18:00:00",
            "reason": "future-planned-time",
        },
    ]


def test_fact_sheet_still_marks_snapshot_stale_from_updated_at_baseline(tmp_path: Path) -> None:
    seed_project(tmp_path)
    sprint_dir = tmp_path / "iterations" / "archive" / "sprint-999"
    for name in ("sprint.md", "release-note.md", "acceptance-report.md"):
        (sprint_dir / name).write_text(
            "---\nupdated_at: 2026-07-03 09:00:00\n---\n# Doc\n",
            encoding="utf-8",
        )
    snapshot_dir = tmp_path / "data" / "ai-usage" / "sprints"
    snapshot_dir.mkdir(parents=True)
    (snapshot_dir / "sprint-999.json").write_text(
        json.dumps(
            {
                "sprint_id": "sprint-999",
                "generated_at": "2026-07-03T00:30:00Z",
                "estimated": False,
                "coverage": {
                    "requirements": ["REQ-9999-demo"],
                    "bugs": ["BUG-9999-demo"],
                    "changes": ["add-demo"],
                },
                "totals": {"command_run_count": 1, "model_call_count": 1, "total_tokens": 100},
                "usage_matrices": {"metrics": ["total_tokens"], "columns": [], "rows": []},
                "warnings": [],
            }
        ),
        encoding="utf-8",
    )

    fact_sheet = generate_sprint_fact_sheet.build_fact_sheet("sprint-999", root=tmp_path)
    summary = generate_sprint_fact_sheet.build_summary(fact_sheet)

    ai_usage = fact_sheet["ai_usage_snapshot"]
    baseline = summary["ai_usage_snapshot"]["freshness_baseline"]
    assert baseline["source"] == "sprint.md:updated_at"
    assert baseline["min_generated_at"] == "2026-07-03T01:00:00Z"
    assert ai_usage["snapshot_status"] == "stale"
    assert ai_usage["ai_usage_mode"] == "estimated_fallback"
    assert ai_usage["fresh_gate"]["status"] == "blocker"
    assert "snapshot-stale" in ai_usage["warnings"]


def test_fact_sheet_summary_exposes_ai_usage_fresh_gate_without_evidence_hints(tmp_path: Path) -> None:
    seed_project(tmp_path)
    snapshot_dir = tmp_path / "data" / "ai-usage" / "sprints"
    snapshot_dir.mkdir(parents=True)
    (snapshot_dir / "sprint-999.json").write_text(
        json.dumps(
            {
                "sprint_id": "sprint-999",
                "generated_at": "2026-07-03T00:00:00Z",
                "estimated": False,
                "coverage": {
                    "requirements": ["REQ-9999-demo"],
                    "bugs": [],
                    "changes": ["add-demo"],
                },
                "totals": {"command_run_count": 1, "model_call_count": 1, "total_tokens": 100},
                "usage_matrices": {},
                "warnings": [],
            }
        ),
        encoding="utf-8",
    )

    fact_sheet = generate_sprint_fact_sheet.build_fact_sheet("sprint-999", root=tmp_path)
    summary = generate_sprint_fact_sheet.build_summary(fact_sheet)
    ai_usage = summary["ai_usage_snapshot"]
    fresh_gate = summary["ai_usage_snapshot"]["fresh_gate"]

    assert ai_usage["snapshot_status"] == "present"
    assert ai_usage["ai_usage_mode"] == "estimated_fallback"
    assert fresh_gate["status"] == "blocker"
    assert fresh_gate["generated_at"] == "2026-07-03T00:00:00Z"
    assert fresh_gate["usage_matrices_present"] is False
    assert fresh_gate["coverage_status"]["bugs"] == "missing"
    assert "bugs-coverage-missing" in fresh_gate["blockers"]
    assert "usage-matrices-missing" in fresh_gate["blockers"]
    assert "evidence_hints" not in summary


def test_large_sprint_summary_uses_compact_ai_usage_matrix_summary(tmp_path: Path) -> None:
    seed_project(tmp_path)
    change_ids = write_large_sprint(tmp_path, change_count=11)
    snapshot_dir = tmp_path / "data" / "ai-usage" / "sprints"
    snapshot_dir.mkdir(parents=True)
    (snapshot_dir / "sprint-998.json").write_text(
        json.dumps(
            {
                "sprint_id": "sprint-998",
                "generated_at": "2026-07-02T11:00:00Z",
                "estimated": False,
                "coverage": {
                    "requirements": [],
                    "bugs": [],
                    "changes": change_ids,
                },
                "totals": {"command_run_count": 1, "model_call_count": 1, "total_tokens": 123},
                "usage_matrices": {
                    "metrics": ["total_tokens"],
                    "columns": [{"key": "opsx.apply", "label": "Opsx-Apply"}],
                    "rows": [
                        {
                            "object_id": "Total",
                            "metrics": {"total_tokens": {"Opsx-Apply": 123}},
                        }
                    ],
                },
                "warnings": [],
            }
        ),
        encoding="utf-8",
    )

    fact_sheet = generate_sprint_fact_sheet.build_fact_sheet("sprint-998", root=tmp_path)
    summary = generate_sprint_fact_sheet.build_summary(fact_sheet)
    matrix_summary = summary["ai_usage_snapshot"]["usage_matrices_summary"]

    assert summary["scope"]["counts"]["changes"] == 11
    assert "usage_matrices" not in summary["ai_usage_snapshot"]
    assert matrix_summary["available"] is True
    assert matrix_summary["omitted"] is True
    assert matrix_summary["rows_count"] == 1
    assert matrix_summary["columns_count"] == 1
    assert matrix_summary["fields_path"] == "ai_usage_snapshot.usage_matrices"
    assert fact_sheet["ai_usage_snapshot"]["usage_matrices"]["rows"][0]["object_id"] == "Total"


def test_cli_json_output_is_parseable() -> None:
    result = subprocess.run(
        [sys.executable, str(SCRIPT), "--sprint", "sprint-005", "--json"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=True,
    )

    payload = json.loads(result.stdout)
    assert payload["sprint"]["sprint_id"] == "sprint-005"
    assert "changes" in payload
    assert "token_risks" in payload
    assert "evidence_hints" in payload


def test_cli_summary_output_is_compact_and_parseable() -> None:
    result = subprocess.run(
        [sys.executable, str(SCRIPT), "--sprint", "sprint-005", "--summary"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=True,
    )

    payload = json.loads(result.stdout)
    assert payload["sprint"]["sprint_id"] == "sprint-005"
    assert "token_risks" in payload
    assert "detail_triggers" in payload
    assert "usage_matrices" not in payload["ai_usage_snapshot"]
    assert "usage_matrices_summary" in payload["ai_usage_snapshot"]
    assert "evidence_hints" not in payload


def test_cli_fields_output_can_return_evidence_hints() -> None:
    result = subprocess.run(
        [sys.executable, str(SCRIPT), "--sprint", "sprint-005", "--fields", "evidence_hints"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=True,
    )

    payload = json.loads(result.stdout)
    assert "evidence_hints" in payload
    assert isinstance(payload["evidence_hints"], list)


def test_cli_ai_usage_markdown_outputs_retrospective_section() -> None:
    result = subprocess.run(
        [sys.executable, str(SCRIPT), "--sprint", "sprint-005", "--ai-usage-markdown"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=True,
    )

    assert result.stdout.startswith("## 模型 Token 使用分析")
    assert "### Token Usage Fact Sheet" in result.stdout
    assert "### total_tokens 矩阵" in result.stdout or "完整矩阵缺失" in result.stdout


def test_cli_fields_unknown_path_returns_nonzero() -> None:
    result = subprocess.run(
        [sys.executable, str(SCRIPT), "--sprint", "sprint-005", "--fields", "does_not_exist"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 3
    assert "unknown field path" in result.stderr


def test_missing_sprint_returns_nonzero() -> None:
    result = subprocess.run(
        [sys.executable, str(SCRIPT), "--sprint", "sprint-does-not-exist"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode != 0
    assert "sprint.yaml not found" in result.stderr
