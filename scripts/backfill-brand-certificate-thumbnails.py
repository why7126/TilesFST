#!/usr/bin/env python3
"""Audit or backfill brand logo and brand certificate image thumbnails."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

from sqlalchemy import text

PROJECT_ROOT = Path(__file__).resolve().parents[1]
BACKEND_ROOT = PROJECT_ROOT / "src" / "backend"
if str(BACKEND_ROOT) not in sys.path:
    sys.path.insert(0, str(BACKEND_ROOT))

from app.core.exceptions import AppError  # noqa: E402
from app.db.session import get_session_factory  # noqa: E402
from app.modules.media.storage import (  # noqa: E402
    generate_image_thumbnail,
    get_media_storage_client,
    same_directory_thumbnail_object_key,
)

IMAGE_MIME_TYPES = {"image/jpeg", "image/jpg", "image/png", "image/webp"}


def _exists(object_key: str) -> bool:
    try:
        get_media_storage_client().get_object_info(object_key)
    except AppError:
        return False
    return True


def _needs_regeneration(original_key: str, thumbnail_key: str) -> tuple[bool, str | None]:
    try:
        original_info = get_media_storage_client().get_object_info(original_key)
    except AppError as exc:
        return False, f"original_missing:{exc.code}"
    try:
        thumbnail_info = get_media_storage_client().get_object_info(thumbnail_key)
    except AppError:
        return True, "thumbnail_missing"

    if original_info.total_size != thumbnail_info.total_size:
        return False, None
    try:
        original = get_media_storage_client().get_object(original_key)
        thumbnail = get_media_storage_client().get_object(thumbnail_key)
    except AppError as exc:
        return True, f"read_failed:{exc.code}"
    return original.content == thumbnail.content, "thumbnail_copied_original"


def _regenerate(original_key: str, thumbnail_key: str) -> tuple[bool, str | None]:
    try:
        original = get_media_storage_client().get_object(original_key)
        thumbnail = generate_image_thumbnail(original.content, original.content_type)
        get_media_storage_client().put_object(thumbnail_key, thumbnail.content, thumbnail.content_type)
    except (AppError, RuntimeError, ValueError, OSError) as exc:
        return False, str(getattr(exc, "code", exc.__class__.__name__))
    return True, None


def _source_rows(limit: int | None) -> list[dict[str, object]]:
    session = get_session_factory()()
    try:
        sql = """
            SELECT 'brand_logo' AS source_type,
                   id AS source_id,
                   logo_object_key AS object_key,
                   NULL AS mime_type
            FROM brands
            WHERE logo_object_key IS NOT NULL
              AND logo_object_key != ''
            UNION ALL
            SELECT 'certificate_file' AS source_type,
                   id AS source_id,
                   file_key AS object_key,
                   file_mime_type AS mime_type
            FROM brand_certificates
            WHERE deleted_at IS NULL
              AND file_key IS NOT NULL
              AND file_key != ''
              AND file_mime_type IN ('image/jpeg', 'image/jpg', 'image/png', 'image/webp')
            UNION ALL
            SELECT 'certificate_image' AS source_type,
                   id AS source_id,
                   file_key AS object_key,
                   file_mime_type AS mime_type
            FROM brand_certificate_images
            WHERE file_key IS NOT NULL
              AND file_key != ''
              AND file_mime_type IN ('image/jpeg', 'image/jpg', 'image/png', 'image/webp')
            ORDER BY source_type ASC, source_id ASC
        """
        params: dict[str, int] = {}
        if limit is not None:
            sql = f"SELECT * FROM ({sql}) scoped LIMIT :limit"
            params["limit"] = limit
        return [dict(row) for row in session.execute(text(sql), params).mappings().all()]
    finally:
        session.close()


def audit(limit: int | None, *, execute: bool = False) -> dict[str, object]:
    items: list[dict[str, object]] = []
    summary = {
        "total": 0,
        "dry_run": not execute,
        "execute": execute,
        "success": 0,
        "failed": 0,
        "skipped": 0,
        "retry_candidates": 0,
        "failure_reasons": {},
    }
    seen: set[str] = set()
    for row in _source_rows(limit):
        object_key = str(row["object_key"] or "").strip()
        if not object_key or object_key in seen:
            continue
        seen.add(object_key)
        thumbnail_key = same_directory_thumbnail_object_key(object_key)
        needs_regeneration, reason = _needs_regeneration(object_key, thumbnail_key)
        status = "dry_run" if needs_regeneration and not execute else "skipped"
        if needs_regeneration:
            summary["retry_candidates"] += 1
            if execute:
                ok, failure = _regenerate(object_key, thumbnail_key)
                if ok:
                    status = "regenerated"
                    summary["success"] += 1
                    reason = None
                else:
                    status = "failed"
                    summary["failed"] += 1
                    reason = failure
                    failure_reasons = summary["failure_reasons"]
                    assert isinstance(failure_reasons, dict)
                    failure_reasons[reason or "unknown"] = failure_reasons.get(reason or "unknown", 0) + 1
        else:
            summary["skipped"] += 1

        items.append(
            {
                "source_type": row["source_type"],
                "source_id": row["source_id"],
                "object_key": object_key,
                "thumbnail_key": thumbnail_key,
                "thumbnail_exists": _exists(thumbnail_key),
                "needs_regeneration": needs_regeneration,
                "status": status,
                "reason": reason,
            }
        )

    summary["total"] = len(items)
    return {"summary": summary, "items": items}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--limit", type=int, default=None)
    parser.add_argument("--execute", action="store_true", help="Write missing or invalid thumbnails")
    args = parser.parse_args()
    print(json.dumps(audit(args.limit, execute=args.execute), ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
