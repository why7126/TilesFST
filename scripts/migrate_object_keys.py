#!/usr/bin/env python3
"""Migrate legacy object storage keys to REQ-0012 semantic layout.

Backup before apply:
  - SQLite: cp data/sqlite/tilesfst.db data/sqlite/tilesfst.db.bak
  - Object storage: snapshot bucket or export referenced objects

Rollback:
  - Restore SQLite backup
  - Restore object storage bucket snapshot (or re-run with reversed mapping — not automated)

Usage:
  python scripts/migrate_object_keys.py --dry-run
  python scripts/migrate_object_keys.py --apply
"""

from __future__ import annotations

import argparse
import os
import sqlite3
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
BACKEND_ROOT = PROJECT_ROOT / "src" / "backend"
if str(BACKEND_ROOT) not in sys.path:
    sys.path.insert(0, str(BACKEND_ROOT))

from app.modules.media.key_migration import KeyMigration, collect_migrations  # noqa: E402


def default_db_path(project_root: Path) -> Path:
    return project_root / "data" / "sqlite" / "tilesfst.db"


def _object_storage_client():
    from minio import Minio

    endpoint = os.environ.get("OBJECT_STORAGE_ENDPOINT", "localhost:9000")
    access_key = os.environ.get("OBJECT_STORAGE_ACCESS_KEY", "minioadmin")
    secret_key = os.environ.get("OBJECT_STORAGE_SECRET_KEY", "minioadmin")
    secure = os.environ.get("OBJECT_STORAGE_SECURE", "false").lower() in {"1", "true", "yes"}
    bucket = os.environ.get("OBJECT_STORAGE_BUCKET", "tilesfst")
    region = os.environ.get("OBJECT_STORAGE_REGION") or None
    path_style = os.environ.get("OBJECT_STORAGE_PATH_STYLE", "true").lower() in {"1", "true", "yes"}
    client = Minio(endpoint, access_key=access_key, secret_key=secret_key, secure=secure, region=region)
    if not path_style:
        client._base_url._virtual_style_flag = True
    return client, bucket


def migrate_object_storage_object(client, bucket: str, old_key: str, new_key: str, *, apply: bool) -> None:
    from minio.commonconfig import CopySource

    try:
        client.stat_object(bucket, old_key)
    except Exception as exc:
        code = getattr(exc, "code", "")
        if code in {"NoSuchKey", "NoSuchObject"}:
            raise RuntimeError(f"Object storage object missing for DB key: {old_key}") from exc
        raise

    if not apply:
        return

    client.copy_object(bucket, new_key, CopySource(bucket, old_key))
    client.stat_object(bucket, new_key)
    client.remove_object(bucket, old_key)


def apply_db_updates(db_path: Path, migrations: list[KeyMigration], *, apply: bool) -> None:
    if not apply:
        return

    connection = sqlite3.connect(db_path)
    try:
        for item in migrations:
            connection.execute(
                f"UPDATE {item.table} SET {item.column} = ? WHERE rowid = ?",
                (item.new_key, item.row_id),
            )
        connection.commit()
    finally:
        connection.close()


def run_migration(db_path: Path, *, apply: bool) -> int:
    migrations = collect_migrations(db_path)
    if not migrations:
        print("No legacy object keys found in database.")
        return 0

    print(f"{'APPLY' if apply else 'DRY-RUN'}: {len(migrations)} object key(s) to migrate")
    for item in migrations:
        print(f"  [{item.table}.{item.column}] {item.old_key} -> {item.new_key}")

    if not apply:
        print("Dry-run complete; no changes written.")
        return 0

    client, bucket = _object_storage_client()
    seen: set[tuple[str, str]] = set()
    for item in migrations:
        pair = (item.old_key, item.new_key)
        if pair in seen:
            continue
        seen.add(pair)
        migrate_object_storage_object(client, bucket, item.old_key, item.new_key, apply=apply)

    apply_db_updates(db_path, migrations, apply=True)
    print("Migration applied successfully.")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Migrate legacy object storage keys to REQ-0012 layout.",
        epilog=(
            "Backup SQLite and object storage before --apply. "
            "Rollback by restoring backups; this script does not auto-reverse."
        ),
    )
    parser.add_argument("--db", type=Path, default=None, help="SQLite database path")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview mappings without writing MinIO or SQLite",
    )
    parser.add_argument(
        "--apply",
        action="store_true",
        help="Copy objects in object storage and update SQLite references",
    )
    args = parser.parse_args(argv)

    if args.apply == args.dry_run:
        parser.error("Specify exactly one of --dry-run or --apply")

    db_path = args.db or default_db_path(PROJECT_ROOT)
    if not db_path.is_file():
        print(f"Database not found: {db_path}", file=sys.stderr)
        return 1

    try:
        return run_migration(db_path, apply=args.apply)
    except RuntimeError as exc:
        print(str(exc), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
