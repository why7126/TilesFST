#!/usr/bin/env python3
"""Migrate flat iterations/sprint-* dirs into change/archive.

See rules/iterations-lifecycle.md.
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
STAGE_DIRS = ("change", "archive")


@dataclass
class MigrationItem:
    sprint_id: str
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


def parse_sprint_status(yaml_text: str) -> str | None:
    for line in yaml_text.splitlines():
        if line.startswith("status:"):
            return line.split(":", 1)[1].strip()
    return None


def classify_stage(status: str | None) -> str:
    value = (status or "planning").lower()
    if value in {"completed", "closed", "archived"}:
        return "archive"
    return "change"


def iter_flat_sprint_dirs(base: Path) -> list[Path]:
    if not base.is_dir():
        return []
    result: list[Path] = []
    for path in sorted(base.iterdir()):
        if not path.is_dir():
            continue
        if path.name in STAGE_DIRS or path.name.startswith("_"):
            continue
        if path.name.startswith("sprint-") and (path / "sprint.yaml").exists():
            result.append(path)
    return result


def collect_migrations() -> list[MigrationItem]:
    base = ROOT / "iterations"
    items: list[MigrationItem] = []
    for src in iter_flat_sprint_dirs(base):
        yaml_path = src / "sprint.yaml"
        status = parse_sprint_status(read_text(yaml_path))
        stage = classify_stage(status)
        dest = base / stage / src.name
        items.append(
            MigrationItem(
                sprint_id=src.name,
                status=status or "unknown",
                stage=stage,
                src=src,
                dest=dest,
            )
        )
    return items


def patch_sprint_yaml(yaml_path: Path, stage: str) -> bool:
    if not yaml_path.exists():
        return False
    text = read_text(yaml_path)
    original = text

    if re.search(r"^lifecycle_stage:\s*", text, flags=re.MULTILINE):
        text = re.sub(
            r"^lifecycle_stage:\s*.+$",
            f"lifecycle_stage: {stage}",
            text,
            count=1,
            flags=re.MULTILINE,
        )
    else:
        text = re.sub(
            r"(^status: .+$)",
            rf"\1\nlifecycle_stage: {stage}",
            text,
            count=1,
            flags=re.MULTILINE,
        )

    old_base = f"iterations/{yaml_path.parent.name}"
    new_base = f"iterations/{stage}/{yaml_path.parent.name}"
    if old_base in text:
        text = text.replace(old_base, new_base)

    if text != original:
        write_text(yaml_path, text)
        return True
    return False


def patch_sprint_md(md_path: Path, stage: str, stamp: str) -> bool:
    if not md_path.exists():
        return False
    text = read_text(md_path)
    original = text
    sprint_id = md_path.parent.name

    old_base = f"iterations/{sprint_id}"
    new_base = f"iterations/{stage}/{sprint_id}"
    if old_base in text:
        text = text.replace(old_base, new_base)

    entry = f"| {stamp} | lifecycle-stage-migrate | 迁入 `{stage}/`（status → stage 映射） |"
    if entry not in text:
        if "## 变更记录" in text:
            text = text.replace("## 变更记录\n\n", f"## 变更记录\n\n{entry}\n", 1)
        elif "## 里程碑" in text:
            text = text.replace("## 里程碑\n", f"## 变更记录\n\n{entry}\n\n## 里程碑\n", 1)

    if text != original:
        write_text(md_path, text)
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
        new_base = f"iterations/{m.stage}/{m.sprint_id}"
        replacements.append((f"iterations/{m.sprint_id}/", f"{new_base}/"))
        replacements.append((f"iterations/{m.sprint_id}", new_base))
    replacements.sort(key=lambda pair: len(pair[0]), reverse=True)

    legacy_pattern = re.compile(
        r"iterations/"
        r"(?!change/|archive/)"
        r"(sprint-\d{3}[^/\s`\"']*)"
    )

    def rewrite_legacy_paths(text: str) -> str:
        id_to_stage = {m.sprint_id: m.stage for m in items}

        def repl(match: re.Match[str]) -> str:
            sprint_id = match.group(1)
            stage = id_to_stage.get(sprint_id)
            if stage is None:
                return match.group(0)
            return f"iterations/{stage}/{sprint_id}"

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
        if path.name == "migrate-iterations-lifecycle-stage.py":
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
    base = ROOT / "iterations"
    items: list[MigrationItem] = []
    for stage in STAGE_DIRS:
        stage_root = base / stage
        if not stage_root.is_dir():
            continue
        for path in sorted(stage_root.iterdir()):
            if path.is_dir() and path.name.startswith("sprint-"):
                items.append(
                    MigrationItem(
                        sprint_id=path.name,
                        status="",
                        stage=stage,
                        src=path,
                        dest=path,
                    )
                )
    return items


def main() -> int:
    parser = argparse.ArgumentParser(description="Migrate iterations to change/archive")
    parser.add_argument("--apply", action="store_true", help="Perform moves (default dry-run)")
    parser.add_argument("--skip-ref-update", action="store_true", help="Do not bulk-update path references")
    parser.add_argument(
        "--ref-update-only",
        action="store_true",
        help="Only bulk-update path references for staged sprint dirs",
    )
    args = parser.parse_args()

    if args.ref_update_only:
        items = collect_staged_items()
        if not items:
            print("No staged sprint directories found.")
            return 0
        updated = update_repo_references(items)
        print(f"Updated path references in {updated} files.")
        return 0

    items = collect_migrations()
    if not items:
        print("No flat sprint-* directories to migrate.")
        return 0

    by_stage: dict[str, list[MigrationItem]] = {s: [] for s in STAGE_DIRS}
    for item in items:
        by_stage[item.stage].append(item)

    print(f"Found {len(items)} sprint directories to migrate\n")
    for stage in STAGE_DIRS:
        print(f"## {stage}/ ({len(by_stage[stage])})")
        for item in by_stage[stage]:
            rel_src = item.src.relative_to(ROOT)
            rel_dest = item.dest.relative_to(ROOT)
            print(f"  {item.sprint_id}  status={item.status}")
            print(f"    {rel_src} -> {rel_dest}")
        print()

    if not args.apply:
        print("Dry-run only. Re-run with --apply to migrate.")
        return 0

    stamp = now_shanghai()
    for item in items:
        git_mv(item.src, item.dest)
        patch_sprint_yaml(item.dest / "sprint.yaml", item.stage)
        patch_sprint_md(item.dest / "sprint.md", item.stage, stamp)
        print(f"moved {item.sprint_id} -> {item.stage}/")

    if not args.skip_ref_update:
        updated = update_repo_references(items)
        print(f"\nUpdated path references in {updated} files.")

    print("\nMigration complete. Consider running: python scripts/sync-workflow-status.py --check")
    return 0


if __name__ == "__main__":
    sys.exit(main())
