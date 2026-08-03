#!/usr/bin/env python3
"""Migrate public SKU main images from pending tile paths into SKU directories."""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import sys

from sqlalchemy import text

PROJECT_ROOT = Path(__file__).resolve().parents[1]
BACKEND_ROOT = PROJECT_ROOT / "src" / "backend"
if str(BACKEND_ROOT) not in sys.path:
    sys.path.insert(0, str(BACKEND_ROOT))

from app.core.exceptions import AppError  # noqa: E402
from app.core.config import settings  # noqa: E402
from app.db.session import get_session_factory  # noqa: E402
from app.modules.media.storage import get_media_storage_client, same_directory_thumbnail_object_key  # noqa: E402
from app.modules.media.tile_images import (  # noqa: E402
    PENDING_TILE_IMAGE_PREFIX,
    deterministic_formal_tile_image_key,
    formalize_tile_image_object,
)


DEFAULT_LOCAL_DATABASE_URL = f"sqlite:///{PROJECT_ROOT / 'data' / 'sqlite' / 'tilesfst.db'}"

if not os.environ.get("DATABASE_URL") and settings.database_url.startswith("sqlite:////app/"):
    settings.database_url = DEFAULT_LOCAL_DATABASE_URL


def _object_exists(object_key: str) -> bool:
    try:
        get_media_storage_client().get_object_info(object_key)
    except AppError:
        return False
    return True


def _select_rows(limit: int | None) -> list[dict[str, object]]:
    session = get_session_factory()()
    try:
        sql = """
            SELECT
              t.id AS tile_id,
              t.sku_code,
              ti.id AS image_id,
              ti.object_key
            FROM tiles t
            JOIN tile_images ti
              ON ti.tile_id = t.id
             AND ti.is_main = 1
            JOIN brands b ON b.id = t.brand_id
            JOIN tile_categories c ON c.id = t.category_id
            LEFT JOIN tile_specs s ON s.id = t.spec_id
            WHERE t.status = 'PUBLISHED'
              AND b.status = 'ENABLED'
              AND c.status = 'ENABLED'
              AND (t.spec_id IS NULL OR s.status = 'ENABLED')
              AND ti.object_key LIKE :pending_prefix
            ORDER BY t.id ASC, ti.id ASC
        """
        params: dict[str, object] = {"pending_prefix": f"{PENDING_TILE_IMAGE_PREFIX}%"}
        if limit is not None:
            sql += " LIMIT :limit"
            params["limit"] = limit
        return [dict(row) for row in session.execute(text(sql), params).mappings().all()]
    finally:
        session.close()


def _update_image_reference(*, image_id: int, target_key: str) -> None:
    session = get_session_factory()()
    try:
        session.execute(
            text(
                """
                UPDATE tile_images
                SET object_key = :object_key,
                    url = :url
                WHERE id = :image_id
                """
            ),
            {
                "image_id": image_id,
                "object_key": target_key,
                "url": f"/media/{target_key}",
            },
        )
        session.commit()
    finally:
        session.close()


def migrate(*, apply: bool, limit: int | None = None) -> dict[str, object]:
    rows = _select_rows(limit)
    items: list[dict[str, object]] = []
    missing_original = 0
    missing_thumbnail = 0
    target_exists = 0
    success = 0
    failed = 0
    failure_reasons: dict[str, int] = {}

    for row in rows:
        tile_id = int(row["tile_id"])
        image_id = int(row["image_id"])
        object_key = str(row["object_key"])
        target_key = deterministic_formal_tile_image_key(tile_id, object_key)
        thumbnail_key = same_directory_thumbnail_object_key(object_key)
        target_thumbnail_key = same_directory_thumbnail_object_key(target_key)
        original_exists = _object_exists(object_key)
        thumbnail_exists = _object_exists(thumbnail_key)
        destination_exists = _object_exists(target_key)

        missing_original += 0 if original_exists else 1
        missing_thumbnail += 0 if thumbnail_exists else 1
        target_exists += 1 if destination_exists else 0
        status = "dry_run"
        failure_reason = None

        if apply:
            if not original_exists:
                failed += 1
                status = "failed"
                failure_reason = "missing_original"
                failure_reasons[failure_reason] = failure_reasons.get(failure_reason, 0) + 1
            else:
                try:
                    formalize_tile_image_object(
                        tile_id=tile_id,
                        object_key=object_key,
                        target_key=target_key,
                    )
                    _update_image_reference(image_id=image_id, target_key=target_key)
                    success += 1
                    status = "migrated"
                except AppError as exc:
                    failed += 1
                    status = "failed"
                    failure_reason = str(exc.code)
                    failure_reasons[failure_reason] = failure_reasons.get(failure_reason, 0) + 1

        items.append(
            {
                "tile_id": tile_id,
                "sku_code": str(row["sku_code"]),
                "image_id": image_id,
                "source_key": object_key,
                "target_key": target_key,
                "source_thumbnail_key": thumbnail_key,
                "target_thumbnail_key": target_thumbnail_key,
                "original_exists": original_exists,
                "thumbnail_exists": thumbnail_exists,
                "target_exists": destination_exists,
                "status": status,
                "failure_reason": failure_reason,
            }
        )

    return {
        "mode": "apply" if apply else "dry_run",
        "dry_run": not apply,
        "total": len(rows),
        "success": success,
        "failed": failed,
        "missing_original": missing_original,
        "missing_thumbnail": missing_thumbnail,
        "target_exists": target_exists,
        "failure_reasons": failure_reasons,
        "items": items,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--limit", type=int, default=None)
    parser.add_argument("--apply", action="store_true", help="Write object storage and database updates")
    args = parser.parse_args()
    print(json.dumps(migrate(apply=args.apply, limit=args.limit), ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
