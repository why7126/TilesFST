from datetime import datetime
from types import SimpleNamespace

import pytest
from sqlalchemy import text

from app.core.exceptions import AppError
from app.db.session import get_session_factory
from app.modules.media.storage import MEDIA_NOT_FOUND, MediaObjectInfo, set_media_storage_client, S3CompatibleMediaStorageClient, TencentCOSMediaStorageClient
from app.repositories.media_read_repository import MediaReadRepository, OwnedMedia
from app.schemas.media_read import MediaReadRequest, MediaReadReference
from app.services.media_read_service import MediaReadService, media_candidates


class Storage:
    def __init__(self):
        self.probes = []
        self.fail = None
        self.missing = set()

    def get_object_info(self, key):
        self.probes.append(key)
        if self.fail:
            raise self.fail
        if key in self.missing:
            raise AppError(status_code=404, code=MEDIA_NOT_FOUND, message='missing')
        return MediaObjectInfo(content_type='image/webp', total_size=128)

    def build_direct_read_url(self, key, ttl):
        assert ttl == 300
        return 'https://storage.example.test/object?signature=synthetic-get'

    def build_direct_head_url(self, key, ttl):
        assert ttl == 300
        return 'https://storage.example.test/object?signature=synthetic-head'


@pytest.fixture()
def storage(monkeypatch, tmp_path):
    from app.core.config import settings
    monkeypatch.setattr(settings, "object_storage_direct_read_enabled", True)
    monkeypatch.setattr(settings, "media_read_clients", "web_admin,web_catalog,wechat_miniapp,unknown")
    monkeypatch.setattr(settings, "media_read_proxy_budget_dir", str(tmp_path / "budget"))
    result = Storage()
    set_media_storage_client(result)
    yield result
    set_media_storage_client(None)


def ref(**kwargs):
    return {'resource_type': 'brand_logo', 'resource_id': '901', 'variant': 'original', **kwargs}


def seed_brand():
    with get_session_factory()() as db:
        db.execute(text("INSERT INTO brands (id,name,sort_order,logo_object_key,status,sku_count,created_at,updated_at) VALUES (901,'测试品牌',1,'images/default/brands/901/logo.webp','ENABLED',0,'2026-09-08','2026-09-08')"))
        db.commit()


def test_batch_visibility_ttl_and_revocation(api_client, storage):
    seed_brand()
    response = api_client.post('/api/v1/media/read-authorizations', json={'items': [ref(), ref(resource_id='999999'), ref(resource_type='avatar')]})
    assert response.status_code == 200
    assert response.headers['cache-control'] == 'no-store'
    data = response.json()['data']
    assert [item['status'] for item in data['items']] == ['ready', 'unavailable', 'unavailable']
    descriptor = data['items'][0]['descriptor']
    remaining = datetime.fromisoformat(descriptor['expires_at'].replace('Z', '+00:00')) - datetime.fromisoformat(data['server_time'].replace('Z', '+00:00'))
    assert 295 <= remaining.total_seconds() <= 300
    assert descriptor['head_url'] != descriptor['url']
    assert len(storage.probes) == 1
    with get_session_factory()() as db:
        db.execute(text("UPDATE brands SET status='DISABLED' WHERE id=901"))
        db.commit()
    assert api_client.post('/api/v1/media/read-authorizations', json={'items': [ref()]}).json()['data']['items'][0]['status'] == 'unavailable'
    assert len(storage.probes) == 1


@pytest.mark.parametrize('items', [[], [ref()] * 51, [ref(object_key='arbitrary')], [ref(resource_type='unknown')], [ref(resource_id='../901')]])
def test_rejects_invalid_requests(api_client, items):
    assert api_client.post('/api/v1/media/read-authorizations', json={'items': items}).status_code == 422


def test_admin_identity_required_and_can_read_disabled(api_client, storage):
    seed_brand()
    path = '/api/v1/admin/media/read-authorizations'
    assert api_client.post(path, json={'items': [ref()]}).status_code == 401
    login = api_client.post('/api/v1/auth/login', json={'username': 'admin', 'password': 'AdminPass123!'})
    token = login.json()['data']['access_token']
    with get_session_factory()() as db:
        db.execute(text("UPDATE brands SET status='DISABLED' WHERE id=901"))
        db.commit()
    assert api_client.post(path, json={'items': [ref()]}, headers={'Authorization': f'Bearer {token}'}).json()['data']['items'][0]['status'] == 'ready'


def test_employee_avatar_isolation(api_client):
    with get_session_factory()() as db:
        repo = MediaReadRepository(db)
        actor = SimpleNamespace(id='employee', role='employee', status='active')
        assert repo.resolve(MediaReadReference(**ref(resource_type='avatar', resource_id='other')), actor) is None


def test_only_missing_continues_and_original_fallback_is_bounded(storage):
    repo = SimpleNamespace(resolve=lambda ref, actor: OwnedMedia(f'images/default/brands/{ref.resource_id}/logo.webp', True))
    storage.missing = {key for index in range(1, 4) for key, variant in media_candidates(f'images/default/brands/{index}/logo.webp', 'thumbnail', True) if variant != 'original'}
    request = MediaReadRequest(items=[ref(resource_id=str(index), variant='thumbnail') for index in range(1, 4)])
    data = MediaReadService(repo).authorize(request)
    assert [item.status for item in data.items] == ['ready', 'ready', 'unavailable']
    assert all(item.descriptor.degraded for item in data.items[:2])
    storage.probes.clear()
    storage.fail = AppError(status_code=403, code=50001, message='secret internal diagnostics')
    data = MediaReadService(repo).authorize(MediaReadRequest(items=[ref(variant='thumbnail')]))
    assert len(storage.probes) == 1
    assert 'secret' not in data.model_dump_json()


def test_external_never_fetched_and_cache_is_request_local(storage):
    repo = SimpleNamespace(resolve=lambda ref, actor: OwnedMedia('https://external.example.test/image.jpg', True))
    result = MediaReadService(repo).authorize(MediaReadRequest(items=[ref()]))
    assert result.items[0].descriptor.read_mode == 'external'
    assert result.items[0].descriptor.expires_at is None
    assert not storage.probes
    repo.resolve = lambda ref, actor: OwnedMedia('images/default/brands/901/logo.webp', True)
    service = MediaReadService(repo)
    request = MediaReadRequest(items=[ref(), ref()])
    service.authorize(request)
    assert len(storage.probes) == 1
    service.authorize(request)
    assert len(storage.probes) == 2


@pytest.mark.parametrize('adapter', [S3CompatibleMediaStorageClient, TencentCOSMediaStorageClient])
def test_head_signature_uses_head_method(adapter):
    calls = []
    client = adapter()
    client._client = SimpleNamespace(get_presigned_url=lambda *args, **kwargs: calls.append((args, kwargs)) or 'https://storage.example.test/head')
    assert client.build_direct_head_url('images/default/brands/901/logo.webp', 300).endswith('/head')
    args, kwargs = calls[0]
    assert (kwargs.get('Method') or args[0]) == 'HEAD'


def test_trace_and_request_log_do_not_persist_signed_urls(api_client, storage):
    seed_brand()
    assert api_client.post('/api/v1/media/read-authorizations', json={'items': [ref()]}).status_code == 200
    with get_session_factory()() as db:
        traces = db.execute(text("SELECT metadata FROM task_traces WHERE task_type='media_read_authorization'")).scalars().all()
        logs = db.execute(text("SELECT metadata FROM request_logs WHERE path='/api/v1/media/read-authorizations'")).scalars().all()
    assert traces and logs
    assert 'synthetic-get' not in str(traces + logs)
    assert 'logo.webp' not in str(traces + logs)


def test_own_absolute_url_is_resigned_without_fetching_arbitrary_origin(storage, monkeypatch):
    from app.core.config import settings
    monkeypatch.setattr(settings, 'object_storage_endpoint', 'storage.example.test')
    monkeypatch.setattr(settings, 'object_storage_bucket', 'test-bucket')
    repo = SimpleNamespace(resolve=lambda ref, actor: OwnedMedia('https://test-bucket.storage.example.test/images/default/brands/901/logo.webp?old-signature=synthetic', True))
    data = MediaReadService(repo).authorize(MediaReadRequest(items=[ref()]))
    assert data.items[0].descriptor.read_mode == 'direct'
    assert storage.probes == ['images/default/brands/901/logo.webp']
    assert 'old-signature' not in data.model_dump_json()


def test_sku_media_cannot_be_borrowed_or_read_after_parent_disabled(api_client, storage):
    from test_miniapp_home import _seed_public_catalog
    _seed_public_catalog(api_client)
    with get_session_factory()() as db:
        own = db.execute(text('SELECT id FROM tile_images WHERE tile_id=1 LIMIT 1')).scalar_one()
        other = db.execute(text('SELECT id FROM tile_images WHERE tile_id=2 LIMIT 1')).scalar_one()
    payload = {'items': [ref(resource_type='sku_image', resource_id='1', media_id=own), ref(resource_type='sku_image', resource_id='1', media_id=other), ref(resource_type='sku_image', resource_id='3')]}
    assert [item['status'] for item in api_client.post('/api/v1/media/read-authorizations', json=payload).json()['data']['items']] == ['ready', 'unavailable', 'unavailable']
    with get_session_factory()() as db:
        db.execute(text("UPDATE tile_categories SET status='DISABLED' WHERE id=1"))
        db.commit()
    assert api_client.post('/api/v1/media/read-authorizations', json=payload).json()['data']['items'][0]['status'] == 'unavailable'


def test_upload_session_requires_owner_ready_and_unexpired(api_client, storage):
    from datetime import UTC, timedelta
    from app.modules.media.upload_sessions import UploadSessionRepository, upload_sessions
    from sqlalchemy import update
    actor = SimpleNamespace(id='owner', role='employee', status='active', token_version=0)
    with get_session_factory()() as db:
        repo = UploadSessionRepository(db)
        row = repo.create(owner_id=actor.id, idempotency_key='read-test', media_kind='sku_image', business_id=None,
                          expected_size=128, mime_type='image/webp', part_size=128, mode='proxy',
                          temporary_key='tmp/read-test.webp', stable_key='images/default/tiles/pending/read-test.webp', now=datetime.now(UTC))
        reference = MediaReadReference(resource_type='upload_session', resource_id=row['id'])
        reader = MediaReadRepository(db)
        assert reader.resolve(reference, actor) is None
        db.execute(update(upload_sessions).where(upload_sessions.c.id == row['id']).values(state='ready', actual_mime_type='image/webp'))
        assert reader.resolve(reference, actor).reference == row['stable_key']
        assert reader.resolve(reference, None) is None
        assert reader.resolve(reference, SimpleNamespace(id='other', role='admin', status='active')) is None
        db.execute(update(upload_sessions).where(upload_sessions.c.id == row['id']).values(state='bound'))
        assert reader.resolve(reference, actor) is None
        db.execute(update(upload_sessions).where(upload_sessions.c.id == row['id']).values(state='ready', expires_at=(datetime.now(UTC)-timedelta(seconds=1)).isoformat()))
        assert reader.resolve(reference, actor) is None


def test_ticket_get_head_range_and_revocation(api_client, storage, monkeypatch):
    from app.core.config import settings
    from app.modules.media.storage import StoredMediaObject
    monkeypatch.setattr(settings, 'object_storage_direct_read_enabled', False)
    storage.get_object = lambda key: StoredMediaObject(b'x' * 128, 'image/webp', 128)
    storage.get_object_range = lambda key, offset, length: StoredMediaObject(b'x' * length, 'image/webp', 128)
    seed_brand()
    descriptor = api_client.post('/api/v1/media/read-authorizations', json={'items': [ref()]}).json()['data']['items'][0]['descriptor']
    assert descriptor['read_mode'] == 'proxy'
    assert api_client.get(descriptor['url']).content == b'x' * 128
    head = api_client.head(descriptor['head_url'])
    assert head.status_code == 200 and head.headers['content-length'] == '128' and not head.content
    assert api_client.head(descriptor['url']).status_code == 404
    assert api_client.get(descriptor['head_url']).status_code == 404
    ranged = api_client.get(descriptor['url'], headers={'Range': 'bytes=10-19'})
    assert ranged.status_code == 206 and ranged.headers['content-range'] == 'bytes 10-19/128'
    assert len(ranged.content) == 10 and ranged.headers['cache-control'] == 'no-store'
    assert api_client.get(descriptor['url'], headers={'Range': 'bytes=500-600'}).status_code == 416
    with get_session_factory()() as db:
        db.execute(text("UPDATE brands SET status='DISABLED' WHERE id=901")); db.commit()
    assert api_client.get(descriptor['url']).status_code == 404


def test_ticket_rejects_wrong_purpose_expired_tampered_and_replacement(api_client, storage, monkeypatch):
    from datetime import UTC, timedelta
    from jose import jwt
    from app.core.config import settings
    from app.modules.media.read_tickets import decode_ticket, make_ticket
    reference = MediaReadReference(**ref())
    ticket = make_ticket(reference, 'images/default/brands/901/logo.webp', 'GET')
    with pytest.raises(AppError): decode_ticket(ticket + 'tampered', 'GET')
    with pytest.raises(AppError): decode_ticket(ticket, 'HEAD')
    expired = jwt.encode({'aud':'media-proxy','purpose':'media-read','method':'GET','iat':datetime.now(UTC)-timedelta(seconds=400),'exp':datetime.now(UTC)-timedelta(seconds=100)}, settings.app_secret_key, algorithm=settings.jwt_algorithm)
    with pytest.raises(AppError): decode_ticket(expired, 'GET')
    from app.core.security import create_access_token, decode_access_token
    login_token, _ = create_access_token(user_id='test', role='admin')
    with pytest.raises(AppError): decode_ticket(login_token, 'GET')
    from jose import JWTError
    with pytest.raises(JWTError): decode_access_token(ticket)
    seed_brand()
    with get_session_factory()() as db:
        db.execute(text("UPDATE brands SET logo_object_key='images/default/brands/901/replacement.webp' WHERE id=901")); db.commit()
    assert api_client.get('/api/v1/media/read', params={'ticket':ticket}).status_code == 404


def test_rollout_and_explicit_proxy_never_bypass_storage_failure(storage, monkeypatch):
    from app.core.config import settings
    repo = SimpleNamespace(resolve=lambda ref, actor: OwnedMedia('images/default/brands/901/logo.webp', True))
    service = MediaReadService(repo)
    request = MediaReadRequest(items=[ref()])
    monkeypatch.setattr(settings, 'media_read_clients', 'web_admin')
    assert service.authorize(request, client_type='web_catalog').items[0].descriptor.read_mode == 'proxy'
    assert service.authorize(request, client_type='web_admin').items[0].descriptor.read_mode == 'direct'
    monkeypatch.setattr(settings, 'media_read_kinds', 'sku_video')
    assert service.authorize(request, client_type='web_admin').items[0].descriptor.read_mode == 'proxy'
    proxy = MediaReadRequest(items=[ref()], mode='proxy')
    assert service.authorize(proxy).items[0].status == 'unavailable'
    monkeypatch.setattr(settings, 'media_read_proxy_fallback_enabled', True)
    assert service.authorize(proxy).items[0].descriptor.read_mode == 'proxy'
    storage.fail = AppError(status_code=502, code=50001, message='unavailable')
    assert service.authorize(proxy).items[0].status == 'failed'


def test_proxy_capacity_memory_and_minute_budget(tmp_path, monkeypatch):
    import time
    from app.core.config import settings
    from app.modules.media.read_tickets import SharedProxyBudget, PROXY_MAX_BYTES
    monkeypatch.setattr(settings, "media_read_proxy_budget_dir", str(tmp_path))
    clock = [0]
    monkeypatch.setattr(time, "time", lambda: clock[0])
    budget = SharedProxyBudget()
    with budget.claim(1), budget.claim(1):
        with pytest.raises(AppError):
            with budget.claim(1): pass
    with pytest.raises(AppError):
        with budget.claim(PROXY_MAX_BYTES + 1): pass
    clock[0] = 60
    with budget.claim(PROXY_MAX_BYTES): pass
    with budget.claim(PROXY_MAX_BYTES): pass
    with pytest.raises(AppError):
        with budget.claim(1): pass
    clock[0] = 120
    with budget.claim(1): pass


def test_historical_derivative_does_not_probe_sibling_original(storage):
    key = 'original/default/tiles/901/images/2026/06/photo.jpg'
    candidates = media_candidates(key, 'thumbnail', True)
    assert len(candidates) <= 8
    assert (f'thumbnails/{key}', 'thumbnail') in candidates
    assert all(not candidate.endswith('photo.png') for candidate, _ in candidates)
    storage.missing = {candidate for candidate, _ in candidates if candidate != f'thumbnails/{key}'}
    repo = SimpleNamespace(resolve=lambda ref, actor: OwnedMedia(key, True))
    item = MediaReadService(repo).authorize(MediaReadRequest(items=[ref(variant='thumbnail')])).items[0]
    assert item.status == 'ready' and not item.descriptor.degraded


def test_nested_diagnostics_redact_signed_urls_tickets_and_keys():
    from app.services.log_service import sanitize_metadata
    from app.services.task_trace_service import safe_task_metadata
    from app.modules.media.read_tickets import make_ticket
    ticket = make_ticket(MediaReadReference(**ref()), 'images/default/brands/901/logo.webp', 'GET')
    payload = {'unexpected': ['https://storage.example.test/images/default/test.webp?q-signature=secret', {'note': f'failed /api/v1/media/read?ticket={ticket}'}],
               'detail': 'images/default/brands/901/logo.webp', 'ticket': ticket}
    for sanitize in [sanitize_metadata, safe_task_metadata]:
        result = str(sanitize(payload))
        assert 'secret' not in result and ticket not in result and 'logo.webp' not in result and 'q-signature=' not in result


def test_media_capability_errors_are_never_cached(api_client):
    for response in (
        api_client.get('/api/v1/media/read', params={'ticket': 'invalid'}),
        api_client.post('/api/v1/media/read-authorizations', json={'items': []}),
        api_client.post('/api/v1/admin/media/read-authorizations', json={'items': [ref()]}),
    ):
        assert response.status_code in {401, 404, 422}
        assert response.headers['cache-control'] == 'no-store'
        assert response.headers['referrer-policy'] == 'no-referrer'


def test_access_logs_and_nested_lists_strip_capabilities():
    import logging
    from app.core.media_redaction import MediaAccessLogFilter
    from app.services.log_service import sanitize_metadata
    url = '/api/v1/media/read?ticket=synthetic-secret'
    record = logging.LogRecord('uvicorn.access', logging.INFO, '', 0, '%s %s', ('GET', url), None)
    assert MediaAccessLogFilter().filter(record)
    assert 'synthetic-secret' not in record.getMessage()
    assert sanitize_metadata({'nested': [[url]]}) == {'nested': [['******']]}


def test_shared_proxy_budget_coordinates_instances_and_fails_closed(tmp_path, monkeypatch):
    from app.core.config import settings
    from app.modules.media.read_tickets import SharedProxyBudget, PROXY_MAX_BYTES
    monkeypatch.setattr(settings, "media_read_proxy_budget_dir", str(tmp_path))
    first, second, third = SharedProxyBudget(), SharedProxyBudget(), SharedProxyBudget()
    with first.claim(PROXY_MAX_BYTES):
        with second.claim(PROXY_MAX_BYTES):
            with pytest.raises(AppError) as capacity:
                with third.claim(1): pass
            assert capacity.value.code == 42903
    with pytest.raises(AppError):
        with third.claim(1): pass
    (tmp_path / "bytes.json").write_text('broken')
    with pytest.raises(AppError):
        with first.claim(1): pass


def test_shared_proxy_budget_is_enforced_across_processes(tmp_path, monkeypatch):
    import os
    import subprocess
    import sys
    from pathlib import Path
    from app.core.config import settings
    from app.modules.media.read_tickets import SharedProxyBudget
    monkeypatch.setattr(settings, "media_read_proxy_budget_dir", str(tmp_path))
    child = "from app.modules.media.read_tickets import SharedProxyBudget; from app.core.exceptions import AppError\ntry:\n with SharedProxyBudget().claim(1): print('accepted')\nexcept AppError as e: print(e.code)"
    environment = {**os.environ, "MEDIA_READ_PROXY_BUDGET_DIR": str(tmp_path), "PYTHONPATH": str(Path(__file__).resolve().parents[1] / "src/backend")}
    budget = SharedProxyBudget()
    with budget.claim(1), budget.claim(1):
        result = subprocess.run([sys.executable, "-c", child], env=environment, capture_output=True, text=True, timeout=10)
        assert result.returncode == 0 and result.stdout.strip() == '42903'
    result = subprocess.run([sys.executable, "-c", child], env=environment, capture_output=True, text=True, timeout=10)
    assert result.returncode == 0 and result.stdout.strip() == 'accepted'


def test_legacy_path_requires_current_public_ownership(api_client, storage):
    seed_brand()
    key = 'images/default/brands/901/logo.webp'
    storage.get_object = lambda key: SimpleNamespace(content=b'x' * 128)
    storage.get_object_range = lambda key, start, length: SimpleNamespace(content=b'x' * length)
    response = api_client.get('/media/' + key, headers={'Range': 'bytes=1-4'})
    assert response.status_code == 206
    assert response.content == b'xxxx'
    assert response.headers['cache-control'] == 'no-store'
    assert api_client.head('/media/' + key).status_code == 200
    assert api_client.get('/media/images/default/brands/901/logo.display.webp').status_code == 200
    storage.probes.clear()
    assert api_client.get('/media/images/default/private/secret.webp').status_code == 404
    assert storage.probes == []
    with get_session_factory()() as db:
        db.execute(text("UPDATE brands SET status='DISABLED' WHERE id=901"))
        db.commit()
    response = api_client.get('/media/' + key)
    assert response.status_code == 404
    assert response.headers['cache-control'] == 'no-store'
    assert storage.probes == []


@pytest.mark.parametrize('client_type', ['web_admin', 'web_catalog', 'wechat_miniapp'])
def test_media_events_keep_database_result_contract_and_redact(api_client, client_type):
    import json
    for phase, outcome, result in [('play', 'started', 'success'), ('authorization', 'unavailable', 'failed'), ('recovery', 'success', 'success')]:
        response = api_client.post('/api/v1/usage-events', json={'event_name':'media_read','client_type':client_type,'properties':{'resource_type':'sku_video','variant':'original','phase':phase,'result':result,'outcome':outcome}})
        assert response.status_code == 200
    bad = api_client.post('/api/v1/usage-events', json={'event_name':'media_read','properties':{'resource_type':'sku_video','variant':'original','phase':'play','result':'started'}})
    assert bad.status_code == 400
    with get_session_factory()() as db:
        rows = db.execute(text("SELECT result,metadata FROM usage_events WHERE event_name='media_read'")).all()
    assert len(rows) == 3
    assert {row[0] for row in rows} == {'success','failed'}
    assert {json.loads(row[1])['outcome'] for row in rows} == {'started','unavailable','success'}


def test_exception_tracebacks_strip_storage_capabilities():
    import logging
    import sys
    from app.core.media_redaction import MediaAccessLogFilter
    try:
        raise RuntimeError('read failed https://storage.example.test/images/default/private.webp?X-Amz-Signature=synthetic-secret')
    except RuntimeError:
        record = logging.LogRecord('uvicorn.error', logging.ERROR, '', 0, 'storage failed', (), sys.exc_info())
    MediaAccessLogFilter().filter(record)
    formatted = logging.Formatter().format(record)
    assert 'RuntimeError' in formatted
    assert 'synthetic-secret' not in formatted
    assert 'private.webp' not in formatted


def test_certificate_card_resolves_current_main_image_and_original_attachment(api_client, storage):
    seed_brand()
    with get_session_factory()() as db:
        db.execute(text("""INSERT INTO brand_certificates
          (id,brand_id,name,type,file_url,file_key,file_name,file_mime_type,file_size_bytes,is_permanent,is_visible,created_at,updated_at)
          VALUES (901,901,'测试证书','QUALITY','/media/cert.pdf','cert.pdf','cert.pdf','application/pdf',128,1,1,'2026-09-09','2026-09-09')"""))
        db.execute(text("""INSERT INTO brand_certificate_images
          (id,certificate_id,file_url,file_key,file_name,file_mime_type,file_size_bytes,is_main,created_at,updated_at)
          VALUES (902,901,'/media/images/cert.webp','images/cert.webp','cert.webp','image/webp',128,1,'2026-09-09','2026-09-09')"""))
        db.commit()
        repo = MediaReadRepository(db)
        card = MediaReadReference(**ref(resource_type='certificate', variant='thumbnail'))
        assert repo.resolve(card, None).reference == 'images/cert.webp'
        assert repo.resolve(card.model_copy(update={'variant':'original'}), None).reference == 'cert.pdf'
        assert repo.resolve(card.model_copy(update={'media_id':999}), None) is None
        db.execute(text('UPDATE brand_certificates SET is_visible=0 WHERE id=901'))
        db.commit()
        assert repo.resolve(card, None) is None


def test_registered_store_logo_cannot_select_other_settings(api_client, storage):
    from app.repositories.system_settings_repository import SystemSettingsRepository
    with get_session_factory()() as db:
        SystemSettingsRepository(db).set('miniapp.logo_url', 'images/store.webp', None)
        repo = MediaReadRepository(db)
        logo = MediaReadReference(resource_type='store_logo', resource_id='store', variant='thumbnail')
        assert repo.resolve(logo, None).reference == 'images/store.webp'
        assert repo.resolve(logo.model_copy(update={'resource_id':'app_secret'}), None) is None
        assert repo.resolve(logo.model_copy(update={'media_id':1}), None) is None


def test_external_image_variant_fallback_is_bounded_without_fetch(storage):
    repo = SimpleNamespace(resolve=lambda ref, actor: OwnedMedia('https://external.example.test/image.jpg', True))
    request = MediaReadRequest(items=[ref(resource_id=str(i),variant='thumbnail') for i in range(3)])
    result = MediaReadService(repo).authorize(request)
    assert [item.status for item in result.items] == ['ready','ready','unavailable']
    assert all(item.descriptor.degraded for item in result.items[:2])
    assert not storage.probes
