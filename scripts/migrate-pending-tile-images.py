#!/usr/bin/env python3
"""Compatibility wrapper for the backend media maintenance CLI."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
BACKEND_ROOT = PROJECT_ROOT / "src" / "backend"
if str(BACKEND_ROOT) not in sys.path:
    sys.path.insert(0, str(BACKEND_ROOT))

from app.modules.media import maintenance  # noqa: E402
from app.modules.media.maintenance import run_pending_tile_formalization  # noqa: E402
from app.modules.media.tile_images import deterministic_formal_tile_image_key  # noqa: E402
from app.modules.media.storage import get_media_storage_client  # noqa: E402
from app.db.session import get_session_factory  # noqa: E402


def migrate(*, apply: bool = False, limit: int | None = None) -> dict[str, object]:
    original_storage = maintenance.get_media_storage_client
    original_session_factory = maintenance.get_session_factory
    maintenance.get_media_storage_client = get_media_storage_client
    maintenance.get_session_factory = get_session_factory
    try:
        rows = maintenance._pending_tile_rows(limit)
        target_by_image_id = {
            int(row["image_id"]): deterministic_formal_tile_image_key(
                int(row["tile_id"]),
                str(row["object_key"]),
            )
            for row in rows
        }
        result = run_pending_tile_formalization(
            argparse.Namespace(apply=apply, limit=limit, confirm_backup=apply)
        )
    finally:
        maintenance.get_media_storage_client = original_storage
        maintenance.get_session_factory = original_session_factory
    summary = dict(result["summary"])
    summary["dry_run"] = result["dry_run"]
    summary["items"] = [
        {
            "tile_id": item["tile_id"],
            "image_id": item["image_id"],
            "target_key": target_by_image_id.get(int(item["image_id"])),
            "status": item["status"],
            "failure_reason": item["failure_reason"],
        }
        for item in result["items"]
    ]
    return summary


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--limit", type=int, default=None)
    parser.add_argument("--apply", action="store_true", help="Write object storage and database updates")
    parser.add_argument("--confirm-backup", action="store_true")
    args = parser.parse_args()
    if args.apply and not args.confirm_backup:
        print(
            json.dumps({"status": "blocked", "reason": "--apply requires --confirm-backup"}),
            file=sys.stderr,
        )
        return 2
    print(json.dumps(run_pending_tile_formalization(args), ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
