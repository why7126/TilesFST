#!/usr/bin/env python3
"""Promote a REQ/BUG directory between lifecycle stages (plan / review / archive).

Used by workflow commands:
  - /req-review --approve, /bug-review --approve  → plan → review
  - /opsx-archive, /sprint-archive (issue done)   → review → archive

See rules/issues-lifecycle.md.
"""

from __future__ import annotations

import argparse
import re
import shutil
import subprocess
import sys
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

SCRIPTS_DIR = Path(__file__).resolve().parent
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from workflow_sync.collect import resolve_issue_dir  # noqa: E402

ROOT = SCRIPTS_DIR.parent
STAGE_DIRS = frozenset({"plan", "review", "archive"})
VALID_TRANSITIONS = frozenset(
    {
        ("plan", "review"),
        ("legacy", "review"),
        ("review", "archive"),
        ("legacy", "archive"),
    }
)


@dataclass
class Promotion:
    kind: str  # req | bug
    issue_id: str
    from_stage: str
    to_stage: str
    src: Path
    dest: Path
    reason: str


def now_shanghai() -> str:
    return datetime.now(ZoneInfo("Asia/Shanghai")).strftime("%Y-%m-%d %H:%M:%S")


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def write_text(path: Path, text: str) -> None:
    path.write_text(text, encoding="utf-8")


def issues_base(kind: str) -> Path:
    sub = "requirements" if kind == "req" else "bugs"
    return ROOT / "issues" / sub


def detect_stage(issue_dir: Path, base: Path) -> str:
    rel = issue_dir.relative_to(base)
    if len(rel.parts) == 1:
        return "legacy"
    stage = rel.parts[0]
    if stage in STAGE_DIRS:
        return stage
    raise ValueError(f"unexpected issue path under {base}: {issue_dir}")


def normalize_issue_id(kind: str, raw: str) -> str:
    prefix = "REQ-" if kind == "req" else "BUG-"
    value = raw.strip()
    if not value.startswith(prefix):
        value = f"{prefix}{value.removeprefix(prefix)}"
    return value


def resolve_promotion(kind: str, issue_id: str, to_stage: str, reason: str) -> Promotion:
    if to_stage not in STAGE_DIRS:
        raise ValueError(f"invalid target stage: {to_stage}")

    base_rel = f"issues/{'requirements' if kind == 'req' else 'bugs'}"
    src = resolve_issue_dir(base_rel, issue_id)
    if src is None:
        raise FileNotFoundError(f"issue directory not found: {issue_id}")

    issue_id = src.name
    base = issues_base(kind)
    from_stage = detect_stage(src, base)

    if from_stage == to_stage:
        return Promotion(kind, issue_id, from_stage, to_stage, src, src, reason)

    if (from_stage, to_stage) not in VALID_TRANSITIONS:
        raise ValueError(f"invalid transition: {from_stage} → {to_stage}")

    dest = base / to_stage / issue_id
    if dest.exists() and dest != src:
        raise FileExistsError(f"destination already exists: {dest}")

    return Promotion(kind, issue_id, from_stage, to_stage, src, dest, reason)


def git_mv(src: Path, dest: Path) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    if dest.exists():
        raise FileExistsError(f"destination already exists: {dest}")
    try:
        subprocess.run(["git", "mv", str(src), str(dest)], cwd=ROOT, check=True, capture_output=True, text=True)
    except subprocess.CalledProcessError:
        shutil.move(str(src), str(dest))


def patch_trace(trace_path: Path, to_stage: str, from_stage: str, stamp: str, reason: str) -> bool:
    if not trace_path.exists():
        return False

    text = read_text(trace_path)
    original = text

    if re.search(r"^lifecycle_stage:\s*", text, flags=re.MULTILINE):
        text = re.sub(r"^lifecycle_stage:\s*.+$", f"lifecycle_stage: {to_stage}", text, count=1, flags=re.MULTILINE)
    else:
        text = re.sub(
            r"(^status: .+$)",
            rf"\1\nlifecycle_stage: {to_stage}",
            text,
            count=1,
            flags=re.MULTILINE,
        )

    text = re.sub(r"^updated_at: .+$", f"updated_at: {stamp}", text, count=1, flags=re.MULTILINE)

    reason_suffix = f"（{reason}）" if reason else ""
    from_label = from_stage if from_stage != "legacy" else "legacy"
    entry = f"| {stamp} | lifecycle-stage-migrate | {from_label} → {to_stage}{reason_suffix} |"
    if entry not in text and "## 变更记录" in text:
        text = text.replace("## 变更记录\n\n", f"## 变更记录\n\n{entry}\n", 1)

    kind_root = "requirements" if "/requirements/" in trace_path.as_posix() else "bugs"
    issue_id = trace_path.parent.name
    replacements = build_path_replacements(
        "req" if kind_root == "requirements" else "bug",
        issue_id,
        from_stage,
        to_stage,
    )
    for old, new in replacements:
        text = text.replace(old, new)

    if text != original:
        write_text(trace_path, text)
        return True
    return False


def build_path_replacements(kind: str, issue_id: str, from_stage: str, to_stage: str) -> list[tuple[str, str]]:
    base = f"issues/{'requirements' if kind == 'req' else 'bugs'}"
    new_base = f"{base}/{to_stage}/{issue_id}"

    if from_stage == "legacy":
        old_base = f"{base}/{issue_id}"
    else:
        old_base = f"{base}/{from_stage}/{issue_id}"

    replacements = [
        (f"{old_base}/", f"{new_base}/"),
        (old_base, new_base),
    ]
    replacements.sort(key=lambda pair: len(pair[0]), reverse=True)
    return replacements


def update_repo_references(promotion: Promotion) -> int:
    replacements = build_path_replacements(
        promotion.kind,
        promotion.issue_id,
        promotion.from_stage,
        promotion.to_stage,
    )
    if not replacements:
        return 0

    legacy_pattern = re.compile(
        rf"issues/(requirements|bugs)/"
        rf"(?!plan/|review/|archive/)"
        rf"({re.escape(promotion.issue_id)})"
    )
    kind_dir = "requirements" if promotion.kind == "req" else "bugs"
    new_staged = f"issues/{kind_dir}/{promotion.to_stage}/{promotion.issue_id}"

    count = 0
    skip_dirs = {".git", "node_modules", ".venv", "dist", "__pycache__"}
    skip_files = {"migrate-issues-lifecycle-stage.py", "promote-issue-stage.py"}
    for path in ROOT.rglob("*"):
        if not path.is_file():
            continue
        if any(part in skip_dirs for part in path.parts):
            continue
        if path.name in skip_files:
            continue
        if path.suffix not in {".md", ".yaml", ".yml", ".py", ".ts", ".tsx", ".json", ".html"}:
            continue
        text = read_text(path)
        new_text = text
        for old, new in replacements:
            new_text = new_text.replace(old, new)
        new_text = legacy_pattern.sub(
            lambda m: new_staged if m.group(2) == promotion.issue_id else m.group(0),
            new_text,
        )
        if new_text != text:
            write_text(path, new_text)
            count += 1
    return count


def apply_promotion(promotion: Promotion, *, dry_run: bool) -> int:
    rel_src = promotion.src.relative_to(ROOT)
    if promotion.from_stage == promotion.to_stage:
        print(f"## Promote Issue Stage\n\n**Issue:** {promotion.issue_id}")
        print(f"**Stage:** already at `{promotion.to_stage}/` ({rel_src})")
        print("\nNo move required.")
        return 0

    rel_dest = promotion.dest.relative_to(ROOT)
    print(f"## Promote Issue Stage\n")
    print(f"**Issue:** {promotion.issue_id}")
    print(f"**Transition:** {promotion.from_stage} → {promotion.to_stage}")
    print(f"**Move:** `{rel_src}` → `{rel_dest}`")
    if promotion.reason:
        print(f"**Reason:** {promotion.reason}")

    if dry_run:
        print("\nDry-run only. Re-run without `--dry-run` to apply.")
        return 0

    stamp = now_shanghai()
    git_mv(promotion.src, promotion.dest)
    trace_updated = patch_trace(
        promotion.dest / "trace.md",
        promotion.to_stage,
        promotion.from_stage,
        stamp,
        promotion.reason,
    )
    ref_count = update_repo_references(promotion)

    print("\n**Applied:**")
    print(f"- moved to `{rel_dest}`")
    print(f"- trace.md lifecycle_stage → `{promotion.to_stage}`" + (" (updated)" if trace_updated else ""))
    print(f"- path references updated in {ref_count} file(s)")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Promote REQ/BUG issue directory between lifecycle stages")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--req", metavar="REQ-id", help="Requirement id, e.g. REQ-0014-profile-page")
    group.add_argument("--bug", metavar="BUG-id", help="Bug id, e.g. BUG-0021-sidebar-menu-icons-indistinguishable")
    parser.add_argument("--to", required=True, choices=sorted(STAGE_DIRS), help="Target lifecycle stage directory")
    parser.add_argument("--reason", default="", help="Changelog reason, e.g. '/req-review --approve'")
    parser.add_argument("--dry-run", action="store_true", help="Report planned move without applying")
    args = parser.parse_args()

    kind = "req" if args.req else "bug"
    raw_id = args.req or args.bug or ""
    issue_id = normalize_issue_id(kind, raw_id)

    try:
        promotion = resolve_promotion(kind, issue_id, args.to, args.reason.strip())
    except (FileNotFoundError, ValueError, FileExistsError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    return apply_promotion(promotion, dry_run=args.dry_run)


if __name__ == "__main__":
    raise SystemExit(main())
