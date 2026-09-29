"""Expired direct-upload cleanup, scoped to session-owned keys and exact versions."""
from app.modules.media.upload_observability import record_upload_span, prune_upload_observability
from datetime import datetime, timezone
import argparse
import json
import time

from sqlalchemy import select, text

from app.core.config import settings
from app.db.session import get_session_factory
from app.modules.media.upload_sessions import UploadSessionRepository, UploadSessionConflict, upload_sessions, utc_timestamp
from app.services.upload_session_service import get_upload_gateway

REFERENCE_COLUMNS = (
    ('tile_videos', 'object_key'), ('tile_images', 'object_key'), ('tile_images', 'url'),
    ('users', 'avatar_object_key'), ('brands', 'logo_object_key'), ('banners', 'image_object_key'),
    ('topics', 'cover_object_key'), ('brand_certificates', 'file_key'),
    ('brand_certificates', 'file_url'), ('brand_certificate_images', 'file_key'),
    ('brand_certificate_images', 'file_url'),
)


def referenced(db, keys):
    # Do not exclude deleted/hidden records: historical references remain protected.
    for table, column in REFERENCE_COLUMNS:
        for key in keys:
            if db.execute(text(f'SELECT 1 FROM {table} WHERE {column}=:key OR {column}=:url LIMIT 1'),
                          {'key': key, 'url': '/media/' + key}).first():
                return True
    return False


def cleanup_session(db, row, gateway, *, clock=None, reference_check=referenced):
    now = clock or (lambda: datetime.now(timezone.utc))
    repo = UploadSessionRepository(db)
    if row['state'] == 'bound':
        return {'state': 'protected', 'deleted_versions': 0, 'aborted_uploads': 0}
    keys = {row['temporary_key'], row['stable_key']}
    metadata = json.loads(row.get('variants_json') or '{}')
    for key in metadata.get('planned_keys', []):
        if not key.startswith(row['stable_key'] + '.processing/'):
            raise UploadSessionConflict('Derivative cleanup key is outside session scope')
        keys.add(key)
    resource = {"brand_logo": "brand-logos", "banner": "banners", "avatar": "user-avatars", "certificate": "brand-certificates"}.get(row["media_kind"], "tiles")
    pending = "/" + resource + "/pending/"
    if row["bound_business_id"] and pending in row["stable_key"]:
        keys.add(row["stable_key"].replace(pending, "/" + resource + "/" + row["bound_business_id"] + "/", 1))
    manifest = json.loads(row.get('object_versions_json') or '{}')
    from app.modules.media.storage import same_directory_thumbnail_object_key, same_directory_display_object_key
    formal = manifest.get('formal_key', row['stable_key'])
    expected_derivatives = {same_directory_thumbnail_object_key(formal), same_directory_display_object_key(formal)}
    for key in manifest.get('derivative_keys', {}).values():
        if key not in expected_derivatives:
            raise UploadSessionConflict('Derivative cleanup key is outside business scope')
        keys.add(key)
    if row['state'] == 'bound' or reference_check(db, keys):
        return {'state': 'protected', 'deleted_versions': 0, 'aborted_uploads': 0}
    row = repo.reserve_cleanup(row, now=now())
    db.commit()
    if reference_check(db, keys):
        db.rollback()
        return {'state': 'protected', 'deleted_versions': 0, 'aborted_uploads': 0}
    db.rollback()
    deleted = aborted = 0
    for upload_id in gateway.multipart_uploads(row['temporary_key']):
        row = repo.heartbeat(row, now=now()); db.commit()
        gateway.abort(row['temporary_key'], upload_id)
        aborted += 1
    for key in sorted(keys):
        for version in gateway.versions(key):
            row = repo.heartbeat(row, now=now()); db.commit()
            gateway.delete_version(key, version)
            deleted += 1
    repo.finish(row, 'cleaned', now=now()); db.commit()
    record_upload_span(db, row, 'cleanup', metadata={'deleted_versions':deleted, 'aborted_uploads':aborted})
    return {'state': 'cleaned', 'deleted_versions': deleted, 'aborted_uploads': aborted}


def run_once(*, limit=50, apply=False):
    summary = {'candidates': 0, 'cleaned': 0, 'protected': 0, 'failed': 0, 'deleted_versions': 0, 'aborted_uploads': 0}
    if settings.effective_object_storage_provider() != 'tencent-cos':
        return summary
    with get_session_factory()() as db:
        rows = db.execute(select(upload_sessions).where(
            upload_sessions.c.expires_at <= utc_timestamp(datetime.now(timezone.utc)),
            upload_sessions.c.state != 'bound',
        ).order_by(upload_sessions.c.updated_at).limit(limit)).mappings().all()
        db.rollback()
        summary['candidates'] = len(rows)
        if not apply:
            try:
                summary['observability_retention'] = prune_upload_observability(db)
            except Exception:
                summary['observability_retention_failed'] = True
            return summary
        gateway = get_upload_gateway()
        for row in rows:
            try:
                result = cleanup_session(db, dict(row), gateway)
                summary[result['state']] += 1
                summary['deleted_versions'] += result['deleted_versions']
                summary['aborted_uploads'] += result['aborted_uploads']
            except UploadSessionConflict:
                db.rollback()
                summary['protected'] += 1
            except Exception:
                db.rollback()
                summary['failed'] += 1
    try:
        with get_session_factory()() as db:
            summary['observability_retention'] = prune_upload_observability(db, apply=apply)
    except Exception:
        summary['observability_retention_failed'] = True
    return summary


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='清理已过期且无业务引用的直传会话')
    parser.add_argument('--loop', action='store_true', help='每小时执行一次，适合专用 worker')
    parser.add_argument('--apply', action='store_true', help='执行删除，默认仅统计候选')
    parser.add_argument('--confirm-backup', action='store_true', help='确认数据库和对象存储备份完成')
    args = parser.parse_args()
    if args.apply and not args.confirm_backup:
        parser.error('--apply 需要 --confirm-backup')
    while True:
        print(json.dumps(run_once(apply=args.apply)), flush=True)  # counts only; never keys or signed URLs
        if not args.loop:
            break
        time.sleep(3600)
