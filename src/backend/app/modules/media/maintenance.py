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
from app.core.error_codes import STORAGE_UNAVAILABLE
from app.core.exceptions import AppError
from app.db.session import get_session_factory
from app.modules.media.storage import (
    DISPLAY_IMAGE_JPEG_QUALITY,
    DISPLAY_IMAGE_MAX_HEIGHT,
    DISPLAY_IMAGE_MAX_WIDTH,
    DISPLAY_IMAGE_TARGET_MAX_SIZE_KB,
    DISPLAY_IMAGE_WEBP_QUALITY,
    MEDIA_NOT_FOUND,
    generate_image_thumbnail,
    get_media_storage_client,
    same_directory_display_object_key,
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
OBJECT_STORAGE_UNREACHABLE = "object_storage_unreachable"
OBJECT_MISSING = "object_missing"
OBJECT_CHECK_FAILED = "object_check_failed"
OBJECT_STORAGE_RECOMMENDED_ACTION = (
    "检查 endpoint、region、bucket、权限、网络与 env 注入，修复后重新 dry-run"
)
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


@dataclass(frozen=True)
class ObjectStorageBlockedError(Exception):
    category: str
    error_code: str
    operation: str


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


def _classify_storage_error(exc: BaseException) -> str:
    if isinstance(exc, AppError):
        if exc.code == MEDIA_NOT_FOUND:
            return OBJECT_MISSING
        if exc.code == STORAGE_UNAVAILABLE or exc.status_code >= 500:
            return OBJECT_STORAGE_UNREACHABLE
        return OBJECT_CHECK_FAILED
    if isinstance(exc, (TimeoutError, ConnectionError, OSError)):
        return OBJECT_STORAGE_UNREACHABLE
    return OBJECT_CHECK_FAILED


def _raise_if_storage_blocked(exc: BaseException, *, operation: str) -> None:
    category = _classify_storage_error(exc)
    if category == OBJECT_STORAGE_UNREACHABLE:
        error_code = str(getattr(exc, "code", exc.__class__.__name__))
        raise ObjectStorageBlockedError(
            category=OBJECT_STORAGE_UNREACHABLE,
            error_code=error_code,
            operation=operation,
        ) from exc


def _storage_blocked_summary(
    *,
    task: str,
    affected_tasks: list[str],
    checked_items: int,
    error: ObjectStorageBlockedError,
) -> dict[str, Any]:
    return {
        "status": "blocked",
        "failure_category": OBJECT_STORAGE_UNREACHABLE,
        "failure_reason": OBJECT_STORAGE_UNREACHABLE,
        "error_code": error.error_code,
        "operation": error.operation,
        "checked_items": checked_items,
        "affected_tasks": affected_tasks,
        "failed": 0,
        "retry_candidates": 0,
        "can_apply": False,
        "recommended_action": OBJECT_STORAGE_RECOMMENDED_ACTION,
        "task": task,
    }


def _storage_blocked_acceptance_summary(
    *,
    task: str,
    total: int,
    thumbnail_applicable: bool,
    render_applicable: bool,
) -> dict[str, Any]:
    summary = _media_acceptance_summary(
        task=task,
        total=total,
        failed=0,
        thumbnail_applicable=thumbnail_applicable,
        render_applicable=render_applicable,
    )
    summary["object"] = {
        "status": "blocked",
        "samples": total,
        "reason": OBJECT_STORAGE_UNREACHABLE,
    }
    if thumbnail_applicable:
        summary["thumbnail_benefit"] = {
            "status": "blocked",
            "reason": OBJECT_STORAGE_UNREACHABLE,
        }
    return summary


def _apply_storage_blocked_result(
    result: dict[str, Any],
    *,
    task: str,
    affected_tasks: list[str],
    checked_items: int,
    error: ObjectStorageBlockedError,
    thumbnail_applicable: bool,
    render_applicable: bool,
) -> dict[str, Any]:
    result["status"] = "blocked"
    result["summary"] = _storage_blocked_summary(
        task=task,
        affected_tasks=affected_tasks,
        checked_items=checked_items,
        error=error,
    )
    result["acceptance_summary"] = _storage_blocked_acceptance_summary(
        task=task,
        total=checked_items,
        thumbnail_applicable=thumbnail_applicable,
        render_applicable=render_applicable,
    )
    return result


def _is_storage_blocked(result: dict[str, Any]) -> bool:
    summary = result.get("summary")
    return isinstance(summary, dict) and summary.get("failure_category") == OBJECT_STORAGE_UNREACHABLE


def _skipped_after_storage_block(
    *,
    task: str,
    limit: int | None,
    thumbnail_applicable: bool,
    render_applicable: bool,
) -> dict[str, Any]:
    result = _base_summary(task=task, apply=False, limit=limit)
    result["status"] = "blocked"
    result["summary"] = {
        "status": "blocked",
        "failure_category": OBJECT_STORAGE_UNREACHABLE,
        "failure_reason": "skipped_after_object_storage_unreachable",
        "failed": 0,
        "retry_candidates": 0,
        "can_apply": False,
        "recommended_action": OBJECT_STORAGE_RECOMMENDED_ACTION,
        "task": task,
    }
    result["items"] = []
    result["acceptance_summary"] = _storage_blocked_acceptance_summary(
        task=task,
        total=0,
        thumbnail_applicable=thumbnail_applicable,
        render_applicable=render_applicable,
    )
    return result


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
    except AppError as exc:
        if _classify_storage_error(exc) == OBJECT_MISSING:
            return False
        _raise_if_storage_blocked(exc, operation="object_info")
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
        _raise_if_storage_blocked(exc, operation="original_info")
        return False, f"original_missing:{exc.code}"
    try:
        thumbnail_info = get_media_storage_client().get_object_info(thumbnail_key)
    except AppError as exc:
        _raise_if_storage_blocked(exc, operation="variant_info")
        return True, "thumbnail_missing"

    normalized_variant_type = (thumbnail_info.content_type or "").lower().split(";", 1)[0].strip()
    if normalized_variant_type != "image/webp":
        return True, "variant_not_webp"

    target_bytes = max(0, int(thumbnail_max_size_kb or 0)) * 1024
    if target_bytes and thumbnail_info.total_size > target_bytes:
        return True, "thumbnail_exceeds_target_size"

    if original_info.total_size != thumbnail_info.total_size:
        return False, None
    try:
        original = get_media_storage_client().get_object(original_key)
        thumbnail = get_media_storage_client().get_object(thumbnail_key)
    except AppError as exc:
        _raise_if_storage_blocked(exc, operation="variant_read")
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


def _effective_display_max_size_kb() -> int:
    session = get_session_factory()()
    try:
        return EffectiveSettingsService(SystemSettingsRepository(session)).display_max_size_kb()
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


def _regenerate_display(
    original_key: str,
    display_key: str,
    *,
    display_max_size_kb: int = DISPLAY_IMAGE_TARGET_MAX_SIZE_KB,
) -> tuple[bool, str | None, bool]:
    try:
        original = get_media_storage_client().get_object(original_key)
        display = generate_image_thumbnail(
            original.content,
            original.content_type,
            max_width=DISPLAY_IMAGE_MAX_WIDTH,
            max_height=DISPLAY_IMAGE_MAX_HEIGHT,
            jpeg_quality=DISPLAY_IMAGE_JPEG_QUALITY,
            webp_quality=DISPLAY_IMAGE_WEBP_QUALITY,
            target_max_size_kb=display_max_size_kb,
        )
        get_media_storage_client().put_object(display_key, display.content, display.content_type)
    except (AppError, RuntimeError, ValueError, OSError) as exc:
        return False, str(getattr(exc, "code", exc.__class__.__name__)), False
    target_bytes = max(0, display_max_size_kb) * 1024
    return True, None, bool(target_bytes and display.size > target_bytes)


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
        try:
            needs_regeneration, reason = _needs_regeneration(
                object_key,
                thumbnail_key,
                thumbnail_max_size_kb=thumbnail_max_size_kb,
            )
            thumbnail_exists = _object_exists(thumbnail_key)
        except ObjectStorageBlockedError as exc:
            return _apply_storage_blocked_result(
                result,
                task="backfill-brand-certificate-thumbnails",
                affected_tasks=["backfill-brand-certificate-thumbnails"],
                checked_items=len(items),
                error=exc,
                thumbnail_applicable=True,
                render_applicable=False,
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
                "thumbnail_exists": thumbnail_exists,
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


def run_image_variant_backfill(args: argparse.Namespace) -> dict[str, Any]:
    execute = bool(args.apply)
    limit = args.limit
    thumbnail_max_size_kb = _effective_thumbnail_max_size_kb()
    display_max_size_kb = _effective_display_max_size_kb()
    result: dict[str, Any] = _base_summary(
        task="backfill-image-variants",
        apply=execute,
        limit=limit,
    )
    summary: dict[str, Any] = {
        "total": 0,
        "success": 0,
        "failed": 0,
        "skipped": 0,
        "thumbnail_missing": 0,
        "display_missing": 0,
        "thumbnail_no_benefit": 0,
        "display_no_benefit": 0,
        "estimated_writes": 0,
        "not_within_target": 0,
        "retry_candidates": 0,
        "failure_reasons": {},
        "thumbnail_max_size_kb": thumbnail_max_size_kb,
        "display_max_width": DISPLAY_IMAGE_MAX_WIDTH,
        "display_max_height": DISPLAY_IMAGE_MAX_HEIGHT,
        "display_max_size_kb": display_max_size_kb,
    }
    items: list[dict[str, Any]] = []
    seen: set[str] = set()
    for row in _thumbnail_source_rows(limit):
        object_key = str(row["object_key"] or "").strip()
        if not object_key or object_key in seen:
            continue
        seen.add(object_key)
        thumbnail_key = same_directory_thumbnail_object_key(object_key)
        display_key = same_directory_display_object_key(object_key)
        try:
            thumbnail_needs, thumbnail_reason = _needs_regeneration(
                object_key,
                thumbnail_key,
                thumbnail_max_size_kb=thumbnail_max_size_kb,
            )
            display_needs, display_reason = _needs_regeneration(
                object_key,
                display_key,
                thumbnail_max_size_kb=display_max_size_kb,
            )
            thumbnail_exists = _object_exists(thumbnail_key)
            display_exists = _object_exists(display_key)
        except ObjectStorageBlockedError as exc:
            return _apply_storage_blocked_result(
                result,
                task="backfill-image-variants",
                affected_tasks=["backfill-image-variants"],
                checked_items=len(items),
                error=exc,
                thumbnail_applicable=True,
                render_applicable=True,
            )
        required_writes = int(thumbnail_needs) + int(display_needs)
        status = "dry_run" if required_writes and not execute else "skipped"
        summary["estimated_writes"] += required_writes
        summary["retry_candidates"] += 1 if required_writes else 0
        if thumbnail_reason == "thumbnail_missing":
            summary["thumbnail_missing"] += 1
        if display_reason == "thumbnail_missing":
            summary["display_missing"] += 1
        if thumbnail_reason in {"thumbnail_same_size", "thumbnail_copied_original"}:
            summary["thumbnail_no_benefit"] += 1
        if display_reason in {"thumbnail_same_size", "thumbnail_copied_original"}:
            summary["display_no_benefit"] += 1

        variant_results: dict[str, str] = {}
        if execute and required_writes:
            status = "generated"
            for variant, needs, key in (
                ("thumbnail", thumbnail_needs, thumbnail_key),
                ("display", display_needs, display_key),
            ):
                if not needs:
                    variant_results[variant] = "skipped"
                    continue
                if variant == "thumbnail":
                    ok, failure, not_within_target = _regenerate_thumbnail(
                        object_key,
                        key,
                        thumbnail_max_size_kb=thumbnail_max_size_kb,
                    )
                else:
                    ok, failure, not_within_target = _regenerate_display(
                        object_key,
                        key,
                        display_max_size_kb=display_max_size_kb,
                    )
                if ok:
                    summary["success"] += 1
                    summary["not_within_target"] += 1 if not_within_target else 0
                    variant_results[variant] = "generated"
                else:
                    status = "failed"
                    summary["failed"] += 1
                    variant_results[variant] = "failed"
                    reasons = summary["failure_reasons"]
                    reasons[failure or "unknown"] = reasons.get(failure or "unknown", 0) + 1
        elif not required_writes:
            summary["skipped"] += 1
        items.append(
            {
                "source_type": row["source_type"],
                "source_id": row["source_id"],
                "original": _safe_object_ref(object_key),
                "thumbnail": _safe_object_ref(thumbnail_key),
                "display": _safe_object_ref(display_key),
                "thumbnail_exists": thumbnail_exists,
                "display_exists": display_exists,
                "needs": {
                    "thumbnail": thumbnail_needs,
                    "display": display_needs,
                },
                "reasons": {
                    "thumbnail": thumbnail_reason,
                    "display": display_reason,
                },
                "variant_results": variant_results,
                "status": status,
                "display_max_size_kb": display_max_size_kb,
            }
        )
    summary["total"] = len(items)
    result["summary"] = summary
    result["items"] = items
    result["acceptance_summary"] = _media_acceptance_summary(
        task="backfill-image-variants",
        total=summary["total"],
        failed=summary["failed"],
        thumbnail_applicable=True,
        render_applicable=True,
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
    display_max_size_kb = _effective_display_max_size_kb()
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
        "display_max_size_kb": display_max_size_kb,
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
        try:
            original_exists = _object_exists(object_key)
            thumbnail_exists = _object_exists(thumbnail_key)
            destination_exists = _object_exists(target_key)
        except ObjectStorageBlockedError as exc:
            return _apply_storage_blocked_result(
                result,
                task="formalize-pending-tile-images",
                affected_tasks=["formalize-pending-tile-images"],
                checked_items=len(items),
                error=exc,
                thumbnail_applicable=True,
                render_applicable=True,
            )
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
                        display_max_size_kb=display_max_size_kb,
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
        try:
            original_exists = _object_exists(source_key)
            target_exists = _object_exists(target_key)
        except ObjectStorageBlockedError as exc:
            return _apply_storage_blocked_result(
                result,
                task="migrate-certificate-image-keys",
                affected_tasks=["migrate-certificate-image-keys"],
                checked_items=len(items),
                error=exc,
                thumbnail_applicable=False,
                render_applicable=True,
            )
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
    task_name = getattr(args, "task", "media-drift-reconcile")
    result = _base_summary(task=task_name, apply=bool(args.apply), limit=args.limit)
    task_plan: list[tuple[str, Callable[[argparse.Namespace], dict[str, Any]], argparse.Namespace]] = [
        ("sku_pending_formalization", run_pending_tile_formalization, args),
        ("certificate_image_key_migration", run_certificate_image_key_migration, args),
        ("brand_logo_and_certificate_thumbnail_backfill", run_thumbnail_backfill, args),
        ("object_key_audit", run_object_key_audit, argparse.Namespace(apply=False, limit=args.limit)),
    ]
    tasks: dict[str, dict[str, Any]] = {}
    blocked_affected_tasks: list[str] = []
    for index, (name, runner, runner_args) in enumerate(task_plan):
        tasks[name] = runner(runner_args)
        if _is_storage_blocked(tasks[name]):
            blocked_affected_tasks = [task_name for task_name, _, _ in task_plan[index:]]
            for skipped_name, _, _ in task_plan[index + 1 :]:
                tasks[skipped_name] = _skipped_after_storage_block(
                    task=skipped_name,
                    limit=args.limit,
                    thumbnail_applicable=skipped_name
                    == "brand_logo_and_certificate_thumbnail_backfill",
                    render_applicable=skipped_name != "object_key_audit",
                )
            break
    failed = sum(int(task["summary"].get("failed", 0)) for task in tasks.values())
    retry_candidates = sum(
        int(task["summary"].get("retry_candidates", 0))
        for task in tasks.values()
        if isinstance(task.get("summary"), dict)
    )
    result["tasks"] = tasks
    if blocked_affected_tasks:
        first_blocked = next(task for task in tasks.values() if _is_storage_blocked(task))
        first_summary = first_blocked["summary"]
        result["status"] = "blocked"
        result["summary"] = {
            "task_count": len(tasks),
            "status": "blocked",
            "failure_category": OBJECT_STORAGE_UNREACHABLE,
            "failure_reason": OBJECT_STORAGE_UNREACHABLE,
            "failed": failed,
            "retry_candidates": retry_candidates,
            "affected_tasks": blocked_affected_tasks,
            "can_apply": False,
            "recommended_action": OBJECT_STORAGE_RECOMMENDED_ACTION,
            "blocked_at_task": first_summary.get("task"),
            "checked_items": first_summary.get("checked_items", 0),
        }
        result["acceptance_summary"] = _storage_blocked_acceptance_summary(
            task=task_name,
            total=sum(int(task["summary"].get("checked_items", 0)) for task in tasks.values()),
            thumbnail_applicable=True,
            render_applicable=True,
        )
        return result
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
        task=task_name,
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
            try:
                object_exists = _object_exists(object_key)
            except ObjectStorageBlockedError as exc:
                return _apply_storage_blocked_result(
                    result,
                    task="object-key-audit",
                    affected_tasks=["object-key-audit"],
                    checked_items=len(items),
                    error=exc,
                    thumbnail_applicable=False,
                    render_applicable=False,
                )
            items.append(
                {
                    "source_type": row["source_type"],
                    "source_id": row["source_id"],
                    **_safe_object_ref(object_key),
                    "issue": issue,
                    "object_exists": object_exists,
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
    "backfill-image-variants": MaintenanceTask(
        name="backfill-image-variants",
        description="Audit or generate thumbnail and display variants for historical image media.",
        runner=run_image_variant_backfill,
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
        description="Historical alias for media-drift-reconcile.",
        runner=run_bug_0116_media_drift,
        supports_apply=True,
    ),
    "media-drift-reconcile": MaintenanceTask(
        name="media-drift-reconcile",
        description="Audit or reconcile SKU, brand Logo and certificate image drift.",
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
