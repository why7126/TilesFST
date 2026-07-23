#!/usr/bin/env python3
"""Generate a compact Sprint fact sheet for `/sprint-exps`.

The fact sheet is a read-first summary. It does not replace sprint.yaml,
trace.md, tasks.md, or acceptance reports as source files.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import timezone
from pathlib import Path
from typing import Any
from zoneinfo import ZoneInfo

from workflow_sync import collect
from workflow_sync.issue_status_residuals import scan_issue_status_residuals

import archived_path_residuals
import ai_usage
import sprint_change_batches


ROOT = Path(__file__).resolve().parents[1]
PROJECT_TZ = ZoneInfo("Asia/Shanghai")


def rel(path: Path, root: Path) -> str:
    try:
        return str(path.relative_to(root))
    except ValueError:
        return str(path)


def read_yaml_file(path: Path) -> dict[str, Any]:
    return collect.parse_simple_yaml(collect.read_text(path))


def read_sprint_yaml(path: Path) -> dict[str, Any]:
    raw = collect.read_text(path)
    data = collect.parse_simple_yaml(raw)
    capacity: dict[str, str] = {}
    in_capacity = False
    capacity_indent = 0
    for line in raw.splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        indent = len(line) - len(line.lstrip(" "))
        stripped = line.strip()
        if stripped == "capacity:":
            in_capacity = True
            capacity_indent = indent
            continue
        if in_capacity and indent <= capacity_indent:
            break
        if in_capacity and ":" in stripped:
            key, value = stripped.split(":", 1)
            capacity[key.strip()] = value.strip()
    if capacity:
        data["capacity"] = capacity
    return data


def line_count(path: Path) -> int:
    if not path.exists():
        return 0
    return len(collect.read_text(path).splitlines())


def change_dir_for(root: Path, change: collect.ChangeRecord) -> Path | None:
    if change.location == "active":
        return root / "openspec" / "changes" / change.change_id
    if change.location == "archived" and change.archive_dir:
        return root / "openspec" / "changes" / "archive" / change.archive_dir
    return None


def scan_issue_residual_status(issue: collect.IssueRecord, root: Path) -> list[dict[str, str]]:
    return [
        {"file": rel(residual.file, root), "status": residual.status}
        for residual in scan_issue_status_residuals(issue.path, issue_id=issue.issue_id)
    ]


def acceptance_summary(sprint_path: Path, root: Path) -> dict[str, Any]:
    path = sprint_path / "acceptance-report.md"
    if not path.exists():
        return {
            "path": rel(path, root),
            "exists": False,
            "line_count": 0,
            "signals": [],
        }

    text = collect.read_text(path)
    signals: list[str] = []
    preferred_sections: list[str] = []
    for heading in ("最终验收摘要", "最终归档检查", "Final Acceptance Summary", "Final Archive Check"):
        match = re.search(rf"^## {re.escape(heading)}\s*\n(.*?)(?=^##\s+|\Z)", text, re.MULTILINE | re.DOTALL)
        if match:
            preferred_sections.extend(match.group(1).splitlines())

    candidate_lines = preferred_sections or text.splitlines()
    for raw in candidate_lines:
        line = raw.strip()
        if not line:
            continue
        lower = line.lower()
        if any(keyword in lower for keyword in ("final", "verdict", "blocked")) or lower.endswith("pass"):
            signals.append(line)
        elif any(keyword in line for keyword in ("最终", "归档", "通过", "阻断", "未完成")):
            signals.append(line)
        if len(signals) >= 8:
            break

    if len(signals) < 8 and preferred_sections:
        for raw in text.splitlines():
            line = raw.strip()
            if not line or line in signals:
                continue
            lower = line.lower()
            if "原始 ac" in lower or "raw ac" in lower:
                signals.append(line)
            if len(signals) >= 8:
                break

    return {
        "path": rel(path, root),
        "exists": True,
        "line_count": line_count(path),
        "signals": signals,
    }


def ai_usage_snapshot(
    sprint_id: str,
    root: Path,
    *,
    expected_scope: dict[str, list[str]] | None = None,
    min_generated_at: str | None = None,
) -> dict[str, Any]:
    path = root / "data" / "ai-usage" / "sprints" / f"{sprint_id}.json"
    status = ai_usage.check_sprint_snapshot(
        path,
        sprint_id,
        expected_scope=expected_scope,
        min_generated_at=min_generated_at,
    )
    status["snapshot_path"] = rel(path, root)
    safe: dict[str, Any] = {
        "path": rel(path, root),
        "exists": path.exists(),
        "estimated": status["usage_mode"] != "actual",
        "ai_usage_mode": status["usage_mode"],
        "snapshot_status": status["snapshot_status"],
        "generated_at": status["generated_at"],
        "coverage": status["coverage"],
        "totals": status["totals"],
        "usage_matrices": status.get("usage_matrices") or {},
        "warnings": status["warnings"],
        "warning_count": status["warning_count"],
        "recommended_action": status["recommended_action"],
        "note": None,
    }
    if safe["ai_usage_mode"] == "estimated_fallback":
        safe["note"] = "ai_usage_mode: estimated_fallback; /sprint-exps must state reason and recommended_action."
    return safe


def project_time_to_utc_iso(value: Any) -> str | None:
    """Convert project document timestamps to timezone-aware UTC ISO for usage checks."""

    if not isinstance(value, str) or not value.strip():
        return None
    parsed = ai_usage.parse_datetime(value)
    if parsed is None:
        return value
    if re.fullmatch(r"\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}", value.strip()):
        parsed = parsed.replace(tzinfo=PROJECT_TZ)
    return parsed.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")


def build_fact_sheet(sprint_id: str, *, root: Path = ROOT) -> dict[str, Any]:
    root = root.resolve()
    previous_root = collect.ROOT
    collect.ROOT = root
    try:
        sprint = collect.load_sprint(sprint_id)
        if sprint is None:
            raise FileNotFoundError(f"sprint.yaml not found for: {sprint_id}")

        sprint_yaml = read_sprint_yaml(sprint.path / "sprint.yaml")
        issues = collect.load_all_issues()
        openspec_data = collect.run_openspec_list()

        requirements = [issues.get(issue_id) for issue_id in sprint.requirements]
        bugs = [issues.get(issue_id) for issue_id in sprint.bugs]

        issue_rows: list[dict[str, Any]] = []
        warnings: list[dict[str, str]] = []
        evidence_hints: list[dict[str, str]] = [
            {
                "reason": "Sprint machine source",
                "path": rel(sprint.path / "sprint.yaml", root),
            }
        ]

        for issue in [item for item in (*requirements, *bugs) if item is not None]:
            residuals = scan_issue_residual_status(issue, root)
            if residuals:
                warnings.append(
                    {
                        "kind": "issue-status-residual",
                        "target": issue.issue_id,
                        "detail": f"{len(residuals)} document status value(s) may need review",
                    }
                )
            issue_rows.append(
                {
                    "issue_id": issue.issue_id,
                    "kind": issue.kind,
                    "path": rel(issue.path, root),
                    "stage": issue.path.parent.name,
                    "trace_status": issue.trace_status,
                    "priority": issue.priority,
                    "related_changes": [
                        oc.get("change_id")
                        for oc in issue.openspec_changes
                        if oc.get("change_id")
                    ]
                    or issue.related_changes
                    or ([issue.related_change] if issue.related_change else []),
                    "residual_statuses": residuals,
                }
            )
            evidence_hints.append(
                {
                    "reason": f"{issue.issue_id} trace/status",
                    "path": rel(issue.path / "trace.md", root),
                }
            )

        change_rows: list[dict[str, Any]] = []
        total_tasks = 0
        done_tasks = 0
        for change_id in sprint.changes:
            change = collect.load_change_record(change_id, issues, openspec_data)
            change_dir = change_dir_for(root, change)
            trace_exists = bool(change_dir and (change_dir / "trace.md").exists())
            if change.location == "missing":
                warnings.append(
                    {
                        "kind": "change-missing",
                        "target": change.change_id,
                        "detail": "change directory not found",
                    }
                )
            if change_dir and not trace_exists:
                warnings.append(
                    {
                        "kind": "change-trace-missing",
                        "target": change.change_id,
                        "detail": "trace.md not found in change directory",
                    }
                )
            if change.tasks.total and change.tasks.done < change.tasks.total:
                warnings.append(
                    {
                        "kind": "change-tasks-incomplete",
                        "target": change.change_id,
                        "detail": f"{change.tasks.done}/{change.tasks.total} tasks complete",
                    }
                )
            done_tasks += change.tasks.done
            total_tasks += change.tasks.total
            change_rows.append(
                {
                    "change_id": change.change_id,
                    "location": change.location,
                    "path": rel(change_dir, root) if change_dir else None,
                    "archive_dir": change.archive_dir,
                    "archive_date": change.archive_date,
                    "openspec_status": change.openspec_status,
                    "tasks": {
                        "done": change.tasks.done,
                        "total": change.tasks.total,
                    },
                    "linked_req": change.linked_req,
                    "linked_bug": change.linked_bug,
                    "trace_exists": trace_exists,
                }
            )
            if change_dir:
                evidence_hints.append(
                    {
                        "reason": f"{change.change_id} tasks",
                        "path": rel(change_dir / "tasks.md", root),
                    }
                )
                if not trace_exists:
                    evidence_hints.append(
                        {
                            "reason": f"{change.change_id} missing trace fallback",
                            "path": rel(change_dir, root),
                        }
                    )

        four_piece = {
            name: {
                "path": rel(sprint.path / name, root),
                "line_count": line_count(sprint.path / name),
                "exists": (sprint.path / name).exists(),
            }
            for name in ("sprint.yaml", "sprint.md", "release-note.md", "acceptance-report.md")
        }
        long_docs = [
            item
            for item in four_piece.values()
            if item["exists"] and int(item["line_count"]) >= 200
        ]
        token_risks = [
            {
                "source": "Sprint four-piece",
                "impact": "high" if long_docs else "medium",
                "detail": f"{len(long_docs)} file(s) have >= 200 lines; prefer this fact sheet before raw reads",
            },
            {
                "source": "OpenSpec changes",
                "impact": "high" if len(change_rows) >= 8 else "medium",
                "detail": f"{len(change_rows)} change(s), {done_tasks}/{total_tasks} tasks",
            },
            {
                "source": "Archive lookup",
                "impact": "medium",
                "detail": "Archive paths are resolved from sprint.yaml change ids; avoid broad archive searches",
            },
        ]

        missing_requirements = [
            issue_id for issue_id, record in zip(sprint.requirements, requirements) if record is None
        ]
        missing_bugs = [
            issue_id for issue_id, record in zip(sprint.bugs, bugs) if record is None
        ]
        for issue_id in (*missing_requirements, *missing_bugs):
            warnings.append(
                {
                    "kind": "issue-missing",
                    "target": issue_id,
                    "detail": "issue directory not found",
                }
            )

        path_residual_report = archived_path_residuals.build_report(sprint.sprint_id, root=root)
        for residual in path_residual_report.residuals:
            suggested = residual.new_path or "unresolved"
            warnings.append(
                {
                    "kind": "archived-path-residual",
                    "target": residual.target,
                    "detail": (
                        f"{residual.file}:{residual.line} keeps `{residual.old_path}`; "
                        f"suggest `{suggested}`"
                    ),
                }
            )
            evidence_hints.append(
                {
                    "reason": f"Archived path residual: {residual.target}",
                    "path": residual.file,
                }
            )

        change_batches = sprint_change_batches.build_change_batches(
            change_rows,
            warnings=warnings,
            evidence_hints=evidence_hints,
            ordering="sprint.yaml changes[]",
        )

        return {
            "sprint": {
                "sprint_id": sprint.sprint_id,
                "path": rel(sprint.path, root),
                "status": sprint.status,
                "lifecycle_stage": sprint_yaml.get("lifecycle_stage"),
                "start_date": sprint_yaml.get("start_date"),
                "end_date": sprint_yaml.get("end_date"),
                "capacity": sprint_yaml.get("capacity") or {},
                "estimated_story_points": sprint_yaml.get("estimated_story_points"),
                "estimated_person_days": sprint_yaml.get("estimated_person_days"),
            },
            "scope": {
                "requirements": sprint.requirements,
                "bugs": sprint.bugs,
                "changes": sprint.changes,
                "counts": {
                    "requirements": len(sprint.requirements),
                    "bugs": len(sprint.bugs),
                    "changes": len(sprint.changes),
                    "tasks_done": done_tasks,
                    "tasks_total": total_tasks,
                },
            },
            "changes": change_rows,
            "change_batches": change_batches,
            "issues": issue_rows,
            "acceptance": acceptance_summary(sprint.path, root),
            "archived_path_residuals": archived_path_residuals.report_to_dict(path_residual_report),
            "ai_usage_snapshot": ai_usage_snapshot(
                sprint.sprint_id,
                root,
                expected_scope={
                    "requirements": sprint.requirements,
                    "bugs": sprint.bugs,
                    "changes": sprint.changes,
                },
                min_generated_at=project_time_to_utc_iso(
                    sprint_yaml.get("end_date") or sprint_yaml.get("start_date")
                ),
            ),
            "four_piece": four_piece,
            "warnings": warnings,
            "needs_detail": bool(warnings),
            "token_risks": token_risks,
            "evidence_hints": evidence_hints,
        }
    finally:
        collect.ROOT = previous_root


def warning_summary(warnings: list[dict[str, str]]) -> dict[str, Any]:
    by_kind: dict[str, int] = {}
    for warning in warnings:
        kind = warning.get("kind", "unknown")
        by_kind[kind] = by_kind.get(kind, 0) + 1
    return {
        "count": len(warnings),
        "by_kind": by_kind,
        "items": warnings,
    }


def build_summary(fact_sheet: dict[str, Any]) -> dict[str, Any]:
    ai_usage = fact_sheet.get("ai_usage_snapshot") or {}
    residuals = fact_sheet.get("archived_path_residuals") or {}
    return {
        "sprint": fact_sheet["sprint"],
        "scope": {
            "counts": fact_sheet["scope"]["counts"],
            "requirements": fact_sheet["scope"]["requirements"],
            "bugs": fact_sheet["scope"]["bugs"],
            "changes": fact_sheet["scope"]["changes"],
        },
        "tasks": {
            "done": fact_sheet["scope"]["counts"]["tasks_done"],
            "total": fact_sheet["scope"]["counts"]["tasks_total"],
        },
        "change_batches": {
            "applicable": fact_sheet["change_batches"]["applicable"],
            "reason": fact_sheet["change_batches"]["reason"],
            "threshold": fact_sheet["change_batches"]["threshold"],
            "batch_size": fact_sheet["change_batches"]["batch_size"],
            "total_changes": fact_sheet["change_batches"]["total_changes"],
            "batch_count": fact_sheet["change_batches"]["batch_count"],
            "ordering": fact_sheet["change_batches"]["ordering"],
            "batches": [
                {
                    "batch_id": batch["batch_id"],
                    "change_ids": batch["change_ids"],
                    "counts": batch["counts"],
                    "warning_labels": batch["warning_labels"],
                    "recommended_next_read": batch["recommended_next_read"],
                }
                for batch in fact_sheet["change_batches"]["batches"]
            ],
        },
        "acceptance": fact_sheet["acceptance"],
        "warnings": warning_summary(fact_sheet["warnings"]),
        "needs_detail": fact_sheet["needs_detail"],
        "detail_triggers": {
            "warning_count": len(fact_sheet["warnings"]),
            "evidence_hint_count": len(fact_sheet["evidence_hints"]),
            "archived_path_residual_count": residuals.get("residual_count", 0),
            "ai_usage_warning_count": ai_usage.get("warning_count", 0),
        },
        "ai_usage_snapshot": {
            "exists": ai_usage.get("exists", False),
            "ai_usage_mode": ai_usage.get("ai_usage_mode", "estimated_fallback"),
            "snapshot_status": ai_usage.get("snapshot_status", "missing"),
            "estimated": ai_usage.get("estimated", True),
            "generated_at": ai_usage.get("generated_at"),
            "warning_count": ai_usage.get("warning_count", 0),
            "recommended_action": ai_usage.get("recommended_action"),
            "note": ai_usage.get("note"),
            "totals": ai_usage.get("totals") or {},
            "usage_matrices": ai_usage.get("usage_matrices") or {},
        },
        "token_risks": fact_sheet["token_risks"],
        "four_piece": fact_sheet["four_piece"],
        "archived_path_residuals": {
            "ok": residuals.get("ok", True),
            "residual_count": residuals.get("residual_count", 0),
        },
        "read_strategy": {
            "default_for_sprint_exps": "summary",
            "evidence_hints": "Use --fields evidence_hints only when needs_detail, warnings, missing/inconsistent facts, or user-requested detail requires raw evidence lookup.",
        },
    }


def select_field(payload: Any, field_path: str) -> Any:
    current = payload
    for part in field_path.split("."):
        if not part:
            raise KeyError(field_path)
        if isinstance(current, dict):
            if part not in current:
                raise KeyError(field_path)
            current = current[part]
        elif isinstance(current, list) and part.isdigit():
            index = int(part)
            try:
                current = current[index]
            except IndexError as exc:
                raise KeyError(field_path) from exc
        else:
            raise KeyError(field_path)
    return current


def select_fields(payload: dict[str, Any], field_paths: list[str]) -> dict[str, Any]:
    return {field_path: select_field(payload, field_path) for field_path in field_paths}


def render_markdown(fact_sheet: dict[str, Any]) -> str:
    sprint = fact_sheet["sprint"]
    scope = fact_sheet["scope"]
    lines = [
        f"# Sprint Fact Sheet: {sprint['sprint_id']}",
        "",
        "## Sprint",
        "",
        "| 指标 | 值 |",
        "|---|---|",
        f"| 路径 | `{sprint['path']}` |",
        f"| 状态 | {sprint.get('status') or ''} / {sprint.get('lifecycle_stage') or ''} |",
        f"| 周期 | {sprint.get('start_date') or ''} ~ {sprint.get('end_date') or ''} |",
        f"| 容量 | {sprint.get('capacity') or {}} |",
        f"| 估算 | {sprint.get('estimated_story_points') or ''} SP / {sprint.get('estimated_person_days') or ''} 人天 |",
        f"| Scope | REQ {scope['counts']['requirements']} / BUG {scope['counts']['bugs']} / Change {scope['counts']['changes']} |",
        f"| Tasks | {scope['counts']['tasks_done']}/{scope['counts']['tasks_total']} |",
        "",
        "## Changes",
        "",
        "| Change | Location | Tasks | Trace | Linked Issue | Path |",
        "|---|---|---:|---|---|---|",
    ]
    for change in fact_sheet["changes"]:
        linked = change.get("linked_bug") or change.get("linked_req") or ""
        trace = "yes" if change.get("trace_exists") else "no"
        tasks = change.get("tasks") or {}
        path = change.get("path") or ""
        lines.append(
            f"| `{change['change_id']}` | {change['location']} | {tasks.get('done', 0)}/{tasks.get('total', 0)} | {trace} | {linked} | `{path}` |"
        )

    change_batches = fact_sheet["change_batches"]
    lines.extend(
        [
            "",
            "## Change Batches",
            "",
            f"- Applicable: {change_batches['applicable']} ({change_batches['reason']})",
            f"- Total Changes: {change_batches['total_changes']}",
            f"- Batch Count: {change_batches['batch_count']}",
            f"- Batch Size: {change_batches['batch_size']}",
        ]
    )
    if change_batches["batches"]:
        lines.extend(
            [
                "",
                "| Batch | Changes | Tasks | Blockers | Warnings | Next Read |",
                "|---|---:|---:|---:|---:|---|",
            ]
        )
        for batch in change_batches["batches"]:
            counts = batch["counts"]
            lines.append(
                f"| `{batch['batch_id']}` | {counts['changes']} | {counts['tasks_done']}/{counts['tasks_total']} | {counts['blockers']} | {counts['warnings']} | {batch['recommended_next_read']} |"
            )

    lines.extend(
        [
            "",
            "## Issues",
            "",
            "| Issue | Kind | Stage | Trace Status | Related Changes | Residual Statuses |",
            "|---|---|---|---|---|---:|",
        ]
    )
    for issue in fact_sheet["issues"]:
        related = ", ".join(str(item) for item in issue.get("related_changes") or [])
        residual_count = len(issue.get("residual_statuses") or [])
        lines.append(
            f"| `{issue['issue_id']}` | {issue['kind']} | {issue['stage']} | {issue.get('trace_status') or ''} | {related} | {residual_count} |"
        )

    acceptance = fact_sheet["acceptance"]
    lines.extend(
        [
            "",
            "## Acceptance",
            "",
            f"- Path: `{acceptance['path']}`",
            f"- Exists: {acceptance['exists']}",
            f"- Lines: {acceptance['line_count']}",
        ]
    )
    if acceptance.get("signals"):
        lines.append("- Signals:")
        for signal in acceptance["signals"]:
            lines.append(f"  - {signal}")

    lines.extend(["", "## Warnings", ""])
    if fact_sheet["warnings"]:
        lines.extend(["| Kind | Target | Detail |", "|---|---|---|"])
        for warning in fact_sheet["warnings"]:
            lines.append(f"| {warning['kind']} | `{warning['target']}` | {warning['detail']} |")
    else:
        lines.append("- None")

    ai_usage = fact_sheet.get("ai_usage_snapshot") or {}
    totals = ai_usage.get("totals") or {}
    lines.extend(["", "## AI Usage Snapshot", "", "| Metric | Value |", "|---|---:|"])
    lines.append(f"| Exists | {ai_usage.get('exists', False)} |")
    lines.append(f"| Status | {ai_usage.get('snapshot_status', 'missing')} |")
    lines.append(f"| Mode | {ai_usage.get('ai_usage_mode', 'estimated_fallback')} |")
    lines.append(f"| Estimated | {ai_usage.get('estimated', True)} |")
    lines.append(f"| Generated At | {ai_usage.get('generated_at') or ''} |")
    lines.append(f"| Warning Count | {ai_usage.get('warning_count', len(ai_usage.get('warnings') or []))} |")
    for key in (
        "command_run_count",
        "model_call_count",
        "tool_call_count",
        "retry_count",
        "input_tokens",
        "cached_input_tokens",
        "output_tokens",
        "reasoning_output_tokens",
        "total_tokens",
        "tool_output_chars",
    ):
        lines.append(f"| {key} | {totals.get(key, 0)} |")
    if ai_usage.get("note"):
        lines.append(f"| note | {ai_usage['note']} |")
    if ai_usage.get("recommended_action"):
        lines.append(f"| recommended_action | {ai_usage['recommended_action']} |")
    usage_matrices = ai_usage.get("usage_matrices") or {}
    matrix_columns = [
        str(column.get("label"))
        for column in usage_matrices.get("columns", [])
        if column.get("label")
    ]
    matrix_rows = usage_matrices.get("rows") or []
    if matrix_columns and matrix_rows:
        lines.extend(["", "### AI Usage Matrices", ""])
        for metric in ("total_tokens", "input_tokens", "output_tokens", "model_call_count"):
            lines.extend(
                [
                    f"#### {metric}",
                    "",
                    "| 对象 | " + " | ".join(matrix_columns) + " |",
                    "|---|" + "|".join("---:" for _ in matrix_columns) + "|",
                ]
            )
            for row in matrix_rows:
                cells = ((row.get("metrics") or {}).get(metric) or {})
                lines.append(
                    f"| {row.get('object_id')} | "
                    + " | ".join(str(cells.get(column, 0)) for column in matrix_columns)
                    + " |"
                )
            lines.append("")
        if usage_matrices.get("note"):
            lines.append(f"> {usage_matrices['note']}")

    lines.extend(["", "## Token Risks", "", "| Source | Impact | Detail |", "|---|---|---|"])
    for risk in fact_sheet["token_risks"]:
        lines.append(f"| {risk['source']} | {risk['impact']} | {risk['detail']} |")

    lines.extend(["", "## Evidence Hints", "", "| Reason | Path |", "|---|---|"])
    for hint in fact_sheet["evidence_hints"]:
        lines.append(f"| {hint['reason']} | `{hint['path']}` |")

    lines.extend(
        [
            "",
            "## Read Strategy",
            "",
            "- `/sprint-exps` MUST read this Fact Sheet before raw Sprint/Issue/Change documents.",
            "- Read raw files only for warnings, missing evidence, inconsistent status, or user-requested detail.",
        ]
    )
    return "\n".join(lines) + "\n"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--sprint", required=True, help="Sprint id, e.g. sprint-005")
    parser.add_argument("--root", type=Path, default=ROOT, help=argparse.SUPPRESS)
    parser.add_argument("--json", action="store_true", help="Emit machine-readable JSON")
    parser.add_argument(
        "--summary",
        action="store_true",
        help="Emit compact JSON for /sprint-exps default consumption without full evidence_hints",
    )
    parser.add_argument(
        "--fields",
        nargs="+",
        metavar="FIELD",
        help="Emit selected field paths as JSON, e.g. evidence_hints warnings ai_usage_snapshot.totals",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        fact_sheet = build_fact_sheet(args.sprint, root=args.root)
    except FileNotFoundError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    if args.fields:
        try:
            print(json.dumps(select_fields(fact_sheet, args.fields), ensure_ascii=False, indent=2))
        except KeyError as exc:
            print(f"ERROR: unknown field path: {exc.args[0]}", file=sys.stderr)
            return 3
    elif args.summary:
        print(json.dumps(build_summary(fact_sheet), ensure_ascii=False, indent=2))
    elif args.json:
        print(json.dumps(fact_sheet, ensure_ascii=False, indent=2))
    else:
        print(render_markdown(fact_sheet), end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
