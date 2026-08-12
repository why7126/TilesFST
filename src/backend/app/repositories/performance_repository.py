"""Repository for real-user performance events."""

from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import UTC, datetime
from uuid import uuid4

from sqlalchemy import text
from sqlalchemy.orm import Session

from app.schemas.performance import PerformanceEventCreate, PerformanceSampleQueryParams, PerformanceSummaryQueryParams


@dataclass
class PerformanceAggregateRecord:
    client_type: str
    page_key: str
    metric_name: str
    app_version: str | None
    network_type: str | None
    device_class: str | None
    durations: list[int]


@dataclass
class PerformanceSampleRecord:
    id: str
    client_type: str
    page_key: str
    metric_name: str
    duration_ms: int
    app_version: str | None
    network_type: str | None
    device_class: str | None
    request_id: str | None
    occurred_at: str
    server_received_at: str


class PerformanceRepository:
    def __init__(self, db: Session) -> None:
        self._db = db

    def insert_events(self, events: list[PerformanceEventCreate], *, metadata: dict[str, str | None]) -> int:
        now = datetime.now(UTC).isoformat()
        for event in events:
            self._db.execute(
                text(
                    """
                    INSERT INTO performance_events (
                      id, client_type, page_key, app_version, network_type, device_class,
                      metric_name, duration_ms, sample_rate, occurred_at, server_received_at,
                      request_id, metadata
                    ) VALUES (
                      :id, :client_type, :page_key, :app_version, :network_type, :device_class,
                      :metric_name, :duration_ms, :sample_rate, :occurred_at, :server_received_at,
                      :request_id, :metadata
                    )
                    """
                ),
                {
                    "id": str(uuid4()),
                    "client_type": event.client_type,
                    "page_key": event.page_key,
                    "app_version": event.app_version,
                    "network_type": event.network_type,
                    "device_class": event.device_class,
                    "metric_name": event.metric_name,
                    "duration_ms": event.duration_ms,
                    "sample_rate": event.sample_rate,
                    "occurred_at": event.occurred_at,
                    "server_received_at": now,
                    "request_id": event.request_id,
                    "metadata": json.dumps(metadata, ensure_ascii=False),
                },
            )
        self._db.commit()
        return len(events)

    def aggregate(self, params: PerformanceSummaryQueryParams) -> list[PerformanceAggregateRecord]:
        records = self._aggregate_all(params)
        start = (params.page - 1) * params.page_size
        end = start + params.page_size
        return records[start:end]

    def count_aggregate_groups(self, params: PerformanceSummaryQueryParams) -> int:
        return len(self._aggregate_all(params))

    def _aggregate_all(self, params: PerformanceSummaryQueryParams) -> list[PerformanceAggregateRecord]:
        where, values = self._build_filters(params)
        sql = f"""
            SELECT client_type, page_key, metric_name, app_version, network_type, device_class, duration_ms
            FROM performance_events
            {where}
            ORDER BY server_received_at DESC
        """
        rows = self._db.execute(text(sql), values).mappings().all()
        grouped: dict[tuple[str, str, str, str | None, str | None, str | None], list[int]] = {}
        for row in rows:
            key = (
                str(row["client_type"]),
                str(row["page_key"]),
                str(row["metric_name"]),
                row["app_version"],
                row["network_type"],
                row["device_class"],
            )
            grouped.setdefault(key, []).append(int(row["duration_ms"]))
        records = [
            PerformanceAggregateRecord(
                client_type=key[0],
                page_key=key[1],
                metric_name=key[2],
                app_version=key[3],
                network_type=key[4],
                device_class=key[5],
                durations=durations,
            )
            for key, durations in grouped.items()
        ]
        return sorted(records, key=_aggregate_sort_key, reverse=True)

    def count(self, params: PerformanceSummaryQueryParams) -> int:
        where, values = self._build_filters(params)
        return int(self._db.execute(text(f"SELECT COUNT(*) FROM performance_events {where}"), values).scalar_one() or 0)

    def list_samples(self, params: PerformanceSampleQueryParams) -> list[PerformanceSampleRecord]:
        where, values = self._build_filters(params)
        values["limit"] = params.limit or params.page_size
        values["offset"] = (params.page - 1) * (params.limit or params.page_size)
        rows = self._db.execute(
            text(
                f"""
                SELECT id, client_type, page_key, metric_name, duration_ms, app_version,
                       network_type, device_class, request_id, occurred_at, server_received_at
                FROM performance_events
                {where}
                ORDER BY server_received_at DESC
                LIMIT :limit OFFSET :offset
                """
            ),
            values,
        ).mappings().all()
        return [
            PerformanceSampleRecord(
                id=str(row["id"]),
                client_type=str(row["client_type"]),
                page_key=str(row["page_key"]),
                metric_name=str(row["metric_name"]),
                duration_ms=int(row["duration_ms"]),
                app_version=row["app_version"],
                network_type=row["network_type"],
                device_class=row["device_class"],
                request_id=row["request_id"],
                occurred_at=str(row["occurred_at"]),
                server_received_at=str(row["server_received_at"]),
            )
            for row in rows
        ]

    def count_samples(self, params: PerformanceSampleQueryParams) -> int:
        where, values = self._build_filters(params)
        return int(self._db.execute(text(f"SELECT COUNT(*) FROM performance_events {where}"), values).scalar_one() or 0)

    def _build_filters(self, params: PerformanceSummaryQueryParams | PerformanceSampleQueryParams) -> tuple[str, dict[str, object]]:
        clauses: list[str] = []
        values: dict[str, object] = {}
        for field in ("client_type", "page_key", "app_version", "network_type", "device_class", "metric_name"):
            value = getattr(params, field)
            if value:
                clauses.append(f"{field} = :{field}")
                values[field] = value
        if params.start_time:
            clauses.append("server_received_at >= :start_time")
            values["start_time"] = params.start_time
        if params.end_time:
            clauses.append("server_received_at <= :end_time")
            values["end_time"] = params.end_time
        return (f"WHERE {' AND '.join(clauses)}" if clauses else ""), values


def _percentile(values: list[int], ratio: float) -> int:
    if not values:
        return 0
    sorted_values = sorted(values)
    index = min(len(sorted_values) - 1, max(0, round((len(sorted_values) - 1) * ratio)))
    return sorted_values[index]


def _aggregate_sort_key(item: PerformanceAggregateRecord) -> tuple[int, int, int]:
    return (_percentile(item.durations, 0.95), len(item.durations), max(item.durations) if item.durations else 0)
