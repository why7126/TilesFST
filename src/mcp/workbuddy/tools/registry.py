"""Tool registry shared by stdio and HTTP MCP transports."""

from __future__ import annotations

from typing import Any, Callable
import hashlib
import json
import logging
import time

from pydantic import ValidationError

from src.mcp.workbuddy.adapters.api_client import BackendApiError, TilesFSTApiClient, safe_error_result
from src.mcp.workbuddy.adapters.idempotency import WriteJournal
from src.mcp.workbuddy.config import WorkBuddyConnectorConfig
from src.mcp.workbuddy.schemas.tools import tool_schemas
from src.mcp.workbuddy.schemas.validation import validate_arguments
from src.mcp.workbuddy.tools import catalog, write


ReadHandler = Callable[[TilesFSTApiClient, dict[str, Any]], dict[str, Any]]
WriteHandler = Callable[[TilesFSTApiClient, WorkBuddyConnectorConfig, dict[str, Any]], dict[str, Any]]
logger = logging.getLogger(__name__)


class ToolRegistry:
    def __init__(
        self,
        client: TilesFSTApiClient,
        config: WorkBuddyConnectorConfig,
        principal: str | None = None,
    ) -> None:
        self.client = client
        self.config = config
        self.principal = principal
        self.journal = WriteJournal(config.idempotency_dir)
        self._read_handlers: dict[str, ReadHandler] = {
            "search_tile_skus": catalog.search_tile_skus,
            "get_tile_sku_detail": catalog.get_tile_sku_detail,
            "list_tile_brands": catalog.list_tile_brands,
            "list_tile_categories": catalog.list_tile_categories,
            "summarize_catalog": catalog.summarize_catalog,
            "preview_create_tile_sku": write.preview_create_tile_sku,
            "preview_update_tile_sku": write.preview_update_tile_sku,
            "preview_publish_tile_sku": write.preview_publish_tile_sku,
            "preview_manage_brand": write.preview_manage_brand,
            "preview_manage_category": write.preview_manage_category,
            "preview_media_upload": write.preview_media_upload,
        }
        self._write_handlers: dict[str, WriteHandler] = {
            "create_tile_sku": write.create_tile_sku,
            "update_tile_sku": write.update_tile_sku,
            "set_tile_sku_status": write.set_tile_sku_status,
            "manage_brand": write.manage_brand,
            "manage_category": write.manage_category,
            "upload_tile_media": write.upload_tile_media,
        }

    def list_tools(self) -> list[dict[str, Any]]:
        return tool_schemas(include_remote_write_tools=self.config.enable_write_tools)

    def call_tool(self, name: str, arguments: dict[str, Any] | None = None) -> dict[str, Any]:
        started = time.monotonic()
        if hasattr(self.client, "last_client_request_id"):
            self.client.last_client_request_id = None
        result = self._call_tool(name, arguments)
        request_id = getattr(self.client, "last_client_request_id", None)
        if request_id:
            result["client_request_id"] = request_id
        logger.info(json.dumps({
            "event": "workbuddy_tool_call", "tool": name if name in self._read_handlers or name in self._write_handlers else "unknown",
            "principal_hash": hashlib.sha256(self.principal.encode()).hexdigest() if self.principal else None,
            "ok": result.get("ok") is True, "client_request_id": request_id,
            "operation_ref": result.get("operation_ref"), "elapsed_ms": round((time.monotonic() - started) * 1000),
        }))
        return result

    def _call_tool(self, name: str, arguments: dict[str, Any] | None = None) -> dict[str, Any]:
        args = arguments or {}
        try:
            if name not in {tool["name"] for tool in self.list_tools()}:
                return {"ok": False, "error": "unknown_tool", "message": "Tool is unavailable"}
            args = dict(args)
            if name == "search_tile_skus" and type(args.get("page_size")) is int:
                args["page_size"] = catalog._sku_page_size(args["page_size"])
            args = validate_arguments(name, args)
            if name in self._read_handlers:
                return self._read_handlers[name](self.client, args)
            if name in self._write_handlers and self.config.enable_write_tools:
                gate = write._write_gate(self.config, name, args)
                if gate:
                    return gate
                principal = self.principal
                if principal is None:
                    profile = self.client.get("/api/v1/auth/me").get("data", {})
                    principal = str(profile.get("id") or "")
                    if not principal:
                        return {"ok": False, "error": "identity_required"}
                    self.principal = principal
                return self.journal.execute(
                    f"{self.config.api_base_url}|{principal}", args["idempotency_key"], name, args,
                    lambda: self._write_handlers[name](self.client, self.config, args),
                )
        except BackendApiError as exc:
            return safe_error_result(exc)
        except ValidationError:
            return {"ok": False, "error": "invalid_arguments", "message": "参数不符合工具 schema，请检查必填字段、类型和取值范围。"}
        except Exception:
            return {"ok": False, "error": "tool_failed", "message": "工具执行失败，请通过请求日志核对结果后再操作。"}
        return {"ok": False, "error": "unknown_tool", "message": f"Unknown tool: {name}"}


def build_registry(config: WorkBuddyConnectorConfig) -> ToolRegistry:
    return ToolRegistry(TilesFSTApiClient(config), config)
