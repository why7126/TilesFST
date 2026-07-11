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
from pathlib import Path
from typing import Any

from workflow_sync import collect
from workflow_sync.issue_status_residuals import scan_issue_status_residuals


ROOT = Path(__file__).resolve().parents[1]


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


def ai_usage_snapshot(sprint_id: str, root: Path) -> dict[str, Any]:
    path = root / "data" / "ai-usage" / "sprints" / f"{sprint_id}.json"
    if not path.exists():
        return {
            "path": rel(path, root),
            "exists": False,
            "estimated": True,
            "note": "无精确 token 计量；/sprint-exps must use estimated fallback.",
        }
    try:
        data = json.loads(collect.read_text(path))
    except json.JSONDecodeError:
        return {
            "path": rel(path, root),
            "exists": True,
            "estimated": True,
            "warnings": ["invalid-ai-usage-json"],
        }
    safe = {
        "path": rel(path, root),
        "exists": True,
        "estimated": bool(data.get("estimated")),
        "totals": data.get("totals") or {},
        "by_workflow_event": data.get("by_workflow_event") or {},
        "warnings": data.get("warnings") or [],
    }
    return safe


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
            "issues": issue_rows,
            "acceptance": acceptance_summary(sprint.path, root),
            "ai_usage_snapshot": ai_usage_snapshot(sprint.sprint_id, root),
            "four_piece": four_piece,
            "warnings": warnings,
            "needs_detail": bool(warnings),
            "token_risks": token_risks,
            "evidence_hints": evidence_hints,
        }
    finally:
        collect.ROOT = previous_root


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
    lines.append(f"| Estimated | {ai_usage.get('estimated', True)} |")
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
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        fact_sheet = build_fact_sheet(args.sprint, root=args.root)
    except FileNotFoundError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    if args.json:
        print(json.dumps(fact_sheet, ensure_ascii=False, indent=2))
    else:
        print(render_markdown(fact_sheet), end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
