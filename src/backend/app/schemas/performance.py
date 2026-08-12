"""Schemas for real-user performance monitoring."""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field, field_validator

ClientType = Literal["web_admin", "web_catalog", "wechat_miniapp"]


class PerformanceEventCreate(BaseModel):
    client_type: ClientType
    page_key: str = Field(min_length=1, max_length=120, pattern=r"^[a-zA-Z0-9_:/.-]+$")
    app_version: str | None = Field(default=None, max_length=64)
    network_type: str | None = Field(default=None, max_length=32)
    device_class: str | None = Field(default=None, max_length=32)
    metric_name: str = Field(min_length=1, max_length=64, pattern=r"^[a-zA-Z0-9_.:-]+$")
    duration_ms: int = Field(ge=0, le=300_000)
    sample_rate: float = Field(default=1.0, ge=0.0, le=1.0)
    occurred_at: str = Field(min_length=1, max_length=64)
    request_id: str | None = Field(default=None, max_length=128)

    @field_validator("app_version", "network_type", "device_class", "request_id")
    @classmethod
    def blank_to_none(cls, value: str | None) -> str | None:
        if value is None:
            return None
        stripped = value.strip()
        return stripped or None


class PerformanceEventBatchCreate(BaseModel):
    events: list[PerformanceEventCreate] = Field(min_length=1, max_length=50)


class PerformanceEventIngestData(BaseModel):
    accepted: int
    rejected: int = 0


class PerformanceSummaryQueryParams(BaseModel):
    client_type: ClientType | None = None
    page_key: str | None = Field(default=None, max_length=120)
    app_version: str | None = Field(default=None, max_length=64)
    network_type: str | None = Field(default=None, max_length=32)
    device_class: str | None = Field(default=None, max_length=32)
    metric_name: str | None = Field(default=None, max_length=64)
    start_time: str | None = Field(default=None, max_length=64)
    end_time: str | None = Field(default=None, max_length=64)
    min_samples: int = Field(default=20, ge=1, le=10_000)
    page: int = Field(default=1, ge=1)
    page_size: int = Field(default=20, ge=1, le=100)
    limit: int | None = Field(default=None, ge=1, le=100)

    @field_validator("page_key", "app_version", "network_type", "device_class", "metric_name", "start_time", "end_time")
    @classmethod
    def blank_query_to_none(cls, value: str | None) -> str | None:
        if value is None:
            return None
        stripped = value.strip()
        return stripped or None


class PerformanceAggregateItem(BaseModel):
    client_type: str
    page_key: str
    metric_name: str
    app_version: str | None = None
    network_type: str | None = None
    device_class: str | None = None
    sample_count: int
    average_ms: float
    max_ms: int
    p50_ms: int
    p75_ms: int
    p95_ms: int
    p99_ms: int
    sample_status: Literal["ok", "insufficient"]


class PerformanceSummaryData(BaseModel):
    items: list[PerformanceAggregateItem]
    slow_pages: list[PerformanceAggregateItem]
    total: int
    page: int
    page_size: int
    total_pages: int
    total_events: int
    filters: dict[str, str | int | None]
    thresholds: dict[str, int]


class PerformanceSampleQueryParams(BaseModel):
    client_type: ClientType | None = None
    page_key: str | None = Field(default=None, max_length=120)
    app_version: str | None = Field(default=None, max_length=64)
    network_type: str | None = Field(default=None, max_length=32)
    device_class: str | None = Field(default=None, max_length=32)
    metric_name: str | None = Field(default=None, max_length=64)
    start_time: str | None = Field(default=None, max_length=64)
    end_time: str | None = Field(default=None, max_length=64)
    page: int = Field(default=1, ge=1)
    page_size: int = Field(default=20, ge=1, le=100)
    limit: int | None = Field(default=None, ge=1, le=100)

    @field_validator("page_key", "app_version", "network_type", "device_class", "metric_name", "start_time", "end_time")
    @classmethod
    def blank_query_to_none(cls, value: str | None) -> str | None:
        if value is None:
            return None
        stripped = value.strip()
        return stripped or None


class PerformanceSampleItem(BaseModel):
    id: str
    client_type: str
    page_key: str
    metric_name: str
    duration_ms: int
    app_version: str | None = None
    network_type: str | None = None
    device_class: str | None = None
    request_id: str | None = None
    occurred_at: str
    server_received_at: str


class PerformanceSampleData(BaseModel):
    items: list[PerformanceSampleItem]
    total: int
    page: int
    page_size: int
    total_pages: int
    filters: dict[str, str | int | None]
