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
    change_dir = root / "openspec" / "changes" / "archive" / "2026-07-02-add-demo"
    change_dir.mkdir(parents=True)
    (change_dir / "tasks.md").write_text("- [x] implement\n- [x] test\n", encoding="utf-8")
    (change_dir / "trace.md").write_text("---\nstatus: done\n---\n", encoding="utf-8")
    (change_dir / "proposal.md").write_text("REQ-9999 BUG-9999\n", encoding="utf-8")


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


def test_render_markdown_includes_evidence_hints(tmp_path: Path) -> None:
    seed_project(tmp_path)
    fact_sheet = generate_sprint_fact_sheet.build_fact_sheet("sprint-999", root=tmp_path)

    markdown = generate_sprint_fact_sheet.render_markdown(fact_sheet)

    assert "# Sprint Fact Sheet: sprint-999" in markdown
    assert "## Evidence Hints" in markdown
    assert "openspec/changes/archive/2026-07-02-add-demo/tasks.md" in markdown


def test_fact_sheet_reads_ai_usage_snapshot(tmp_path: Path) -> None:
    seed_project(tmp_path)
    snapshot_dir = tmp_path / "data" / "ai-usage" / "sprints"
    snapshot_dir.mkdir(parents=True)
    (snapshot_dir / "sprint-999.json").write_text(
        json.dumps(
            {
                "sprint_id": "sprint-999",
                "estimated": False,
                "totals": {
                    "command_run_count": 2,
                    "model_call_count": 3,
                    "total_tokens": 123,
                },
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
    assert fact_sheet["ai_usage_snapshot"]["totals"]["total_tokens"] == 123
    assert "## AI Usage Snapshot" in markdown
    assert "| total_tokens | 123 |" in markdown


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
