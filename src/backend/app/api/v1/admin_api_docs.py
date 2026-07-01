"""Admin API documentation inventory routes."""

from __future__ import annotations

import re
from typing import Any

from fastapi import APIRouter, Depends, Request
from fastapi.routing import APIRoute

from app.core.config import settings
from app.core.deps import require_system_admin
from app.schemas.admin_api_docs import (
    ApiDocsData,
    ApiDocsEnvironmentPolicy,
    ApiDocsRouteItem,
    ApiDocsSummary,
)
from app.schemas.common import ApiResponse

router = APIRouter(dependencies=[Depends(require_system_admin)])

HTTP_METHOD_ORDER = {
    "GET": 0,
    "POST": 1,
    "PUT": 2,
    "PATCH": 3,
    "DELETE": 4,
}


def _method_sort_key(method: str) -> tuple[int, str]:
    return (HTTP_METHOD_ORDER.get(method, 99), method)


def _operation_to_orval_method(operation_id: str | None) -> str | None:
    if not operation_id:
        return None
    parts = [part for part in re.split(r"[_\W]+", operation_id) if part]
    if not parts:
        return None
    return parts[0] + "".join(part[:1].upper() + part[1:] for part in parts[1:])


def _auth_requirement(path: str) -> str:
    if path in {"/health", "/openapi.json"} or path.startswith("/docs"):
        return "public"
    if path.startswith("/media/"):
        return "public"
    if path == "/api/v1/auth/login":
        return "public"
    if path.startswith("/api/v1/admin/users"):
        return "admin"
    if path.startswith("/api/v1/admin/system-settings"):
        return "admin"
    if path.startswith("/api/v1/admin/api-docs"):
        return "admin"
    if path.startswith("/api/v1/admin/"):
        return "admin/employee"
    if path.startswith("/api/v1/profile") or path.startswith("/api/v1/admin/profile"):
        return "admin/employee"
    if path in {"/api/v1/auth/me", "/api/v1/auth/logout"}:
        return "login"
    return "public"


def _route_source(path: str, included_in_openapi: bool) -> str:
    if path.startswith("/api/v1/"):
        return "openapi" if included_in_openapi else "fastapi-app"
    if path == "/health":
        return "health-check"
    if path.startswith("/media/"):
        return "media-passthrough"
    return "fastapi-app"


def _display_path(path: str) -> str:
    if path == "/media/{object_key}":
        return "/media/{object_key:path}"
    return path


def _openapi_operations(openapi_schema: dict[str, Any]) -> dict[tuple[str, str], dict[str, Any]]:
    operations: dict[tuple[str, str], dict[str, Any]] = {}
    for path, methods in openapi_schema.get("paths", {}).items():
        if not isinstance(methods, dict):
            continue
        for method, operation in methods.items():
            if not isinstance(operation, dict):
                continue
            operations[(path, method.upper())] = operation
    return operations


def _build_route_items(request: Request) -> list[ApiDocsRouteItem]:
    openapi_operations = _openapi_operations(request.app.openapi())
    items: list[ApiDocsRouteItem] = []

    for route in request.app.routes:
        path = getattr(route, "path_format", getattr(route, "path", ""))
        if not path:
            continue

        raw_methods = getattr(route, "methods", None) or {"GET"}
        methods = sorted(
            method for method in raw_methods if method not in {"HEAD", "OPTIONS"}
        )
        if not methods:
            continue

        display_path = _display_path(path)
        for method in methods:
            operation = openapi_operations.get((path, method))
            included_in_openapi = operation is not None
            operation_id = operation.get("operationId") if operation else None
            orval_method_name = _operation_to_orval_method(operation_id)
            tags = operation.get("tags") if operation else getattr(route, "tags", None)
            tag = tags[0] if isinstance(tags, list) and tags else "system"
            summary = (
                operation.get("summary")
                if operation
                else getattr(route, "summary", None)
                or getattr(route, "name", path)
            )
            missing_reason = None
            if not orval_method_name:
                missing_reason = (
                    "未纳入 OpenAPI schema"
                    if not included_in_openapi
                    else "OpenAPI 未提供 operationId"
                )

            items.append(
                ApiDocsRouteItem(
                    method=method,
                    path=display_path,
                    tag=tag,
                    summary=str(summary),
                    auth_requirement=_auth_requirement(display_path),
                    included_in_openapi=included_in_openapi,
                    operation_id=operation_id,
                    orval_method_name=orval_method_name,
                    source=_route_source(display_path, included_in_openapi),
                    missing_orval_reason=missing_reason,
                )
            )

    return sorted(items, key=lambda item: (item.path, _method_sort_key(item.method)))


def _environment_policy() -> ApiDocsEnvironmentPolicy:
    app_env = settings.app_env.strip().lower()
    allow_try_it_out = settings.allow_swagger_try_it_out()
    if allow_try_it_out:
        return ApiDocsEnvironmentPolicy(
            app_env=app_env,
            allow_try_it_out=True,
            label="允许在线调试",
            description="当前环境允许通过 Swagger Try It Out 调试接口。",
        )
    return ApiDocsEnvironmentPolicy(
        app_env=app_env,
        allow_try_it_out=False,
        label="生产环境仅查看",
        description="当前环境仅允许查看接口文档，Swagger Try It Out 必须隐藏或禁用。",
    )


@router.get(
    "",
    response_model=ApiResponse[ApiDocsData],
    tags=["admin-api-docs"],
    summary="管理端接口文档目录",
)
def get_api_docs(request: Request) -> ApiResponse[ApiDocsData]:
    routes = _build_route_items(request)
    summary = ApiDocsSummary(
        total_routes=len(routes),
        protected_routes=sum(1 for item in routes if item.auth_requirement != "public"),
        orval_mapped_routes=sum(1 for item in routes if item.orval_method_name),
        non_api_v1_routes=sum(1 for item in routes if not item.path.startswith("/api/v1/")),
    )
    return ApiResponse(
        data=ApiDocsData(
            routes=routes,
            summary=summary,
            environment=_environment_policy(),
        )
    )
