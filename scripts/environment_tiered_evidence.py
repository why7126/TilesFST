#!/usr/bin/env python3
"""Shared evidence source diagnostics helpers."""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


PASS_VALUES = {"pass", "passed", "success", "verified", "通过", "已通过"}
PENDING_VALUES = {"production_only_pending"}
TARGETS = {"development", "trial", "production"}

DEV_RE = re.compile(r"(DevTools|开发者工具|development|开发环境|本地|local|pytest|vitest|开发 API|dev smoke)", re.I)
PROD_PASS_RE = re.compile(r"(production|生产|正式环境).{0,24}(pass|passed|verified|通过|已验证|验收通过)", re.I)
TRIAL_PASS_RE = re.compile(r"(trial|体验版).{0,24}(pass|passed|verified|通过|已验证|验收通过)", re.I)
DEVICE_PASS_RE = re.compile(r"(real[-_ ]?device|真机).{0,24}(pass|passed|verified|通过|已验证|验收通过)", re.I)
PROTECTIVE_RE = re.compile(r"(不得|不可|不能|must not|should not|禁止|阻断|防止|避免|不能宣称)", re.I)
NETWORK_SOURCE_RE = re.compile(r"(network_trial|real_device|体验版\s*Network|真机\s*Network|真机设备)", re.I)
EVIDENCE_FIELD_RE = re.compile(r"^\s*(evidence|evidence_ref|artifact|screenshot|network_summary|request_domain|executed_at)\s*[:=]\s*(.+)\s*$", re.I)
EMPTY_VALUE_RE = re.compile(r"^(null|none|n/a|na|待补充|待填写|tbd|todo|)$", re.I)


@dataclass(frozen=True)
class EnvironmentEvidenceIssue:
    severity: str
    rule_id: str
    file: str
    line: int
    message: str
    snippet: str


@dataclass(frozen=True)
class EnvironmentEvidenceReport:
    target: str
    scope: str
    checked_files: list[str]
    blockers: list[EnvironmentEvidenceIssue] = field(default_factory=list)
    warnings: list[EnvironmentEvidenceIssue] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return not self.blockers


def _rel(path: Path, root: Path) -> str:
    try:
        return str(path.resolve().relative_to(root.resolve()))
    except ValueError:
        return str(path)


def _non_empty(value: Any) -> bool:
    if value is None:
        return False
    if isinstance(value, str):
        return EMPTY_VALUE_RE.match(value.strip()) is None
    if isinstance(value, (list, tuple, set, dict)):
        return bool(value)
    return True


def _text(value: Any) -> str:
    if isinstance(value, str):
        return value
    if value is None:
        return ""
    return json.dumps(value, ensure_ascii=False, sort_keys=True)


def _issue(path: Path, root: Path, rule_id: str, message: str, snippet: str, *, line: int = 1) -> EnvironmentEvidenceIssue:
    return EnvironmentEvidenceIssue(
        severity="blocker",
        rule_id=rule_id,
        file=_rel(path, root),
        line=line,
        message=message,
        snippet=snippet.strip()[:240],
    )


def _has_evidence(record: dict[str, Any]) -> bool:
    for key in ("evidence_ref", "evidence", "artifact", "screenshot", "screenshots", "network_summary", "request_domain", "executed_at"):
        if _non_empty(record.get(key)):
            return True
    return False


def _status_value(record: dict[str, Any]) -> str:
    return str(record.get("status") or record.get("verdict") or record.get("result") or "").strip().lower()


def _classification(record: dict[str, Any]) -> str:
    return str(record.get("classification") or record.get("status") or "").strip().lower()


def _is_network_pass(record: dict[str, Any]) -> bool:
    status = _status_value(record)
    source = " ".join(
        _text(record.get(key))
        for key in ("source", "source_type", "target_environment", "evidence_type", "phase", "name")
    )
    return status in PASS_VALUES and NETWORK_SOURCE_RE.search(source) is not None


def _path_text(path_parts: tuple[str, ...]) -> str:
    return ".".join(path_parts).lower()


def _scan_mapping(
    record: dict[str, Any],
    *,
    source_path: Path,
    root: Path,
    target: str,
    path_parts: tuple[str, ...],
) -> list[EnvironmentEvidenceIssue]:
    issues: list[EnvironmentEvidenceIssue] = []
    snippet = json.dumps(record, ensure_ascii=False, sort_keys=True)

    if _is_network_pass(record) and not _has_evidence(record):
        issues.append(
            _issue(
                source_path,
                root,
                "network-pass-missing-evidence",
                "体验版/真机 Network 证据标记为 passed 时必须包含 evidence_ref、artifact、network_summary、request_domain 或 executed_at 等可定位证据。",
                snippet,
            )
        )

    classification = _classification(record)
    if classification in PENDING_VALUES:
        if target == "production":
            issues.append(
                _issue(
                    source_path,
                    root,
                    "production-pending-at-production-target",
                    "生产发布目标下不得保留 production_only_pending，必须重新判定为生产 evidence、N/A、environment_unavailable 或发布阻塞项。",
                    snippet,
                )
            )
        missing = [
            key
            for key in ("target_environment", "phase", "blocking_scope")
            if not _non_empty(record.get(key))
        ]
        if missing:
            issues.append(
                _issue(
                    source_path,
                    root,
                    "production-pending-missing-scope",
                    f"production_only_pending 必须声明目标环境、阶段和阻塞范围，缺少：{', '.join(missing)}。",
                    snippet,
                )
            )

    if target == "production" and _status_value(record) in PASS_VALUES:
        evidence = " ".join(_text(record.get(key)) for key in ("evidence", "evidence_ref", "current_evidence"))
        proof_path = _path_text(path_parts)
        production_like = "production_deployment" in proof_path or any(
            key in proof_path for key in ("public_api", "media_no_fallback", "runtime_smoke", "backup", "rollback")
        )
        if production_like and DEV_RE.search(evidence):
            issues.append(
                _issue(
                    source_path,
                    root,
                    "development-proof-used-for-production",
                    "生产发布证据不得使用 DevTools、本地测试或 development smoke 冒充生产通过。",
                    snippet,
                )
            )

    return issues


def _walk_json(value: Any, *, source_path: Path, root: Path, target: str, path_parts: tuple[str, ...] = ()) -> list[EnvironmentEvidenceIssue]:
    issues: list[EnvironmentEvidenceIssue] = []
    if isinstance(value, dict):
        issues.extend(_scan_mapping(value, source_path=source_path, root=root, target=target, path_parts=path_parts))
        for key, child in value.items():
            issues.extend(_walk_json(child, source_path=source_path, root=root, target=target, path_parts=path_parts + (str(key),)))
    elif isinstance(value, list):
        for index, child in enumerate(value):
            issues.extend(_walk_json(child, source_path=source_path, root=root, target=target, path_parts=path_parts + (str(index),)))
    return issues


def _line_number(text: str, offset: int) -> int:
    return text.count("\n", 0, offset) + 1


def _paragraphs(text: str) -> list[tuple[int, str]]:
    result: list[tuple[int, str]] = []
    start = 0
    for match in re.finditer(r"\n\s*\n", text):
        chunk = text[start : match.start()]
        if chunk.strip():
            result.append((_line_number(text, start), chunk))
        start = match.end()
    tail = text[start:]
    if tail.strip():
        result.append((_line_number(text, start), tail))
    return result


def _block_has_evidence(block: str) -> bool:
    for line in block.splitlines():
        match = EVIDENCE_FIELD_RE.match(line)
        if match and EMPTY_VALUE_RE.match(match.group(2).strip()) is None:
            return True
    return False


def _scan_text(path: Path, root: Path, text: str, *, target: str) -> list[EnvironmentEvidenceIssue]:
    issues: list[EnvironmentEvidenceIssue] = []
    for line_no, block in _paragraphs(text):
        compact = " ".join(block.split())
        if PROTECTIVE_RE.search(compact):
            continue
        if DEV_RE.search(compact) and (PROD_PASS_RE.search(compact) or TRIAL_PASS_RE.search(compact) or DEVICE_PASS_RE.search(compact)):
            issues.append(
                _issue(
                    path,
                    root,
                    "environment-claim-mismatch",
                    "开发环境证据不得宣称体验版、真机或生产环境已通过。",
                    compact,
                    line=line_no,
                )
            )
        if NETWORK_SOURCE_RE.search(compact) and re.search(r"status\s*[:=]\s*(passed|pass|通过|已通过)", compact, re.I):
            if not _block_has_evidence(block):
                issues.append(
                    _issue(
                        path,
                        root,
                        "network-pass-missing-evidence",
                        "体验版/真机 Network 标记 passed 时必须带可定位 evidence_ref 或等价证据字段。",
                        compact,
                        line=line_no,
                    )
                )
    lines = text.splitlines()
    for index, line in enumerate(lines):
        if "production_only_pending" not in line.lower():
            continue
        window = "\n".join(lines[max(index - 3, 0) : min(index + 4, len(lines))])
        if PROTECTIVE_RE.search(window):
            continue
        lowered = window.lower()
        evidence_like = any(token in lowered for token in ("classification:", "status:", "target_environment:", "blocking_scope:"))
        if not evidence_like:
            continue
        compact = " ".join(window.split())
        if target == "production":
            issues.append(
                _issue(
                    path,
                    root,
                    "production-pending-at-production-target",
                    "生产发布目标下不得保留 production_only_pending，必须重新判定。",
                    compact,
                    line=index + 1,
                )
            )
        if not all(token in lowered for token in ("target_environment", "phase", "blocking_scope")):
            issues.append(
                _issue(
                    path,
                    root,
                    "production-pending-missing-scope",
                    "production_only_pending 证据块必须同时声明 target_environment、phase 和 blocking_scope。",
                    compact,
                    line=index + 1,
                )
            )
    return issues


def _read_and_scan(path: Path, root: Path, *, target: str) -> list[EnvironmentEvidenceIssue]:
    text = path.read_text(encoding="utf-8")
    issues: list[EnvironmentEvidenceIssue] = []
    if path.suffix == ".json":
        try:
            issues.extend(_walk_json(json.loads(text), source_path=path, root=root, target=target))
        except json.JSONDecodeError:
            return issues
    issues.extend(_scan_text(path, root, text, target=target))
    return issues


def _existing(paths: list[Path]) -> list[Path]:
    return [path for path in paths if path.exists() and path.is_file()]


def find_archived_change_dir(root: Path, change_id: str) -> Path | None:
    archive_root = root / "openspec" / "archive"
    if not archive_root.exists():
        return None
    matches = sorted(archive_root.glob(f"*-{change_id}"))
    return matches[-1] if matches else None


def resolve_change_dir(root: Path, change_id: str) -> Path | None:
    active = root / "openspec" / "changes" / change_id
    if active.exists():
        return active
    return find_archived_change_dir(root, change_id)


def change_files(root: Path, change_id: str) -> list[Path]:
    change_dir = resolve_change_dir(root, change_id)
    if change_dir is None:
        return []
    names = ("proposal.md", "design.md", "tasks.md", "trace.md", "acceptance.md", "test-plan.md")
    return _existing([change_dir / name for name in names])


def parse_sprint_changes(sprint_yaml: Path) -> list[str]:
    changes: list[str] = []
    in_changes = False
    changes_indent = 0
    for line in sprint_yaml.read_text(encoding="utf-8").splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        indent = len(line) - len(line.lstrip(" "))
        stripped = line.strip()
        if re.match(r"^changes\s*:\s*$", stripped):
            in_changes = True
            changes_indent = indent
            continue
        if in_changes and indent <= changes_indent and not stripped.startswith("- "):
            break
        if in_changes:
            match = re.match(r"^-\s*['\"]?([^'\"\s#]+)['\"]?", stripped)
            if match:
                changes.append(match.group(1))
    return changes


def resolve_sprint_dir(root: Path, sprint_id: str) -> Path | None:
    for stage in ("change", "archive"):
        candidate = root / "iterations" / stage / sprint_id
        if (candidate / "sprint.yaml").exists():
            return candidate
    return None


def sprint_files(root: Path, sprint_id: str) -> list[Path]:
    sprint_dir = resolve_sprint_dir(root, sprint_id)
    if sprint_dir is None:
        return []
    files = _existing([sprint_dir / name for name in ("sprint.yaml", "sprint.md", "acceptance-report.md", "release-note.md")])
    for change_id in parse_sprint_changes(sprint_dir / "sprint.yaml"):
        files.extend(change_files(root, change_id))
    return files


def release_files(release_dir: Path) -> list[Path]:
    files = _existing(
        [
            release_dir / "release.json",
            release_dir / "announcement.mdx",
            release_dir / "image-build-plan.json",
            release_dir / "image-manifest.json",
        ]
    )
    upgrade_dir = release_dir / "upgrade-plans"
    if upgrade_dir.exists():
        files.extend(sorted(upgrade_dir.glob("*.json")))
    return files


def validate_files(files: list[Path], root: Path, *, target: str, scope: str) -> EnvironmentEvidenceReport:
    checked = []
    blockers: list[EnvironmentEvidenceIssue] = []
    for path in dict.fromkeys(files):
        checked.append(_rel(path, root))
        blockers.extend(_read_and_scan(path, root, target=target))
    return EnvironmentEvidenceReport(target=target, scope=scope, checked_files=checked, blockers=blockers)


def validate_change(root: Path, change_id: str, *, target: str = "development") -> EnvironmentEvidenceReport:
    return validate_files(change_files(root, change_id), root, target=target, scope=f"change:{change_id}")


def validate_sprint(root: Path, sprint_id: str, *, target: str = "development") -> EnvironmentEvidenceReport:
    return validate_files(sprint_files(root, sprint_id), root, target=target, scope=f"sprint:{sprint_id}")


def validate_release(root: Path, release_dir: Path, *, target: str = "development") -> EnvironmentEvidenceReport:
    return validate_files(release_files(release_dir), root, target=target, scope=f"release:{release_dir.name}")
