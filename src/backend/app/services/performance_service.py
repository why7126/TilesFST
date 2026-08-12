"""Service for real-user performance monitoring."""

from __future__ import annotations

import math

from app.core.exceptions import AuthInvalidRequestError
from app.repositories.performance_repository import PerformanceAggregateRecord, PerformanceRepository
from app.schemas.performance import (
    PerformanceAggregateItem,
    PerformanceEventBatchCreate,
    PerformanceEventIngestData,
    PerformanceSampleData,
    PerformanceSampleItem,
    PerformanceSampleQueryParams,
    PerformanceSummaryData,
    PerformanceSummaryQueryParams,
)

FORBIDDEN_EVENT_WORDS = {
    "authorization",
    "cookie",
    "token",
    "password",
    "openid",
    "phone",
    "sign",
    "signature",
    "raw_payload",
    "raw_response",
}


class PerformanceService:
    def __init__(self, repository: PerformanceRepository) -> None:
        self._repository = repository

    def ingest(self, payload: PerformanceEventBatchCreate, *, user_agent: str | None, ip_family: str | None) -> PerformanceEventIngestData:
        for event in payload.events:
            joined = " ".join(
                str(value).lower()
                for value in (
                    event.page_key,
                    event.metric_name,
                    event.request_id,
                    event.network_type,
                    event.device_class,
                )
                if value
            )
            if any(word in joined for word in FORBIDDEN_EVENT_WORDS):
                raise AuthInvalidRequestError("性能事件包含禁止字段或敏感信息")
        accepted = self._repository.insert_events(
            payload.events,
            metadata={
                "user_agent_summary": _summarize_user_agent(user_agent),
                "ip_family": ip_family,
            },
        )
        return PerformanceEventIngestData(accepted=accepted)

    def summarize(self, params: PerformanceSummaryQueryParams) -> PerformanceSummaryData:
        records = self._repository.aggregate(params)
        items = [_to_item(record, params.min_samples) for record in records]
        total = self._repository.count_aggregate_groups(params)
        return PerformanceSummaryData(
            items=items,
            slow_pages=items,
            total=total,
            page=params.page,
            page_size=params.page_size,
            total_pages=max(1, math.ceil(total / params.page_size)),
            total_events=self._repository.count(params),
            filters=params.model_dump(),
            thresholds={"min_samples": params.min_samples, "slow_page_p95_ms": 3000},
        )

    def list_samples(self, params: PerformanceSampleQueryParams) -> PerformanceSampleData:
        total = self._repository.count_samples(params)
        return PerformanceSampleData(
            items=[
                PerformanceSampleItem(
                    id=record.id,
                    client_type=record.client_type,
                    page_key=record.page_key,
                    metric_name=record.metric_name,
                    duration_ms=record.duration_ms,
                    app_version=record.app_version,
                    network_type=record.network_type,
                    device_class=record.device_class,
                    request_id=record.request_id,
                    occurred_at=record.occurred_at,
                    server_received_at=record.server_received_at,
                )
                for record in self._repository.list_samples(params)
            ],
            total=total,
            page=params.page,
            page_size=params.limit or params.page_size,
            total_pages=max(1, math.ceil(total / (params.limit or params.page_size))),
            filters=params.model_dump(),
        )


def _to_item(record: PerformanceAggregateRecord, min_samples: int) -> PerformanceAggregateItem:
    durations = sorted(record.durations)
    sample_count = len(durations)
    return PerformanceAggregateItem(
        client_type=record.client_type,
        page_key=record.page_key,
        metric_name=record.metric_name,
        app_version=record.app_version,
        network_type=record.network_type,
        device_class=record.device_class,
        sample_count=sample_count,
        average_ms=round(sum(durations) / sample_count, 2) if sample_count else 0,
        max_ms=max(durations) if durations else 0,
        p50_ms=_percentile(durations, 0.5),
        p75_ms=_percentile(durations, 0.75),
        p95_ms=_percentile(durations, 0.95),
        p99_ms=_percentile(durations, 0.99),
        sample_status="ok" if sample_count >= min_samples else "insufficient",
    )


def _percentile(values: list[int], ratio: float) -> int:
    if not values:
        return 0
    index = min(len(values) - 1, max(0, round((len(values) - 1) * ratio)))
    return values[index]


def _summarize_user_agent(value: str | None) -> str | None:
    if not value:
        return None
    return value[:160]
