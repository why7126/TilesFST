"""Schemas for product usage logging and admin log audit."""

from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, Field, field_validator


class LogQueryParams(BaseModel):
    page: int = Field(default=1, ge=1)
    page_size: int = Field(default=20, ge=1, le=100)
    log_type: Literal["request", "usage_event", "audit"] | None = None
    keyword: str | None = Field(default=None, max_length=120)
    actor_user_id: str | None = Field(default=None, max_length=64)
    client_type: str | None = Field(default=None, max_length=32)
    status_code: int | None = Field(default=None, ge=100, le=599)
    result: Literal["success", "failed"] | None = None
    resource_id: str | None = Field(default=None, max_length=128)
    path_or_request_id: str | None = Field(default=None, max_length=180)
    start_time: str | None = Field(default=None, max_length=64)
    end_time: str | None = Field(default=None, max_length=64)

    @field_validator("keyword", "actor_user_id", "client_type", "resource_id", "path_or_request_id")
    @classmethod
    def blank_to_none(cls, value: str | None) -> str | None:
        if value is None:
            return None
        stripped = value.strip()
        return stripped or None


class LogListItem(BaseModel):
    id: str
    log_type: str
    created_at: str
    summary: str
    actor_name: str | None = None
    actor_role: str | None = None
    client_type: str
    result: str
    status_code: int | None = None
    duration_ms: int | None = None
    request_id: str | None = None
    event_name: str | None = None
    method: str | None = None
    path: str | None = None


class LogMetricsData(BaseModel):
    today_logs: int
    api_errors: int
    slow_requests: int
    sensitive_ops: int


class LogListData(BaseModel):
    items: list[LogListItem]
    total: int
    page: int
    page_size: int
    summary: LogMetricsData


class LogDetailSection(BaseModel):
    title: str
    fields: dict[str, Any]


class LogDetailData(BaseModel):
    log: LogListItem
    basic: LogDetailSection
    request: LogDetailSection
    actor: LogDetailSection
    context: LogDetailSection
    event: LogDetailSection
    metadata_json: str


class UsageEventCreate(BaseModel):
    event_name: str = Field(min_length=1, max_length=64)
    properties: dict[str, Any] = Field(default_factory=dict)
    client_type: str | None = Field(default="web_admin", max_length=32)
    page_path: str | None = Field(default=None, max_length=768)
    request_id: str | None = Field(default=None, max_length=128)
    session_id: str | None = Field(default=None, max_length=128)
    duration_ms: int | None = Field(default=None, ge=0, le=86_400_000)
    summary: str | None = Field(default=None, max_length=220)


class UsageEventData(BaseModel):
    id: str
    accepted: bool
