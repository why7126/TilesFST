#!/usr/bin/env python3
"""Clean legacy business media orphans under data/uploads after MinIO migration (BUG-0008)."""

from __future__ import annotations

import argparse
import sqlite3
import sys
from dataclasses import dataclass
from pathlib import Path

SKIP_FILENAMES = frozenset({".gitkeep", ".DS_Store"})

MEDIA_OBJECT_KEY_QUERIES: tuple[tuple[str, str], ...] = (
    ("brands", "logo_object_key"),
    ("users", "avatar_object_key"),
    ("tile_images", "object_key"),
    ("tile_videos", "object_key"),
)


@dataclass(frozen=True)
class ScanResult:
    referenced_keys: frozenset[str]
    orphan_files: tuple[Path, ...]
    uploads_root: Path


def default_project_root() -> Path:
    return Path(__file__).resolve().parent.parent


def default_db_path(project_root: Path) -> Path:
    return project_root / "data" / "sqlite" / "tile-info-platform.db"


def default_uploads_root(project_root: Path) -> Path:
    return project_root / "data" / "uploads"


def collect_referenced_object_keys(db_path: Path) -> set[str]:
    if not db_path.is_file():
        return set()

    keys: set[str] = set()
    connection = sqlite3.connect(db_path)
    try:
        for table, column in MEDIA_OBJECT_KEY_QUERIES:
            try:
                rows = connection.execute(
                    f"SELECT {column} FROM {table} WHERE {column} IS NOT NULL AND TRIM({column}) != ''"
                ).fetchall()
            except sqlite3.OperationalError:
                continue
            for (value,) in rows:
                normalized = str(value).strip().lstrip("/")
                if normalized:
                    keys.add(normalized)
    finally:
        connection.close()
    return keys


def iter_upload_media_files(uploads_root: Path) -> list[Path]:
    if not uploads_root.is_dir():
        return []

    files: list[Path] = []
    for path in uploads_root.rglob("*"):
        if not path.is_file():
            continue
        if path.name in SKIP_FILENAMES:
            continue
        files.append(path)
    return sorted(files)


def relative_object_key(path: Path, uploads_root: Path) -> str:
    return path.relative_to(uploads_root).as_posix()


def scan_legacy_uploads(
    *,
    db_path: Path,
    uploads_root: Path,
) -> ScanResult:
    referenced = frozenset(collect_referenced_object_keys(db_path))
    orphan_files: list[Path] = []
    for file_path in iter_upload_media_files(uploads_root):
        key = relative_object_key(file_path, uploads_root)
        if key not in referenced:
            orphan_files.append(file_path)
    return ScanResult(
        referenced_keys=referenced,
        orphan_files=tuple(orphan_files),
        uploads_root=uploads_root,
    )


def apply_cleanup(orphan_files: tuple[Path, ...], *, dry_run: bool) -> int:
    deleted = 0
    for file_path in orphan_files:
        if dry_run:
            print(f"[dry-run] would delete: {file_path}")
        else:
            file_path.unlink(missing_ok=True)
            print(f"deleted: {file_path}")
        deleted += 1
    return deleted


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Remove legacy business media orphans from data/uploads (post MinIO migration).",
    )
    parser.add_argument(
        "--project-root",
        type=Path,
        default=default_project_root(),
        help="Repository root (default: parent of scripts/).",
    )
    parser.add_argument(
        "--db-path",
        type=Path,
        default=None,
        help="SQLite database path (default: data/sqlite/tile-info-platform.db).",
    )
    parser.add_argument(
        "--uploads-root",
        type=Path,
        default=None,
        help="Legacy uploads directory (default: data/uploads).",
    )
    parser.add_argument(
        "--apply",
        action="store_true",
        help="Delete orphan files under data/uploads.",
    )
    parser.add_argument(
        "--check-only",
        action="store_true",
        help="Exit 0 when no orphans remain; exit 1 when orphans exist.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    project_root: Path = args.project_root
    db_path = args.db_path or default_db_path(project_root)
    uploads_root = args.uploads_root or default_uploads_root(project_root)

    result = scan_legacy_uploads(db_path=db_path, uploads_root=uploads_root)
    orphan_count = len(result.orphan_files)

    print(f"uploads_root: {uploads_root}")
    print(f"db_path: {db_path}")
    print(f"referenced_object_keys: {len(result.referenced_keys)}")
    print(f"orphan_files: {orphan_count}")

    if args.check_only:
        if orphan_count == 0:
            print("status: no legacy upload residue")
            return 0
        for file_path in result.orphan_files:
            print(f"orphan: {file_path}")
        print("status: legacy upload residue found")
        return 1

    dry_run = not args.apply
    if orphan_count == 0:
        print("nothing to clean")
        return 0

    apply_cleanup(result.orphan_files, dry_run=dry_run)
    if dry_run:
        print("dry-run complete; re-run with --apply to delete")
    else:
        print(f"cleanup complete; deleted {orphan_count} file(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
