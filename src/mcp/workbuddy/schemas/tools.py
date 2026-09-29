"""Tool schemas exposed to WorkBuddy through MCP."""

from __future__ import annotations

from typing import Any


JsonSchema = dict[str, Any]
SKU_PAGE_SIZES = (10, 20, 50, 100)


def _object_schema(properties: dict[str, JsonSchema], required: list[str] | None = None) -> JsonSchema:
    return {
        "type": "object",
        "additionalProperties": False,
        "properties": properties,
        "required": required or [],
    }


READ_TOOLS: list[dict[str, Any]] = [
    {
        "name": "search_tile_skus",
        "description": "Search admin-visible tile SKUs with keyword and catalog filters.",
        "inputSchema": _object_schema(
            {
                "keyword": {"type": "string", "maxLength": 80},
                "brand_id": {"type": "integer", "minimum": 1},
                "category_id": {"type": "integer", "minimum": 1},
                "status": {"type": "string", "enum": ["PUBLISHED", "DRAFT", "NEEDS_COMPLETION", "DISABLED"]},
                "material_completeness": {
                    "type": "string",
                    "enum": ["complete", "missing_main_image", "missing_images", "missing_videos"],
                },
                "page": {"type": "integer", "minimum": 1, "default": 1},
                "page_size": {"type": "integer", "enum": list(SKU_PAGE_SIZES), "default": 20},
            },
        ),
    },
    {
        "name": "get_tile_sku_detail",
        "description": "Fetch one admin-visible SKU detail by numeric SKU id.",
        "inputSchema": _object_schema({"sku_id": {"type": "integer", "minimum": 1}}, ["sku_id"]),
    },
    {
        "name": "list_tile_brands",
        "description": "List tile brands for WorkBuddy query and maintenance workflows.",
        "inputSchema": _object_schema(
            {
                "keyword": {"type": "string", "maxLength": 80},
                "status": {"type": "string", "enum": ["ENABLED", "DISABLED"]},
                "page": {"type": "integer", "minimum": 1, "default": 1},
                "page_size": {"type": "integer", "minimum": 1, "maximum": 100, "default": 20},
            },
        ),
    },
    {
        "name": "list_tile_categories",
        "description": "List tile categories or return the category tree.",
        "inputSchema": _object_schema(
            {
                "tree": {"type": "boolean", "default": False},
                "keyword": {"type": "string", "maxLength": 80},
                "status": {"type": "string", "enum": ["ENABLED", "DISABLED"]},
                "level": {"type": "integer", "minimum": 1},
                "parent_id": {"type": "integer", "minimum": 1},
                "page": {"type": "integer", "minimum": 1, "default": 1},
                "page_size": {"type": "integer", "minimum": 1, "maximum": 50, "default": 20},
            },
        ),
    },
    {
        "name": "summarize_catalog",
        "description": "Return a deterministic catalog summary over SKU, brand, and category data.",
        "inputSchema": _object_schema(
            {
                "keyword": {"type": "string", "maxLength": 80},
                "brand_id": {"type": "integer", "minimum": 1},
                "category_id": {"type": "integer", "minimum": 1},
                "status": {"type": "string", "enum": ["PUBLISHED", "DRAFT", "NEEDS_COMPLETION", "DISABLED"]},
                "sample_size": {"type": "integer", "minimum": 1, "maximum": 50, "default": 10},
            },
        ),
    },
]


DRY_RUN_WRITE_TOOLS: list[dict[str, Any]] = [
    {
        "name": "preview_create_tile_sku",
        "description": "Preview SKU creation payload, required fields, scopes, and risks without writing.",
        "inputSchema": _object_schema({"payload": {"type": "object"}}, ["payload"]),
    },
    {
        "name": "preview_update_tile_sku",
        "description": "Preview SKU update diff without writing.",
        "inputSchema": _object_schema(
            {
                "sku_id": {"type": "integer", "minimum": 1},
                "payload": {"type": "object"},
                "current": {"type": "object"},
            },
            ["sku_id", "payload"],
        ),
    },
    {
        "name": "preview_publish_tile_sku",
        "description": "Preview SKU publish or unpublish action without writing.",
        "inputSchema": _object_schema(
            {
                "sku_id": {"type": "integer", "minimum": 1},
                "target_status": {"type": "string", "enum": ["PUBLISHED", "DISABLED", "DRAFT"],
                                  "description": "Use DISABLED to unpublish. DRAFT is a legacy alias for DISABLED, not a draft conversion."},
            },
            ["sku_id", "target_status"],
        ),
    },
    {
        "name": "preview_manage_brand",
        "description": "Preview brand create, update, enable, or disable without writing.",
        "inputSchema": _object_schema(
            {
                "operation": {"type": "string", "enum": ["create", "update", "enable", "disable"]},
                "brand_id": {"type": "integer", "minimum": 1},
                "payload": {"type": "object"},
            },
            ["operation"],
        ),
    },
    {
        "name": "preview_manage_category",
        "description": "Preview category create, update, enable, or disable without writing.",
        "inputSchema": _object_schema(
            {
                "operation": {"type": "string", "enum": ["create", "update", "enable", "disable"]},
                "category_id": {"type": "integer", "minimum": 1},
                "payload": {"type": "object"},
            },
            ["operation"],
        ),
    },
    {
        "name": "preview_media_upload",
        "description": "Preview media upload classification and limits without uploading bytes.",
        "inputSchema": _object_schema(
            {
                "target": {
                    "type": "string",
                    "enum": ["tile_image", "tile_video", "brand_logo", "brand_certificate"],
                },
                "file_name": {"type": "string", "maxLength": 255},
                "content_type": {"type": "string", "maxLength": 120},
                "file_size_bytes": {"type": "integer", "minimum": 0},
                "tile_id": {"type": "integer", "minimum": 1},
            },
            ["target", "file_name", "content_type", "file_size_bytes"],
        ),
    },
]


REMOTE_WRITE_TOOLS: list[dict[str, Any]] = [
    {
        "name": "create_tile_sku",
        "description": "Create one SKU through the existing admin API after explicit confirmation.",
        "inputSchema": _object_schema(
            {
                "payload": {"type": "object"},
                "confirmed": {"type": "boolean"},
                "idempotency_key": {"type": "string", "minLength": 8, "maxLength": 128},
            },
            ["payload", "confirmed", "idempotency_key"],
        ),
    },
    {
        "name": "update_tile_sku",
        "description": "Update one SKU through the existing admin API after explicit confirmation.",
        "inputSchema": _object_schema(
            {
                "sku_id": {"type": "integer", "minimum": 1},
                "payload": {"type": "object"},
                "confirmed": {"type": "boolean"},
                "idempotency_key": {"type": "string", "minLength": 8, "maxLength": 128},
            },
            ["sku_id", "payload", "confirmed", "idempotency_key"],
        ),
    },
    {
        "name": "set_tile_sku_status",
        "description": "Publish or unpublish one SKU through the existing admin API after confirmation.",
        "inputSchema": _object_schema(
            {
                "sku_id": {"type": "integer", "minimum": 1},
                "target_status": {"type": "string", "enum": ["PUBLISHED", "DISABLED", "DRAFT"],
                                  "description": "Use DISABLED to unpublish. DRAFT is a legacy alias for DISABLED, not a draft conversion."},
                "confirmed": {"type": "boolean"},
                "idempotency_key": {"type": "string", "minLength": 8, "maxLength": 128},
            },
            ["sku_id", "target_status", "confirmed", "idempotency_key"],
        ),
    },
    {
        "name": "manage_brand",
        "description": "Create, update, enable, or disable a brand after explicit confirmation.",
        "inputSchema": _object_schema(
            {
                "operation": {"type": "string", "enum": ["create", "update", "enable", "disable"]},
                "brand_id": {"type": "integer", "minimum": 1},
                "payload": {"type": "object"},
                "confirmed": {"type": "boolean"},
                "idempotency_key": {"type": "string", "minLength": 8, "maxLength": 128},
            },
            ["operation", "confirmed", "idempotency_key"],
        ),
    },
    {
        "name": "manage_category",
        "description": "Create, update, enable, or disable a category after explicit confirmation.",
        "inputSchema": _object_schema(
            {
                "operation": {"type": "string", "enum": ["create", "update", "enable", "disable"]},
                "category_id": {"type": "integer", "minimum": 1},
                "payload": {"type": "object"},
                "confirmed": {"type": "boolean"},
                "idempotency_key": {"type": "string", "minLength": 8, "maxLength": 128},
            },
            ["operation", "confirmed", "idempotency_key"],
        ),
    },
    {
        "name": "upload_tile_media",
        "description": "Upload base64 media through the existing admin upload API after confirmation.",
        "inputSchema": _object_schema(
            {
                "target": {
                    "type": "string",
                    "enum": ["tile_image", "tile_video", "brand_logo", "brand_certificate"],
                },
                "file_name": {"type": "string", "maxLength": 255},
                "content_type": {"type": "string", "maxLength": 120},
                "base64_content": {"type": "string"},
                "tile_id": {"type": "integer", "minimum": 1},
                "confirmed": {"type": "boolean"},
                "idempotency_key": {"type": "string", "minLength": 8, "maxLength": 128},
            },
            ["target", "file_name", "content_type", "base64_content", "confirmed", "idempotency_key"],
        ),
    },
]


def tool_schemas(include_remote_write_tools: bool = False) -> list[dict[str, Any]]:
    tools = [*READ_TOOLS, *DRY_RUN_WRITE_TOOLS]
    if include_remote_write_tools:
        tools.extend(REMOTE_WRITE_TOOLS)
    return tools
