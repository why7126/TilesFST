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
from app.modules.media.maintenance import run_thumbnail_backfill  # noqa: E402
from app.modules.media.storage import get_media_storage_client  # noqa: E402
from app.db.session import get_session_factory  # noqa: E402


def audit(*, limit: int | None = None, execute: bool = False) -> dict[str, object]:
    original_storage = maintenance.get_media_storage_client
    original_session_factory = maintenance.get_session_factory
    maintenance.get_media_storage_client = get_media_storage_client
    maintenance.get_session_factory = get_session_factory
    try:
        return run_thumbnail_backfill(
            argparse.Namespace(apply=execute, limit=limit, confirm_backup=execute)
        )
    finally:
        maintenance.get_media_storage_client = original_storage
        maintenance.get_session_factory = original_session_factory


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--limit", type=int, default=None)
    parser.add_argument("--execute", action="store_true", help="Write missing or invalid thumbnails")
    parser.add_argument(
        "--confirm-backup",
        action="store_true",
        help="Required with --execute for production-safe apply",
    )
    args = parser.parse_args()
    args.apply = args.execute
    if args.execute and not args.confirm_backup:
        print(
            json.dumps({"status": "blocked", "reason": "--execute requires --confirm-backup"}),
            file=sys.stderr,
        )
        return 2
    print(json.dumps(run_thumbnail_backfill(args), ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
