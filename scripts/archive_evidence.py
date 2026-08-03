"""Shared archived OpenSpec Change evidence checks."""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path


FALLBACK_SUMMARY_FILES = ("proposal.md", "design.md", "tasks.md")
FALLBACK_SUMMARY_REQUIREMENTS = {
    "validation": ("验证命令", "验证结果", "测试命令", "test", "pytest", "validate"),
    "acceptance": ("验收结论", "验收结果", "acceptance", "verdict"),
    "issue_or_sprint_status": ("Issue", "Sprint", "REQ-", "BUG-", "状态"),
    "archive_evidence": ("归档路径", "归档时间", "openspec/archive", "archive"),
}


@dataclass(frozen=True)
class ArchiveEvidenceResult:
    change_id: str
    archive_path: str
    status: str
    trace_exists: bool
    checked_files: list[str]
    fallback_summary_file: str | None = None
    missing_items: list[str] | None = None
    blocker: str | None = None

    @property
    def ok(self) -> bool:
        return self.blocker is None


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def rel(path: Path, root: Path) -> str:
    try:
        return str(path.relative_to(root))
    except ValueError:
        return str(path)


def extract_archive_summary(text: str) -> str | None:
    match = re.search(r"^## 归档验证摘要\s*\n(.*?)(?=^##\s+|\Z)", text, re.MULTILINE | re.DOTALL)
    if not match:
        return None
    return match.group(1).strip()


def missing_fallback_summary_items(summary: str) -> list[str]:
    missing: list[str] = []
    lowered = summary.lower()
    for key, terms in FALLBACK_SUMMARY_REQUIREMENTS.items():
        if not any(term.lower() in lowered for term in terms):
            missing.append(key)
    return missing


def validate_archive_evidence(change_dir: Path, root: Path, *, change_id: str | None = None) -> ArchiveEvidenceResult:
    resolved_root = root.resolve()
    resolved_change_dir = change_dir.resolve()
    checked_files = [rel(resolved_change_dir / name, resolved_root) for name in FALLBACK_SUMMARY_FILES]
    resolved_change_id = change_id or resolved_change_dir.name.split("-", 3)[-1]
    archive_path = rel(resolved_change_dir, resolved_root)

    if (resolved_change_dir / "trace.md").exists():
        return ArchiveEvidenceResult(
            change_id=resolved_change_id,
            archive_path=archive_path,
            status="trace-present",
            trace_exists=True,
            checked_files=checked_files,
            missing_items=[],
        )

    best_missing = list(FALLBACK_SUMMARY_REQUIREMENTS)
    for name in FALLBACK_SUMMARY_FILES:
        path = resolved_change_dir / name
        if not path.exists():
            continue
        summary = extract_archive_summary(read_text(path))
        if summary is None:
            continue
        missing = missing_fallback_summary_items(summary)
        if not missing:
            return ArchiveEvidenceResult(
                change_id=resolved_change_id,
                archive_path=archive_path,
                status="fallback-summary-pass",
                trace_exists=False,
                checked_files=checked_files,
                fallback_summary_file=rel(path, resolved_root),
                missing_items=[],
            )
        if len(missing) < len(best_missing):
            best_missing = missing

    blocker = (
        "archived change missing trace.md and complete fallback summary "
        f"(change: {resolved_change_id}; archive: {archive_path}; "
        f"checked: {', '.join(checked_files)}; missing: {', '.join(best_missing)})"
    )
    return ArchiveEvidenceResult(
        change_id=resolved_change_id,
        archive_path=archive_path,
        status="missing",
        trace_exists=False,
        checked_files=checked_files,
        missing_items=best_missing,
        blocker=blocker,
    )
