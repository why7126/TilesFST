#!/usr/bin/env python3
"""Audit public miniapp brand-chain image object references."""

from __future__ import annotations

import argparse
import copy
import hashlib
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


def _key_hash(object_key: str) -> str | None:
    if not object_key:
        return None
    return hashlib.sha256(object_key.encode("utf-8")).hexdigest()[:12]


def _key_prefix(object_key: str) -> str | None:
    if not object_key:
        return None
    parts = object_key.split("/")
    return "/".join(parts[: min(3, len(parts))])


def _classify_media_item(
    *,
    object_key: str,
    pending: bool,
    original_exists: bool,
    thumbnail_exists: bool,
    needs_regeneration: bool,
) -> str:
    if not object_key:
        return "missing_key"
    if not original_exists:
        return "object_missing"
    if pending:
        return "url_fallback_risk"
    if not thumbnail_exists:
        return "thumbnail_missing"
    if needs_regeneration:
        return "thumbnail_no_benefit"
    return "closed"


def _four_part_status(
    *,
    object_key: str,
    pending: bool,
    original_exists: bool,
    thumbnail_exists: bool,
    needs_regeneration: bool,
) -> dict[str, str]:
    return {
        "key": "fail" if not object_key else ("blocked" if pending else "pass"),
        "object": "pass" if original_exists and thumbnail_exists and not needs_regeneration else "fail",
        "url": "blocked" if pending else ("pass" if original_exists else "fail"),
        "render": "blocked" if pending or not original_exists else "requires_device_evidence",
    }


def deidentify_audit_result(result: dict[str, object]) -> dict[str, object]:
    """Return a safe-to-share audit payload without raw object keys or labels."""
    payload = copy.deepcopy(result)
    safe_items = []
    for item in payload.get("items", []):
        if not isinstance(item, dict):
            continue
        safe_items.append(
            {
                "resource_type": item.get("resource_type"),
                "resource_id": item.get("resource_id"),
                "object_key_hash": item.get("object_key_hash"),
                "object_key_prefix": item.get("object_key_prefix"),
                "thumbnail_key_hash": item.get("thumbnail_key_hash"),
                "thumbnail_key_prefix": item.get("thumbnail_key_prefix"),
                "classification": item.get("classification"),
                "four_part_status": item.get("four_part_status"),
                "failure_reason": item.get("failure_reason"),
                "backfill_status": item.get("backfill_status"),
            }
        )
    payload["items"] = safe_items
    payload["deidentified"] = True
    return payload


def audit(limit: int | None, *, backfill: bool = False, execute: bool = False) -> dict[str, object]:
    session = get_session_factory()()
    try:
        sql = """
            SELECT 1 AS resource_order, 'product_card' AS resource_type, t.id AS resource_id, t.sku_code AS label,
                   ti.object_key AS object_key
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
            UNION ALL
            SELECT 2 AS resource_order, 'brand_logo' AS resource_type, b.id AS resource_id, b.name AS label,
                   b.logo_object_key AS object_key
            FROM brands b
            WHERE b.status = 'ENABLED'
              AND COALESCE(b.logo_object_key, '') <> ''
            UNION ALL
            SELECT 3 AS resource_order, 'brand_banner' AS resource_type, bn.id AS resource_id, bn.title AS label,
                   bn.image_object_key AS object_key
            FROM banners bn
            WHERE bn.status = 'ONLINE'
              AND bn.position = 'MINIAPP_BRAND_LIST_CAROUSEL'
              AND COALESCE(bn.image_object_key, '') <> ''
            UNION ALL
            SELECT 4 AS resource_order, 'brand_certificate' AS resource_type, bci.id AS resource_id, bc.name AS label,
                   bci.file_key AS object_key
            FROM brand_certificate_images bci
            JOIN brand_certificates bc ON bc.id = bci.certificate_id
            JOIN brands b ON b.id = bc.brand_id
            WHERE bc.deleted_at IS NULL
              AND bc.is_visible = 1
              AND b.status = 'ENABLED'
              AND bci.file_mime_type IN ('image/jpeg', 'image/jpg', 'image/png', 'image/webp')
              AND COALESCE(bci.file_key, '') <> ''
            ORDER BY resource_order ASC, resource_id ASC
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
    resources_by_type: dict[str, int] = {}
    backfill_success = 0
    backfill_failed = 0
    failure_reasons: dict[str, int] = {}
    classification_summary: dict[str, int] = {}
    for row in rows:
        resource_type = str(row["resource_type"])
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
        resources_by_type[resource_type] = resources_by_type.get(resource_type, 0) + 1
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
        classification = _classify_media_item(
            object_key=object_key,
            pending=is_pending,
            original_exists=original_exists,
            thumbnail_exists=thumbnail_exists,
            needs_regeneration=row_needs_regeneration,
        )
        classification_summary[classification] = classification_summary.get(classification, 0) + 1
        items.append(
            {
                "resource_type": resource_type,
                "resource_id": int(row["resource_id"]),
                "label": str(row["label"]),
                "product_id": int(row["resource_id"]) if resource_type == "product_card" else None,
                "sku_code": str(row["label"]) if resource_type == "product_card" else None,
                "main_object_key_present": bool(object_key),
                "pending_main_image": is_pending,
                "object_key_hash": _key_hash(object_key),
                "object_key_prefix": _key_prefix(object_key),
                "original_exists": original_exists,
                "thumbnail_key": thumbnail_key or None,
                "thumbnail_key_hash": _key_hash(thumbnail_key),
                "thumbnail_key_prefix": _key_prefix(thumbnail_key),
                "thumbnail_exists": thumbnail_exists,
                "same_size_thumbnail": same_size,
                "same_bytes_thumbnail": same_bytes,
                "needs_thumbnail_regeneration": row_needs_regeneration,
                "classification": classification,
                "four_part_status": _four_part_status(
                    object_key=object_key,
                    pending=is_pending,
                    original_exists=original_exists,
                    thumbnail_exists=thumbnail_exists,
                    needs_regeneration=row_needs_regeneration,
                ),
                "backfill_status": backfill_status,
                "failure_reason": failure_reason,
            }
        )

    return {
        "dry_run": not execute,
        "writes_enabled": execute,
        "security": {
            "deidentified_cli_default": True,
            "raw_items_require_flag": "--raw-items",
            "forbidden_output": [
                "access_key",
                "secret_key",
                "authorization_header",
                "cookie",
                "database_url",
                "local_absolute_path",
                "raw_object_key_in_default_cli",
            ],
        },
        "total_public_products": resources_by_type.get("product_card", 0),
        "total_resources": len(items),
        "resources_by_type": resources_by_type,
        "classification_summary": classification_summary,
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
    parser.add_argument(
        "--raw-items",
        action="store_true",
        help="Print raw labels and object keys; default output is deidentified",
    )
    args = parser.parse_args()
    result = audit(args.limit, backfill=args.backfill, execute=args.execute)
    if not args.raw_items:
        result = deidentify_audit_result(result)
    print(
        json.dumps(
            result,
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
