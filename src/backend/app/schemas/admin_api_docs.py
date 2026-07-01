"""Schemas for admin API documentation inventory."""

from __future__ import annotations

from pydantic import BaseModel


class ApiDocsRouteItem(BaseModel):
    method: str
    path: str
    tag: str
    summary: str
    auth_requirement: str
    included_in_openapi: bool
    operation_id: str | None = None
    orval_method_name: str | None = None
    source: str
    missing_orval_reason: str | None = None


class ApiDocsSummary(BaseModel):
    total_routes: int
    protected_routes: int
    orval_mapped_routes: int
    non_api_v1_routes: int


class ApiDocsEnvironmentPolicy(BaseModel):
    app_env: str
    allow_try_it_out: bool
    label: str
    description: str


class ApiDocsData(BaseModel):
    routes: list[ApiDocsRouteItem]
    summary: ApiDocsSummary
    environment: ApiDocsEnvironmentPolicy
