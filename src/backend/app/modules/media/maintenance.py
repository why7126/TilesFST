"""Production-safe media maintenance task entrypoint.

The module is intentionally importable from the backend package so production
Docker images can run maintenance commands without bind-mounting repository
root scripts into the container.
"""

from __future__ import annotations

import argparse
from collections.abc import Callable
from dataclasses import dataclass
import hashlib
import json
import mimetypes
import sys
from typing import Any

from sqlalchemy import text

from app.core.config import settings
from app.core.exceptions import AppError
from app.db.session import get_session_factory
from app.modules.media.storage import (
    generate_image_thumbnail,
    get_media_storage_client,
    same_directory_thumbnail_object_key,
)
from app.modules.media.tile_images import (
    PENDING_TILE_IMAGE_PREFIX,
    deterministic_formal_tile_image_key,
    formalize_tile_image_object,
)
from app.repositories.system_settings_repository import SystemSettingsRepository
from app.services.effective_settings_service import EffectiveSettingsService

IMAGE_MIME_TYPES = {"image/jpeg", "image/jpg", "image/png", "image/webp"}
CERTIFICATE_FILE_PREFIX = "files/default/brand-certificates/"
CERTIFICATE_IMAGE_PREFIX = "images/default/brand-certificates/"
SENSITIVE_KEYS = (
    "authorization",
    "cookie",
    "password",
    "secret",
    "token",
    "access_key",
    "secret_key",
    "database_url",
    "raw_env",
)


@dataclass(frozen=True)
class MaintenanceTask:
    name: str
    description: str
    runner: Callable[[argparse.Namespace], dict[str, Any]]
    supports_apply: bool = False


def _fingerprint(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()[:12]


def _safe_object_ref(object_key: str | None) -> dict[str, str | None]:
    if not object_key:
        return {"object_key_hash": None, "object_key_prefix": None}
    prefix = object_key.rsplit("/", 1)[0] if "/" in object_key else ""
    return {
        "object_key_hash": _fingerprint(object_key),
        "object_key_prefix": prefix,
    }


def _assert_no_sensitive_output(value: Any, *, path: str = "$") -> None:
    if isinstance(value, dict):
        for key, item in value.items():
            normalized = str(key).lower()
            if any(part in normalized for part in SENSITIVE_KEYS):
                raise ValueError(f"sensitive output key blocked at {path}.{key}")
            _assert_no_sensitive_output(item, path=f"{path}.{key}")
    elif isinstance(value, list):
        for index, item in enumerate(value):
            _assert_no_sensitive_output(item, path=f"{path}[{index}]")
    elif isinstance(value, str):
        if "://" in value and ("@" in value or "password" in value.lower()):
            raise ValueError(f"sensitive output value blocked at {path}")


def _base_summary(*, task: str, apply: bool, limit: int | None) -> dict[str, Any]:
    return {
        "task": task,
        "mode": "apply" if apply else "dry_run",
        "dry_run": not apply,
        "limit": limit,
        "environment": {
            "app_env": settings.app_env,
            "database_backend": _database_backend_summary(),
            "object_storage_provider": settings.effective_object_storage_provider(),
            "object_storage_bucket_hash": _fingerprint(settings.effective_object_storage_bucket()),
            "auto_create_bucket": settings.effective_object_storage_auto_create_bucket(),
        },
    }


def _database_backend_summary() -> str:
    database_url = settings.database_url or ""
    if database_url.startswith("sqlite"):
        return "sqlite"
    if database_url.startswith("mysql"):
        return "mysql"
    return "configured" if database_url else "missing"


def _object_exists(object_key: str) -> bool:
    try:
        get_media_storage_client().get_object_info(object_key)
    except AppError:
        return False
    return True


def _needs_regeneration(
    original_key: str,
    thumbnail_key: str,
    *,
    thumbnail_max_size_kb: int = 0,
) -> tuple[bool, str | None]:
    try:
        original_info = get_media_storage_client().get_object_info(original_key)
    except AppError as exc:
        return False, f"original_missing:{exc.code}"
    try:
        thumbnail_info = get_media_storage_client().get_object_info(thumbnail_key)
    except AppError:
        return True, "thumbnail_missing"

    target_bytes = max(0, int(thumbnail_max_size_kb or 0)) * 1024
    if target_bytes and thumbnail_info.total_size > target_bytes:
        return True, "thumbnail_exceeds_target_size"

    if original_info.total_size != thumbnail_info.total_size:
        return False, None
    try:
        original = get_media_storage_client().get_object(original_key)
        thumbnail = get_media_storage_client().get_object(thumbnail_key)
    except AppError as exc:
        return True, f"read_failed:{exc.code}"
    if original.content == thumbnail.content:
        return True, "thumbnail_copied_original"
    return True, "thumbnail_same_size"


def _effective_thumbnail_max_size_kb() -> int:
    session = get_session_factory()()
    try:
        return EffectiveSettingsService(SystemSettingsRepository(session)).thumbnail_max_size_kb()
    finally:
        session.close()


def _regenerate_thumbnail(
    original_key: str,
    thumbnail_key: str,
    *,
    thumbnail_max_size_kb: int = 0,
) -> tuple[bool, str | None, bool]:
    try:
        original = get_media_storage_client().get_object(original_key)
        thumbnail = generate_image_thumbnail(
            original.content,
            original.content_type,
            target_max_size_kb=thumbnail_max_size_kb,
        )
        get_media_storage_client().put_object(thumbnail_key, thumbnail.content, thumbnail.content_type)
    except (AppError, RuntimeError, ValueError, OSError) as exc:
        return False, str(getattr(exc, "code", exc.__class__.__name__)), False
    target_bytes = max(0, thumbnail_max_size_kb) * 1024
    return True, None, bool(target_bytes and thumbnail.size > target_bytes)


def _image_content_type_for_key(object_key: str, content_type: str | None) -> str | None:
    normalized = (content_type or "").lower().split(";", 1)[0].strip()
    if normalized in IMAGE_MIME_TYPES:
        return "image/jpeg" if normalized == "image/jpg" else normalized
    guessed = mimetypes.guess_type(object_key)[0]
    if guessed in IMAGE_MIME_TYPES:
        return "image/jpeg" if guessed == "image/jpg" else guessed
    return None


def _thumbnail_source_rows(limit: int | None) -> list[dict[str, object]]:
    session = get_session_factory()()
    try:
        sql = """
            SELECT 'sku_image' AS source_type,
                   id AS source_id,
                   object_key AS object_key,
                   NULL AS mime_type
            FROM tile_images
            WHERE object_key IS NOT NULL
              AND object_key != ''
              AND object_key LIKE 'images/%'
            UNION ALL
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


def run_thumbnail_backfill(args: argparse.Namespace) -> dict[str, Any]:
    execute = bool(args.apply)
    limit = args.limit
    thumbnail_max_size_kb = _effective_thumbnail_max_size_kb()
    result: dict[str, Any] = _base_summary(
        task="backfill-brand-certificate-thumbnails",
        apply=execute,
        limit=limit,
    )
    summary: dict[str, Any] = {
        "total": 0,
        "success": 0,
        "failed": 0,
        "skipped": 0,
        "missing_thumbnail": 0,
        "same_size": 0,
        "same_bytes": 0,
        "exceeds_target_size": 0,
        "already_conformant": 0,
        "estimated_writes": 0,
        "not_within_target": 0,
        "retry_candidates": 0,
        "failure_reasons": {},
        "thumbnail_max_size_kb": thumbnail_max_size_kb,
    }
    items: list[dict[str, Any]] = []
    seen: set[str] = set()
    for row in _thumbnail_source_rows(limit):
        object_key = str(row["object_key"] or "").strip()
        if not object_key or object_key in seen:
            continue
        seen.add(object_key)
        thumbnail_key = same_directory_thumbnail_object_key(object_key)
        needs_regeneration, reason = _needs_regeneration(
            object_key,
            thumbnail_key,
            thumbnail_max_size_kb=thumbnail_max_size_kb,
        )
        status = "dry_run" if needs_regeneration and not execute else "skipped"
        if needs_regeneration:
            summary["retry_candidates"] += 1
            summary["estimated_writes"] += 1
            if reason == "thumbnail_missing":
                summary["missing_thumbnail"] += 1
            if reason in {"thumbnail_same_size", "thumbnail_copied_original"}:
                summary["same_size"] += 1
            if reason == "thumbnail_copied_original":
                summary["same_bytes"] += 1
            if reason == "thumbnail_exceeds_target_size":
                summary["exceeds_target_size"] += 1
            if execute:
                ok, failure, not_within_target = _regenerate_thumbnail(
                    object_key,
                    thumbnail_key,
                    thumbnail_max_size_kb=thumbnail_max_size_kb,
                )
                if ok:
                    status = "regenerated"
                    summary["success"] += 1
                    if not_within_target:
                        summary["not_within_target"] += 1
                    reason = None
                else:
                    status = "failed"
                    summary["failed"] += 1
                    reason = failure
                    reasons = summary["failure_reasons"]
                    reasons[reason or "unknown"] = reasons.get(reason or "unknown", 0) + 1
        else:
            summary["skipped"] += 1
            summary["already_conformant"] += 1
        items.append(
            {
                "source_type": row["source_type"],
                "source_id": row["source_id"],
                **_safe_object_ref(object_key),
                "thumbnail": _safe_object_ref(thumbnail_key),
                "thumbnail_exists": _object_exists(thumbnail_key),
                "needs_regeneration": needs_regeneration,
                "status": status,
                "reason": reason,
                "thumbnail_max_size_kb": thumbnail_max_size_kb,
            }
        )
    summary["total"] = len(items)
    result["summary"] = summary
    result["items"] = items
    result["acceptance_summary"] = _media_acceptance_summary(
        task="backfill-brand-certificate-thumbnails",
        total=summary["total"],
        failed=summary["failed"],
        thumbnail_applicable=True,
        render_applicable=False,
    )
    return result


def _pending_tile_rows(limit: int | None) -> list[dict[str, object]]:
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
            {"image_id": image_id, "object_key": target_key, "url": f"/media/{target_key}"},
        )
        session.commit()
    finally:
        session.close()


def run_pending_tile_formalization(args: argparse.Namespace) -> dict[str, Any]:
    execute = bool(args.apply)
    limit = args.limit
    rows = _pending_tile_rows(limit)
    thumbnail_max_size_kb = _effective_thumbnail_max_size_kb()
    result: dict[str, Any] = _base_summary(
        task="formalize-pending-tile-images",
        apply=execute,
        limit=limit,
    )
    summary = {
        "total": len(rows),
        "success": 0,
        "failed": 0,
        "missing_original": 0,
        "missing_thumbnail": 0,
        "target_exists": 0,
        "thumbnail_max_size_kb": thumbnail_max_size_kb,
        "failure_reasons": {},
    }
    items: list[dict[str, Any]] = []
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
        summary["missing_original"] += 0 if original_exists else 1
        summary["missing_thumbnail"] += 0 if thumbnail_exists else 1
        summary["target_exists"] += 1 if destination_exists else 0
        status = "dry_run"
        failure_reason = None
        if execute:
            if not original_exists:
                status = "failed"
                failure_reason = "missing_original"
                summary["failed"] += 1
            else:
                try:
                    formalize_tile_image_object(
                        tile_id=tile_id,
                        object_key=object_key,
                        target_key=target_key,
                        thumbnail_max_size_kb=thumbnail_max_size_kb,
                    )
                    _update_image_reference(image_id=image_id, target_key=target_key)
                    status = "migrated"
                    summary["success"] += 1
                except AppError as exc:
                    status = "failed"
                    failure_reason = str(exc.code)
                    summary["failed"] += 1
            if failure_reason:
                reasons = summary["failure_reasons"]
                reasons[failure_reason] = reasons.get(failure_reason, 0) + 1
        items.append(
            {
                "tile_id": tile_id,
                "image_id": image_id,
                "source": _safe_object_ref(object_key),
                "target": _safe_object_ref(target_key),
                "source_thumbnail": _safe_object_ref(thumbnail_key),
                "target_thumbnail": _safe_object_ref(target_thumbnail_key),
                "original_exists": original_exists,
                "thumbnail_exists": thumbnail_exists,
                "target_exists": destination_exists,
                "thumbnail_max_size_kb": thumbnail_max_size_kb,
                "status": status,
                "failure_reason": failure_reason,
            }
        )
    result["summary"] = summary
    result["items"] = items
    result["acceptance_summary"] = _media_acceptance_summary(
        task="formalize-pending-tile-images",
        total=summary["total"],
        failed=summary["failed"],
        thumbnail_applicable=True,
        render_applicable=True,
    )
    return result


def _certificate_image_rows(limit: int | None) -> list[dict[str, object]]:
    session = get_session_factory()()
    try:
        sql = """
            SELECT 'brand_certificates' AS table_name,
                   id AS source_id,
                   file_key AS object_key,
                   file_mime_type AS mime_type
            FROM brand_certificates
            WHERE deleted_at IS NULL
              AND file_key IS NOT NULL
              AND file_key != ''
              AND file_key LIKE :files_prefix
            UNION ALL
            SELECT 'brand_certificate_images' AS table_name,
                   id AS source_id,
                   file_key AS object_key,
                   file_mime_type AS mime_type
            FROM brand_certificate_images
            WHERE file_key IS NOT NULL
              AND file_key != ''
              AND file_key LIKE :files_prefix
            ORDER BY table_name ASC, source_id ASC
        """
        params: dict[str, object] = {"files_prefix": f"{CERTIFICATE_FILE_PREFIX}%"}
        if limit is not None:
            sql = f"SELECT * FROM ({sql}) scoped LIMIT :limit"
            params["limit"] = limit
        return [dict(row) for row in session.execute(text(sql), params).mappings().all()]
    finally:
        session.close()


def _certificate_target_key(object_key: str) -> str:
    return CERTIFICATE_IMAGE_PREFIX + object_key.removeprefix(CERTIFICATE_FILE_PREFIX)


def _update_certificate_key(*, table_name: str, source_id: int, target_key: str) -> None:
    if table_name not in {"brand_certificates", "brand_certificate_images"}:
        raise ValueError(f"unsupported certificate table: {table_name}")
    session = get_session_factory()()
    try:
        session.execute(
            text(f"UPDATE {table_name} SET file_key = :file_key WHERE id = :source_id"),
            {"file_key": target_key, "source_id": source_id},
        )
        session.commit()
    finally:
        session.close()


def run_certificate_image_key_migration(args: argparse.Namespace) -> dict[str, Any]:
    execute = bool(args.apply)
    limit = args.limit
    rows = _certificate_image_rows(limit)
    result: dict[str, Any] = _base_summary(
        task="migrate-certificate-image-keys",
        apply=execute,
        limit=limit,
    )
    summary: dict[str, Any] = {
        "total": 0,
        "image_candidates": 0,
        "document_skipped": 0,
        "success": 0,
        "failed": 0,
        "missing_original": 0,
        "target_exists": 0,
        "failure_reasons": {},
    }
    items: list[dict[str, Any]] = []
    for row in rows:
        source_key = str(row["object_key"] or "").strip()
        mime_type = _image_content_type_for_key(source_key, str(row["mime_type"] or ""))
        if mime_type is None:
            summary["document_skipped"] += 1
            items.append(
                {
                    "table": row["table_name"],
                    "source_id": row["source_id"],
                    "source": _safe_object_ref(source_key),
                    "target": None,
                    "status": "skipped",
                    "reason": "not_supported_image",
                }
            )
            continue

        target_key = _certificate_target_key(source_key)
        original_exists = _object_exists(source_key)
        target_exists = _object_exists(target_key)
        summary["image_candidates"] += 1
        summary["missing_original"] += 0 if original_exists else 1
        summary["target_exists"] += 1 if target_exists else 0
        status = "dry_run"
        failure_reason = None
        if execute:
            if not original_exists:
                status = "failed"
                failure_reason = "missing_original"
                summary["failed"] += 1
            else:
                try:
                    storage = get_media_storage_client()
                    original = storage.get_object(source_key)
                    storage.put_object(target_key, original.content, mime_type)
                    _update_certificate_key(
                        table_name=str(row["table_name"]),
                        source_id=int(row["source_id"]),
                        target_key=target_key,
                    )
                    status = "migrated"
                    summary["success"] += 1
                except (AppError, ValueError) as exc:
                    status = "failed"
                    failure_reason = str(getattr(exc, "code", exc.__class__.__name__))
                    summary["failed"] += 1
            if failure_reason:
                reasons = summary["failure_reasons"]
                reasons[failure_reason] = reasons.get(failure_reason, 0) + 1

        items.append(
            {
                "table": row["table_name"],
                "source_id": row["source_id"],
                "source": _safe_object_ref(source_key),
                "target": _safe_object_ref(target_key),
                "mime_type": mime_type,
                "original_exists": original_exists,
                "target_exists": target_exists,
                "status": status,
                "failure_reason": failure_reason,
            }
        )
    summary["total"] = len(items)
    result["summary"] = summary
    result["items"] = items
    result["acceptance_summary"] = _media_acceptance_summary(
        task="migrate-certificate-image-keys",
        total=summary["image_candidates"],
        failed=summary["failed"],
        thumbnail_applicable=False,
        render_applicable=True,
    )
    return result


def run_bug_0116_media_drift(args: argparse.Namespace) -> dict[str, Any]:
    result = _base_summary(task="bug-0116-media-drift", apply=bool(args.apply), limit=args.limit)
    tasks = {
        "sku_pending_formalization": run_pending_tile_formalization(args),
        "certificate_image_key_migration": run_certificate_image_key_migration(args),
        "brand_logo_and_certificate_thumbnail_backfill": run_thumbnail_backfill(args),
        "object_key_audit": run_object_key_audit(argparse.Namespace(apply=False, limit=args.limit)),
    }
    failed = sum(int(task["summary"].get("failed", 0)) for task in tasks.values())
    retry_candidates = sum(
        int(task["summary"].get("retry_candidates", 0))
        for task in tasks.values()
        if isinstance(task.get("summary"), dict)
    )
    result["tasks"] = tasks
    result["summary"] = {
        "task_count": len(tasks),
        "failed": failed,
        "retry_candidates": retry_candidates,
        "pending_main_images": tasks["sku_pending_formalization"]["summary"].get("total", 0),
        "certificate_file_image_candidates": tasks["certificate_image_key_migration"][
            "summary"
        ].get("image_candidates", 0),
        "thumbnail_candidates": tasks["brand_logo_and_certificate_thumbnail_backfill"][
            "summary"
        ].get("retry_candidates", 0),
        "non_standard_keys_after_audit": tasks["object_key_audit"]["summary"].get(
            "non_standard", 0
        ),
    }
    result["acceptance_summary"] = _media_acceptance_summary(
        task="bug-0116-media-drift",
        total=sum(int(task["summary"].get("total", 0)) for task in tasks.values()),
        failed=failed,
        thumbnail_applicable=True,
        render_applicable=True,
    )
    return result


def run_object_key_audit(args: argparse.Namespace) -> dict[str, Any]:
    if args.apply:
        raise ValueError("object-key-audit is read-only; use a dedicated migration task for apply")
    limit = args.limit
    result = _base_summary(task="object-key-audit", apply=False, limit=limit)
    session = get_session_factory()()
    try:
        rows = session.execute(
            text(
                """
                SELECT 'brand_logo' AS source_type, id AS source_id, logo_object_key AS object_key
                FROM brands
                WHERE logo_object_key IS NOT NULL AND logo_object_key != ''
                UNION ALL
                SELECT 'certificate_file' AS source_type, id AS source_id, file_key AS object_key
                FROM brand_certificates
                WHERE file_key IS NOT NULL AND file_key != ''
                UNION ALL
                SELECT 'certificate_image' AS source_type, id AS source_id, file_key AS object_key
                FROM brand_certificate_images
                WHERE file_key IS NOT NULL AND file_key != ''
                ORDER BY source_type ASC, source_id ASC
                """
            )
        ).mappings()
        items: list[dict[str, Any]] = []
        for index, row in enumerate(rows):
            if limit is not None and index >= limit:
                break
            object_key = str(row["object_key"] or "")
            issue = _object_key_issue(source_type=str(row["source_type"]), object_key=object_key)
            items.append(
                {
                    "source_type": row["source_type"],
                    "source_id": row["source_id"],
                    **_safe_object_ref(object_key),
                    "issue": issue,
                    "object_exists": _object_exists(object_key),
                }
            )
    finally:
        session.close()
    result["summary"] = {
        "total": len(items),
        "non_standard": sum(1 for item in items if item["issue"] is not None),
        "missing_objects": sum(1 for item in items if not item["object_exists"]),
    }
    result["items"] = items
    result["acceptance_summary"] = _media_acceptance_summary(
        task="object-key-audit",
        total=len(items),
        failed=0,
        thumbnail_applicable=False,
        render_applicable=False,
    )
    return result


def _object_key_issue(*, source_type: str, object_key: str) -> str | None:
    if not object_key:
        return "empty"
    if source_type in {"brand_logo", "certificate_image"} and not object_key.startswith("images/"):
        return "image_not_in_images_prefix"
    if source_type == "certificate_file":
        suffix = object_key.rsplit(".", 1)[-1].lower() if "." in object_key else ""
        if suffix in {"jpg", "jpeg", "png", "webp"} and not object_key.startswith("images/"):
            return "certificate_image_file_not_in_images_prefix"
    if object_key.startswith("original/"):
        return "legacy_original_prefix"
    return None


def _media_acceptance_summary(
    *,
    task: str,
    total: int,
    failed: int,
    thumbnail_applicable: bool,
    render_applicable: bool,
) -> dict[str, Any]:
    status = "fail" if failed else "pass"
    return {
        "task": task,
        "key": {"status": status, "samples": total},
        "object": {"status": status, "samples": total},
        "URL": {"status": "n/a", "reason": "maintenance audit does not call HTTP media URLs"},
        "thumbnail_benefit": {
            "status": status if thumbnail_applicable else "n/a",
            "reason": None if thumbnail_applicable else "task does not create or audit thumbnails",
        },
        "render": {
            "status": "blocked" if render_applicable else "n/a",
            "reason": (
                "requires Web or miniapp evidence after apply"
                if render_applicable
                else "task is storage/database audit only"
            ),
        },
    }


TASKS: dict[str, MaintenanceTask] = {
    "backfill-brand-certificate-thumbnails": MaintenanceTask(
        name="backfill-brand-certificate-thumbnails",
        description="Audit or regenerate SKU, brand logo and brand certificate image thumbnails.",
        runner=run_thumbnail_backfill,
        supports_apply=True,
    ),
    "formalize-pending-tile-images": MaintenanceTask(
        name="formalize-pending-tile-images",
        description="Move public SKU main images out of pending object key paths.",
        runner=run_pending_tile_formalization,
        supports_apply=True,
    ),
    "migrate-certificate-image-keys": MaintenanceTask(
        name="migrate-certificate-image-keys",
        description="Move historical certificate image objects from files/ to images/ keys.",
        runner=run_certificate_image_key_migration,
        supports_apply=True,
    ),
    "bug-0116-media-drift": MaintenanceTask(
        name="bug-0116-media-drift",
        description="Audit or repair SKU, brand Logo and certificate image drift for BUG-0116.",
        runner=run_bug_0116_media_drift,
        supports_apply=True,
    ),
    "object-key-audit": MaintenanceTask(
        name="object-key-audit",
        description="Read-only audit for non-standard media object key prefixes.",
        runner=run_object_key_audit,
        supports_apply=False,
    ),
}


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Production-safe media maintenance tasks.")
    parser.add_argument("task", choices=sorted(TASKS))
    parser.add_argument("--limit", type=int, default=None)
    parser.add_argument("--apply", action="store_true", help="Write database or object storage changes")
    parser.add_argument(
        "--confirm-backup",
        action="store_true",
        help="Confirm MySQL and object storage bucket/prefix snapshots exist before apply",
    )
    return parser


def run(args: argparse.Namespace) -> dict[str, Any]:
    task = TASKS[args.task]
    if args.apply and not task.supports_apply:
        raise ValueError(f"{args.task} does not support apply")
    if args.apply and not args.confirm_backup:
        raise ValueError("--apply requires --confirm-backup")
    result = task.runner(args)
    _assert_no_sensitive_output(result)
    return result


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        result = run(args)
    except ValueError as exc:
        print(json.dumps({"status": "blocked", "reason": str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 2
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
