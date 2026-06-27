from __future__ import annotations

import argparse
from dataclasses import dataclass, field

from .collect import (
    load_all_issues,
    load_change_record,
    load_registry,
    load_sprint,
    resolve_sprint_id,
    run_openspec_list,
)
from .derive import (
    derive_change_state,
    derive_issue,
    openspec_change_status,
    release_status_line,
    sprint_summary_note,
)
from .patch import (
    PatchResult,
    patch_acceptance_report,
    patch_issue_trace,
    patch_parent_requirement_bug_index,
    patch_registry_entry,
    patch_release_note,
    patch_sprint_md,
)
from .constants import ROOT


@dataclass
class SyncReport:
    sprint_id: str | None = None
    sprint_skip_reason: str | None = None
    event: str | None = None
    focus_issue: str | None = None
    focus_change: str | None = None
    updated: list[PatchResult] = field(default_factory=list)
    skipped: list[PatchResult] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return not self.errors

    def format_text(self) -> str:
        lines = ["## Workflow Sync Report", ""]
        if self.sprint_id:
            lines.append(f"**Sprint:** {self.sprint_id}")
        elif self.sprint_skip_reason:
            lines.append(f"**Sprint:** _{self.sprint_skip_reason}_")
        if self.event:
            lines.append(f"**Event:** {self.event}")
        if self.focus_issue:
            lines.append(f"**Issue:** {self.focus_issue}")
        if self.focus_change:
            lines.append(f"**Change:** {self.focus_change}")
        lines.append("")
        if self.updated:
            lines.append("**Updated:**")
            for item in self.updated:
                suffix = f" — {item.detail}" if item.detail else ""
                lines.append(f"- `{item.path}`{suffix}")
        if self.skipped:
            lines.append("")
            lines.append("**Skipped (no delta):**")
            for item in self.skipped:
                lines.append(f"- `{item.path}`")
        if self.errors:
            lines.append("")
            lines.append("**Errors:**")
            for err in self.errors:
                lines.append(f"- {err}")
        return "\n".join(lines)


class SyncEngine:
    def __init__(self, dry_run: bool = False, check: bool = False):
        self.dry_run = dry_run
        self.check = check

    def run(
        self,
        *,
        sprint_id: str | None = None,
        event: str | None = None,
        change_id: str | None = None,
        req_id: str | None = None,
        bug_id: str | None = None,
    ) -> SyncReport:
        report = SyncReport(
            event=event,
            focus_issue=req_id or bug_id,
            focus_change=change_id,
        )
        resolved, skip_reason = resolve_sprint_id(
            sprint_id,
            event=event,
            req_id=req_id,
            bug_id=bug_id,
            change_id=change_id,
        )
        report.sprint_id = resolved
        report.sprint_skip_reason = skip_reason

        issues = load_all_issues()
        openspec_data = run_openspec_list()

        sprint = load_sprint(resolved) if resolved else None
        if not sprint and not any([change_id, req_id, bug_id]):
            report.errors.append("No sprint found to sync")
            return report

        change_ids = set(sprint.changes if sprint else [])
        if change_id:
            change_ids.add(change_id)
        for issue_id in (req_id, bug_id):
            issue = issues.get(issue_id or "")
            if not issue:
                continue
            for oc in issue.openspec_changes:
                cid = oc.get("change_id")
                if isinstance(cid, str):
                    change_ids.add(cid)
            if issue.related_change:
                change_ids.add(issue.related_change)

        change_records = {
            cid: load_change_record(cid, issues, openspec_data) for cid in sorted(change_ids)
        }
        derived_changes = {cid: derive_change_state(rec) for cid, rec in change_records.items()}

        issue_ids = set(sprint.requirements if sprint else []) | set(sprint.bugs if sprint else [])
        if req_id:
            issue_ids.add(req_id)
        if bug_id:
            issue_ids.add(bug_id)
        for change in derived_changes.values():
            if change.linked_req:
                issue_ids.add(change.linked_req)
            if change.linked_bug:
                issue_ids.add(change.linked_bug)

        derived_issues = {
            iid: derive_issue(issues[iid], derived_changes, sprint)
            for iid in issue_ids
            if iid in issues
        }

        write = not (self.dry_run or self.check)

        planned: list[PatchResult] = []
        if sprint:
            summary = sprint_summary_note(sprint, derived_changes)
            release_line = release_status_line(sprint, derived_changes)
            planned.append(
                patch_sprint_md(
                    sprint, issues, derived_issues, derived_changes, summary, write=write
                )
            )
            planned.append(patch_release_note(sprint, release_line, write=write))
            planned.append(
                patch_acceptance_report(sprint, issues, derived_issues, derived_changes, write=write)
            )

        parent_requirement_ids: set[str] = set()
        for iid, derived in derived_issues.items():
            issue = issues[iid]
            change_status_map = {
                oc.get("change_id"): openspec_change_status(
                    derived_changes.get(str(oc.get("change_id")))
                )
                for oc in issue.openspec_changes
                if oc.get("change_id")
            }
            planned.append(
                patch_issue_trace(issue, derived, change_status_map, write=write)
            )
            registry = (
                ROOT / "issues/requirements/_registry.yaml"
                if issue.kind == "req"
                else ROOT / "issues/bugs/_registry.yaml"
            )
            planned.append(
                patch_registry_entry(
                    registry, issue.issue_id, derived.display_status, write=write
                )
            )
            if issue.kind == "bug" and issue.related_requirement:
                parent_requirement_ids.add(issue.related_requirement)

        for parent_req_id in sorted(parent_requirement_ids):
            planned.append(
                patch_parent_requirement_bug_index(
                    parent_req_id,
                    issues,
                    derived_issues,
                    derived_changes,
                    write=write,
                )
            )

        for result in planned:
            if result.changed:
                report.updated.append(result)
            else:
                report.skipped.append(result)
        if self.check and report.updated:
            report.errors.append(
                f"Drift detected in {len(report.updated)} file(s); run without --check to fix"
            )
        return report


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Sync REQ/BUG/Sprint/OpenSpec workflow status across derived documents.",
    )
    parser.add_argument("--sprint", default="auto", help="Sprint id or 'auto'")
    parser.add_argument("--event", help="Workflow event name (e.g. opsx.archive)")
    parser.add_argument("--change", dest="change_id")
    parser.add_argument("--req", dest="req_id")
    parser.add_argument("--bug", dest="bug_id")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--check", action="store_true")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    engine = SyncEngine(dry_run=args.dry_run, check=args.check)
    report = engine.run(
        sprint_id=args.sprint,
        event=args.event,
        change_id=args.change_id,
        req_id=args.req_id,
        bug_id=args.bug_id,
    )
    print(report.format_text())
    return 0 if report.ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
