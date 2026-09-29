from datetime import datetime, timedelta, timezone
from concurrent.futures import ThreadPoolExecutor
import threading
import os

import pytest
from sqlalchemy import create_engine, inspect, select
from sqlalchemy.orm import Session

from app.modules.media.upload_sessions import (
    UploadSessionRepository, UploadSessionConflict, UploadSessionNotFound,
    ensure_upload_sessions, upload_sessions,
)

NOW = datetime(2026, 9, 8, tzinfo=timezone.utc)


@pytest.fixture
def engine(tmp_path):
    url = os.environ.get('REQ135_TEST_DATABASE_URL') or 'sqlite:///' + str(tmp_path / 'uploads.db')
    engine = create_engine(url, connect_args={'check_same_thread': False} if url.startswith('sqlite') else {})
    if os.environ.get('REQ135_TEST_DATABASE_URL'):
        assert engine.url.database == 'req135_test'
        upload_sessions.drop(engine, checkfirst=True)
    with engine.begin() as c:
        ensure_upload_sessions(c)
        ensure_upload_sessions(c)
    yield engine
    engine.dispose()


def create(repo, **extra):
    return repo.create(**dict(owner_id='test-user', idempotency_key='upload-1', media_kind='sku_video',
        business_id=None, expected_size=8388609, mime_type='video/mp4', part_size=8388608,
        mode='cos_direct', temporary_key='tmp/test/session', stable_key='videos/pending/test/stable',
        now=NOW, **extra))


def ready(repo):
    row=create(repo)
    row=repo.move(row,'uploading',now=NOW)
    row=repo.claim(row,'verifying',now=NOW)
    return repo.finish(row,'ready',now=NOW,source_version_id='source-v1')


def test_migration_restart_and_idempotency(engine):
    with Session(engine) as db, db.begin():
        repo=UploadSessionRepository(db);a=create(repo);b=create(repo)
        assert a['id']==b['id']
        assert 'lease_token' in a
    with Session(engine) as db:
        assert UploadSessionRepository(db).get(a['id'],'test-user')['expected_size']==8388609
        with pytest.raises(UploadSessionNotFound):UploadSessionRepository(db).get(a['id'],'another-user')
    assert {'ix_media_upload_expiry','ix_media_upload_business','ix_media_upload_task'} <= {x['name'] for x in inspect(engine).get_indexes('media_upload_sessions')}


def test_idempotency_conflicting_payload_does_not_poison_transaction(engine):
    with Session(engine) as db, db.begin():
        repo=UploadSessionRepository(db);a=create(repo)
        with pytest.raises(UploadSessionConflict):
            repo.create(owner_id='test-user',idempotency_key='upload-1',media_kind='sku_video',business_id=None,
                expected_size=1,mime_type='video/mp4',part_size=8388608,mode='cos_direct',
                temporary_key='tmp/other',stable_key='videos/other',now=NOW)
        assert repo.get(a['id'],'test-user')['expected_size']==8388609


def test_lease_recovery_fences_old_worker(engine):
    with Session(engine) as db, db.begin():
        repo=UploadSessionRepository(db);row=repo.move(create(repo),'uploading',now=NOW)
        old=repo.claim(row,'verifying',now=NOW,lease_seconds=1)
        with pytest.raises(UploadSessionConflict):repo.claim(old,'verifying',now=NOW)
        new=repo.claim(old,'verifying',now=NOW+timedelta(seconds=2))
        assert old['lease_token'] != new['lease_token']
        with pytest.raises(UploadSessionConflict):repo.finish(old,'ready',now=NOW+timedelta(seconds=2))
        done=repo.finish(new,'ready',now=NOW+timedelta(seconds=2))
        assert done['lease_token'] is None


def test_stale_snapshot_cannot_bind_after_cancel(engine):
    with Session(engine) as db, db.begin():
        repo=UploadSessionRepository(db);snapshot=ready(repo)
        cancelled=repo.move(snapshot,'cancelled',now=NOW)
        with pytest.raises(UploadSessionConflict):repo.claim(snapshot,'binding',now=NOW)
        with pytest.raises(UploadSessionConflict):repo.claim(cancelled,'verifying',now=NOW)


def test_cleaner_cannot_touch_bound_or_retained_object(engine):
    with Session(engine) as db, db.begin():
        repo=UploadSessionRepository(db);row=ready(repo)
        with pytest.raises(UploadSessionConflict):repo.claim(row,'cleaning',now=NOW)
        row=repo.claim(row,'binding',now=NOW)
        bound=repo.finish(row,'bound',now=NOW,bound_business_id=1)
        with pytest.raises(UploadSessionConflict):repo.claim(bound,'cleaning',now=NOW+timedelta(days=2))


def test_cleanup_lease_and_expired_binding(engine):
    with Session(engine) as db, db.begin():
        repo=UploadSessionRepository(db);row=ready(repo);later=NOW+timedelta(days=2)
        with pytest.raises(UploadSessionConflict):repo.claim(row,'binding',now=later)
        cleaning=repo.claim(row,'cleaning',now=later)
        assert repo.finish(cleaning,'cleaned',now=later)['state']=='cleaned'


def test_same_snapshot_has_one_claim_winner(engine):
    with Session(engine) as db, db.begin():snapshot=ready(UploadSessionRepository(db))
    barrier=threading.Barrier(2)
    def worker(_):
        with Session(engine) as db, db.begin():
            repo=UploadSessionRepository(db);barrier.wait()
            try:repo.claim(snapshot,'binding',now=NOW);return True
            except UploadSessionConflict:return False
    with ThreadPoolExecutor(max_workers=2) as pool:assert sum(pool.map(worker,range(2)))==1


def test_heartbeat_fences_old_version(engine):
    with Session(engine) as db, db.begin():
        repo=UploadSessionRepository(db);row=repo.claim(ready(repo),'binding',now=NOW)
        new=repo.heartbeat(row,now=NOW+timedelta(seconds=1))
        with pytest.raises(UploadSessionConflict):repo.finish(row,'bound',now=NOW+timedelta(seconds=1))
        assert repo.finish(new,'bound',now=NOW+timedelta(seconds=1),bound_business_id=1)['state']=='bound'


def test_create_rollback_leaves_no_session(engine):
    with Session(engine) as db:
        row=create(UploadSessionRepository(db));db.rollback()
    with Session(engine) as db:
        assert db.execute(select(upload_sessions)).first() is None


def test_idempotency_key_case_is_consistent_across_databases(engine):
    with Session(engine) as db, db.begin():
        repo=UploadSessionRepository(db)
        def upload(key):
            return repo.create(owner_id='test-user',idempotency_key=key,media_kind='sku_video',business_id=None,
                expected_size=1,mime_type='video/mp4',part_size=8388608,mode='cos_direct',
                temporary_key='tmp/'+key,stable_key='videos/'+key,now=NOW)
        assert upload('Case')['id'] != upload('case')['id']


def test_initialization_cancel_fences_multipart_activation(engine):
    with Session(engine) as db, db.begin():
        repo = UploadSessionRepository(db)
        row = repo.reserve_initialization(create(repo), now=NOW)
        with pytest.raises(UploadSessionConflict): repo.reserve_initialization(row, now=NOW)
        repo.cancel(row, now=NOW)
        with pytest.raises(UploadSessionConflict): repo.activate(row, upload_id='orphan', now=NOW)


def test_cleanup_reclaims_expired_operation_but_never_bound(engine):
    with Session(engine) as db, db.begin():
        repo = UploadSessionRepository(db)
        row = repo.claim(ready(repo), 'binding', now=NOW)
        with pytest.raises(UploadSessionConflict): repo.reserve_cleanup(row, now=NOW)
        later = NOW + timedelta(days=2)
        cleaning = repo.reserve_cleanup(row, now=later)
        with pytest.raises(UploadSessionConflict): repo.finish(row, 'bound', now=later)
        done = repo.finish(cleaning, 'cleaned', now=later)
        assert repo.reserve_cleanup(done, now=later)['state'] == 'cleaning'


def test_stable_key_changes_only_at_binding_commit(engine):
    with Session(engine) as db, db.begin():
        repo = UploadSessionRepository(db)
        row = repo.claim(ready(repo), 'binding', now=NOW)
        with pytest.raises(ValueError): repo.checkpoint(row, now=NOW, stable_key='videos/forged')
        with pytest.raises(UploadSessionConflict): repo.finish(row, 'ready', now=NOW, stable_key='videos/forged')
        bound = repo.finish(row, 'bound', now=NOW, stable_key='videos/formal', bound_business_id='7')
        assert bound['stable_key'] == 'videos/formal'
        with pytest.raises(UploadSessionConflict): repo.reserve_cleanup(bound, now=NOW + timedelta(days=2))
