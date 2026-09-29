"""Bind verified direct SKU media with the business reference in one DB transaction."""
from datetime import datetime, timezone
from functools import wraps
import json
import re
from time import perf_counter

from app.modules.media.upload_observability import record_upload_span

from sqlalchemy import select, text, or_

from app.core.exceptions import AppError
from app.core.error_codes import UPLOAD_SESSION_CONFLICT, UPLOAD_SESSION_NOT_FOUND
from app.modules.media.upload_sessions import UploadSessionRepository, UploadSessionConflict, upload_sessions
from app.services.upload_session_service import get_upload_gateway
from app.modules.media.storage import same_directory_thumbnail_object_key, same_directory_display_object_key


def _state_errors(operation):
    @wraps(operation)
    def wrapped(*args, **kwargs):
        try:
            return operation(*args, **kwargs)
        except UploadSessionConflict:
            raise AppError(status_code=409, code=UPLOAD_SESSION_CONFLICT, message="媒体状态已变化，请刷新后重试") from None
    return wrapped


RESOURCES = {"sku_video": ("tiles", "tile_videos", "tile_id", "object_key"),
             "sku_image": ("tiles", "tile_images", "tile_id", "object_key"),
             "brand_logo": ("brand-logos", "brands", "id", "logo_object_key"),
             "banner": ("banners", "banners", "id", "image_object_key"),
             "avatar": ("user-avatars", "users", "id", "avatar_object_key"),
             "certificate": ("brand-certificates", "brand_certificates", "id", "file_key")}


class VideoUploadBinding:
    def __init__(self, db, actor_id, *, gateway_factory=None):
        self.db = db
        self.actor_id = actor_id
        self.repo = UploadSessionRepository(db)
        self.gateway_factory = gateway_factory or get_upload_gateway

    @staticmethod
    def now():
        return datetime.now(timezone.utc)

    def resolve(self, videos, business_id=None, *, media_kind="sku_video", context_id=None):
        if media_kind not in RESOURCES:
            raise ValueError("Unsupported binding kind")
        resource, table, id_column, key_column = RESOURCES[media_kind]
        rows = []
        for video in videos:
            key = video["object_key"]
            if "/direct-upload/" not in key:
                continue  # existing proxy/legacy media retain their current contract
            suffix = key.rsplit("/direct-upload/", 1)[-1]
            if not re.fullmatch(r"[a-f0-9]{32}\.[a-z0-9]+", suffix):
                raise AppError(status_code=404, code=UPLOAD_SESSION_NOT_FOUND, message="媒体尚未确认或不可访问")
            row = self.db.execute(select(upload_sessions).where(or_(
                upload_sessions.c.stable_key == key,
                upload_sessions.c.stable_key.like("%/direct-upload/" + suffix),
            ))).mappings().one_or_none()
            if row is None or row["media_kind"] != media_kind:
                raise AppError(status_code=404, code=UPLOAD_SESSION_NOT_FOUND, message="媒体尚未确认或不可访问")
            row = dict(row)
            pending_key = row["stable_key"].replace("/" + resource + "/" + str(row["bound_business_id"]) + "/", "/" + resource + "/pending/", 1)
            if key != row["stable_key"] and not ((row["business_id"] is None or media_kind == "certificate") and key == pending_key):
                raise AppError(status_code=404, code=UPLOAD_SESSION_NOT_FOUND, message="媒体尚未确认或不可访问")
            if row["state"] == "bound" and business_id is not None and row["bound_business_id"] == str(business_id):
                existing = self.db.execute(text(f"SELECT 1 FROM {table} WHERE {id_column}=:id AND {key_column}=:key"), {"id": business_id, "key": row["stable_key"]}).first()
                if not existing and media_kind == "certificate":
                    existing = self.db.execute(text("SELECT 1 FROM brand_certificate_images WHERE certificate_id=:id AND file_key=:key"),
                                               {"id": business_id, "key": row["stable_key"]}).first()
                if existing:
                    row["existing_binding"] = True
                    rows.append(row)
                    continue  # another admin may retain an already attached video
            expected_context = context_id if media_kind == "certificate" else business_id
            if row["owner_id"] != self.actor_id or row["business_id"] not in {None, expected_context}:
                raise AppError(status_code=404, code=UPLOAD_SESSION_NOT_FOUND, message="媒体尚未确认或不可访问")
            if row["mime_type"].startswith("image/") and row["state"] in {"ready", "binding", "bound"}:
                outputs = json.loads(row["variants_json"] or "{}").get("outputs", {})
                if set(outputs) != {"thumbnail", "display"}:
                    raise AppError(status_code=409, code=UPLOAD_SESSION_CONFLICT, message="图片派生未就绪，不能保存")
            if row["state"] not in {"ready", "binding", "bound"}:
                raise AppError(status_code=409, code=UPLOAD_SESSION_CONFLICT, message="媒体未就绪，不能保存")
            if row["bound_business_id"] and business_id is not None and row["bound_business_id"] != str(business_id):
                raise AppError(status_code=409, code=UPLOAD_SESSION_CONFLICT, message="媒体已关联其他业务")
            if row["id"] not in {item["id"] for item in rows}:
                rows.append(row)
        return rows

    @_state_errors
    def claim(self, rows, business_id):
        self._binding_started = perf_counter()
        claimed = []
        for row in rows:
            if row.get("existing_binding"):
                claimed.append(row)
                continue
            if row["state"] == "bound":
                raise UploadSessionConflict("Completed binding cannot be reused for a new business")
            row = self.repo.claim(row, "binding", now=self.now())
            row = self.repo.checkpoint(row, now=self.now(), bound_business_id=str(business_id))
            claimed.append(row)
        return claimed

    @_state_errors
    def copy(self, rows):
        # Caller committed reservations and releases any read snapshot before COS.
        self.db.rollback()
        copied = []
        for row in rows:
            if row.get("existing_binding"):
                copied.append(row)
                continue
            resource = RESOURCES[row["media_kind"]][0]
            copy_started = perf_counter()
            target = row["stable_key"].replace("/" + resource + "/pending/", "/" + resource + "/" + row["bound_business_id"] + "/", 1)
            if target != row["stable_key"]:
                gateway = self.gateway_factory()
                source = gateway.inspect(row["stable_key"], version_id=row["stable_version_id"], expected_size=row["actual_size"])
                stable = gateway.copy_stable(source, target)
                manifest = {"formal_key": target, "formal_version": stable.version_id}
                row = self.repo.checkpoint(row, now=self.now(), object_versions_json=json.dumps(manifest))
                self.db.commit()
            if row["mime_type"].startswith("image/"):
                gateway = self.gateway_factory()
                outputs = json.loads(row["variants_json"])["outputs"]
                manifest = json.loads(row["object_versions_json"] or "{}")
                derivative_keys = {"thumbnail": same_directory_thumbnail_object_key(target),
                                   "display": same_directory_display_object_key(target)}
                manifest["derivative_keys"] = derivative_keys
                row = self.repo.checkpoint(row, now=self.now(), object_versions_json=json.dumps(manifest)); self.db.commit()
                for name, key in derivative_keys.items():
                    item = outputs[name]
                    source = gateway.inspect(item["key"], version_id=item["version_id"], expected_size=item["size"])
                    copied_object = gateway.copy_stable(source, key)
                    manifest.setdefault("derivative_versions", {})[name] = copied_object.version_id
                    row = self.repo.checkpoint(row, now=self.now(), object_versions_json=json.dumps(manifest)); self.db.commit()
            record_upload_span(self.db, row, 'binding_copy', duration_ms=round((perf_counter()-copy_started)*1000),
                metadata={'duration_scope':'component_in_binding','file_size_bytes':row['actual_size']})
            copied.append(row)
        return copied

    @_state_errors
    def finish(self, rows, videos):
        replacements = {}
        for row in rows:
            manifest = json.loads(row["object_versions_json"] or "{}")
            target = manifest.get("formal_key", row["stable_key"])
            version = manifest.get("formal_version", row["stable_version_id"])
            if not row.get("existing_binding"):
                self.repo.finish(row, "bound", now=self.now(), stable_key=target, stable_version_id=version)
            replacements[row["stable_key"]] = (target, row["actual_size"], row["media_kind"])
            if (row["business_id"] is None or row["media_kind"] == "certificate") and row["bound_business_id"]:
                resource = RESOURCES[row["media_kind"]][0]
                pending = target.replace("/" + resource + "/" + row["bound_business_id"] + "/", "/" + resource + "/pending/", 1)
                replacements[pending] = replacements[row["stable_key"]]
        output = []
        for video in videos:
            item = dict(video)
            if item["object_key"] in replacements:
                item["object_key"], size, kind = replacements[item["object_key"]]
                if kind != "sku_video":
                    item["url"] = "/media/" + item["object_key"]
                else:
                    item["file_size_bytes"] = size
            output.append(item)
        return output

    def record_bound(self, rows, *, success=True):
        duration = round((perf_counter()-self._binding_started)*1000) if hasattr(self, '_binding_started') else None
        for row in rows:
            if not row.get('existing_binding'):
                record_upload_span(self.db, row, 'binding', duration_ms=duration,
                    status='success' if success else 'failed',
                    metadata={'duration_scope':'inclusive_business_commit','file_size_bytes':row['actual_size']})

    def release(self, rows):
        self.db.rollback()
        for row in rows:
            current = self.repo.get(row["id"], row["owner_id"])
            if current["state"] == "binding" and current["lease_token"] == row["lease_token"]:
                try:
                    self.repo.finish(current, "ready", now=self.now())
                    self.db.commit()
                except UploadSessionConflict:
                    self.db.rollback()
        self.record_bound(rows, success=False)


def save_with_avatar(repository, actor_id, object_key, business_id, save):
    """Run the business write and avatar binding atomically; never persist passwords in sessions."""
    from uuid import uuid4
    if not object_key or "/direct-upload/" not in object_key:
        return save(business_id, object_key)
    binding = VideoUploadBinding(repository.db, actor_id)
    media = [{"object_key": object_key}]
    rows = binding.resolve(media, business_id, media_kind="avatar")
    target_id = business_id or rows[0]["bound_business_id"] or str(uuid4())
    with repository.atomic():
        rows = binding.claim(rows, target_id)
    try:
        rows = binding.copy(rows)
        with repository.atomic():
            key = binding.finish(rows, media)[0]["object_key"]
            result = save(target_id, key)
            if result is None:
                raise AppError(status_code=409, code=UPLOAD_SESSION_CONFLICT, message="用户已变化，请刷新后重试")
        binding.record_bound(rows)
        return result
    except Exception:
        binding.release(rows)
        raise
