"""Safe, independent telemetry for a verified upload session."""
from sqlalchemy.orm import Session

from app.repositories.task_trace_repository import TaskTraceRepository
from app.services.task_trace_service import TaskTraceService


def record_upload_span(db, row, name, *, duration_ms=None, status='success', error_code=None, metadata=None):
    """Accept metrics from code, never raw storage exceptions, object names or credentials."""
    try:
        with Session(db.get_bind()) as trace_db:
            repository = TaskTraceRepository(trace_db)
            existing = repository.get_trace(row['task_trace_id'])
            service = TaskTraceService(repository)
            context = service.build_context(task_type='media_direct_upload', task_trace_id=row['task_trace_id'],
                actor_user_id=row['owner_id'], client_type='web_admin',
                request_id=existing.parent_request_id if existing else None,
                behavior_trace_id=existing.behavior_trace_id if existing else None)
            safe = {'source':'backend', 'mode':'cos_direct', 'media_kind':row['media_kind']}
            for key in ('duration_scope','deleted_versions','aborted_uploads','file_size_bytes'):
                if metadata and key in metadata:
                    safe[key] = metadata[key]
            service.record_context_span_safe(context, span_name=name, duration_ms=duration_ms,
                status=status, error_code=error_code, metadata=safe)
    except Exception:
        pass


def prune_upload_observability(db, *, now=None, apply=False, limit=500):
    """Bounded retention for this task type only; audit logs and other tasks are untouched."""
    from datetime import datetime, timedelta, timezone
    from sqlalchemy import bindparam, text
    now = now or datetime.now(timezone.utc)
    counts = {}
    for table, days, timestamp in (
        ('task_trace_spans', 90, 'created_at'),
        ('task_traces', 90, 'updated_at'),
        ('request_logs', 90, 'created_at'),
        ('usage_events', 180, 'created_at'),
    ):
        cutoff = (now-timedelta(days=days)).isoformat()
        ids = list(db.execute(text(f'SELECT id FROM {table} WHERE task_type=:kind AND {timestamp}<:cutoff ORDER BY {timestamp} LIMIT :limit'),
            {'kind':'media_direct_upload', 'cutoff':cutoff, 'limit':limit}).scalars())
        counts[table] = len(ids)
        if apply and ids:
            db.execute(text(f'DELETE FROM {table} WHERE id IN :ids AND task_type=:kind AND {timestamp}<:cutoff')
                .bindparams(bindparam('ids', expanding=True)), {'ids':ids, 'kind':'media_direct_upload', 'cutoff':cutoff})
    if apply:
        db.commit()
    else:
        db.rollback()
    return counts
