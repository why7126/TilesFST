#!/usr/bin/env python3
"""Repair users.avatar_object_key values that point to missing media objects."""

from __future__ import annotations

import argparse
import hashlib
import json
import sqlite3
import sys
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path
from typing import Any

PROJECT_ROOT = Path(__file__).resolve().parent.parent
BACKEND_ROOT = PROJECT_ROOT / "src" / "backend"
if str(BACKEND_ROOT) not in sys.path:
    sys.path.insert(0, str(BACKEND_ROOT))


@dataclass(frozen=True)
class AvatarCandidate:
    user_id: str
    username: str
    object_key: str


def default_db_path(project_root: Path = PROJECT_ROOT) -> Path:
    return project_root / "data" / "sqlite" / "tilesfst.db"


def object_key_ref(object_key: str) -> dict[str, str]:
    prefix = object_key.rsplit("/", 1)[0] if "/" in object_key else ""
    return {
        "object_key_hash": hashlib.sha256(object_key.encode("utf-8")).hexdigest()[:16],
        "object_key_prefix": prefix,
    }


def collect_avatar_candidates(db_path: Path) -> list[AvatarCandidate]:
    connection = sqlite3.connect(db_path)
    try:
        rows = connection.execute(
            """
            SELECT id, username, avatar_object_key
            FROM users
            WHERE avatar_object_key IS NOT NULL
              AND TRIM(avatar_object_key) != ''
            ORDER BY username ASC, id ASC
            """
        ).fetchall()
    finally:
        connection.close()
    return [
        AvatarCandidate(
            user_id=str(row[0]),
            username=str(row[1]),
            object_key=str(row[2]),
        )
        for row in rows
    ]


def default_object_exists(object_key: str) -> bool:
    from app.core.exceptions import AppError
    from app.modules.media.storage import MEDIA_NOT_FOUND, get_media_storage_client

    try:
        get_media_storage_client().get_object_info(object_key)
    except ValueError:
        return False
    except AppError as exc:
        if exc.code == MEDIA_NOT_FOUND:
            return False
        raise RuntimeError("object storage unavailable during avatar repair") from exc
    return True


def scan_missing_avatar_objects(
    db_path: Path,
    *,
    exists: Callable[[str], bool] = default_object_exists,
) -> list[AvatarCandidate]:
    missing: list[AvatarCandidate] = []
    for candidate in collect_avatar_candidates(db_path):
        if not exists(candidate.object_key):
            missing.append(candidate)
    return missing


def clear_avatar_keys(db_path: Path, candidates: list[AvatarCandidate]) -> int:
    if not candidates:
        return 0
    connection = sqlite3.connect(db_path)
    try:
        for candidate in candidates:
            connection.execute(
                """
                UPDATE users
                SET avatar_object_key = NULL,
                    updated_at = CURRENT_TIMESTAMP
                WHERE id = ?
                  AND avatar_object_key = ?
                """,
                (candidate.user_id, candidate.object_key),
            )
        connection.commit()
        return int(connection.total_changes)
    finally:
        connection.close()


def build_summary(
    *,
    mode: str,
    candidates: list[AvatarCandidate],
    missing: list[AvatarCandidate],
    cleared: int = 0,
) -> dict[str, Any]:
    missing_ids = {item.user_id for item in missing}
    return {
        "task": "repair-user-avatar-objects",
        "mode": mode,
        "summary": {
            "checked_users": len(candidates),
            "missing_objects": len(missing),
            "cleared_avatar_keys": cleared,
        },
        "items": [
            {
                "user_ref": hashlib.sha256(item.user_id.encode("utf-8")).hexdigest()[:12],
                "username": item.username,
                **object_key_ref(item.object_key),
                "object_exists": item.user_id not in missing_ids,
                "action": "clear_avatar_object_key" if item.user_id in missing_ids else "keep",
            }
            for item in candidates
        ],
        "acceptance_summary": {
            "key": "pass" if not missing or mode == "apply" else "pending",
            "object": "pass" if not missing or mode == "apply" else "pending",
            "url": "pending",
            "render": "pending",
        },
    }


def run_repair(db_path: Path, *, apply: bool, exists: Callable[[str], bool] = default_object_exists) -> dict[str, Any]:
    candidates = collect_avatar_candidates(db_path)
    missing = [item for item in candidates if not exists(item.object_key)]
    cleared = clear_avatar_keys(db_path, missing) if apply else 0
    return build_summary(
        mode="apply" if apply else "dry_run",
        candidates=candidates,
        missing=missing,
        cleared=cleared,
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Audit or clear users.avatar_object_key values that point to missing media objects.",
    )
    parser.add_argument("--db", type=Path, default=None, help="SQLite database path")
    parser.add_argument("--dry-run", action="store_true", help="Inspect missing avatar objects without writing")
    parser.add_argument("--apply", action="store_true", help="Clear missing avatar_object_key values")
    parser.add_argument(
        "--confirm-backup",
        action="store_true",
        help="Required with --apply to confirm database and object storage backup review",
    )
    args = parser.parse_args(argv)

    if args.apply == args.dry_run:
        parser.error("Specify exactly one of --dry-run or --apply")
    if args.apply and not args.confirm_backup:
        parser.error("--apply requires --confirm-backup")

    db_path = args.db or default_db_path()
    if not db_path.is_file():
        print(f"Database not found: {db_path}", file=sys.stderr)
        return 1

    result = run_repair(db_path, apply=args.apply)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
