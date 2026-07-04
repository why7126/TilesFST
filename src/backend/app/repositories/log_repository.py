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
    client_type: str | None
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
        method: str,
        path: str,
        status_code: int,
        duration_ms: int,
        ip_address_masked: str | None,
        user_agent_summary: str | None,
        summary: str,
        error_code: str | None = None,
        result: str = "success",
        metadata: str | None = None,
    ) -> str:
        log_id = str(uuid4())
        self._db.execute(
            text(
                """
                INSERT INTO request_logs (
                  id, request_id, actor_user_id, actor_role, client_type,
                  method, path, status_code, duration_ms, ip_address_masked,
                  user_agent_summary, summary, error_code, result, metadata, created_at
                ) VALUES (
                  :id, :request_id, :actor_user_id, :actor_role, :client_type,
                  :method, :path, :status_code, :duration_ms, :ip_address_masked,
                  :user_agent_summary, :summary, :error_code, :result, :metadata, :created_at
                )
                """
            ),
            {
                "id": log_id,
                "request_id": request_id,
                "actor_user_id": actor_user_id,
                "actor_role": actor_role,
                "client_type": client_type,
                "method": method,
                "path": path,
                "status_code": status_code,
                "duration_ms": duration_ms,
                "ip_address_masked": ip_address_masked,
                "user_agent_summary": user_agent_summary,
                "summary": summary,
                "error_code": error_code,
                "result": result,
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
        event_name: str,
        event_category: str,
        page_path: str | None,
        session_id: str | None,
        ip_address_masked: str | None,
        user_agent_summary: str | None,
        summary: str,
        duration_ms: int | None,
        result: str,
        metadata: str | None,
    ) -> str:
        event_id = str(uuid4())
        self._db.execute(
            text(
                """
                INSERT INTO usage_events (
                  id, request_id, actor_user_id, actor_role, client_type,
                  event_name, event_category, page_path, session_id,
                  ip_address_masked, user_agent_summary, summary, duration_ms, result, metadata, created_at
                ) VALUES (
                  :id, :request_id, :actor_user_id, :actor_role, :client_type,
                  :event_name, :event_category, :page_path, :session_id,
                  :ip_address_masked, :user_agent_summary, :summary, :duration_ms, :result, :metadata, :created_at
                )
                """
            ),
            {
                "id": event_id,
                "request_id": request_id,
                "actor_user_id": actor_user_id,
                "actor_role": actor_role,
                "client_type": client_type,
                "event_name": event_name,
                "event_category": event_category,
                "page_path": page_path,
                "session_id": session_id,
                "ip_address_masked": ip_address_masked,
                "user_agent_summary": user_agent_summary,
                "summary": summary,
                "duration_ms": duration_ms,
                "result": result,
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
        start_time: str | None = None,
        end_time: str | None = None,
    ) -> LogQueryResult:
        where, params = self._build_filters(
            log_type=log_type,
            keyword=keyword,
            actor_user_id=actor_user_id,
            client_type=client_type,
            status_code=status_code,
            result=result,
            resource_id=resource_id,
            path_or_request_id=path_or_request_id,
            start_time=start_time,
            end_time=end_time,
        )
        params["limit"] = page_size
        params["offset"] = (page - 1) * page_size
        source = self._union_source_sql()
        total = int(
            self._db.execute(
                text(f"SELECT COUNT(*) FROM ({source}) logs {where}"),
                params,
            ).scalar_one()
            or 0
        )
        rows = (
            self._db.execute(
                text(
                    f"""
                    SELECT * FROM ({source}) logs
                    {where}
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
        source = self._union_source_sql()
        row = (
            self._db.execute(
                text(
                    f"""
                    SELECT
                      SUM(CASE WHEN created_at >= :today_start THEN 1 ELSE 0 END) AS today_logs,
                      SUM(CASE WHEN log_type = 'request' AND status_code >= 400 THEN 1 ELSE 0 END) AS api_errors,
                      SUM(CASE WHEN log_type = 'request' AND duration_ms >= :slow_threshold_ms THEN 1 ELSE 0 END) AS slow_requests,
                      SUM(CASE WHEN log_type = 'audit' AND created_at >= :today_start THEN 1 ELSE 0 END) AS sensitive_ops
                    FROM ({source}) logs
                    """
                ),
                {"today_start": today_start, "slow_threshold_ms": slow_threshold_ms},
            )
            .mappings()
            .one()
        )
        return LogMetrics(
            today_logs=int(row["today_logs"] or 0),
            api_errors=int(row["api_errors"] or 0),
            slow_requests=int(row["slow_requests"] or 0),
            sensitive_ops=int(row["sensitive_ops"] or 0),
        )

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
                  OR request_id LIKE :keyword OR actor_name LIKE :keyword
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
            clauses.append("(path LIKE :path_or_request_id OR request_id LIKE :path_or_request_id)")
            params["path_or_request_id"] = f"%{path_or_request_id}%"

        start_time = filters.get("start_time")
        if start_time:
            clauses.append("created_at >= :start_time")
            params["start_time"] = start_time

        end_time = filters.get("end_time")
        if end_time:
            clauses.append("created_at <= :end_time")
            params["end_time"] = end_time

        return ("WHERE " + " AND ".join(clauses), params) if clauses else ("", params)

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
              r.client_type AS client_type,
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
              r.metadata AS metadata,
              r.created_at AS created_at
            FROM request_logs r
            LEFT JOIN users u ON u.id = r.actor_user_id
            UNION ALL
            SELECT
              e.id AS id,
              'usage_event' AS log_type,
              e.request_id AS request_id,
              e.actor_user_id AS actor_user_id,
              e.actor_role AS actor_role,
              COALESCE(u.display_name, u.username) AS actor_name,
              e.client_type AS client_type,
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
              e.metadata AS metadata,
              e.created_at AS created_at
            FROM usage_events e
            LEFT JOIN users u ON u.id = e.actor_user_id
            UNION ALL
            SELECT
              a.id AS id,
              'audit' AS log_type,
              NULL AS request_id,
              a.actor_user_id AS actor_user_id,
              NULL AS actor_role,
              COALESCE(u.display_name, u.username) AS actor_name,
              'backend' AS client_type,
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
              a.metadata AS metadata,
              a.created_at AS created_at
            FROM audit_logs a
            LEFT JOIN users u ON u.id = a.actor_user_id
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
            client_type=row.get("client_type"),
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
            metadata=row.get("metadata"),
            created_at=str(row["created_at"]),
        )
