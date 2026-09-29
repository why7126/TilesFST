"""Single-job durable image worker. Run one instance with the documented resource cap."""
from __future__ import annotations

import argparse
import json
import os
import signal
import subprocess
import sys
import time
from datetime import datetime, timezone

from sqlalchemy import select

from app.db.session import get_session_factory
from app.modules.media.upload_sessions import UploadSessionRepository, UploadSessionConflict, upload_sessions, utc_timestamp

RETRY_DELAYS = (5, 15, 45)


def _limits():
    import resource
    resource.setrlimit(resource.RLIMIT_CPU, (120, 120))
    if sys.platform.startswith('linux'):
        resource.setrlimit(resource.RLIMIT_AS, (512 * 1024 * 1024, 512 * 1024 * 1024))


def run_isolated(job, pulse, *, timeout=120, command=None):
    process = subprocess.Popen(command or [sys.executable, '-m', 'app.modules.media.image_processing'],
        stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL,
        text=True, start_new_session=True, preexec_fn=_limits)
    started = time.monotonic()
    try:
        payload = json.dumps(job)
        while True:
            try:
                output, _ = process.communicate(input=payload, timeout=min(1, timeout))
                break
            except subprocess.TimeoutExpired:
                payload = None
                pulse()
                if time.monotonic() - started >= timeout:
                    return {'ok': False, 'reason': 'processing_timeout', 'retryable': False}
        if process.returncode != 0:
            return {'ok': False, 'reason': 'process_resource_or_exit', 'retryable': False}
        if len(output) > 65536:
            return {'ok': False, 'reason': 'invalid_worker_result', 'retryable': False}
        result = json.loads(output)
        if not isinstance(result, dict) or not isinstance(result.get('ok'), bool):
            raise ValueError('Invalid worker result')
        return result
    finally:
        if process.poll() is None:
            os.killpg(process.pid, signal.SIGKILL)
        process.communicate()


def record_processing_result(db, row, result, attempt):
    """Separate telemetry transaction; include metrics only, never keys or SDK output."""
    try:
        from sqlalchemy.orm import Session
        from app.repositories.task_trace_repository import TaskTraceRepository
        from app.services.task_trace_service import TaskTraceService
        with Session(db.get_bind()) as trace_db:
            repository = TaskTraceRepository(trace_db)
            existing = repository.get_trace(row['task_trace_id'])
            trace = TaskTraceService(repository)
            context = trace.build_context(task_type='media_direct_upload', task_trace_id=row['task_trace_id'],
                actor_user_id=row['owner_id'], client_type='web_admin',
                request_id=existing.parent_request_id if existing else None,
                behavior_trace_id=existing.behavior_trace_id if existing else None)
            spans = [('source_download', result.get('download_ms'))] if result.get('ok') else [('image_processing', None)]
            for name, value in result.get('outputs', {}).items():
                if name in {'thumbnail', 'display'}:
                    spans.extend([(name + '_generate', value.get('duration_ms')), (name + '_put', value.get('put_ms'))])
            for sequence, (name, duration) in enumerate(spans):
                trace.record_context_span_safe(context, span_name=name, sequence=sequence,
                    status='success' if result.get('ok') else 'failed',
                    duration_ms=round(duration) if duration is not None else None,
                    error_code=None if result.get('ok') else '30084',
                    metadata={'mode': 'cos_direct', 'processing_location': 'backend', 'attempt': attempt, 'source':'backend', 'duration_scope':'processing_component'})
    except Exception:
        pass


def process_session(db, row, *, runner=run_isolated, clock=None):
    now = clock or (lambda: datetime.now(timezone.utc))
    repo = UploadSessionRepository(db)
    row = repo.claim(row, 'processing', now=now()); db.commit()
    metadata = json.loads(row['variants_json'] or '{}')
    attempt = int(metadata.get('attempt', 0)) + 1
    output_keys = {name: row['stable_key'] + '.processing/' + row['lease_token'] + '/' + name + '.webp'
                   for name in ('thumbnail', 'display')}
    # Record possible side effects before launching. A killed worker may have uploaded one output.
    planned = list(metadata.get('planned_keys', [])) + list(output_keys.values())
    metadata.update(attempt=attempt, planned_keys=planned)
    row = repo.checkpoint(row, now=now(), variants_json=json.dumps(metadata)); db.commit()
    last_heartbeat = time.monotonic()

    def pulse():
        nonlocal row, last_heartbeat
        current = repo.get(row['id'], row['owner_id']); db.rollback()
        if current['version'] != row['version'] or current['lease_token'] != row['lease_token']:
            raise UploadSessionConflict('Image operation lost its lease')
        if time.monotonic() - last_heartbeat >= 30:
            row = repo.heartbeat(row, now=now()); db.commit()
            last_heartbeat = time.monotonic()

    job = {k: row[k] for k in ('stable_key', 'stable_version_id', 'expected_size', 'mime_type')}
    job.update(output_keys=output_keys, thumbnail_target_kib=int(metadata.get('thumbnail_target_kib', 0)),
               display_target_kib=int(metadata.get('display_target_kib', 768)))
    try:
        result = runner(job, pulse)
        pulse()
        if result['ok']:
            outputs = result['outputs']
            if set(outputs) != set(output_keys) or any(
                outputs[name]['key'] != key or not outputs[name].get('version_id')
                or outputs[name].get('mime_type') != 'image/webp'
                for name, key in output_keys.items()
            ):
                raise ValueError('Invalid derivative manifest')
            metadata.update(outputs=outputs, download_ms=result.get('download_ms'), failure=None)
            row = repo.finish(row, 'ready', now=now(), variants_json=json.dumps(metadata), error_code=None)
        else:
            metadata.update(failure=result['reason'])
            if result.get('retryable') and attempt <= len(RETRY_DELAYS):
                row = repo.queue_processing(row, now=now(), metadata=metadata, delay_seconds=RETRY_DELAYS[attempt - 1])
            else:
                row = repo.finish(row, 'failed', now=now(), variants_json=json.dumps(metadata), error_code='30084')
        db.commit()
        record_processing_result(db, row, result, attempt)
        return row['state']
    except UploadSessionConflict:
        db.rollback()
        return 'superseded'
    except Exception:
        db.rollback()
        try:
            metadata.update(failure='worker_failed')
            repo.finish(row, 'failed', now=now(), variants_json=json.dumps(metadata), error_code='30084'); db.commit()
        except UploadSessionConflict:
            db.rollback()
        return 'failed'


def run_once():
    with get_session_factory()() as db:
        stamp = utc_timestamp(datetime.now(timezone.utc))
        row = db.execute(select(upload_sessions).where(
            upload_sessions.c.state == 'processing', upload_sessions.c.lease_expires_at <= stamp,
            upload_sessions.c.expires_at > stamp,
        ).order_by(upload_sessions.c.updated_at).limit(1)).mappings().first()
        db.rollback()
        if not row:
            return 'idle'
        try:
            return process_session(db, dict(row))
        except UploadSessionConflict:
            return 'superseded'


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='单任务图片派生工作者')
    parser.add_argument('--once', action='store_true')
    args = parser.parse_args()
    while True:
        state = run_once()
        print(json.dumps({'state': state}), flush=True)
        if args.once:
            break
        if state == 'idle':
            time.sleep(2)
