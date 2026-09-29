"""Controlled write and dry-run tools for WorkBuddy."""

from __future__ import annotations

import base64
import binascii
from pathlib import PurePosixPath
from typing import Any

from pydantic import ValidationError

from src.mcp.workbuddy.adapters.api_client import TilesFSTApiClient, unwrap_data
from src.mcp.workbuddy.adapters.audit import redact_payload
from src.mcp.workbuddy.config import WorkBuddyConnectorConfig
from src.mcp.workbuddy.schemas.payloads import payload_model

WRITE_SCOPE_BY_TOOL = {
    "create_tile_sku": "tile_sku:write",
    "update_tile_sku": "tile_sku:write",
    "set_tile_sku_status": "tile_sku:publish",
    "manage_brand": "brand:write",
    "manage_category": "category:write",
    "upload_tile_media": "media:upload",
}

MEDIA_EXTENSIONS = {
    "image/jpeg": {".jpg", ".jpeg"}, "image/jpg": {".jpg", ".jpeg"},
    "image/png": {".png"}, "image/webp": {".webp"}, "image/gif": {".gif"},
    "image/svg+xml": {".svg"}, "image/bmp": {".bmp"}, "image/tiff": {".tif", ".tiff"},
    "image/heic": {".heic"}, "video/mp4": {".mp4"}, "video/quicktime": {".mov"},
    "video/x-msvideo": {".avi"}, "video/webm": {".webm"}, "video/x-matroska": {".mkv"},
    "video/mpeg": {".mpeg", ".mpg"}, "video/3gpp": {".3gp"}, "application/pdf": {".pdf"},
}


def _valid_media_filename(filename: str, mime: str) -> bool:
    return bool(filename) and not any(
        char in filename for char in ('/', '\\', '\r', '\n', '"', '\0')
    ) and PurePosixPath(filename).suffix.lower() in MEDIA_EXTENSIONS.get(mime, set())


def preview_create_tile_sku(_: TilesFSTApiClient, args: dict[str, Any]) -> dict[str, Any]:
    payload = args.get("payload") or {}
    return _preview("create_tile_sku", payload=payload, missing_fields=_missing_sku_create(payload))


def preview_update_tile_sku(_: TilesFSTApiClient, args: dict[str, Any]) -> dict[str, Any]:
    payload = args.get("payload") or {}
    current = args.get("current") or {}
    return _preview(
        "update_tile_sku",
        payload=payload,
        target={"sku_id": args.get("sku_id")},
        diff=_diff(current, payload) if isinstance(current, dict) else {},
        missing_fields=_missing_sku_create(payload),
    )


def preview_publish_tile_sku(_: TilesFSTApiClient, args: dict[str, Any]) -> dict[str, Any]:
    return _preview(
        "set_tile_sku_status",
        target={"sku_id": args.get("sku_id"), "target_status": (
            "DISABLED" if args.get("target_status") == "DRAFT" else args.get("target_status")
        )},
        warnings=["Publishing may expose SKU data to public catalog views."],
    )


def preview_manage_brand(_: TilesFSTApiClient, args: dict[str, Any]) -> dict[str, Any]:
    return _preview(
        "manage_brand",
        payload=args.get("payload") or {},
        target={"operation": args.get("operation"), "brand_id": args.get("brand_id")},
        missing_fields=_maintenance_missing("manage_brand", args),
    )


def preview_manage_category(_: TilesFSTApiClient, args: dict[str, Any]) -> dict[str, Any]:
    return _preview(
        "manage_category",
        payload=args.get("payload") or {},
        target={"operation": args.get("operation"), "category_id": args.get("category_id")},
        missing_fields=_maintenance_missing("manage_category", args),
    )


def preview_media_upload(_: TilesFSTApiClient, args: dict[str, Any]) -> dict[str, Any]:
    target = str(args.get("target") or "")
    content_type = str(args.get("content_type") or "")
    size = int(args.get("file_size_bytes") or 0)
    max_bytes = 500 * 1024 * 1024 if target == "tile_video" else 25 * 1024 * 1024
    warnings: list[str] = []
    if not _valid_media_filename(str(args.get("file_name") or ""), content_type):
        warnings.append("文件名必须是无路径的文件名，扩展名须与 MIME 一致。")
    if size <= 0:
        warnings.append("文件内容不能为空。")
    if size > max_bytes:
        warnings.append("File size exceeds the connector preview limit.")
    if target in {"tile_image", "brand_logo"} and not content_type.startswith("image/"):
        warnings.append("Expected an image MIME type for this target.")
    if target == "tile_video" and not content_type.startswith("video/"):
        warnings.append("Expected a video MIME type for this target.")
    return _preview(
        "upload_tile_media",
        target={
            "target": target,
            "content_type": content_type,
            "file_size_bytes": size,
            "tile_id": args.get("tile_id"),
        },
        warnings=warnings,
    )


def create_tile_sku(
    client: TilesFSTApiClient, config: WorkBuddyConnectorConfig, args: dict[str, Any]
) -> dict[str, Any]:
    gate = _write_gate(config, "create_tile_sku", args)
    if gate:
        return gate
    data = unwrap_data(
        client.post(
            "/api/v1/admin/tile-skus",
            json_body=args["payload"],
            idempotency_key=args["idempotency_key"],
            task_type="sku_create",
        )
    )
    return {"ok": True, "data": data}


def update_tile_sku(
    client: TilesFSTApiClient, config: WorkBuddyConnectorConfig, args: dict[str, Any]
) -> dict[str, Any]:
    gate = _write_gate(config, "update_tile_sku", args)
    if gate:
        return gate
    sku_id = int(args["sku_id"])
    data = unwrap_data(
        client.put(
            f"/api/v1/admin/tile-skus/{sku_id}",
            json_body=args["payload"],
            idempotency_key=args["idempotency_key"],
            task_type="sku_update",
        )
    )
    return {"ok": True, "data": data}


def set_tile_sku_status(
    client: TilesFSTApiClient, config: WorkBuddyConnectorConfig, args: dict[str, Any]
) -> dict[str, Any]:
    gate = _write_gate(config, "set_tile_sku_status", args)
    if gate:
        return gate
    sku_id = int(args["sku_id"])
    action = "publish" if args["target_status"] == "PUBLISHED" else "unpublish"
    data = unwrap_data(
        client.post(
            f"/api/v1/admin/tile-skus/{sku_id}/{action}",
            idempotency_key=args["idempotency_key"],
            task_type=f"sku_{action}",
        )
    )
    return {"ok": True, "data": data}


def manage_brand(
    client: TilesFSTApiClient, config: WorkBuddyConnectorConfig, args: dict[str, Any]
) -> dict[str, Any]:
    gate = _write_gate(config, "manage_brand", args)
    if gate:
        return gate
    operation = args["operation"]
    path = "/api/v1/admin/brands"
    method = client.post
    if operation in {"update", "enable", "disable"}:
        brand_id = int(args["brand_id"])
        path = f"{path}/{brand_id}" if operation == "update" else f"{path}/{brand_id}/{operation}"
        method = client.put if operation == "update" else client.post
    data = unwrap_data(
        method(
            path,
            json_body=args.get("payload") if operation in {"create", "update"} else None,
            idempotency_key=args["idempotency_key"],
        )
    )
    return {"ok": True, "data": data}


def manage_category(
    client: TilesFSTApiClient, config: WorkBuddyConnectorConfig, args: dict[str, Any]
) -> dict[str, Any]:
    gate = _write_gate(config, "manage_category", args)
    if gate:
        return gate
    operation = args["operation"]
    path = "/api/v1/admin/tile-categories"
    method = client.post
    if operation in {"update", "enable", "disable"}:
        category_id = int(args["category_id"])
        path = f"{path}/{category_id}" if operation == "update" else f"{path}/{category_id}/{operation}"
        method = client.put if operation == "update" else client.post
    data = unwrap_data(
        method(
            path,
            json_body=args.get("payload") if operation in {"create", "update"} else None,
            idempotency_key=args["idempotency_key"],
        )
    )
    return {"ok": True, "data": data}


def upload_tile_media(
    client: TilesFSTApiClient, config: WorkBuddyConnectorConfig, args: dict[str, Any]
) -> dict[str, Any]:
    gate = _write_gate(config, "upload_tile_media", args)
    if gate:
        return gate
    target = args["target"]
    route_by_target = {
        "tile_image": "/api/v1/admin/uploads/tile-images",
        "tile_video": "/api/v1/admin/uploads/tile-videos",
        "brand_logo": "/api/v1/admin/uploads/brand-logos",
        "brand_certificate": "/api/v1/admin/uploads/brand-certificates",
    }
    raw = base64.b64decode(args["base64_content"], validate=True)
    data = unwrap_data(
        client.upload_file(
            route_by_target[target],
            file_bytes=raw,
            file_name=args["file_name"],
            content_type=args["content_type"],
            query={"tile_id": args.get("tile_id")},
            idempotency_key=args["idempotency_key"],
            task_type=f"{target}_upload",
        )
    )
    return {"ok": True, "data": redact_payload(data)}


def _preview(
    real_tool: str,
    *,
    payload: dict[str, Any] | None = None,
    target: dict[str, Any] | None = None,
    missing_fields: list[str] | None = None,
    diff: dict[str, Any] | None = None,
    warnings: list[str] | None = None,
) -> dict[str, Any]:
    return {
        "ok": True,
        "dry_run": True,
        "side_effects": False,
        "real_tool": real_tool,
        "required_scope": WRITE_SCOPE_BY_TOOL[real_tool],
        "requires_confirmation": True,
        "target": target or {},
        "payload_summary": {"fields": sorted((payload or {}).keys())},
        "missing_fields": missing_fields or [],
        "diff": diff or {},
        "warnings": warnings or [],
        "next_step": "核对目标、字段和风险，补齐缺失字段后明确确认；预览未执行写入。",
    }


def _write_gate(
    config: WorkBuddyConnectorConfig, tool_name: str, args: dict[str, Any]
) -> dict[str, Any] | None:
    scope = WRITE_SCOPE_BY_TOOL[tool_name]
    if not config.enable_write_tools:
        return {
            "ok": False,
            "error": "write_tools_disabled",
            "message": "Controlled write tools are disabled for this connector runtime.",
            "required_scope": scope,
        }
    if scope not in config.write_scopes:
        return {
            "ok": False,
            "error": "missing_scope",
            "message": "Connector token is not allowed to perform this write operation.",
            "required_scope": scope,
        }
    if args.get("confirmed") is not True:
        return {
            "ok": False,
            "error": "confirmation_required",
            "message": "Explicit confirmation is required before a write operation.",
            "required_scope": scope,
        }
    if not isinstance(args.get("idempotency_key"), str) or not 8 <= len(args["idempotency_key"]) <= 128:
        return {
            "ok": False,
            "error": "idempotency_key_required",
            "message": "Write operations require an idempotency key.",
            "required_scope": scope,
        }
    if tool_name == "upload_tile_media":
        filename = args.get("file_name", "")
        mime = args.get("content_type", "")
        try:
            valid_content = bool(base64.b64decode(args.get("base64_content", ""), validate=True))
        except (binascii.Error, ValueError):
            valid_content = False
        if not (_valid_media_filename(filename, mime) and valid_content):
            return {"ok": False, "error": "invalid_media", "message": "文件名、扩展名与 MIME 必须一致，内容必须为非空有效 Base64。"}
    model = payload_model(tool_name)
    operation = args.get("operation", "create")
    if tool_name in {"manage_brand", "manage_category"} and operation != "create":
        field = "brand_id" if tool_name == "manage_brand" else "category_id"
        if not args.get(field):
            return {"ok": False, "error": "target_required", "message": "必须指定业务对象 ID。"}
    if model and operation in {"create", "update"}:
        try:
            model.model_validate(args.get("payload", {}))
        except ValidationError:
            return {"ok": False, "error": "invalid_payload", "message": "业务字段缺失或类型不正确。"}
    return None


def _missing_sku_create(payload: dict[str, Any]) -> list[str]:
    try:
        payload_model("create_tile_sku").model_validate(payload)
        return []
    except ValidationError as exc:
        return [str(error["loc"][0]) for error in exc.errors() if error["loc"]]


def _diff(current: dict[str, Any], proposed: dict[str, Any]) -> dict[str, Any]:
    diff: dict[str, Any] = {}
    for key, value in proposed.items():
        if current.get(key) != value:
            diff[key] = {"changed": True}
    return diff


def _maintenance_missing(tool: str, args: dict[str, Any]) -> list[str]:
    missing = []
    if args.get("operation") != "create":
        field = "brand_id" if tool == "manage_brand" else "category_id"
        if not args.get(field):
            missing.append(field)
    if args.get("operation") in {"create", "update"}:
        model = payload_model(tool)
        try:
            model.model_validate(args.get("payload", {}))
        except ValidationError as exc:
            missing.extend(str(error["loc"][0]) for error in exc.errors() if error["loc"])
    return missing
