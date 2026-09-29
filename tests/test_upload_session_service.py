"""Control-plane tests use an isolated database and a deterministic storage adapter."""
from datetime import datetime, timedelta, timezone
from types import SimpleNamespace
import os
from unittest.mock import Mock

import pytest
from sqlalchemy import create_engine, select, text
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.exceptions import AppError
from app.modules.media.cos_upload import ConfirmedObject, UploadObjectMismatch
from app.modules.media.upload_sessions import (
    ensure_upload_sessions, upload_sessions, UploadSessionConflict, UploadSessionNotFound,
)
from app.schemas.upload_session import UploadSessionCreate
from app.services.upload_session_service import UploadSessionService, PART_SIZE

ACTOR = SimpleNamespace(id='upload-user', role='admin')
MP4 = b'\x00\x00\x00\x18ftypisom\x00\x00\x02\x00isommp42'


@pytest.fixture
def control(tmp_path, monkeypatch):
    test_url = os.environ.get('REQ135_TEST_DATABASE_URL')
    engine = create_engine(test_url or 'sqlite:///' + str(tmp_path / 'control.db'))
    if test_url:
        assert engine.url.database == 'req135_test'
        upload_sessions.drop(engine, checkfirst=True)
        with engine.begin() as conn:
            conn.execute(text('DROP TABLE IF EXISTS tiles'))
    with engine.begin() as conn:
        ensure_upload_sessions(conn)
        conn.execute(text('CREATE TABLE tiles (id INTEGER PRIMARY KEY)'))
        conn.execute(text('INSERT INTO tiles (id) VALUES (7)'))
    monkeypatch.setattr(settings, 'object_storage_provider', 'tencent-cos')
    monkeypatch.setattr(settings, 'object_storage_direct_video_upload_enabled', True)
    effective = SimpleNamespace(allowed_video_type_set=lambda: {'video/mp4'}, max_video_size_mb=lambda: 500)
    gateway = Mock()
    gateway.initiate.return_value = 'multipart-1'
    gateway.authorize.return_value = 'https://cos.invalid/temp?signature=secret'
    def obj(key, version_id=None, expected_size=None):
        return ConfirmedObject(key, version_id or 'v1', 'etag', expected_size or len(MP4), 'video/mp4')
    gateway.inspect.side_effect = obj
    gateway.complete.side_effect = lambda key, upload_id, expected_size, part_size: obj(key, expected_size=expected_size)
    gateway.copy_stable.side_effect = lambda source, key: obj(key, 'stable-v1', source.size)
    gateway.read_prefix.return_value = MP4
    now = [datetime(2026, 9, 8, tzinfo=timezone.utc)]
    with Session(engine) as db:
        yield UploadSessionService(db, effective, gateway_factory=lambda: gateway, clock=lambda: now[0]), gateway, now
    engine.dispose()


def create(service, **kwargs):
    data = dict(media_kind='sku_video', business_id=None, expected_size=len(MP4), mime_type='video/mp4', client_idempotency_key='request-1')
    data.update(kwargs)
    return service.create(UploadSessionCreate(**data), ACTOR)


def test_simple_upload_confirm_is_idempotent_and_hides_private_fields(control):
    service, gateway, _ = control
    created = create(service)
    sid = created.session.session_id
    assert create(service).session.session_id == sid
    assert created.session.media is None
    auth = service.renew(sid, ACTOR)
    assert auth.authorization.length == len(MP4)
    ready = service.confirm(sid, ACTOR)
    assert ready.state == 'ready' and ready.media.size == len(MP4)
    assert service.confirm(sid, ACTOR) == ready
    gateway.copy_stable.assert_called_once()
    serialized = ready.model_dump_json()
    assert 'lease_token' not in serialized and 'temporary_key' not in serialized and 'signature' not in serialized


def test_multipart_parts_use_server_sizes_and_do_not_expose_upload_id(control):
    service, gateway, _ = control
    sid = create(service, expected_size=PART_SIZE + 1).session.session_id
    assert service.renew(sid, ACTOR).authorization is None
    part = service.authorize(sid, ACTOR, 2)
    assert part.length == 1
    assert gateway.authorize.call_args.kwargs['upload_id'] == 'multipart-1'
    with pytest.raises(UploadObjectMismatch): service.authorize(sid, ACTOR, 3)
    assert service.confirm(sid, ACTOR).state == 'ready'
    gateway.complete.assert_called_once()


def test_each_control_operation_rechecks_ownership(control):
    service, _, _ = control
    sid = create(service).session.session_id
    other = SimpleNamespace(id='other-admin', role='admin')
    for operation in (service.query, service.renew, service.authorize, service.confirm, service.cancel):
        with pytest.raises(UploadSessionNotFound): operation(sid, other)
    with pytest.raises(AppError) as error: service.query(sid, SimpleNamespace(id=ACTOR.id, role='shop_owner'))
    assert error.value.code == 40302
    service.db.execute(text('DELETE FROM tiles WHERE id=7')); service.db.commit()
    with pytest.raises(AppError) as error: create(service, business_id=7)
    assert error.value.code == 30080


def test_effective_limits_and_explicit_proxy_capability(control, monkeypatch):
    service, gateway, _ = control
    with pytest.raises(AppError) as error: create(service, expected_size=501 * 1024 * 1024)
    assert error.value.code == 50003
    with pytest.raises(AppError) as error: create(service, mime_type='image/png')
    assert error.value.code == 50002
    assert create(service, media_kind='sku_image').mode == 'proxy'
    monkeypatch.setattr(settings, 'object_storage_direct_video_upload_enabled', False)
    assert create(service).mode == 'proxy'
    gateway.require_versioning.assert_not_called()


def test_existing_session_finishes_after_new_sessions_are_disabled(control, monkeypatch):
    service, _, _ = control
    sid = create(service).session.session_id
    monkeypatch.setattr(settings, 'object_storage_direct_video_upload_enabled', False)
    assert service.renew(sid, ACTOR).authorization is not None
    assert service.confirm(sid, ACTOR).state == 'ready'


def test_expired_authorization_never_extends_absolute_lifetime(control):
    service, gateway, now = control
    sid = create(service).session.session_id
    now[0] += timedelta(days=1)
    with pytest.raises(AppError) as error: service.renew(sid, ACTOR)
    assert error.value.code == 30081
    gateway.authorize.assert_not_called()
    assert service.cancel(sid, ACTOR).state == 'cancelled'


def test_cancelled_worker_cannot_publish_ready(control):
    service, gateway, _ = control
    sid = create(service).session.session_id
    def cancel_during_copy(source, key):
        service.cancel(sid, ACTOR)
        return ConfirmedObject(key, 'abandoned-copy', 'etag', len(MP4), 'video/mp4')
    gateway.copy_stable.side_effect = cancel_during_copy
    with pytest.raises(UploadSessionConflict): service.confirm(sid, ACTOR)
    service.db.rollback()
    assert service.query(sid, ACTOR).state == 'cancelled'
    with pytest.raises(UploadSessionConflict): service.renew(sid, ACTOR)


def test_cancel_persists_even_if_abort_fails_and_can_retry(control):
    service, gateway, _ = control
    sid = create(service, expected_size=PART_SIZE + 1).session.session_id
    gateway.abort.side_effect = AppError(status_code=502, code=50001, message='unavailable')
    with pytest.raises(AppError): service.cancel(sid, ACTOR)
    assert service.query(sid, ACTOR).state == 'cancelled'
    gateway.abort.side_effect = None
    assert service.cancel(sid, ACTOR).state == 'cancelled'


def test_wrong_content_fails_before_copy(control):
    service, gateway, _ = control
    sid = create(service).session.session_id
    gateway.read_prefix.return_value = b'<html>not a video</html>'
    with pytest.raises(UploadObjectMismatch): service.confirm(sid, ACTOR)
    gateway.copy_stable.assert_not_called()
    status = service.query(sid, ACTOR)
    assert status.state == 'failed' and not status.retryable and status.media is None
    with pytest.raises(UploadSessionConflict): service.confirm(sid, ACTOR)


def test_retry_uses_persisted_source_version_even_after_temp_overwrite(control):
    service, gateway, _ = control
    sid = create(service).session.session_id
    gateway.copy_stable.side_effect = AppError(status_code=502, code=50001, message='unavailable')
    with pytest.raises(AppError): service.confirm(sid, ACTOR)
    assert service.query(sid, ACTOR).retryable
    gateway.copy_stable.side_effect = lambda source, key: ConfirmedObject(key, 'stable', 'etag', source.size, 'video/mp4')
    assert service.confirm(sid, ACTOR).state == 'ready'
    assert gateway.inspect.call_args.kwargs['version_id'] == 'v1'


def test_restart_recovers_expired_verification_lease(control):
    service, gateway, now = control
    sid = create(service).session.session_id
    row = service.repo.get(sid, ACTOR.id)
    service.repo.claim(row, 'verifying', now=now[0], lease_seconds=1); service.db.commit()
    assert service.confirm(sid, ACTOR).state == 'verifying'
    now[0] += timedelta(seconds=2)
    with Session(service.db.get_bind()) as recovered_db:
        recovered = UploadSessionService(recovered_db, service.effective, gateway_factory=lambda: gateway, clock=lambda: now[0])
        assert recovered.confirm(sid, ACTOR).state == 'ready'


def test_http_contract_no_store_auth_and_error_mapping(api_client, control):
    from app.main import app
    from app.api.v1.upload_sessions import get_service
    from app.core.deps import require_admin_access
    service, _, _ = control
    app.dependency_overrides[get_service] = lambda: service
    app.dependency_overrides[require_admin_access] = lambda: ACTOR
    root = '/api/v1/admin/uploads/sessions'
    payload = dict(media_kind='sku_video', expected_size=len(MP4), mime_type='video/mp4', client_idempotency_key='api-1')
    response = api_client.post(root, json=payload)
    assert response.status_code == 200, response.text
    assert response.headers['cache-control'] == 'no-store'
    body = response.json()
    assert body['code'] == 0 and body['message'] == 'success'
    sid = body['data']['session']['session_id']
    renewed = api_client.post(f'{root}/{sid}/renew')
    assert renewed.status_code == 200 and renewed.headers['cache-control'] == 'no-store'
    assert renewed.json()['data']['authorization']['length'] == len(MP4)
    assert api_client.post(f'{root}/{sid}/confirm').json()['data']['state'] == 'ready'
    app.dependency_overrides[require_admin_access] = lambda: SimpleNamespace(id='other-admin', role='admin')
    for method, suffix in [('get',''), ('post','/renew'), ('post','/confirm'), ('post','/cancel'), ('post','/parts/1/authorize')]:
        r = getattr(api_client, method)(f'{root}/{sid}{suffix}')
        assert r.status_code == 404 and r.json()['code'] == 30080
        assert r.headers['cache-control'] == 'no-store'
    app.dependency_overrides.pop(require_admin_access)
    unauthorized = api_client.get(f'{root}/{sid}')
    assert unauthorized.status_code == 401 and unauthorized.json()['code'] == 40102
    assert unauthorized.headers['cache-control'] == 'no-store'
    app.dependency_overrides.pop(get_service)


def test_idempotent_creation_does_not_switch_transport_after_rollout_disabled(control, monkeypatch):
    service, _, _ = control
    original = create(service)
    monkeypatch.setattr(settings, 'object_storage_direct_video_upload_enabled', False)
    retry = create(service)
    assert retry.mode == 'cos_direct' and retry.session.session_id == original.session.session_id
    with pytest.raises(UploadSessionConflict): create(service, expected_size=100)


def test_mime_metadata_must_match_verified_container(control):
    service, gateway, _ = control
    sid = create(service).session.session_id
    gateway.inspect.side_effect = lambda key, expected_size: ConfirmedObject(key, 'v1', 'etag', expected_size, 'text/html')
    with pytest.raises(UploadObjectMismatch): service.confirm(sid, ACTOR)
    gateway.copy_stable.assert_not_called()


def test_new_sku_binds_pending_video_and_repeated_save_keeps_same_sku(api_client, control, monkeypatch):
    from app.main import app
    from app.core.deps import require_admin_access
    from app.db.session import get_session_factory
    import app.modules.media.upload_binding as binding_module
    _, gateway, _ = control
    monkeypatch.setattr(binding_module, 'get_upload_gateway', lambda: gateway)
    app.dependency_overrides[require_admin_access] = lambda: ACTOR
    brand = api_client.post('/api/v1/admin/brands', json={'name':'直传测试品牌','sort_order':1}).json()['data']['id']
    category = api_client.post('/api/v1/admin/tile-categories', json={'name':'测试类目','sort_order':1}).json()['data']['id']
    with get_session_factory()() as db:
        service = UploadSessionService(db, control[0].effective, gateway_factory=lambda: gateway)
        sid = create(service).session.session_id
        pending = service.confirm(sid, ACTOR).media.object_key
    payload = {'save_mode':'draft','name':'直传保存测试','brand_id':brand,'category_id':category,
               'videos':[{'object_key':pending,'file_name':'synthetic.mp4','file_size_bytes':99999}]}
    response = api_client.post('/api/v1/admin/tile-skus', json=payload)
    assert response.status_code == 200, response.text
    data = response.json()['data']
    assert '/pending/' not in data['videos'][0]['object_key']
    assert '/tiles/' + str(data['id']) + '/' in data['videos'][0]['object_key']
    assert data['videos'][0]['file_size_bytes'] == len(MP4)
    repeated = api_client.post('/api/v1/admin/tile-skus', json=payload)
    assert repeated.status_code == 200, repeated.text
    assert repeated.json()['data']['id'] == data['id']
    # Cross-business reuse of an already bound file is forbidden.
    other = api_client.post('/api/v1/admin/tile-skus', json={
        'save_mode':'draft','name':'其他SKU','brand_id':brand,'category_id':category}).json()['data']
    forged = dict(payload, videos=[{'object_key':data['videos'][0]['object_key'],'file_name':'forged.mp4'}])
    assert api_client.put('/api/v1/admin/tile-skus/'+str(other['id']), json=forged).status_code in {404,409}
    # Editing a SKU uses a fresh session scoped to that SKU, while retaining the fixed source version.
    with get_session_factory()() as db:
        service = UploadSessionService(db, control[0].effective, gateway_factory=lambda: gateway)
        edit_sid = create(service, business_id=data['id'], client_idempotency_key='edit-video').session.session_id
        edit_key = service.confirm(edit_sid, ACTOR).media.object_key
    edit_payload = dict(payload, videos=[{'object_key':edit_key,'file_name':'edited.mp4'}])
    edited = api_client.put('/api/v1/admin/tile-skus/'+str(data['id']), json=edit_payload)
    assert edited.status_code == 200, edited.text
    assert edited.json()['data']['videos'][0]['object_key'] == edit_key
    again = api_client.put('/api/v1/admin/tile-skus/'+str(data['id']), json=edit_payload)
    assert again.status_code == 200 and len(again.json()['data']['videos']) == 1
    with get_session_factory()() as db:
        row = db.execute(select(upload_sessions).where(upload_sessions.c.id == sid)).mappings().one()
        assert row['state'] == 'bound' and row['bound_business_id'] == str(data['id'])
    app.dependency_overrides.pop(require_admin_access)


def test_sku_save_rejects_unconfirmed_video_without_creating_business(api_client, control):
    from app.main import app
    from app.core.deps import require_admin_access
    from app.db.session import get_session_factory
    app.dependency_overrides[require_admin_access] = lambda: ACTOR
    with get_session_factory()() as db:
        service = UploadSessionService(db, control[0].effective, gateway_factory=lambda: control[1])
        sid = create(service).session.session_id
        key = service.repo.get(sid, ACTOR.id)['stable_key']
        before = db.execute(text('SELECT COUNT(*) FROM tiles')).scalar()
    response = api_client.post('/api/v1/admin/tile-skus', json={'name':'非法直接保存','videos':[{'object_key':key,'file_name':'x.mp4'}]})
    assert response.status_code == 409 and response.json()['code'] == 30082
    with get_session_factory()() as db:
        assert db.execute(text('SELECT COUNT(*) FROM tiles')).scalar() == before
    app.dependency_overrides.pop(require_admin_access)


def test_expired_cleanup_fences_old_worker_and_sweeps_late_versions(control):
    from app.modules.media.upload_cleanup import cleanup_session
    service, gateway, now = control
    sid = create(service).session.session_id
    old = service.repo.claim(service.repo.get(sid, ACTOR.id), 'verifying', now=now[0])
    service.db.commit()
    now[0] += timedelta(days=2)
    gateway.multipart_uploads.return_value = ['orphan-init']
    gateway.versions.return_value = ['exact-version']
    result = cleanup_session(service.db, old, gateway, clock=lambda: now[0], reference_check=lambda db, keys: False)
    assert result['state'] == 'cleaned' and result['aborted_uploads'] == 1 and result['deleted_versions'] == 2
    with pytest.raises(UploadSessionConflict): service.repo.finish(old, 'ready', now=now[0])
    service.db.rollback()
    # A late COS side effect from an obsolete worker is swept on the next pass.
    row = service.repo.get(sid, ACTOR.id)
    assert cleanup_session(service.db, row, gateway, clock=lambda: now[0], reference_check=lambda db, keys: False)['state'] == 'cleaned'


def test_cleanup_preserves_referenced_and_bound_objects(control):
    from app.modules.media.upload_cleanup import cleanup_session
    service, gateway, now = control
    sid = create(service).session.session_id
    now[0] += timedelta(days=2)
    row = service.repo.get(sid, ACTOR.id)
    assert cleanup_session(service.db, row, gateway, clock=lambda: now[0], reference_check=lambda db, keys: True)['state'] == 'protected'
    gateway.delete_version.assert_not_called()
    row['state'] = 'bound'
    assert cleanup_session(service.db, row, gateway, clock=lambda: now[0], reference_check=lambda db, keys: False)['state'] == 'protected'
    gateway.versions.assert_not_called()


def test_business_insert_failure_rolls_back_binding_and_retry_reuses_reserved_sku(api_client, control, monkeypatch):
    from app.main import app
    from app.core.deps import require_admin_access
    from app.db.session import get_session_factory
    from app.repositories.tile_sku_repository import TileSkuRepository
    import app.modules.media.upload_binding as binding_module
    _, gateway, _ = control
    monkeypatch.setattr(binding_module, 'get_upload_gateway', lambda: gateway)
    app.dependency_overrides[require_admin_access] = lambda: ACTOR
    brand = api_client.post('/api/v1/admin/brands', json={'name':'失败补偿品牌','sort_order':1}).json()['data']['id']
    category = api_client.post('/api/v1/admin/tile-categories', json={'name':'失败补偿类','sort_order':1}).json()['data']['id']
    with get_session_factory()() as db:
        service = UploadSessionService(db, control[0].effective, gateway_factory=lambda: gateway)
        sid = create(service).session.session_id
        pending = service.confirm(sid, ACTOR).media.object_key
    payload = {'save_mode':'draft','name':'失败补偿','brand_id':brand,'category_id':category,
               'videos':[{'object_key':pending,'file_name':'synthetic.mp4'}]}
    original = TileSkuRepository.replace_videos
    def fail_after_insert(repo, tile_id, videos):
        original(repo, tile_id, videos)
        raise RuntimeError('synthetic database failure after insert')
    monkeypatch.setattr(TileSkuRepository, 'replace_videos', fail_after_insert)
    with pytest.raises(RuntimeError): api_client.post('/api/v1/admin/tile-skus', json=payload)
    with get_session_factory()() as db:
        row = db.execute(select(upload_sessions).where(upload_sessions.c.id == sid)).mappings().one()
        reserved = int(row['bound_business_id'])
        assert row['state'] == 'ready'
        assert db.execute(text('SELECT COUNT(*) FROM tile_videos WHERE tile_id=:id'), {'id':reserved}).scalar() == 0
    monkeypatch.setattr(TileSkuRepository, 'replace_videos', original)
    response = api_client.post('/api/v1/admin/tile-skus', json=payload)
    assert response.status_code == 200, response.text
    assert response.json()['data']['id'] == reserved
    assert '/pending/' not in response.json()['data']['videos'][0]['object_key']
    with get_session_factory()() as db:
        assert db.execute(text('SELECT COUNT(*) FROM tiles WHERE name=:name'), {'name':'失败补偿'}).scalar() == 1
    app.dependency_overrides.pop(require_admin_access)


@pytest.mark.parametrize('mime', ['image/svg+xml', 'application/pdf', 'image/gif', 'image/heic', 'image/tiff', 'image/bmp'])
def test_special_images_explicitly_keep_proxy_policy(control, monkeypatch, mime):
    service, gateway, _ = control
    monkeypatch.setattr(settings, 'object_storage_direct_image_upload_enabled', True)
    result = create(service, media_kind='sku_image', mime_type=mime)
    assert result.mode == 'proxy' and result.session is None and result.reason
    gateway.require_versioning.assert_not_called()


def test_image_confirmation_queues_and_retry_does_not_upload_again(control, monkeypatch):
    import json
    from app.modules.media.image_worker import process_session
    service, gateway, now = control
    monkeypatch.setattr(settings, 'object_storage_direct_image_upload_enabled', True)
    service.effective.allowed_image_type_set = lambda: {'image/png'}
    service.effective.max_image_size_mb = lambda: 20
    service.effective.thumbnail_max_size_kb = lambda: 0
    service.effective.display_max_size_kb = lambda: 768
    gateway.inspect.side_effect = lambda key, version_id=None, expected_size=None: ConfirmedObject(
        key, version_id or 'v1', 'etag', expected_size, 'image/png')
    gateway.copy_stable.side_effect = lambda source, key: ConfirmedObject(key, 'stable-v1', 'etag', source.size, 'image/png')
    created = create(service, media_kind='sku_image', mime_type='image/png', expected_size=100)
    sid = created.session.session_id
    monkeypatch.setattr(settings, 'object_storage_direct_image_upload_enabled', False)
    assert create(service, media_kind='sku_image', mime_type='image/png', expected_size=100).session.session_id == sid
    assert create(service, media_kind='sku_image', mime_type='image/png', expected_size=100,
                  client_idempotency_key='new-after-disable').mode == 'proxy'
    assert service.confirm(sid, ACTOR).state == 'processing'
    assert service.confirm(sid, ACTOR).media is None
    row = service.repo.get(sid, ACTOR.id)
    assert json.loads(row['variants_json'])['display_target_kib'] == 768
    assert process_session(service.db, row, clock=lambda: now[0],
        runner=lambda job, pulse: {'ok': False, 'reason': 'decode_or_encode_failed', 'retryable': False}) == 'failed'
    assert service.query(sid, ACTOR).retryable
    with pytest.raises(UploadSessionNotFound):
        service.retry_processing(sid, SimpleNamespace(id='other', role='admin'))
    assert service.retry_processing(sid, ACTOR).state == 'processing'
    assert service.retry_processing(sid, ACTOR).state == 'processing'
    gateway.copy_stable.assert_called_once()
    service.cancel(sid, ACTOR)
    with pytest.raises(UploadSessionConflict): service.retry_processing(sid, ACTOR)


def test_image_binding_waits_for_derivatives_and_formalizes_all_versions(api_client, control, monkeypatch):
    from app.main import app
    from app.core.deps import require_admin_access
    from app.db.session import get_session_factory
    from app.modules.media.image_worker import process_session
    import app.modules.media.upload_binding as binding_module
    from app.modules.media.storage import same_directory_thumbnail_object_key, same_directory_display_object_key
    _, gateway, _ = control
    monkeypatch.setattr(binding_module, 'get_upload_gateway', lambda: gateway)
    monkeypatch.setattr(settings, 'object_storage_direct_image_upload_enabled', True)
    app.dependency_overrides[require_admin_access] = lambda: ACTOR
    effective = SimpleNamespace(allowed_image_type_set=lambda: {'image/png'}, max_image_size_mb=lambda: 20,
                                thumbnail_max_size_kb=lambda: 0, display_max_size_kb=lambda: 768)
    gateway.inspect.side_effect = lambda key, version_id=None, expected_size=None: ConfirmedObject(
        key, version_id or 'v1', 'etag', expected_size, 'image/webp' if key.endswith('.webp') else 'image/png')
    gateway.copy_stable.side_effect = lambda source, key: ConfirmedObject(key, 'copy-v1', 'etag', source.size, source.content_type)
    brand = api_client.post('/api/v1/admin/brands', json={'name':'图片直传品牌','sort_order':1}).json()['data']['id']
    category = api_client.post('/api/v1/admin/tile-categories', json={'name':'图片直传类','sort_order':1}).json()['data']['id']
    with get_session_factory()() as db:
        service = UploadSessionService(db, effective, gateway_factory=lambda: gateway)
        sid = create(service, media_kind='sku_image', mime_type='image/png', expected_size=100).session.session_id
        assert service.confirm(sid, ACTOR).state == 'processing'
        pending = service.repo.get(sid, ACTOR.id)['stable_key']
    payload = {'save_mode':'draft','name':'异步图片绑定','brand_id':brand,'category_id':category,
               'images':[{'object_key':pending,'url':'/media/'+pending,'is_main':True}]}
    assert api_client.post('/api/v1/admin/tile-skus', json=payload).status_code == 409
    with get_session_factory()() as db:
        service = UploadSessionService(db, effective, gateway_factory=lambda: gateway)
        def runner(job, pulse):
            return {'ok':True, 'outputs':{name:{'key':key,'version_id':'derived-v1','size':80,'mime_type':'image/webp'}
                                        for name,key in job['output_keys'].items()}}
        assert process_session(db, service.repo.get(sid, ACTOR.id), runner=runner) == 'ready'
    response = api_client.post('/api/v1/admin/tile-skus', json=payload)
    assert response.status_code == 200, response.text
    item = response.json()['data'];key = item['images'][0]['object_key']
    assert '/pending/' not in key and item['images'][0]['url'] == '/media/'+key
    targets = [call.args[1] for call in gateway.copy_stable.call_args_list]
    assert same_directory_thumbnail_object_key(key) in targets
    assert same_directory_display_object_key(key) in targets
    assert api_client.post('/api/v1/admin/tile-skus', json=payload).json()['data']['id'] == item['id']
    # A lost response may cause an update to repeat the original pending reference.
    repeated = api_client.put('/api/v1/admin/tile-skus/' + str(item['id']), json=payload)
    assert repeated.status_code == 200, repeated.text
    assert repeated.json()['data']['images'][0]['object_key'] == key
    with get_session_factory()() as db:
        assert db.execute(select(upload_sessions.c.state).where(upload_sessions.c.id==sid)).scalar() == 'bound'
        status = UploadSessionService(db, effective, gateway_factory=lambda: gateway).query(sid, ACTOR)
        assert status.media.display_url == '/media/' + same_directory_display_object_key(key)
        trace_id = db.execute(select(upload_sessions.c.task_trace_id).where(upload_sessions.c.id==sid)).scalar()
        spans = db.execute(text('SELECT span_name, metadata FROM task_trace_spans WHERE task_trace_id=:id'), {'id':trace_id}).all()
        assert {'source_download','thumbnail_generate','thumbnail_put','display_generate','display_put','binding_copy','binding'} <= {entry[0] for entry in spans}
        assert all('direct-upload/' not in (entry[1] or '') and 'signature' not in (entry[1] or '') for entry in spans)

    app.dependency_overrides.pop(require_admin_access)


def test_brand_logo_copy_failure_resumes_reservation_and_atomic_binding(api_client, control, monkeypatch):
    from app.main import app
    from app.core.deps import require_admin_user
    from app.db.session import get_session_factory
    from app.modules.media.image_worker import process_session
    from app.repositories.brand_repository import BrandRepository
    import app.modules.media.upload_binding as binding_module
    _, gateway, _ = control
    monkeypatch.setattr(binding_module, 'get_upload_gateway', lambda: gateway)
    monkeypatch.setattr(settings, 'object_storage_direct_image_upload_enabled', True)
    app.dependency_overrides[require_admin_user] = lambda: ACTOR
    effective = SimpleNamespace(allowed_image_type_set=lambda: {'image/png'}, max_image_size_mb=lambda: 20,
                                thumbnail_max_size_kb=lambda: 0, display_max_size_kb=lambda: 768)
    gateway.inspect.side_effect = lambda key, version_id=None, expected_size=None: ConfirmedObject(
        key, version_id or 'v1', 'etag', expected_size, 'image/webp' if key.endswith('.webp') else 'image/png')
    copy = lambda source, key: ConfirmedObject(key, 'copy-v1', 'etag', source.size, source.content_type)
    gateway.copy_stable.side_effect = copy
    try:
        with get_session_factory()() as db:
            service = UploadSessionService(db, effective, gateway_factory=lambda: gateway)
            employee_session = service.create(UploadSessionCreate(media_kind='brand_logo', expected_size=100, mime_type='image/png',
                client_idempotency_key='employee-logo'), SimpleNamespace(id='employee', role='employee'))
            assert employee_session.mode == 'cos_direct'
            with pytest.raises(UploadSessionNotFound):
                service.query(employee_session.session.session_id, ACTOR)
            sid = create(service, media_kind='brand_logo', mime_type='image/png', expected_size=100).session.session_id
            assert service.confirm(sid, ACTOR).state == 'processing'
            pending = service.repo.get(sid, ACTOR.id)['stable_key']
            def runner(job, pulse):
                return {'ok': True, 'outputs': {name: {'key':key, 'version_id':'derived-v1', 'size':80,
                    'mime_type':'image/webp'} for name,key in job['output_keys'].items()}}
            assert process_session(db, service.repo.get(sid, ACTOR.id), runner=runner) == 'ready'
        payload = {'name':'Logo绑定失败重试品牌','sort_order':1,'logo_object_key':pending}
        gateway.copy_stable.side_effect = AppError(status_code=503, code=50001, message='存储暂时不可用')
        assert api_client.post('/api/v1/admin/brands', json=payload).status_code == 503
        with get_session_factory()() as db:
            row = db.execute(select(upload_sessions).where(upload_sessions.c.id==sid)).mappings().one()
            reserved = int(row['bound_business_id'])
            record = BrandRepository(db).get_by_id(reserved)
            assert row['state']=='ready' and record.logo_object_key is None and record.status=='DISABLED'
        gateway.copy_stable.side_effect = copy
        original = BrandRepository.update
        def fail_after_write(self, *args, **kwargs):
            original(self, *args, **kwargs)
            raise AppError(status_code=503, code=50001, message='模拟引用写入失败')
        monkeypatch.setattr(BrandRepository, 'update', fail_after_write)
        assert api_client.post('/api/v1/admin/brands', json=payload).status_code == 503
        with get_session_factory()() as db:
            assert BrandRepository(db).get_by_id(reserved).logo_object_key is None
            assert db.execute(select(upload_sessions.c.state).where(upload_sessions.c.id==sid)).scalar()=='ready'
        monkeypatch.setattr(BrandRepository, 'update', original)
        response=api_client.post('/api/v1/admin/brands', json=payload)
        assert response.status_code==200, response.text
        item=response.json()['data']
        assert item['id']==reserved and item['status']=='ENABLED' and '/pending/' not in item['logo_object_key']
        assert api_client.post('/api/v1/admin/brands', json=payload).json()['data']['id']==reserved
        assert api_client.put('/api/v1/admin/brands/'+str(reserved), json=payload).json()['data']['logo_object_key']==item['logo_object_key']
        with get_session_factory()() as db:
            assert db.execute(select(upload_sessions.c.state).where(upload_sessions.c.id==sid)).scalar()=='bound'
    finally:
        app.dependency_overrides.pop(require_admin_user, None)


def test_banner_copy_failure_resumes_draft_and_rejects_forged_borrowed_reference(api_client, control, monkeypatch):
    from app.main import app
    from app.core.deps import require_admin_user
    from app.db.session import get_session_factory
    from app.modules.media.image_worker import process_session
    from app.repositories.banner_repository import BannerRepository
    import app.modules.media.upload_binding as binding_module
    _, gateway, _ = control
    monkeypatch.setattr(binding_module, 'get_upload_gateway', lambda: gateway)
    monkeypatch.setattr(settings, 'object_storage_direct_image_upload_enabled', True)
    app.dependency_overrides[require_admin_user] = lambda: ACTOR
    effective = SimpleNamespace(allowed_image_type_set=lambda: {'image/png'}, max_image_size_mb=lambda: 20,
                                thumbnail_max_size_kb=lambda: 0, display_max_size_kb=lambda: 768)
    gateway.inspect.side_effect = lambda key, version_id=None, expected_size=None: ConfirmedObject(
        key, version_id or 'v1', 'etag', expected_size, 'image/webp' if key.endswith('.webp') else 'image/png')
    copy = lambda source, key: ConfirmedObject(key, 'copy-v1', 'etag', source.size, source.content_type)
    gateway.copy_stable.side_effect = copy
    try:
        with get_session_factory()() as db:
            service = UploadSessionService(db, effective, gateway_factory=lambda: gateway)
            employee_session = service.create(UploadSessionCreate(media_kind='banner', expected_size=100, mime_type='image/png',
                client_idempotency_key='employee-banner'), SimpleNamespace(id='employee', role='employee'))
            assert employee_session.mode == 'cos_direct'
            with pytest.raises(UploadSessionNotFound):
                service.query(employee_session.session.session_id, ACTOR)
            sid = create(service, media_kind='banner', mime_type='image/png', expected_size=100).session.session_id
            assert service.confirm(sid, ACTOR).state == 'processing'
            pending = service.repo.get(sid, ACTOR.id)['stable_key']
            def runner(job, pulse):
                return {'ok': True, 'outputs': {name: {'key':key, 'version_id':'derived-v1', 'size':80,
                    'mime_type':'image/webp'} for name,key in job['output_keys'].items()}}
            assert process_session(db, service.repo.get(sid, ACTOR.id), runner=runner) == 'ready'
        payload = {'title':'Banner绑定失败重试','display_client':'MINIAPP_HOME','position':'MINIAPP_HOME_CAROUSEL',
                   'image_source':'custom_upload','jump_type':'NO_JUMP','sort_order':1,'image_object_key':pending}
        forged = dict(payload, image_source='brand_logo')
        assert api_client.post('/api/v1/admin/banners', json=forged).status_code == 400
        gateway.copy_stable.side_effect = AppError(status_code=503, code=50001, message='存储暂时不可用')
        assert api_client.post('/api/v1/admin/banners', json=payload).status_code == 503
        with get_session_factory()() as db:
            row = db.execute(select(upload_sessions).where(upload_sessions.c.id==sid)).mappings().one()
            reserved = int(row['bound_business_id'])
            record = BannerRepository(db).get_by_id(reserved)
            assert row['state']=='ready' and record.image_object_key == '' and record.status=='DRAFT'
        gateway.copy_stable.side_effect = copy
        original = BannerRepository.update
        def fail_after_write(self, *args, **kwargs):
            original(self, *args, **kwargs)
            raise AppError(status_code=503, code=50001, message='模拟引用写入失败')
        monkeypatch.setattr(BannerRepository, 'update', fail_after_write)
        assert api_client.post('/api/v1/admin/banners', json=payload).status_code == 503
        with get_session_factory()() as db:
            assert BannerRepository(db).get_by_id(reserved).image_object_key == ''
            assert db.execute(select(upload_sessions.c.state).where(upload_sessions.c.id==sid)).scalar()=='ready'
        monkeypatch.setattr(BannerRepository, 'update', original)
        response=api_client.post('/api/v1/admin/banners', json=payload)
        assert response.status_code==200, response.text
        item=response.json()['data']
        assert item['id']==reserved and item['status']=='DRAFT' and '/pending/' not in item['image_object_key']
        assert api_client.post('/api/v1/admin/banners', json=payload).json()['data']['id']==reserved
        assert api_client.put('/api/v1/admin/banners/'+str(reserved), json=payload).json()['data']['image_object_key']==item['image_object_key']
        with get_session_factory()() as db:
            assert db.execute(select(upload_sessions.c.state).where(upload_sessions.c.id==sid)).scalar()=='bound'
    finally:
        app.dependency_overrides.pop(require_admin_user, None)


def test_avatar_create_rolls_back_user_and_session_then_profile_preserves_binding(api_client, control, monkeypatch):
    from app.main import app
    from app.core.deps import require_system_admin
    from app.db.session import get_session_factory
    from app.modules.media.image_worker import process_session
    from app.repositories.user_repository import UserRepository
    from app.repositories.profile_activity_repository import ProfileActivityRepository
    from app.services.profile_service import ProfileService
    from app.schemas.profile import ProfilePatchRequest
    import app.modules.media.upload_binding as binding_module
    _, gateway, _ = control
    monkeypatch.setattr(binding_module, 'get_upload_gateway', lambda: gateway)
    monkeypatch.setattr(settings, 'object_storage_direct_image_upload_enabled', True)
    app.dependency_overrides[require_system_admin] = lambda: ACTOR
    effective = SimpleNamespace(allowed_image_type_set=lambda: {'image/png'}, max_image_size_mb=lambda: 20,
                                thumbnail_max_size_kb=lambda: 0, display_max_size_kb=lambda: 768)
    gateway.inspect.side_effect = lambda key, version_id=None, expected_size=None: ConfirmedObject(
        key, version_id or 'v1', 'etag', expected_size, 'image/webp' if key.endswith('.webp') else 'image/png')
    gateway.copy_stable.side_effect = lambda source,key: ConfirmedObject(key,'copy-v1','etag',source.size,source.content_type)
    try:
        with get_session_factory()() as db:
            service = UploadSessionService(db, effective, gateway_factory=lambda: gateway)
            sid = create(service, media_kind='avatar', mime_type='image/png', expected_size=100).session.session_id
            assert service.confirm(sid, ACTOR).state=='processing'
            pending=service.repo.get(sid,ACTOR.id)['stable_key']
            def runner(job,pulse):
                return {'ok':True,'outputs':{name:{'key':key,'version_id':'derived','size':80,'mime_type':'image/webp'}
                    for name,key in job['output_keys'].items()}}
            assert process_session(db,service.repo.get(sid,ACTOR.id),runner=runner)=='ready'
        payload={'username':'avatar_retry_user','display_name':'头像测试','role':'employee','avatar_object_key':pending}
        original=UserRepository.create_user
        def fail_after_write(self,**kwargs):
            original(self,**kwargs)
            raise RuntimeError('synthetic user insert failure')
        monkeypatch.setattr(UserRepository,'create_user',fail_after_write)
        with pytest.raises(RuntimeError): api_client.post('/api/v1/admin/users',json=payload)
        with get_session_factory()() as db:
            assert UserRepository(db).get_by_username(payload['username']) is None
            row=db.execute(select(upload_sessions).where(upload_sessions.c.id==sid)).mappings().one()
            reserved=row['bound_business_id']
            assert row['state']=='ready' and reserved
        monkeypatch.setattr(UserRepository,'create_user',original)
        response=api_client.post('/api/v1/admin/users',json=payload)
        assert response.status_code==200,response.text
        data=response.json()['data'];user_id=data['user']['id']
        assert user_id==reserved and data['initial_password']
        assert '/user-avatars/'+user_id+'/' in data['user']['avatar_object_key']
        with get_session_factory()() as db:
            row=db.execute(select(upload_sessions).where(upload_sessions.c.id==sid)).mappings().one()
            assert row['state']=='bound'
            assert data['initial_password'] not in str(dict(row))
            users=UserRepository(db);user=users.get_by_id(user_id)
            profile=ProfileService(users,ProfileActivityRepository(db))
            updated=profile.patch_me(user,ProfilePatchRequest(display_name='本人修改'))
            assert updated.avatar_object_key==user.avatar_object_key
            other=users.create_user(username='avatar_other_user',password='SyntheticOnly135!',display_name='其他人',role='employee')
            with pytest.raises(AppError):
                profile.patch_me(other,ProfilePatchRequest(avatar_object_key=user.avatar_object_key))
        assert api_client.post('/api/v1/admin/users',json=payload).status_code==409
    finally:
        app.dependency_overrides.pop(require_system_admin,None)


def test_certificate_pdf_image_atomic_binding_and_parent_scope(api_client, control, monkeypatch):
    from app.main import app
    from app.core.deps import require_admin_user, require_system_admin
    from app.db.session import get_session_factory
    from app.modules.media.image_worker import process_session
    from app.repositories.brand_certificate_repository import BrandCertificateRepository
    import app.modules.media.upload_binding as binding_module
    _, gateway, _ = control
    monkeypatch.setattr(binding_module, 'get_upload_gateway', lambda: gateway)
    monkeypatch.setattr(settings, 'object_storage_direct_image_upload_enabled', True)
    effective = SimpleNamespace(max_file_size_mb=lambda:20, thumbnail_max_size_kb=lambda:0, display_max_size_kb=lambda:768)
    current_mime = ['application/pdf']
    gateway.inspect.side_effect = lambda key, version_id=None, expected_size=None: ConfirmedObject(
        key, version_id or 'v1', 'etag', expected_size, 'application/pdf' if key.endswith('.pdf') else (current_mime[0] if key.endswith('/source') else 'image/png'))
    copy = lambda source, key: ConfirmedObject(key, 'copy-v1', 'etag', source.size, source.content_type)
    gateway.copy_stable.side_effect = copy
    app.dependency_overrides[require_admin_user] = lambda: ACTOR
    app.dependency_overrides[require_system_admin] = lambda: ACTOR
    try:
        brand = api_client.post('/api/v1/admin/brands', json={'name':'证书直传品牌','sort_order':1}).json()['data']['id']
        other_brand = api_client.post('/api/v1/admin/brands', json={'name':'另一证书品牌','sort_order':2}).json()['data']['id']
        files = []
        session_ids = []
        with get_session_factory()() as db:
            service = UploadSessionService(db, effective, gateway_factory=lambda:gateway)
            for mime in ['application/pdf', 'image/png']:
                current_mime[0] = mime
                sid = create(service, media_kind='certificate', business_id=brand, expected_size=100,
                             mime_type=mime, client_idempotency_key=mime.replace('/', '-')).session.session_id
                session_ids.append(sid)
                gateway.read_prefix.return_value = b'%PDF-1.7' if mime == 'application/pdf' else b'PNG'
                state = service.confirm(sid, ACTOR)
                if mime.startswith('image/'):
                    assert state.state == 'processing' and state.media is None
                    def runner(job, pulse):
                        return {'ok':True,'outputs':{name:{'key':key,'version_id':'derived-v1','size':80,'mime_type':'image/webp'}
                                for name,key in job['output_keys'].items()}}
                    assert process_session(db, service.repo.get(sid, ACTOR.id), runner=runner) == 'ready'
                    state = service.query(sid, ACTOR)
                else:
                    assert state.state == 'ready' and state.media.thumbnail_url is None
                files.append({'file_key':state.media.object_key, 'file_url':state.media.url,
                              'file_name':'synthetic.pdf' if mime == 'application/pdf' else 'synthetic.png',
                              'file_mime_type':mime, 'file_size_bytes':1})
            with pytest.raises(AppError):
                service.create(UploadSessionCreate(media_kind='certificate', expected_size=100,
                    mime_type='application/pdf',client_idempotency_key='employee-cert'), SimpleNamespace(id='employee',role='employee'))
        payload = {'brand_id':brand,'name':'证书绑定回滚','type':'QUALITY','sort_order':1,
                   'file':files[0], 'images':[dict(files[1],is_main=True,sort_order=0)], 'is_permanent':True,'is_visible':True}
        assert api_client.post('/api/v1/admin/brand-certificates', json=dict(payload,brand_id=other_brand)).status_code == 404
        original = BrandCertificateRepository.update
        def fail_after_write(self,*args,**kwargs):
            original(self,*args,**kwargs)
            raise AppError(status_code=503,code=50001,message='模拟业务引用提交失败')
        monkeypatch.setattr(BrandCertificateRepository, 'update', fail_after_write)
        response = api_client.post('/api/v1/admin/brand-certificates',json=payload)
        assert response.status_code == 503, response.text
        with get_session_factory()() as db:
            rows = db.execute(select(upload_sessions).where(upload_sessions.c.id.in_(session_ids))).mappings().all()
            assert {row['state'] for row in rows} == {'ready'}
            reserved = int(rows[0]['bound_business_id'])
            record = BrandCertificateRepository(db).get_by_id(reserved)
            assert record.file_key == '' and not record.is_visible and not record.images
        monkeypatch.setattr(BrandCertificateRepository,'update',original)
        response = api_client.post('/api/v1/admin/brand-certificates',json=payload)
        assert response.status_code == 200, response.text
        item = response.json()['data']
        assert item['id'] == reserved and item['file_size_bytes'] == 100 and item['images'][0]['file_size_bytes'] == 100
        assert '/pending/' not in item['file_key'] and '/pending/' not in item['images'][0]['file_key']
        assert api_client.post('/api/v1/admin/brand-certificates',json=payload).json()['data']['id'] == reserved
        repeated = api_client.put('/api/v1/admin/brand-certificates/'+str(reserved),json=payload)
        assert repeated.status_code == 200, repeated.text
        with get_session_factory()() as db:
            assert set(db.execute(select(upload_sessions.c.state).where(upload_sessions.c.id.in_(session_ids))).scalars()) == {'bound'}
    finally:
        app.dependency_overrides.pop(require_admin_user,None)
        app.dependency_overrides.pop(require_system_admin,None)


@pytest.mark.parametrize('kind,mime', [('sku_video','video/mp4'),('sku_image','image/png'),('certificate','application/pdf')])
def test_disabling_new_uploads_preserves_existing_session_completion(control, monkeypatch, kind, mime):
    service,gateway,_=control
    monkeypatch.setattr(settings,'object_storage_direct_image_upload_enabled',True)
    service.effective=SimpleNamespace(allowed_video_type_set=lambda:{'video/mp4'},max_video_size_mb=lambda:500,
        allowed_image_type_set=lambda:{'image/png'},max_image_size_mb=lambda:20,max_file_size_mb=lambda:25,
        thumbnail_max_size_kb=lambda:0,display_max_size_kb=lambda:768)
    gateway.inspect.side_effect=lambda key,version_id=None,expected_size=None: ConfirmedObject(key,version_id or 'v1','etag',expected_size,mime)
    gateway.copy_stable.side_effect=lambda source,key: ConfirmedObject(key,'stable-v1','etag',source.size,mime)
    gateway.read_prefix.return_value=b'%PDF-1.7' if mime=='application/pdf' else MP4
    created=create(service,media_kind=kind,mime_type=mime)
    monkeypatch.setattr(settings,'object_storage_direct_video_upload_enabled',False)
    monkeypatch.setattr(settings,'object_storage_direct_image_upload_enabled',False)
    assert create(service,media_kind=kind,mime_type=mime,client_idempotency_key='new-disabled').mode=='proxy'
    sid=created.session.session_id
    assert service.renew(sid,ACTOR).session.session_id==sid
    status=service.confirm(sid,ACTOR)
    assert status.state == ('processing' if mime.startswith('image/') else 'ready')
    assert service.query(sid,ACTOR).state==status.state
