#!/usr/bin/env python3
"""Migrate flat issues/requirements and issues/bugs dirs into plan/review/archive.

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

ROOT = Path(__file__).resolve().parents[1]
STAGE_DIRS = ("plan", "review", "archive")
ISSUE_PREFIXES = ("REQ-", "BUG-")


@dataclass
class MigrationItem:
    kind: str  # req | bug
    issue_id: str
    status: str
    stage: str
    src: Path
    dest: Path


def now_shanghai() -> str:
    return datetime.now(ZoneInfo("Asia/Shanghai")).strftime("%Y-%m-%d %H:%M:%S")


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def write_text(path: Path, text: str) -> None:
    path.write_text(text, encoding="utf-8")


def parse_frontmatter_status(text: str) -> str | None:
    if not text.startswith("---"):
        return None
    end = text.find("\n---", 3)
    if end == -1:
        return None
    block = text[3:end]
    for line in block.splitlines():
        if line.startswith("status:"):
            return line.split(":", 1)[1].strip()
    return None


def parse_trace_status(text: str) -> str | None:
    frontmatter_status = parse_frontmatter_status(text)
    yaml_status: str | None = None
    yaml_match = re.search(r"```yaml\n(.*?)```", text, re.DOTALL)
    if yaml_match:
        for line in yaml_match.group(1).splitlines():
            if line.strip().startswith("status:"):
                yaml_status = line.split(":", 1)[1].strip()
                break
    if yaml_status and (
        frontmatter_status is None
        or frontmatter_status in {"ready", "draft", "captured", "pending_review"}
    ):
        return yaml_status
    return frontmatter_status or yaml_status


def classify_stage(status: str | None) -> str:
    value = (status or "captured").lower()
    if value in {"done", "archived", "resolved", "completed", "closed"}:
        return "archive"
    if value in {"approved", "in_sprint", "applied"}:
        return "review"
    return "plan"


def iter_flat_issue_dirs(base: Path) -> list[Path]:
    if not base.is_dir():
        return []
    result: list[Path] = []
    for path in sorted(base.iterdir()):
        if not path.is_dir():
            continue
        if path.name in STAGE_DIRS or path.name.startswith("_"):
            continue
        if path.name.startswith(ISSUE_PREFIXES):
            result.append(path)
    return result


def collect_migrations() -> list[MigrationItem]:
    items: list[MigrationItem] = []
    for base_rel, kind in (("issues/requirements", "req"), ("issues/bugs", "bug")):
        base = ROOT / base_rel
        for src in iter_flat_issue_dirs(base):
            trace_path = src / "trace.md"
            status = parse_trace_status(read_text(trace_path)) if trace_path.exists() else "captured"
            stage = classify_stage(status)
            dest = base / stage / src.name
            items.append(
                MigrationItem(
                    kind=kind,
                    issue_id=src.name,
                    status=status or "unknown",
                    stage=stage,
                    src=src,
                    dest=dest,
                )
            )
    return items


def patch_trace(trace_path: Path, stage: str, stamp: str) -> bool:
    if not trace_path.exists():
        return False
    text = read_text(trace_path)
    original = text

    if re.search(r"^lifecycle_stage:\s*", text, flags=re.MULTILINE):
        text = re.sub(r"^lifecycle_stage:\s*.+$", f"lifecycle_stage: {stage}", text, count=1, flags=re.MULTILINE)
    else:
        text = re.sub(
            r"(^status: .+$)",
            rf"\1\nlifecycle_stage: {stage}",
            text,
            count=1,
            flags=re.MULTILINE,
        )

    text = re.sub(r"^updated_at: .+$", f"updated_at: {stamp}", text, count=1, flags=re.MULTILINE)

    entry = f"| {stamp} | lifecycle-stage-migrate | 迁入 `{stage}/`（status → stage 映射） |"
    if entry not in text and "## 变更记录" in text:
        text = text.replace("## 变更记录\n\n", f"## 变更记录\n\n{entry}\n", 1)

    old_prefix = trace_path.parent.as_posix().split("issues/", 1)[-1]
    issue_id = trace_path.parent.name
    kind_root = "requirements" if "/requirements/" in trace_path.as_posix() else "bugs"
    old_base = f"issues/{kind_root}/{issue_id}"
    new_base = f"issues/{kind_root}/{stage}/{issue_id}"
    if old_base in text:
        text = text.replace(old_base, new_base)

    if text != original:
        write_text(trace_path, text)
        return True
    return False


def git_mv(src: Path, dest: Path) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    if dest.exists():
        raise FileExistsError(f"destination already exists: {dest}")
    try:
        subprocess.run(["git", "mv", str(src), str(dest)], cwd=ROOT, check=True, capture_output=True, text=True)
    except subprocess.CalledProcessError:
        shutil.move(str(src), str(dest))


def update_repo_references(items: list[MigrationItem]) -> int:
    replacements: list[tuple[str, str]] = []
    for m in items:
        base = f"issues/{'requirements' if m.kind == 'req' else 'bugs'}"
        new_base = f"{base}/{m.stage}/{m.issue_id}"
        replacements.append((f"{base}/{m.issue_id}/", f"{new_base}/"))
        replacements.append((f"{base}/{m.issue_id}", new_base))
    # Longest old path first so trailing-slash variants win over bare ids.
    replacements.sort(key=lambda pair: len(pair[0]), reverse=True)

    legacy_pattern = re.compile(
        r"issues/(requirements|bugs)/"
        r"(?!plan/|review/|archive/)"
        r"((?:REQ|BUG)-\d{4}[^/\s`\"']*)"
    )

    def rewrite_legacy_paths(text: str) -> str:
        id_to_stage = {m.issue_id: m.stage for m in items}

        def repl(match: re.Match[str]) -> str:
            kind_dir = match.group(1)
            issue_id = match.group(2)
            stage = id_to_stage.get(issue_id)
            if stage is None:
                return match.group(0)
            return f"issues/{kind_dir}/{stage}/{issue_id}"

        return legacy_pattern.sub(repl, text)

    count = 0
    skip_dirs = {".git", "node_modules", ".venv", "dist", "__pycache__"}
    for path in ROOT.rglob("*"):
        if not path.is_file():
            continue
        if any(part in skip_dirs for part in path.parts):
            continue
        if path.suffix not in {".md", ".yaml", ".yml", ".py", ".ts", ".tsx", ".json", ".html"}:
            continue
        if path.name == "migrate-issues-lifecycle-stage.py":
            continue
        text = read_text(path)
        new_text = text
        for old, new in replacements:
            new_text = new_text.replace(old, new)
        new_text = rewrite_legacy_paths(new_text)
        if new_text != text:
            write_text(path, new_text)
            count += 1
    return count


def collect_staged_items() -> list[MigrationItem]:
    items: list[MigrationItem] = []
    for kind, base in (("req", "requirements"), ("bug", "bugs")):
        prefix = "REQ-" if kind == "req" else "BUG-"
        for stage in STAGE_DIRS:
            stage_root = ROOT / "issues" / base / stage
            if not stage_root.is_dir():
                continue
            for path in sorted(stage_root.iterdir()):
                if path.is_dir() and path.name.startswith(prefix):
                    items.append(
                        MigrationItem(
                            kind=kind,
                            issue_id=path.name,
                            status="",
                            stage=stage,
                            src=path,
                            dest=path,
                        )
                    )
    return items


def main() -> int:
    parser = argparse.ArgumentParser(description="Migrate issues to plan/review/archive")
    parser.add_argument("--apply", action="store_true", help="Perform moves (default dry-run)")
    parser.add_argument("--skip-ref-update", action="store_true", help="Do not bulk-update path references")
    parser.add_argument(
        "--ref-update-only",
        action="store_true",
        help="Only bulk-update path references for staged issue dirs",
    )
    args = parser.parse_args()

    if args.ref_update_only:
        items = collect_staged_items()
        if not items:
            print("No staged REQ/BUG directories found.")
            return 0
        updated = update_repo_references(items)
        print(f"Updated path references in {updated} files.")
        return 0

    items = collect_migrations()
    if not items:
        print("No flat REQ/BUG directories to migrate.")
        return 0

    by_stage: dict[str, list[MigrationItem]] = {s: [] for s in STAGE_DIRS}
    for item in items:
        by_stage[item.stage].append(item)

    print(f"Found {len(items)} issue directories to migrate\n")
    for stage in STAGE_DIRS:
        print(f"## {stage}/ ({len(by_stage[stage])})")
        for item in by_stage[stage]:
            rel_src = item.src.relative_to(ROOT)
            rel_dest = item.dest.relative_to(ROOT)
            print(f"  [{item.kind}] {item.issue_id}  status={item.status}")
            print(f"    {rel_src} -> {rel_dest}")
        print()

    if not args.apply:
        print("Dry-run only. Re-run with --apply to migrate.")
        return 0

    stamp = now_shanghai()
    for item in items:
        git_mv(item.src, item.dest)
        patch_trace(item.dest / "trace.md", item.stage, stamp)
        print(f"moved {item.issue_id} -> {item.stage}/")

    if not args.skip_ref_update:
        updated = update_repo_references(items)
        print(f"\nUpdated path references in {updated} files.")

    print("\nMigration complete. Consider running: python scripts/sync-workflow-status.py --check")
    return 0


if __name__ == "__main__":
    sys.exit(main())
