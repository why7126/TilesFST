"""Request log, usage event, and unified log audit queries."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime
from typing import Any
from uuid import uuid4

from sqlalchemy import text
from sqlalchemy.orm import Session


@dataclass
class LogRecord:
    id: str
    log_type: str
    request_id: str | None
    actor_user_id: str | None
    actor_role: str | None
    actor_name: str | None
    actor_username: str | None
    client_type: str | None
    client_request_id: str | None
    behavior_trace_id: str | None
    parent_behavior_event_id: str | None
    event_name: str | None
    method: str | None
    path: str | None
    status_code: int | None
    duration_ms: int | None
    ip_address_masked: str | None
    user_agent_summary: str | None
    summary: str
    error_code: str | None
    result: str
    task_trace_id: str | None
    task_type: str | None
    task_status: str | None
    task_duration_ms: int | None
    task_slowest_span_name: str | None
    metadata: str | None
    created_at: str


@dataclass
class LogQueryResult:
    items: list[LogRecord]
    total: int


@dataclass
class LogMetrics:
    today_logs: int
    api_errors: int
    slow_requests: int
    sensitive_ops: int


class LogRepository:
    def __init__(self, db: Session) -> None:
        self._db = db

    def insert_request_log(
        self,
        *,
        request_id: str,
        actor_user_id: str | None,
        actor_role: str | None,
        client_type: str,
        client_request_id: str | None,
        behavior_trace_id: str | None = None,
        parent_behavior_event_id: str | None = None,
        method: str,
        path: str,
        status_code: int,
        duration_ms: int,
        ip_address_masked: str | None,
        user_agent_summary: str | None,
        summary: str,
        error_code: str | None = None,
        result: str = "success",
        task_trace_id: str | None = None,
        task_type: str | None = None,
        metadata: str | None = None,
    ) -> str:
        log_id = str(uuid4())
        self._db.execute(
            text(
                """
                INSERT INTO request_logs (
                  id, request_id, actor_user_id, actor_role, client_type, client_request_id,
                  behavior_trace_id, parent_behavior_event_id,
                  method, path, status_code, duration_ms, ip_address_masked,
                  user_agent_summary, summary, error_code, result, task_trace_id, task_type,
                  metadata, created_at
                ) VALUES (
                  :id, :request_id, :actor_user_id, :actor_role, :client_type, :client_request_id,
                  :behavior_trace_id, :parent_behavior_event_id,
                  :method, :path, :status_code, :duration_ms, :ip_address_masked,
                  :user_agent_summary, :summary, :error_code, :result, :task_trace_id, :task_type,
                  :metadata, :created_at
                )
                """
            ),
            {
                "id": log_id,
                "request_id": request_id,
                "actor_user_id": actor_user_id,
                "actor_role": actor_role,
                "client_type": client_type,
                "client_request_id": client_request_id,
                "behavior_trace_id": behavior_trace_id,
                "parent_behavior_event_id": parent_behavior_event_id,
                "method": method,
                "path": path,
                "status_code": status_code,
                "duration_ms": duration_ms,
                "ip_address_masked": ip_address_masked,
                "user_agent_summary": user_agent_summary,
                "summary": summary,
                "error_code": error_code,
                "result": result,
                "task_trace_id": task_trace_id,
                "task_type": task_type,
                "metadata": metadata,
                "created_at": datetime.now(UTC).isoformat(),
            },
        )
        self._db.commit()
        return log_id

    def insert_usage_event(
        self,
        *,
        request_id: str | None,
        actor_user_id: str | None,
        actor_role: str | None,
        client_type: str,
        behavior_trace_id: str | None = None,
        behavior_event_id: str | None = None,
        event_name: str,
        event_category: str,
        page_path: str | None,
        session_id: str | None,
        ip_address_masked: str | None,
        user_agent_summary: str | None,
        summary: str,
        duration_ms: int | None,
        result: str,
        task_trace_id: str | None,
        task_type: str | None,
        metadata: str | None,
    ) -> str:
        event_id = str(uuid4())
        self._db.execute(
            text(
                """
                INSERT INTO usage_events (
                  id, request_id, actor_user_id, actor_role, client_type,
                  behavior_trace_id, behavior_event_id,
                  event_name, event_category, page_path, session_id,
                  ip_address_masked, user_agent_summary, summary, duration_ms, result,
                  task_trace_id, task_type, metadata, created_at
                ) VALUES (
                  :id, :request_id, :actor_user_id, :actor_role, :client_type,
                  :behavior_trace_id, :behavior_event_id,
                  :event_name, :event_category, :page_path, :session_id,
                  :ip_address_masked, :user_agent_summary, :summary, :duration_ms, :result,
                  :task_trace_id, :task_type, :metadata, :created_at
                )
                """
            ),
            {
                "id": event_id,
                "request_id": request_id,
                "actor_user_id": actor_user_id,
                "actor_role": actor_role,
                "client_type": client_type,
                "behavior_trace_id": behavior_trace_id,
                "behavior_event_id": behavior_event_id,
                "event_name": event_name,
                "event_category": event_category,
                "page_path": page_path,
                "session_id": session_id,
                "ip_address_masked": ip_address_masked,
                "user_agent_summary": user_agent_summary,
                "summary": summary,
                "duration_ms": duration_ms,
                "result": result,
                "task_trace_id": task_trace_id,
                "task_type": task_type,
                "metadata": metadata,
                "created_at": datetime.now(UTC).isoformat(),
            },
        )
        self._db.commit()
        return event_id

    def list_logs(
        self,
        *,
        page: int,
        page_size: int,
        log_type: str | None = None,
        keyword: str | None = None,
        actor_user_id: str | None = None,
        client_type: str | None = None,
        status_code: int | None = None,
        result: str | None = None,
        resource_id: str | None = None,
        path_or_request_id: str | None = None,
        behavior_trace_id: str | None = None,
        task_trace_id: str | None = None,
        start_time: str | None = None,
        end_time: str | None = None,
    ) -> LogQueryResult:
        source, params = self._list_source_sql(
            log_type=log_type,
            keyword=keyword,
            actor_user_id=actor_user_id,
            client_type=client_type,
            status_code=status_code,
            result=result,
            resource_id=resource_id,
            path_or_request_id=path_or_request_id,
            behavior_trace_id=behavior_trace_id,
            task_trace_id=task_trace_id,
            start_time=start_time,
            end_time=end_time,
        )
        params["limit"] = page_size
        params["offset"] = (page - 1) * page_size
        total = int(
            self._db.execute(
                text(f"SELECT COUNT(*) FROM ({source}) logs"),
                params,
            ).scalar_one()
            or 0
        )
        rows = (
            self._db.execute(
                text(
                    f"""
                    SELECT * FROM ({source}) logs
                    ORDER BY created_at DESC
                    LIMIT :limit OFFSET :offset
                    """
                ),
                params,
            )
            .mappings()
            .all()
        )
        return LogQueryResult(items=[self._to_record(dict(row)) for row in rows], total=total)

    def get_log(self, log_id: str) -> LogRecord | None:
        source = self._union_source_sql()
        row = (
            self._db.execute(
                text(f"SELECT * FROM ({source}) logs WHERE id = :id LIMIT 1"),
                {"id": log_id},
            )
            .mappings()
            .first()
        )
        return self._to_record(dict(row)) if row else None

    def get_metrics(self, *, today_start: str, slow_threshold_ms: int = 1000) -> LogMetrics:
        row = self._db.execute(
            text(
                """
                SELECT
                  (
                    SELECT COUNT(*) FROM request_logs WHERE created_at >= :today_start
                  ) + (
                    SELECT COUNT(*) FROM usage_events WHERE created_at >= :today_start
                  ) + (
                    SELECT COUNT(*) FROM audit_logs WHERE created_at >= :today_start
                  ) AS today_logs,
                  (
                    SELECT COUNT(*) FROM request_logs WHERE status_code >= 400
                  ) AS api_errors,
                  (
                    SELECT COUNT(*) FROM request_logs WHERE duration_ms >= :slow_threshold_ms
                  ) AS slow_requests,
                  (
                    SELECT COUNT(*) FROM audit_logs WHERE created_at >= :today_start
                  ) AS sensitive_ops
                """
            ),
            {"today_start": today_start, "slow_threshold_ms": slow_threshold_ms},
        ).mappings().one()
        return LogMetrics(
            today_logs=int(row["today_logs"] or 0),
            api_errors=int(row["api_errors"] or 0),
            slow_requests=int(row["slow_requests"] or 0),
            sensitive_ops=int(row["sensitive_ops"] or 0),
        )

    def get_observability(
        self,
        *,
        filters: dict[str, Any],
        slow_request_threshold_ms: int = 1000,
        slow_task_threshold_ms: int = 1000,
        top_limit: int = 5,
    ) -> dict[str, Any]:
        where, params = self._build_observability_filters(**filters)
        source = self._union_source_sql()
        summary = self._db.execute(
            text(
                f"""
                SELECT
                  COUNT(*) AS total_logs,
                  SUM(CASE WHEN log_type = 'request' AND status_code >= 400 THEN 1 ELSE 0 END) AS api_errors,
                  SUM(CASE WHEN log_type = 'request' AND duration_ms >= :slow_request_threshold_ms THEN 1 ELSE 0 END) AS slow_requests,
                  SUM(CASE WHEN log_type = 'audit' THEN 1 ELSE 0 END) AS audit_operations
                FROM ({source}) logs
                {where}
                """
            ),
            {**params, "slow_request_threshold_ms": slow_request_threshold_ms},
        ).mappings().one()
        request_total = int(
            self._db.execute(
                text(f"SELECT COUNT(*) FROM ({source}) logs {where} AND log_type = 'request'" if where else f"SELECT COUNT(*) FROM ({source}) logs WHERE log_type = 'request'"),
                params,
            ).scalar_one()
            or 0
        )
        task_summary = self._task_summary(
            filters=filters,
            slow_task_threshold_ms=slow_task_threshold_ms,
        )
        return {
            "summary": {
                "total_logs": int(summary["total_logs"] or 0),
                "api_errors": int(summary["api_errors"] or 0),
                "api_error_rate": self._rate(int(summary["api_errors"] or 0), request_total),
                "slow_requests": int(summary["slow_requests"] or 0),
                "audit_operations": int(summary["audit_operations"] or 0),
                **task_summary,
            },
            "distributions": {
                "failure_reasons": self._distribution(
                    f"""
                    SELECT COALESCE(NULLIF(error_code, ''), CASE WHEN result = 'failed' THEN summary ELSE NULL END, 'unknown') AS label,
                           COUNT(*) AS count
                    FROM ({source}) logs
                    {where}
                    {'AND' if where else 'WHERE'} (result = 'failed' OR status_code >= 400)
                    GROUP BY label
                    ORDER BY count DESC
                    LIMIT :top_limit
                    """,
                    params,
                    top_limit,
                ),
                "clients": self._distribution(
                    f"""
                    SELECT COALESCE(NULLIF(client_type, ''), 'unknown') AS label, COUNT(*) AS count
                    FROM ({source}) logs
                    {where}
                    GROUP BY label
                    ORDER BY count DESC
                    LIMIT :top_limit
                    """,
                    params,
                    top_limit,
                ),
                "task_statuses": self._task_status_distribution(filters=filters, top_limit=top_limit),
                "behavior_events": self._distribution(
                    f"""
                    SELECT COALESCE(NULLIF(event_name, ''), 'unknown') AS label, COUNT(*) AS count
                    FROM ({source}) logs
                    {where}
                    {'AND' if where else 'WHERE'} log_type = 'usage_event'
                    GROUP BY label
                    ORDER BY count DESC
                    LIMIT :top_limit
                    """,
                    params,
                    top_limit,
                ),
            },
            "endpoint_errors": self._endpoint_errors(where, params, source, top_limit),
            "rankings": {
                "slow_requests": self._slow_requests(where, params, source, slow_request_threshold_ms, top_limit),
                "slow_tasks": self._slow_tasks(filters, slow_task_threshold_ms, top_limit),
                "slowest_spans": self._slowest_spans(filters, top_limit),
            },
            "trace_results": self._trace_results(filters, source),
        }

    def _task_summary(self, *, filters: dict[str, Any], slow_task_threshold_ms: int) -> dict[str, Any]:
        where, params = self._build_task_filters(prefix="t", **filters)
        row = self._db.execute(
            text(
                f"""
                SELECT
                  COUNT(*) AS task_count,
                  SUM(CASE WHEN t.status = 'success' THEN 1 ELSE 0 END) AS success_tasks,
                  SUM(CASE WHEN t.status != 'success' THEN 1 ELSE 0 END) AS failed_tasks,
                  SUM(CASE WHEN t.duration_ms >= :slow_task_threshold_ms THEN 1 ELSE 0 END) AS slow_tasks
                FROM task_traces t
                {where}
                """
            ),
            {**params, "slow_task_threshold_ms": slow_task_threshold_ms},
        ).mappings().one()
        task_count = int(row["task_count"] or 0)
        success_tasks = int(row["success_tasks"] or 0)
        return {
            "task_success_rate": self._rate(success_tasks, task_count) if task_count else None,
            "failed_tasks": int(row["failed_tasks"] or 0),
            "slow_tasks": int(row["slow_tasks"] or 0),
        }

    def _distribution(self, sql: str, params: dict[str, Any], top_limit: int) -> list[dict[str, Any]]:
        rows = self._db.execute(text(sql), {**params, "top_limit": top_limit}).mappings().all()
        total = sum(int(row["count"] or 0) for row in rows)
        return [
            {
                "label": str(row["label"] or "unknown"),
                "count": int(row["count"] or 0),
                "rate": self._rate(int(row["count"] or 0), total) if total else None,
            }
            for row in rows
        ]

    def _task_status_distribution(self, *, filters: dict[str, Any], top_limit: int) -> list[dict[str, Any]]:
        where, params = self._build_task_filters(prefix="t", **filters)
        return self._distribution(
            f"""
            SELECT COALESCE(NULLIF(t.status, ''), 'unknown') AS label, COUNT(*) AS count
            FROM task_traces t
            {where}
            GROUP BY label
            ORDER BY count DESC
            LIMIT :top_limit
            """,
            params,
            top_limit,
        )

    def _endpoint_errors(self, where: str, params: dict[str, Any], source: str, top_limit: int) -> list[dict[str, Any]]:
        rows = self._db.execute(
            text(
                f"""
                SELECT
                  COALESCE(NULLIF(path, ''), 'unknown') AS path,
                  COALESCE(NULLIF(method, ''), 'UNKNOWN') AS method,
                  status_code AS status_code,
                  COUNT(*) AS request_count,
                  SUM(CASE WHEN status_code >= 400 THEN 1 ELSE 0 END) AS error_count
                FROM ({source}) logs
                {where}
                {'AND' if where else 'WHERE'} log_type = 'request'
                GROUP BY path, method, status_code
                ORDER BY error_count DESC, request_count DESC
                LIMIT :top_limit
                """
            ),
            {**params, "top_limit": top_limit},
        ).mappings().all()
        return [
            {
                "path": str(row["path"]),
                "method": str(row["method"]),
                "status_code": int(row["status_code"]) if row["status_code"] is not None else None,
                "request_count": int(row["request_count"] or 0),
                "error_count": int(row["error_count"] or 0),
                "error_rate": self._rate(int(row["error_count"] or 0), int(row["request_count"] or 0)),
            }
            for row in rows
        ]

    def _slow_requests(
        self,
        where: str,
        params: dict[str, Any],
        source: str,
        slow_request_threshold_ms: int,
        top_limit: int,
    ) -> list[dict[str, Any]]:
        rows = self._db.execute(
            text(
                f"""
                SELECT id, path, method, status_code, duration_ms, client_type, request_id, behavior_trace_id
                FROM ({source}) logs
                {where}
                {'AND' if where else 'WHERE'} log_type = 'request' AND duration_ms >= :slow_request_threshold_ms
                ORDER BY duration_ms DESC, created_at DESC
                LIMIT :top_limit
                """
            ),
            {**params, "slow_request_threshold_ms": slow_request_threshold_ms, "top_limit": top_limit},
        ).mappings().all()
        return [
            {
                "log_id": str(row["id"]),
                "path": str(row["path"] or "-"),
                "method": str(row["method"] or "-"),
                "status_code": int(row["status_code"] or 0),
                "duration_ms": int(row["duration_ms"] or 0),
                "client_type": str(row["client_type"] or "unknown"),
                "request_id": row.get("request_id"),
                "behavior_trace_id": row.get("behavior_trace_id"),
            }
            for row in rows
        ]

    def _slow_tasks(self, filters: dict[str, Any], slow_task_threshold_ms: int, top_limit: int) -> list[dict[str, Any]]:
        where, params = self._build_task_filters(prefix="t", **filters)
        rows = self._db.execute(
            text(
                f"""
                SELECT task_trace_id, task_type, status, duration_ms, client_type, resource_type, error_code, summary
                FROM task_traces t
                {where}
                {'AND' if where else 'WHERE'} duration_ms >= :slow_task_threshold_ms
                ORDER BY duration_ms DESC, created_at DESC
                LIMIT :top_limit
                """
            ),
            {**params, "slow_task_threshold_ms": slow_task_threshold_ms, "top_limit": top_limit},
        ).mappings().all()
        return [
            {
                "task_trace_id": str(row["task_trace_id"]),
                "task_type": str(row["task_type"]),
                "status": str(row["status"]),
                "duration_ms": int(row["duration_ms"]) if row["duration_ms"] is not None else None,
                "client_type": row.get("client_type"),
                "trigger_source": row.get("resource_type"),
                "error_code": row.get("error_code"),
                "summary": str(row["summary"]),
            }
            for row in rows
        ]

    def _slowest_spans(self, filters: dict[str, Any], top_limit: int) -> list[dict[str, Any]]:
        where, params = self._build_task_filters(prefix="s", **filters)
        rows = self._db.execute(
            text(
                f"""
                SELECT task_trace_id, task_type, span_name, status, duration_ms, request_id, behavior_trace_id, error_code, summary
                FROM task_trace_spans s
                {where}
                {'AND' if where else 'WHERE'} duration_ms IS NOT NULL
                ORDER BY duration_ms DESC, created_at DESC
                LIMIT :top_limit
                """
            ),
            {**params, "top_limit": top_limit},
        ).mappings().all()
        return [
            {
                "task_trace_id": str(row["task_trace_id"]),
                "task_type": str(row["task_type"]),
                "span_name": str(row["span_name"]),
                "status": str(row["status"]),
                "duration_ms": int(row["duration_ms"]) if row["duration_ms"] is not None else None,
                "request_id": row.get("request_id"),
                "behavior_trace_id": row.get("behavior_trace_id"),
                "error_code": row.get("error_code"),
                "summary": str(row["summary"]),
            }
            for row in rows
        ]

    def _trace_results(self, filters: dict[str, Any], source: str) -> dict[str, Any]:
        request_id = (filters.get("request_id") or "").strip()
        task_trace_id = (filters.get("task_trace_id") or "").strip()
        if not request_id and not task_trace_id:
            behavior_trace_id = (filters.get("behavior_trace_id") or "").strip()
            if not behavior_trace_id:
                return {"behavior_trace_id": None, "request_id": None, "task_trace_id": None, "log_ids": [], "request_ids": [], "task_trace_ids": [], "reason": None}
        else:
            behavior_trace_id = (filters.get("behavior_trace_id") or "").strip()
        clauses: list[str] = []
        params: dict[str, Any] = {}
        if behavior_trace_id:
            clauses.append("behavior_trace_id = :behavior_trace_id")
            params["behavior_trace_id"] = behavior_trace_id
        if request_id:
            clauses.append("(request_id = :request_id OR client_request_id = :request_id)")
            params["request_id"] = request_id
        if task_trace_id:
            clauses.append("task_trace_id = :trace_task_trace_id")
            params["trace_task_trace_id"] = task_trace_id
        rows = self._db.execute(
            text(
                f"""
                SELECT id, request_id, task_trace_id
                FROM ({source}) logs
                WHERE {' OR '.join(clauses)}
                ORDER BY created_at DESC
                LIMIT 20
                """
            ),
            params,
        ).mappings().all()
        log_ids = [str(row["id"]) for row in rows]
        request_ids = sorted({str(row["request_id"]) for row in rows if row.get("request_id")})
        task_trace_ids = sorted({str(row["task_trace_id"]) for row in rows if row.get("task_trace_id")})
        if request_id:
            task_rows = self._db.execute(
                text(
                    """
                    SELECT task_trace_id
                    FROM task_traces
                    WHERE parent_request_id = :request_id
                    UNION
                    SELECT task_trace_id
                    FROM task_trace_spans
                    WHERE request_id = :request_id
                    LIMIT 20
                    """
                ),
                {"request_id": request_id},
            ).mappings().all()
            task_trace_ids = sorted(
                {task_trace_id for task_trace_id in task_trace_ids}
                | {str(row["task_trace_id"]) for row in task_rows if row.get("task_trace_id")}
            )
        if behavior_trace_id:
            task_rows = self._db.execute(
                text(
                    """
                    SELECT task_trace_id
                    FROM task_traces
                    WHERE behavior_trace_id = :behavior_trace_id
                    UNION
                    SELECT task_trace_id
                    FROM task_trace_spans
                    WHERE behavior_trace_id = :behavior_trace_id
                    LIMIT 20
                    """
                ),
                {"behavior_trace_id": behavior_trace_id},
            ).mappings().all()
            task_trace_ids = sorted(
                {task_trace_id for task_trace_id in task_trace_ids}
                | {str(row["task_trace_id"]) for row in task_rows if row.get("task_trace_id")}
            )
        return {
            "behavior_trace_id": behavior_trace_id or None,
            "request_id": request_id or None,
            "task_trace_id": task_trace_id or None,
            "log_ids": log_ids,
            "request_ids": request_ids,
            "task_trace_ids": task_trace_ids,
            "reason": None if log_ids or task_trace_ids else "not_found",
        }

    @classmethod
    def _build_observability_filters(cls, **filters: Any) -> tuple[str, dict[str, Any]]:
        where, params = cls._build_filters(
            log_type=filters.get("log_type"),
            client_type=filters.get("client_type"),
            status_code=filters.get("status_code"),
            result=filters.get("result"),
            path_or_request_id=filters.get("path_or_request_id"),
            behavior_trace_id=filters.get("behavior_trace_id"),
            task_trace_id=filters.get("task_trace_id"),
            start_time=filters.get("start_time"),
            end_time=filters.get("end_time"),
        )
        clauses: list[str] = []
        if where:
            clauses.append(where.removeprefix("WHERE ").strip())
        task_type = (filters.get("task_type") or "").strip()
        if task_type:
            clauses.append("task_type = :obs_task_type")
            params["obs_task_type"] = task_type
        request_id = (filters.get("request_id") or "").strip()
        if request_id:
            clauses.append("(request_id = :obs_request_id OR client_request_id = :obs_request_id)")
            params["obs_request_id"] = request_id
        behavior_trace_id = (filters.get("behavior_trace_id") or "").strip()
        if behavior_trace_id:
            clauses.append("behavior_trace_id = :obs_behavior_trace_id")
            params["obs_behavior_trace_id"] = behavior_trace_id
        return ("WHERE " + " AND ".join(clauses), params) if clauses else ("", params)

    @staticmethod
    def _build_task_filters(prefix: str, **filters: Any) -> tuple[str, dict[str, Any]]:
        column = lambda name: f"{prefix}.{name}"
        clauses: list[str] = []
        params: dict[str, Any] = {}
        for key in ("client_type", "task_type"):
            value = (filters.get(key) or "").strip()
            if value:
                clauses.append(f"{column(key)} = :task_{key}")
                params[f"task_{key}"] = value
        result = (filters.get("result") or "").strip()
        if result:
            clauses.append(f"{column('status')} = :task_result")
            params["task_result"] = "success" if result == "success" else "failed"
        task_trace_id = (filters.get("task_trace_id") or "").strip()
        if task_trace_id:
            clauses.append(f"{column('task_trace_id')} = :task_trace_id")
            params["task_trace_id"] = task_trace_id
        request_id = (filters.get("request_id") or "").strip()
        if request_id and prefix == "s":
            clauses.append(f"{column('request_id')} = :task_request_id")
            params["task_request_id"] = request_id
        if request_id and prefix == "t":
            clauses.append(f"{column('parent_request_id')} = :task_request_id")
            params["task_request_id"] = request_id
        behavior_trace_id = (filters.get("behavior_trace_id") or "").strip()
        if behavior_trace_id:
            clauses.append(f"{column('behavior_trace_id')} = :task_behavior_trace_id")
            params["task_behavior_trace_id"] = behavior_trace_id
        start_time = filters.get("start_time")
        if start_time:
            clauses.append(f"{column('created_at')} >= :task_start_time")
            params["task_start_time"] = start_time
        end_time = filters.get("end_time")
        if end_time:
            clauses.append(f"{column('created_at')} <= :task_end_time")
            params["task_end_time"] = end_time
        return ("WHERE " + " AND ".join(clauses), params) if clauses else ("", params)

    @staticmethod
    def _rate(numerator: int, denominator: int) -> float:
        if denominator <= 0:
            return 0.0
        return round(numerator / denominator, 4)

    @staticmethod
    def _build_filters(**filters: Any) -> tuple[str, dict[str, Any]]:
        clauses: list[str] = []
        params: dict[str, Any] = {}
        for key in ("log_type", "actor_user_id", "client_type", "status_code", "result"):
            value = filters.get(key)
            if value in (None, ""):
                continue
            clauses.append(f"{key} = :{key}")
            params[key] = value

        keyword = (filters.get("keyword") or "").strip()
        if keyword:
            clauses.append(
                """
                (
                  summary LIKE :keyword OR path LIKE :keyword OR event_name LIKE :keyword
                  OR request_id LIKE :keyword OR client_request_id LIKE :keyword OR actor_name LIKE :keyword
                )
                """
            )
            params["keyword"] = f"%{keyword}%"

        resource_id = (filters.get("resource_id") or "").strip()
        if resource_id:
            clauses.append("metadata LIKE :resource_id")
            params["resource_id"] = f"%{resource_id}%"

        path_or_request_id = (filters.get("path_or_request_id") or "").strip()
        if path_or_request_id:
            clauses.append(
                "(path LIKE :path_or_request_id OR request_id LIKE :path_or_request_id OR client_request_id LIKE :path_or_request_id OR behavior_trace_id LIKE :path_or_request_id OR parent_behavior_event_id LIKE :path_or_request_id OR task_trace_id LIKE :path_or_request_id)"
            )
            params["path_or_request_id"] = f"%{path_or_request_id}%"

        behavior_trace_id = (filters.get("behavior_trace_id") or "").strip()
        if behavior_trace_id:
            clauses.append("behavior_trace_id = :behavior_trace_id")
            params["behavior_trace_id"] = behavior_trace_id

        task_trace_id = (filters.get("task_trace_id") or "").strip()
        if task_trace_id:
            clauses.append("task_trace_id = :task_trace_id")
            params["task_trace_id"] = task_trace_id

        start_time = filters.get("start_time")
        if start_time:
            clauses.append("created_at >= :start_time")
            params["start_time"] = start_time

        end_time = filters.get("end_time")
        if end_time:
            clauses.append("created_at <= :end_time")
            params["end_time"] = end_time

        return ("WHERE " + " AND ".join(clauses), params) if clauses else ("", params)

    @classmethod
    def _list_source_sql(cls, **filters: Any) -> tuple[str, dict[str, Any]]:
        requested_type = (filters.get("log_type") or "").strip()
        source_types = [requested_type] if requested_type else ["request", "usage_event", "audit"]
        params: dict[str, Any] = {}
        sources = [
            cls._typed_source_sql(log_type=source_type, filters=filters, params=params)
            for source_type in source_types
        ]
        return "\nUNION ALL\n".join(source for source in sources if source), params

    @classmethod
    def _typed_source_sql(cls, *, log_type: str, filters: dict[str, Any], params: dict[str, Any]) -> str:
        if log_type == "request":
            where = cls._build_typed_filters(
                log_type="request",
                alias="r",
                filters=filters,
                params=params,
                column_map={
                    "actor_user_id": "actor_user_id",
                    "client_type": "client_type",
                    "status_code": "status_code",
                    "result": "result",
                    "created_at": "created_at",
                    "behavior_trace_id": "behavior_trace_id",
                    "task_trace_id": "task_trace_id",
                    "metadata": "metadata",
                },
            )
            return f"""
            SELECT
              r.id AS id,
              'request' AS log_type,
              r.request_id AS request_id,
              r.actor_user_id AS actor_user_id,
              r.actor_role AS actor_role,
              COALESCE(u.display_name, u.username) AS actor_name,
              u.username AS actor_username,
              r.client_type AS client_type,
              r.client_request_id AS client_request_id,
              r.behavior_trace_id AS behavior_trace_id,
              r.parent_behavior_event_id AS parent_behavior_event_id,
              NULL AS event_name,
              r.method AS method,
              r.path AS path,
              r.status_code AS status_code,
              r.duration_ms AS duration_ms,
              r.ip_address_masked AS ip_address_masked,
              r.user_agent_summary AS user_agent_summary,
              r.summary AS summary,
              r.error_code AS error_code,
              r.result AS result,
              r.task_trace_id AS task_trace_id,
              COALESCE(t.task_type, r.task_type) AS task_type,
              t.status AS task_status,
              t.duration_ms AS task_duration_ms,
              t.slowest_span_name AS task_slowest_span_name,
              r.metadata AS metadata,
              r.created_at AS created_at
            FROM request_logs r
            LEFT JOIN users u ON u.id = r.actor_user_id
            LEFT JOIN task_traces t ON t.task_trace_id = r.task_trace_id
            {where}
            """
        if log_type == "usage_event":
            where = cls._build_typed_filters(
                log_type="usage_event",
                alias="e",
                filters=filters,
                params=params,
                column_map={
                    "actor_user_id": "actor_user_id",
                    "client_type": "client_type",
                    "result": "result",
                    "created_at": "created_at",
                    "behavior_trace_id": "behavior_trace_id",
                    "task_trace_id": "task_trace_id",
                    "metadata": "metadata",
                },
            )
            return f"""
            SELECT
              e.id AS id,
              'usage_event' AS log_type,
              e.request_id AS request_id,
              e.actor_user_id AS actor_user_id,
              e.actor_role AS actor_role,
              COALESCE(u.display_name, u.username) AS actor_name,
              u.username AS actor_username,
              e.client_type AS client_type,
              NULL AS client_request_id,
              e.behavior_trace_id AS behavior_trace_id,
              e.behavior_event_id AS parent_behavior_event_id,
              e.event_name AS event_name,
              NULL AS method,
              e.page_path AS path,
              NULL AS status_code,
              e.duration_ms AS duration_ms,
              e.ip_address_masked AS ip_address_masked,
              e.user_agent_summary AS user_agent_summary,
              e.summary AS summary,
              NULL AS error_code,
              e.result AS result,
              e.task_trace_id AS task_trace_id,
              COALESCE(t.task_type, e.task_type) AS task_type,
              t.status AS task_status,
              t.duration_ms AS task_duration_ms,
              t.slowest_span_name AS task_slowest_span_name,
              e.metadata AS metadata,
              e.created_at AS created_at
            FROM usage_events e
            LEFT JOIN users u ON u.id = e.actor_user_id
            LEFT JOIN task_traces t ON t.task_trace_id = e.task_trace_id
            {where}
            """
        if log_type == "audit":
            where = cls._build_typed_filters(
                log_type="audit",
                alias="a",
                filters=filters,
                params=params,
                column_map={
                    "actor_user_id": "actor_user_id",
                    "created_at": "created_at",
                    "task_trace_id": "task_trace_id",
                    "metadata": "metadata",
                },
            )
            return f"""
            SELECT
              a.id AS id,
              'audit' AS log_type,
              NULL AS request_id,
              a.actor_user_id AS actor_user_id,
              NULL AS actor_role,
              COALESCE(u.display_name, u.username) AS actor_name,
              u.username AS actor_username,
              'backend' AS client_type,
              NULL AS client_request_id,
              NULL AS behavior_trace_id,
              NULL AS parent_behavior_event_id,
              a.action_type AS event_name,
              NULL AS method,
              a.domain AS path,
              NULL AS status_code,
              NULL AS duration_ms,
              NULL AS ip_address_masked,
              NULL AS user_agent_summary,
              a.summary AS summary,
              NULL AS error_code,
              'success' AS result,
              a.task_trace_id AS task_trace_id,
              COALESCE(t.task_type, a.task_type) AS task_type,
              t.status AS task_status,
              t.duration_ms AS task_duration_ms,
              t.slowest_span_name AS task_slowest_span_name,
              a.metadata AS metadata,
              a.created_at AS created_at
            FROM audit_logs a
            LEFT JOIN users u ON u.id = a.actor_user_id
            LEFT JOIN task_traces t ON t.task_trace_id = a.task_trace_id
            {where}
            """
        return ""

    @staticmethod
    def _build_typed_filters(
        *,
        log_type: str,
        alias: str,
        filters: dict[str, Any],
        params: dict[str, Any],
        column_map: dict[str, str],
    ) -> str:
        def column(name: str) -> str:
            return f"{alias}.{column_map[name]}"

        clauses: list[str] = []
        for key in ("actor_user_id", "client_type", "status_code", "result"):
            value = filters.get(key)
            if value in (None, ""):
                continue
            if key == "client_type" and log_type == "audit":
                clauses.append("1 = 1" if value == "backend" else "1 = 0")
                continue
            if key == "status_code" and log_type != "request":
                clauses.append("1 = 0")
                continue
            if key == "result" and log_type == "audit":
                clauses.append("1 = 1" if value == "success" else "1 = 0")
                continue
            if key not in column_map:
                continue
            clauses.append(f"{column(key)} = :{key}")
            params[key] = value

        keyword = (filters.get("keyword") or "").strip()
        if keyword:
            params["keyword"] = f"%{keyword}%"
            if log_type == "request":
                clauses.append(
                    "(r.summary LIKE :keyword OR r.path LIKE :keyword OR r.request_id LIKE :keyword OR r.client_request_id LIKE :keyword OR COALESCE(u.display_name, u.username) LIKE :keyword)"
                )
            elif log_type == "usage_event":
                clauses.append(
                    "(e.summary LIKE :keyword OR e.page_path LIKE :keyword OR e.event_name LIKE :keyword OR e.request_id LIKE :keyword OR COALESCE(u.display_name, u.username) LIKE :keyword)"
                )
            else:
                clauses.append(
                    "(a.summary LIKE :keyword OR a.domain LIKE :keyword OR a.action_type LIKE :keyword OR COALESCE(u.display_name, u.username) LIKE :keyword)"
                )

        resource_id = (filters.get("resource_id") or "").strip()
        if resource_id:
            clauses.append(f"{column('metadata')} LIKE :resource_id")
            params["resource_id"] = f"%{resource_id}%"

        path_or_request_id = (filters.get("path_or_request_id") or "").strip()
        if path_or_request_id:
            params["path_or_request_id"] = f"%{path_or_request_id}%"
            if log_type == "request":
                clauses.append(
                    "(r.path LIKE :path_or_request_id OR r.request_id LIKE :path_or_request_id OR r.client_request_id LIKE :path_or_request_id OR r.behavior_trace_id LIKE :path_or_request_id OR r.parent_behavior_event_id LIKE :path_or_request_id OR r.task_trace_id LIKE :path_or_request_id)"
                )
            elif log_type == "usage_event":
                clauses.append("(e.page_path LIKE :path_or_request_id OR e.request_id LIKE :path_or_request_id OR e.behavior_trace_id LIKE :path_or_request_id OR e.behavior_event_id LIKE :path_or_request_id OR e.task_trace_id LIKE :path_or_request_id)")
            else:
                clauses.append("(a.domain LIKE :path_or_request_id OR a.task_trace_id LIKE :path_or_request_id)")

        behavior_trace_id = (filters.get("behavior_trace_id") or "").strip()
        if behavior_trace_id:
            if "behavior_trace_id" in column_map:
                clauses.append(f"{column('behavior_trace_id')} = :behavior_trace_id")
                params["behavior_trace_id"] = behavior_trace_id
            else:
                clauses.append("1 = 0")

        task_trace_id = (filters.get("task_trace_id") or "").strip()
        if task_trace_id:
            clauses.append(f"{column('task_trace_id')} = :task_trace_id")
            params["task_trace_id"] = task_trace_id

        start_time = filters.get("start_time")
        if start_time:
            clauses.append(f"{column('created_at')} >= :start_time")
            params["start_time"] = start_time

        end_time = filters.get("end_time")
        if end_time:
            clauses.append(f"{column('created_at')} <= :end_time")
            params["end_time"] = end_time

        return "WHERE " + " AND ".join(clauses) if clauses else ""

    @staticmethod
    def _union_source_sql() -> str:
        return """
            SELECT
              r.id AS id,
              'request' AS log_type,
              r.request_id AS request_id,
              r.actor_user_id AS actor_user_id,
              r.actor_role AS actor_role,
              COALESCE(u.display_name, u.username) AS actor_name,
              u.username AS actor_username,
              r.client_type AS client_type,
              r.client_request_id AS client_request_id,
              r.behavior_trace_id AS behavior_trace_id,
              r.parent_behavior_event_id AS parent_behavior_event_id,
              NULL AS event_name,
              r.method AS method,
              r.path AS path,
              r.status_code AS status_code,
              r.duration_ms AS duration_ms,
              r.ip_address_masked AS ip_address_masked,
              r.user_agent_summary AS user_agent_summary,
              r.summary AS summary,
              r.error_code AS error_code,
              r.result AS result,
              r.task_trace_id AS task_trace_id,
              COALESCE(t.task_type, r.task_type) AS task_type,
              t.status AS task_status,
              t.duration_ms AS task_duration_ms,
              t.slowest_span_name AS task_slowest_span_name,
              r.metadata AS metadata,
              r.created_at AS created_at
            FROM request_logs r
            LEFT JOIN users u ON u.id = r.actor_user_id
            LEFT JOIN task_traces t ON t.task_trace_id = r.task_trace_id
            UNION ALL
            SELECT
              e.id AS id,
              'usage_event' AS log_type,
              e.request_id AS request_id,
              e.actor_user_id AS actor_user_id,
              e.actor_role AS actor_role,
              COALESCE(u.display_name, u.username) AS actor_name,
              u.username AS actor_username,
              e.client_type AS client_type,
              NULL AS client_request_id,
              e.behavior_trace_id AS behavior_trace_id,
              e.behavior_event_id AS parent_behavior_event_id,
              e.event_name AS event_name,
              NULL AS method,
              e.page_path AS path,
              NULL AS status_code,
              e.duration_ms AS duration_ms,
              e.ip_address_masked AS ip_address_masked,
              e.user_agent_summary AS user_agent_summary,
              e.summary AS summary,
              NULL AS error_code,
              e.result AS result,
              e.task_trace_id AS task_trace_id,
              COALESCE(t.task_type, e.task_type) AS task_type,
              t.status AS task_status,
              t.duration_ms AS task_duration_ms,
              t.slowest_span_name AS task_slowest_span_name,
              e.metadata AS metadata,
              e.created_at AS created_at
            FROM usage_events e
            LEFT JOIN users u ON u.id = e.actor_user_id
            LEFT JOIN task_traces t ON t.task_trace_id = e.task_trace_id
            UNION ALL
            SELECT
              a.id AS id,
              'audit' AS log_type,
              NULL AS request_id,
              a.actor_user_id AS actor_user_id,
              NULL AS actor_role,
              COALESCE(u.display_name, u.username) AS actor_name,
              u.username AS actor_username,
              'backend' AS client_type,
              NULL AS client_request_id,
              NULL AS behavior_trace_id,
              NULL AS parent_behavior_event_id,
              a.action_type AS event_name,
              NULL AS method,
              a.domain AS path,
              NULL AS status_code,
              NULL AS duration_ms,
              NULL AS ip_address_masked,
              NULL AS user_agent_summary,
              a.summary AS summary,
              NULL AS error_code,
              'success' AS result,
              a.task_trace_id AS task_trace_id,
              COALESCE(t.task_type, a.task_type) AS task_type,
              t.status AS task_status,
              t.duration_ms AS task_duration_ms,
              t.slowest_span_name AS task_slowest_span_name,
              a.metadata AS metadata,
              a.created_at AS created_at
            FROM audit_logs a
            LEFT JOIN users u ON u.id = a.actor_user_id
            LEFT JOIN task_traces t ON t.task_trace_id = a.task_trace_id
        """

    @staticmethod
    def _to_record(row: dict[str, Any]) -> LogRecord:
        return LogRecord(
            id=str(row["id"]),
            log_type=str(row["log_type"]),
            request_id=row.get("request_id"),
            actor_user_id=row.get("actor_user_id"),
            actor_role=row.get("actor_role"),
            actor_name=row.get("actor_name"),
            actor_username=row.get("actor_username"),
            client_type=row.get("client_type"),
            client_request_id=row.get("client_request_id"),
            behavior_trace_id=row.get("behavior_trace_id"),
            parent_behavior_event_id=row.get("parent_behavior_event_id"),
            event_name=row.get("event_name"),
            method=row.get("method"),
            path=row.get("path"),
            status_code=int(row["status_code"]) if row.get("status_code") is not None else None,
            duration_ms=int(row["duration_ms"]) if row.get("duration_ms") is not None else None,
            ip_address_masked=row.get("ip_address_masked"),
            user_agent_summary=row.get("user_agent_summary"),
            summary=str(row["summary"]),
            error_code=row.get("error_code"),
            result=str(row["result"]),
            task_trace_id=row.get("task_trace_id"),
            task_type=row.get("task_type"),
            task_status=row.get("task_status"),
            task_duration_ms=int(row["task_duration_ms"]) if row.get("task_duration_ms") is not None else None,
            task_slowest_span_name=row.get("task_slowest_span_name"),
            metadata=row.get("metadata"),
            created_at=str(row["created_at"]),
        )
