"""Read-only catalog tools for WorkBuddy."""

from __future__ import annotations

from typing import Any

from src.mcp.workbuddy.adapters.api_client import TilesFSTApiClient, unwrap_data
from src.mcp.workbuddy.schemas.tools import SKU_PAGE_SIZES


def _sku_page_size(value: Any = None) -> int:
    requested = 20 if value is None else int(value)
    return next((size for size in SKU_PAGE_SIZES if size >= requested), SKU_PAGE_SIZES[-1])


def search_tile_skus(client: TilesFSTApiClient, args: dict[str, Any]) -> dict[str, Any]:
    query = _pick(args, "keyword", "brand_id", "category_id", "status", "material_completeness")
    query["page"] = int(args.get("page") or 1)
    query["page_size"] = _sku_page_size(args.get("page_size"))
    return {"ok": True, "data": unwrap_data(client.get("/api/v1/admin/tile-skus", query))}


def get_tile_sku_detail(client: TilesFSTApiClient, args: dict[str, Any]) -> dict[str, Any]:
    sku_id = int(args["sku_id"])
    return {"ok": True, "data": unwrap_data(client.get(f"/api/v1/admin/tile-skus/{sku_id}"))}


def list_tile_brands(client: TilesFSTApiClient, args: dict[str, Any]) -> dict[str, Any]:
    query = _pick(args, "keyword", "status")
    query["page"] = int(args.get("page") or 1)
    query["page_size"] = min(int(args.get("page_size") or 20), 100)
    return {"ok": True, "data": unwrap_data(client.get("/api/v1/admin/brands", query))}


def list_tile_categories(client: TilesFSTApiClient, args: dict[str, Any]) -> dict[str, Any]:
    if args.get("tree"):
        return {"ok": True, "data": unwrap_data(client.get("/api/v1/admin/tile-categories/tree"))}
    query = _pick(args, "keyword", "status", "level", "parent_id")
    query["page"] = int(args.get("page") or 1)
    query["page_size"] = min(int(args.get("page_size") or 20), 50)
    return {"ok": True, "data": unwrap_data(client.get("/api/v1/admin/tile-categories", query))}


def summarize_catalog(client: TilesFSTApiClient, args: dict[str, Any]) -> dict[str, Any]:
    sample_size = max(1, min(int(args.get("sample_size") or 10), 50))
    query = _pick(args, "keyword", "brand_id", "category_id", "status")
    skus = unwrap_data(client.get("/api/v1/admin/tile-skus", {**query, "page": 1, "page_size": _sku_page_size(sample_size)}))
    brands = unwrap_data(client.get("/api/v1/admin/brands", {"page": 1, "page_size": 100}))
    categories = unwrap_data(client.get("/api/v1/admin/tile-categories", {"page": 1, "page_size": 50}))
    items = skus.get("items", [])[:sample_size] if isinstance(skus, dict) else []
    summary = skus.get("summary", {}) if isinstance(skus, dict) else {}
    return {
        "ok": True,
        "data": {
            "filters": query,
            "sku_summary": summary,
            "sample_count": len(items),
            "representative_skus": [
                {
                    "id": item.get("id"),
                    "name": item.get("name"),
                    "sku_code": item.get("sku_code"),
                    "status": item.get("status"),
                    "brand_name": item.get("brand_name"),
                    "category_name": item.get("category_name"),
                    "material_completeness": item.get("material_completeness"),
                }
                for item in items
                if isinstance(item, dict)
            ],
            "brand_count": _item_total(brands),
            "category_count": _item_total(categories),
            "data_boundaries": [
                "No raw object keys, credentials, cookies, or database DSNs are returned by the connector.",
                "Catalog summary is deterministic and derived only from ProjectTilesFST API responses.",
            ],
        },
    }


def _pick(args: dict[str, Any], *keys: str) -> dict[str, Any]:
    return {key: args.get(key) for key in keys if args.get(key) not in (None, "")}


def _item_total(payload: Any) -> int | None:
    if isinstance(payload, dict):
        pagination = payload.get("pagination")
        if isinstance(pagination, dict) and "total" in pagination:
            return int(pagination["total"])
        if isinstance(payload.get("items"), list):
            return len(payload["items"])
    if isinstance(payload, list):
        return len(payload)
    return None
