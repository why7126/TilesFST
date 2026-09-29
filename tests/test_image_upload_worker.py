from datetime import datetime, timedelta, timezone
from io import BytesIO
import json
import sys

import pytest
from PIL import Image
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from app.modules.media.image_processing import render_variant, ImageProcessingFailure
from app.modules.media.image_worker import process_session, run_isolated
from app.modules.media.upload_sessions import UploadSessionRepository, UploadSessionConflict, ensure_upload_sessions

NOW = datetime(2026, 9, 8, tzinfo=timezone.utc)


@pytest.fixture
def db(tmp_path):
    engine = create_engine('sqlite:///' + str(tmp_path / 'worker.db'))
    with engine.begin() as connection:
        ensure_upload_sessions(connection)
    with Session(engine) as session:
        yield session
    engine.dispose()


def queued(db):
    repo = UploadSessionRepository(db)
    row = repo.create(owner_id='owner', idempotency_key='image', media_kind='sku_image', business_id=None,
        expected_size=1024, mime_type='image/png', part_size=8388608, mode='cos_direct',
        temporary_key='tmp/direct-upload/test/source', stable_key='images/default/tiles/pending/direct-upload/test.png', now=NOW)
    row = repo.move(row, 'uploading', now=NOW)
    row = repo.claim(row, 'verifying', now=NOW)
    row = repo.checkpoint(row, now=NOW, stable_version_id='fixed-v1', actual_size=1024, actual_mime_type='image/png')
    row = repo.queue_processing(row, now=NOW, metadata={'thumbnail_target_kib': 0, 'display_target_kib': 768})
    db.commit()
    return row


def success(job, pulse):
    pulse()
    return {'ok': True, 'download_ms': 15, 'outputs': {name: {'key': key, 'version_id': 'v1',
        'mime_type': 'image/webp', 'width': 120, 'height': 80, 'size': 100}
        for name, key in job['output_keys'].items()}}


def test_queue_survives_reopen_and_only_one_worker_claims(db):
    row = queued(db)
    repo = UploadSessionRepository(db)
    claimed = repo.claim(row, 'processing', now=NOW); db.commit()
    with pytest.raises(UploadSessionConflict): repo.claim(row, 'processing', now=NOW)
    db.rollback()
    # Crash followed by lease takeover: previous worker cannot publish.
    later = NOW + timedelta(seconds=121)
    current = repo.get(row['id'], 'owner')
    assert process_session(db, current, runner=success, clock=lambda: later) == 'ready'
    with pytest.raises(UploadSessionConflict): repo.finish(claimed, 'ready', now=later)


def test_ready_requires_both_outputs_and_retains_fixed_version(db):
    row = queued(db)
    assert process_session(db, row, runner=success, clock=lambda: NOW) == 'ready'
    result = UploadSessionRepository(db).get(row['id'], 'owner')
    assert result['stable_version_id'] == 'fixed-v1'
    metadata = json.loads(result['variants_json'])
    assert len(metadata['planned_keys']) == 2
    assert set(metadata['outputs']) == {'thumbnail', 'display'}


def test_cancel_fences_late_result(db):
    row = queued(db); repo = UploadSessionRepository(db)
    def cancelled(job, pulse):
        repo.cancel(repo.get(row['id'], 'owner'), now=NOW); db.commit()
        return success(job, lambda: None)
    assert process_session(db, row, runner=cancelled, clock=lambda: NOW) == 'superseded'
    assert repo.get(row['id'], 'owner')['state'] == 'cancelled'


def test_retry_backoff_and_exhaustion_are_persistent(db):
    row = queued(db); repo = UploadSessionRepository(db)
    now = NOW
    failure = lambda job, pulse: {'ok': False, 'reason': 'storage_unavailable', 'retryable': True}
    for attempt, delay in enumerate([5, 15, 45, None], 1):
        result = process_session(db, row, runner=failure, clock=lambda: now)
        row = repo.get(row['id'], 'owner')
        assert json.loads(row['variants_json'])['attempt'] == attempt
        if delay:
            assert result == 'processing'
            with pytest.raises(UploadSessionConflict): repo.claim(row, 'processing', now=now)
            db.rollback(); now += timedelta(seconds=delay)
        else: assert result == 'failed' and row['error_code'] == '30084'
    assert len(json.loads(row['variants_json'])['planned_keys']) == 8


def test_invalid_or_partial_result_cannot_become_ready(db):
    row = queued(db)
    assert process_session(db, row, runner=lambda job, pulse: {'ok': True, 'outputs': {}}, clock=lambda: NOW) == 'failed'
    assert UploadSessionRepository(db).get(row['id'], 'owner')['state'] == 'failed'


def test_permanent_decode_failure_not_automatically_retried(db):
    row = queued(db)
    runner = lambda job, pulse: {'ok': False, 'reason': 'decode_or_encode_failed', 'retryable': False}
    assert process_session(db, row, runner=runner, clock=lambda: NOW) == 'failed'


@pytest.mark.parametrize('fmt,mime', [('JPEG','image/jpeg'), ('PNG','image/png'), ('WEBP','image/webp')])
def test_variants_format_dimensions_and_no_upscale(fmt, mime):
    image = Image.new('RGB', (120, 80), (20, 80, 150)); f = BytesIO(); image.save(f, format=fmt)
    for name in ('thumbnail', 'display'):
        raw, metadata = render_variant(f.getvalue(), mime, name, 768)
        with Image.open(BytesIO(raw)) as result:
            assert result.size == (120, 80) and result.format == 'WEBP'
        assert metadata['warning'] is False


def test_alpha_orientation_and_mime_validation():
    image = Image.new('RGBA', (800, 1200), (20, 80, 150, 100)); f = BytesIO(); image.save(f, format='PNG')
    raw, _ = render_variant(f.getvalue(), 'image/png', 'thumbnail')
    with Image.open(BytesIO(raw)) as result:
        assert result.size == (320, 480) and result.getchannel('A').getextrema() == (100,100)
    with pytest.raises(ImageProcessingFailure): render_variant(f.getvalue(), 'image/jpeg', 'thumbnail')
    exif = Image.Exif(); exif[274] = 6; f = BytesIO(); image.convert('RGB').save(f, format='JPEG', exif=exif)
    raw, _ = render_variant(f.getvalue(), 'image/jpeg', 'thumbnail')
    with Image.open(BytesIO(raw)) as result: assert result.size == (480, 320)
    with pytest.raises(ImageProcessingFailure): render_variant(f.getvalue(), 'image/gif', 'thumbnail')


def test_process_timeout_kills_child():
    result = run_isolated({}, lambda: None, timeout=0.1,
        command=[sys.executable, '-c', 'import time;time.sleep(60)'])
    assert result == {'ok': False, 'reason': 'processing_timeout', 'retryable': False}


def test_process_cancellation_kills_child():
    def cancelled(): raise UploadSessionConflict('cancelled')
    with pytest.raises(UploadSessionConflict):
        run_isolated({}, cancelled, timeout=2,
            command=[sys.executable, '-c', 'import time;time.sleep(60)'])


def test_unreachable_size_target_returns_valid_webp_warning():
    import random
    image = Image.frombytes('RGB', (480, 320), random.Random(135).randbytes(480 * 320 * 3))
    f = BytesIO(); image.save(f, format='PNG')
    raw, metadata = render_variant(f.getvalue(), 'image/png', 'thumbnail', 1)
    assert metadata['warning'] and len(raw) > 1024
    with Image.open(BytesIO(raw)) as out:
        out.load(); assert out.format == 'WEBP'
