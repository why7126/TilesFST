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
    behavior_trace_id: str | None = Field(default=None, max_length=128)
    task_trace_id: str | None = Field(default=None, max_length=96)
    start_time: str | None = Field(default=None, max_length=64)
    end_time: str | None = Field(default=None, max_length=64)

    @field_validator("keyword", "actor_user_id", "client_type", "resource_id", "path_or_request_id", "behavior_trace_id", "task_trace_id")
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
    actor_username: str | None = None
    actor_role: str | None = None
    client_type: str
    result: str
    status_code: int | None = None
    duration_ms: int | None = None
    request_id: str | None = None
    client_request_id: str | None = None
    behavior_trace_id: str | None = None
    parent_behavior_event_id: str | None = None
    task_trace_id: str | None = None
    task_type: str | None = None
    task_status: str | None = None
    task_duration_ms: int | None = None
    task_slowest_span_name: str | None = None
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


class LogObservabilityQueryParams(BaseModel):
    log_type: Literal["request", "usage_event", "audit"] | None = None
    client_type: str | None = Field(default=None, max_length=32)
    task_type: str | None = Field(default=None, max_length=64)
    path_or_request_id: str | None = Field(default=None, max_length=180)
    status_code: int | None = Field(default=None, ge=100, le=599)
    result: Literal["success", "failed"] | None = None
    request_id: str | None = Field(default=None, max_length=128)
    behavior_trace_id: str | None = Field(default=None, max_length=128)
    task_trace_id: str | None = Field(default=None, max_length=96)
    start_time: str | None = Field(default=None, max_length=64)
    end_time: str | None = Field(default=None, max_length=64)

    @field_validator("client_type", "task_type", "path_or_request_id", "request_id", "behavior_trace_id", "task_trace_id")
    @classmethod
    def blank_to_none(cls, value: str | None) -> str | None:
        if value is None:
            return None
        stripped = value.strip()
        return stripped or None


class ObservabilitySummaryData(BaseModel):
    total_logs: int
    api_errors: int
    api_error_rate: float
    slow_requests: int
    task_success_rate: float | None = None
    failed_tasks: int
    slow_tasks: int
    audit_operations: int


class ObservabilityDistributionItem(BaseModel):
    label: str
    count: int
    rate: float | None = None


class ObservabilityEndpointItem(BaseModel):
    path: str
    method: str
    status_code: int | None = None
    request_count: int
    error_count: int
    error_rate: float


class ObservabilitySlowRequestItem(BaseModel):
    log_id: str
    path: str
    method: str
    status_code: int
    duration_ms: int
    client_type: str
    request_id: str | None = None
    behavior_trace_id: str | None = None


class ObservabilityTaskItem(BaseModel):
    task_trace_id: str
    task_type: str
    status: str
    duration_ms: int | None = None
    client_type: str | None = None
    trigger_source: str | None = None
    error_code: str | None = None
    summary: str


class ObservabilitySpanItem(BaseModel):
    task_trace_id: str
    task_type: str
    span_name: str
    status: str
    duration_ms: int | None = None
    request_id: str | None = None
    behavior_trace_id: str | None = None
    error_code: str | None = None
    summary: str


class ObservabilityTraceResultsData(BaseModel):
    behavior_trace_id: str | None = None
    request_id: str | None = None
    task_trace_id: str | None = None
    log_ids: list[str] = Field(default_factory=list)
    request_ids: list[str] = Field(default_factory=list)
    task_trace_ids: list[str] = Field(default_factory=list)
    reason: str | None = None


class LogObservabilityData(BaseModel):
    summary: ObservabilitySummaryData
    distributions: dict[str, list[ObservabilityDistributionItem]]
    endpoint_errors: list[ObservabilityEndpointItem]
    rankings: dict[str, list[ObservabilitySlowRequestItem | ObservabilityTaskItem | ObservabilitySpanItem]]
    trace_results: ObservabilityTraceResultsData
    thresholds: dict[str, int]


class LogDetailSection(BaseModel):
    title: str
    fields: dict[str, Any]


class TaskTraceSpanData(BaseModel):
    span_name: str
    status: str
    started_at: str
    ended_at: str | None = None
    duration_ms: int | None = None
    request_id: str | None = None
    behavior_trace_id: str | None = None
    error_code: str | None = None
    summary: str
    is_slowest: bool = False


class TaskTraceData(BaseModel):
    task_trace_id: str
    task_type: str
    status: str
    parent_request_id: str | None = None
    behavior_trace_id: str | None = None
    duration_ms: int | None = None
    resource_type: str | None = None
    resource_id: str | None = None
    slowest_span_name: str | None = None
    error_code: str | None = None
    summary: str
    spans: list[TaskTraceSpanData]


class RequestSnapshotRequestData(BaseModel):
    method: str | None = None
    path: str | None = None
    route_template: str | None = None
    route_match_status: Literal["matched", "unmatched", "unknown"] = "unknown"
    request_id: str | None = None
    client_request_id: str | None = None
    behavior_trace_id: str | None = None
    parent_behavior_event_id: str | None = None
    trusted_request_id_header: str | None = None
    client_request_id_header: str | None = None
    behavior_trace_id_header: str | None = None
    behavior_event_id_header: str | None = None


class RequestSnapshotInputData(BaseModel):
    query: dict[str, Any] = Field(default_factory=dict)
    body_schema_summary: dict[str, Any] = Field(default_factory=dict)
    redaction_summary: dict[str, Any] = Field(default_factory=dict)


class RequestSnapshotResourceData(BaseModel):
    resource_type: str | None = None
    resource_id: str | None = None
    id_source: str | None = None


class RequestSnapshotResponseData(BaseModel):
    status_code: int | None = None
    error_code: str | None = None
    duration_ms: int | None = None
    result: str | None = None
    error_summary: str | None = None


class RequestSnapshotActorData(BaseModel):
    actor_user_id: str | None = None
    actor_username: str | None = None
    actor_role: str | None = None
    client_type: str | None = None
    ip_summary: str | None = None
    user_agent_summary: str | None = None


class RequestSnapshotTimingData(BaseModel):
    environment: str | None = None
    started_at: str | None = None
    finished_at: str | None = None


class RequestSnapshotData(BaseModel):
    request: RequestSnapshotRequestData = Field(default_factory=RequestSnapshotRequestData)
    input: RequestSnapshotInputData = Field(default_factory=RequestSnapshotInputData)
    resource: RequestSnapshotResourceData = Field(default_factory=RequestSnapshotResourceData)
    response: RequestSnapshotResponseData = Field(default_factory=RequestSnapshotResponseData)
    actor: RequestSnapshotActorData = Field(default_factory=RequestSnapshotActorData)
    timing: RequestSnapshotTimingData = Field(default_factory=RequestSnapshotTimingData)
    raw_json: str
    parse_error: str | None = None


class LogDetailData(BaseModel):
    log: LogListItem
    basic: LogDetailSection
    request: LogDetailSection
    actor: LogDetailSection
    context: LogDetailSection
    event: LogDetailSection
    task_trace: TaskTraceData | None = None
    related_task_traces: list[TaskTraceData] = Field(default_factory=list)
    request_snapshot: RequestSnapshotData | None = None
    metadata_json: str


class UsageEventCreate(BaseModel):
    event_name: str = Field(min_length=1, max_length=64)
    properties: dict[str, Any] = Field(default_factory=dict)
    client_type: str | None = Field(default="web_admin", max_length=32)
    page_path: str | None = Field(default=None, max_length=768)
    request_id: str | None = Field(default=None, max_length=128)
    client_request_id: str | None = Field(default=None, max_length=128)
    behavior_trace_id: str | None = Field(default=None, max_length=128)
    behavior_event_id: str | None = Field(default=None, max_length=128)
    task_trace_id: str | None = Field(default=None, max_length=96)
    task_type: str | None = Field(default=None, max_length=64)
    session_id: str | None = Field(default=None, max_length=128)
    duration_ms: int | None = Field(default=None, ge=0, le=86_400_000)
    summary: str | None = Field(default=None, max_length=220)


class UsageEventData(BaseModel):
    id: str
    accepted: bool
    behavior_trace_id: str | None = None
    behavior_event_id: str | None = None
