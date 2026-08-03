#!/usr/bin/env python3
"""Audit public miniapp product card image object references."""

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


def _exists(object_key: str) -> bool:
    try:
        get_media_storage_client().get_object_info(object_key)
    except AppError:
        return False
    return True


def _thumbnail_audit(original_key: str, thumbnail_key: str) -> dict[str, object]:
    try:
        original_info = get_media_storage_client().get_object_info(original_key)
    except AppError as exc:
        return {"original_exists": False, "thumbnail_exists": False, "failure_reason": str(exc.code)}
    try:
        thumbnail_info = get_media_storage_client().get_object_info(thumbnail_key)
    except AppError:
        return {
            "original_exists": True,
            "thumbnail_exists": False,
            "same_size": False,
            "same_bytes": False,
            "needs_regeneration": True,
            "failure_reason": None,
        }

    same_size = original_info.total_size == thumbnail_info.total_size
    same_bytes = False
    if same_size:
        try:
            original = get_media_storage_client().get_object(original_key)
            thumbnail = get_media_storage_client().get_object(thumbnail_key)
        except AppError as exc:
            return {
                "original_exists": True,
                "thumbnail_exists": True,
                "same_size": same_size,
                "same_bytes": False,
                "needs_regeneration": True,
                "failure_reason": str(exc.code),
            }
        same_bytes = original.content == thumbnail.content

    return {
        "original_exists": True,
        "thumbnail_exists": True,
        "same_size": same_size,
        "same_bytes": same_bytes,
        "needs_regeneration": same_size or same_bytes,
        "failure_reason": None,
    }


def _regenerate_thumbnail(original_key: str, thumbnail_key: str) -> tuple[bool, str | None]:
    try:
        original = get_media_storage_client().get_object(original_key)
        generated = generate_image_thumbnail(original.content, original.content_type)
        get_media_storage_client().put_object(
            thumbnail_key,
            generated.content,
            generated.content_type,
        )
    except (AppError, RuntimeError, ValueError, OSError) as exc:
        return False, str(getattr(exc, "code", exc.__class__.__name__))
    return True, None


def audit(limit: int | None, *, backfill: bool = False, execute: bool = False) -> dict[str, object]:
    session = get_session_factory()()
    try:
        sql = """
            SELECT t.id AS product_id, t.sku_code, ti.object_key
            FROM tiles t
            LEFT JOIN tile_images ti
              ON ti.tile_id = t.id
             AND ti.is_main = 1
            JOIN brands b ON b.id = t.brand_id
            JOIN tile_categories c ON c.id = t.category_id
            LEFT JOIN tile_specs s ON s.id = t.spec_id
            WHERE t.status = 'PUBLISHED'
              AND b.status = 'ENABLED'
              AND c.status = 'ENABLED'
              AND (t.spec_id IS NULL OR s.status = 'ENABLED')
            ORDER BY t.id ASC
        """
        params: dict[str, int] = {}
        if limit is not None:
            sql += " LIMIT :limit"
            params["limit"] = limit
        rows = session.execute(text(sql), params).mappings().all()
    finally:
        session.close()

    items: list[dict[str, object]] = []
    missing_main = 0
    missing_original = 0
    missing_thumbnail = 0
    same_size_thumbnail = 0
    same_bytes_thumbnail = 0
    needs_regeneration = 0
    skipped_valid_thumbnail = 0
    pending_main_image = 0
    backfill_success = 0
    backfill_failed = 0
    failure_reasons: dict[str, int] = {}
    for row in rows:
        object_key = str(row["object_key"] or "").strip()
        thumbnail_key = same_directory_thumbnail_object_key(object_key) if object_key else ""
        is_pending = object_key.startswith("images/default/tiles/pending/")
        audit_result = _thumbnail_audit(object_key, thumbnail_key) if object_key else {}
        original_exists = bool(audit_result.get("original_exists", False))
        thumbnail_exists = bool(audit_result.get("thumbnail_exists", False))
        same_size = bool(audit_result.get("same_size", False))
        same_bytes = bool(audit_result.get("same_bytes", False))
        row_needs_regeneration = bool(audit_result.get("needs_regeneration", False))
        missing_main += 0 if object_key else 1
        missing_original += 0 if (not object_key or original_exists) else 1
        missing_thumbnail += 0 if (not object_key or thumbnail_exists) else 1
        same_size_thumbnail += 1 if same_size else 0
        same_bytes_thumbnail += 1 if same_bytes else 0
        needs_regeneration += 1 if row_needs_regeneration else 0
        skipped_valid_thumbnail += 1 if (thumbnail_exists and not row_needs_regeneration) else 0
        pending_main_image += 1 if is_pending else 0
        backfill_status = "not_requested"
        failure_reason = audit_result.get("failure_reason")
        if backfill and object_key and original_exists and row_needs_regeneration:
            if execute:
                ok, failure_reason = _regenerate_thumbnail(object_key, thumbnail_key)
                if ok:
                    backfill_success += 1
                    thumbnail_exists = True
                    backfill_status = "regenerated"
                else:
                    backfill_failed += 1
                    backfill_status = "failed"
                    failure_reasons[failure_reason or "unknown"] = (
                        failure_reasons.get(failure_reason or "unknown", 0) + 1
                    )
            else:
                backfill_status = "dry_run"
        items.append(
            {
                "product_id": int(row["product_id"]),
                "sku_code": str(row["sku_code"]),
                "main_object_key_present": bool(object_key),
                "pending_main_image": is_pending,
                "original_exists": original_exists,
                "thumbnail_key": thumbnail_key or None,
                "thumbnail_exists": thumbnail_exists,
                "same_size_thumbnail": same_size,
                "same_bytes_thumbnail": same_bytes,
                "needs_thumbnail_regeneration": row_needs_regeneration,
                "backfill_status": backfill_status,
                "failure_reason": failure_reason,
            }
        )

    return {
        "total_public_products": len(items),
        "missing_main_image": missing_main,
        "pending_main_image": pending_main_image,
        "missing_original_object": missing_original,
        "missing_thumbnail_object": missing_thumbnail,
        "same_size_thumbnail_object": same_size_thumbnail,
        "same_bytes_thumbnail_object": same_bytes_thumbnail,
        "needs_thumbnail_regeneration": needs_regeneration,
        "skipped_valid_thumbnail": skipped_valid_thumbnail,
        "backfill": {
            "requested": backfill,
            "execute": execute,
            "dry_run": backfill and not execute,
            "success": backfill_success,
            "failed": backfill_failed,
            "failure_reasons": failure_reasons,
        },
        "items": items,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--limit", type=int, default=None)
    parser.add_argument("--backfill", action="store_true", help="Prepare or execute thumbnail backfill")
    parser.add_argument(
        "--execute",
        action="store_true",
        help="Write missing thumbnails; without this flag backfill is dry-run only",
    )
    args = parser.parse_args()
    print(
        json.dumps(
            audit(args.limit, backfill=args.backfill, execute=args.execute),
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
