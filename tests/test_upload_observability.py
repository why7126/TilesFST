"""Real ingestion contract, isolated retention boundaries and telemetry failure isolation."""
from datetime import datetime, timedelta, timezone
from unittest.mock import Mock

from sqlalchemy import text

from app.db.session import get_session_factory
from app.modules.media.upload_observability import record_upload_span, prune_upload_observability


def test_client_upload_event_contract_and_sensitive_field_rejection(api_client):
    payload = {'event_name':'media_upload','task_type':'media_direct_upload',
        'task_trace_id':'task_upload_observability_test','client_type':'web_admin','page_path':'/admin/tiles',
        'duration_ms':123,'properties':{'media_type':'image','business_type':'sku_image','file_size':123,
        'result':'success','action':'stage','stage':'transferring','source':'browser',
        'duration_scope':'client_stage_wall_time'}}
    response=api_client.post('/api/v1/usage-events',json=payload)
    assert response.status_code == 200 and response.json()['data']['accepted'], response.text
    with get_session_factory()() as db:
        row=db.execute(text('SELECT task_trace_id,metadata FROM usage_events WHERE id=:id'),
            {'id':response.json()['data']['id']}).mappings().one()
        assert row['task_trace_id']==payload['task_trace_id'] and 'browser' in row['metadata']
    payload['properties']['raw_filename']='private.png'
    assert api_client.post('/api/v1/usage-events',json=payload).status_code==400


def test_upload_retention_is_bounded_dry_run_and_preserves_other_tasks(api_client):
    now=datetime.now(timezone.utc)
    with get_session_factory()() as db:
        for ident, kind, days in [('expired','media_direct_upload',181),('recent','media_direct_upload',1),('other','other_task',181)]:
            row={'task_trace_id':'task_upload_retention_'+ident,'owner_id':None,'media_kind':'sku_image'}
            record_upload_span(db,row,'binding',duration_ms=3)
            stamp=(now-timedelta(days=days)).isoformat()
            for table in ['task_traces','task_trace_spans']:
                db.execute(text(f'UPDATE {table} SET task_type=:kind,created_at=:stamp'+(',updated_at=:stamp' if table=='task_traces' else '')+' WHERE task_trace_id=:id'),
                    {'kind':kind,'stamp':stamp,'id':row['task_trace_id']})
            db.commit()
        dry=prune_upload_observability(db,now=now)
        assert dry['task_traces']==1 and dry['task_trace_spans']==1
        assert db.execute(text("SELECT COUNT(*) FROM task_traces WHERE task_trace_id='task_upload_retention_expired'")).scalar()==1
        db.rollback()
        result=prune_upload_observability(db,now=now,apply=True)
        assert result['task_traces']==1
        remaining=set(db.execute(text('SELECT task_trace_id FROM task_traces')).scalars())
        assert {'task_upload_retention_recent','task_upload_retention_other'} <= remaining and 'task_upload_retention_expired' not in remaining
        assert not db.execute(text("SELECT id FROM task_trace_spans WHERE task_trace_id='task_upload_retention_expired'")).first()


def test_telemetry_failure_and_raw_metadata_cannot_escape():
    db=Mock(); db.get_bind.side_effect=RuntimeError('sdk-sensitive-text')
    record_upload_span(db, {'task_trace_id':'tt:test','owner_id':None,'media_kind':'sku_image'},
        'binding',metadata={'object_key':'private','url':'https://cos.invalid/?signature=secret'})


def test_usage_events_keep_180_days_and_ignore_other_task_types(api_client):
    now=datetime.now(timezone.utc)
    ids=[]
    for days,kind in [(181,'media_direct_upload'),(100,'media_direct_upload'),(181,'other_task')]:
        response=api_client.post('/api/v1/usage-events',json={'event_name':'media_upload','task_type':kind,
            'properties':{'media_type':'image','business_type':'sku_image','file_size':123,'result':'success'}})
        assert response.status_code==200
        ident=response.json()['data']['id']; ids.append(ident)
        with get_session_factory()() as db:
            db.execute(text('UPDATE usage_events SET created_at=:stamp WHERE id=:id'),
                {'stamp':(now-timedelta(days=days)).isoformat(),'id':ident}); db.commit()
    with get_session_factory()() as db:
        result=prune_upload_observability(db,now=now,apply=True)
        assert result['usage_events']==1
        remaining=set(db.execute(text('SELECT id FROM usage_events')).scalars())
        assert ids[0] not in remaining and set(ids[1:]) <= remaining
