"""Authorized COS upload control; storage calls never run inside write transactions."""
from __future__ import annotations

from datetime import datetime, timedelta, timezone
from math import ceil
import json
from uuid import uuid4

from sqlalchemy import text
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core import error_codes as codes
from app.core.exceptions import AppError, AuthForbiddenError
from app.modules.media.cos_upload import ConfirmedObject, TencentCOSUploadGateway, UploadObjectMismatch, part_length
from app.modules.media.storage import TencentCOSMediaStorageClient
from app.modules.media.upload_sessions import UploadSessionRepository, UploadSessionConflict, utc_timestamp
from app.schemas.upload_session import (
    UploadAuthorization, UploadSessionCreate, UploadSessionCreated, UploadSessionMedia,
    UploadSessionRenewed, UploadSessionStatus,
)

PART_SIZE = 8 * 1024 * 1024
VIDEO_EXTENSIONS = {
    "video/mp4": "mp4", "video/quicktime": "mov", "video/x-msvideo": "avi",
    "video/webm": "webm", "video/x-matroska": "mkv", "video/mpeg": "mpeg", "video/3gpp": "3gp",
}


def get_upload_gateway() -> TencentCOSUploadGateway:
    if settings.effective_object_storage_provider() != "tencent-cos":
        raise AppError(status_code=503, code=codes.STORAGE_UNAVAILABLE, message="直传存储配置不可用")
    storage = TencentCOSMediaStorageClient()
    return TencentCOSUploadGateway(storage._get_client(),
        bucket=settings.effective_object_storage_bucket(),
        region=settings.effective_object_storage_region() or "")


def validate_video_prefix(content: bytes, mime: str) -> None:
    """Container signature check, not full decoding or a malware scan."""
    valid = False
    if mime in {"video/mp4", "video/quicktime", "video/3gpp"} and len(content) >= 16:
        size = int.from_bytes(content[:4], "big")
        brand = content[8:12]
        valid = 16 <= size <= len(content) and content[4:8] == b"ftyp"
        if mime == "video/3gpp":
            valid = valid and brand.startswith(b"3g")
        elif mime == "video/quicktime":
            valid = valid and brand == b"qt  "
        else:
            valid = valid and brand in {b"isom", b"iso2", b"iso4", b"iso5", b"iso6", b"mp41", b"mp42", b"avc1", b"M4V ", b"dash"}
    elif mime == "video/x-msvideo":
        valid = content.startswith(b"RIFF") and content[8:12] == b"AVI "
    elif mime in {"video/webm", "video/x-matroska"}:
        doc_type = b"webm" if mime == "video/webm" else b"matroska"
        valid = content.startswith(bytes.fromhex("1a45dfa3")) and doc_type in content[:4096]
    elif mime == "video/mpeg":
        valid = content.startswith((bytes.fromhex("000001ba"), bytes.fromhex("000001b3")))
    if not valid:
        raise UploadObjectMismatch("Video container differs from declaration")


class UploadSessionService:
    def __init__(self, db: Session, effective, *, gateway_factory=get_upload_gateway, clock=None):
        self.db = db
        self.repo = UploadSessionRepository(db)
        self.effective = effective
        self.gateway_factory = gateway_factory
        self.clock = clock or (lambda: datetime.now(timezone.utc))

    def _access(self, actor, row=None, *, media_kind=None, business_id=None):
        if actor.role not in {"admin", "employee"}:
            raise AuthForbiddenError()
        kind = row["media_kind"] if row else media_kind
        business_id = row["business_id"] if row else business_id
        if kind == "certificate" and actor.role != "admin":
            raise AuthForbiddenError()
        if kind == "avatar" and business_id is not None:
            raise AuthForbiddenError("头像仅允许当前用户上传")
        table = {"sku_video": "tiles", "sku_image": "tiles", "brand_logo": "brands",
                 "certificate": "brands", "banner": "banners"}.get(kind)
        if table and business_id is not None:
            exists = self.db.execute(text(f"SELECT id FROM {table} WHERE id = :id"), {"id": business_id}).first()
            if not exists:
                raise AppError(status_code=404, code=codes.UPLOAD_SESSION_NOT_FOUND, message="上传资源不存在或不可访问")

    def _get(self, session_id, actor, *, active=False):
        self._access(actor)
        row = self.repo.get(session_id, actor.id)
        self._access(actor, row)
        if active and row["expires_at"] <= utc_timestamp(self.clock()):
            raise AppError(status_code=409, code=codes.UPLOAD_SESSION_EXPIRED, message="上传会话已过期，请重新上传")
        return row

    def status(self, row):
        media = None
        if row["state"] in {"ready", "bound"}:
            outputs = json.loads(row["variants_json"] or "{}").get("outputs", {})
            derivative_keys = json.loads(row["object_versions_json"] or "{}").get("derivative_keys", {}) if row["state"] == "bound" else {}
            media = UploadSessionMedia(object_key=row["stable_key"], url="/media/" + row["stable_key"],
                mime_type=row["actual_mime_type"], size=row["actual_size"],
                thumbnail_url="/media/" + derivative_keys.get("thumbnail", outputs["thumbnail"]["key"]) if "thumbnail" in outputs else None,
                display_url="/media/" + derivative_keys.get("display", outputs["display"]["key"]) if "display" in outputs else None,
                original_url="/media/" + row["stable_key"] if row["mime_type"].startswith("image/") else None,
                processing_warning=any(value.get("warning") for value in outputs.values()))
        return UploadSessionStatus(session_id=row["id"], state=row["state"], expires_at=row["expires_at"],
            part_size=row["part_size"], part_count=ceil(row["expected_size"] / row["part_size"]),
            retryable=row["state"] in {"created", "failed"} and row["error_code"] in {str(codes.STORAGE_UNAVAILABLE), "30084"},
            error_code=int(row["error_code"]) if row["error_code"] else None,
            task_trace_id=row["task_trace_id"], media=media)

    def create(self, payload: UploadSessionCreate, actor):
        self._access(actor, media_kind=payload.media_kind, business_id=payload.business_id)
        existing = self.repo.find_idempotent(actor.id, payload.client_idempotency_key)
        if existing:
            if any(existing[field] != getattr(payload, field) for field in
                   ("media_kind", "business_id", "expected_size", "mime_type")):
                raise UploadSessionConflict("Idempotency key has different input")
            if existing["state"] == "created":
                self._initialize(existing)
            return UploadSessionCreated(mode="cos_direct", session=self.query(existing["id"], actor))
        certificate = payload.media_kind == "certificate"
        image = payload.media_kind in {"sku_image", "brand_logo", "banner", "avatar"}
        if payload.media_kind not in {"sku_video", "sku_image", "brand_logo", "banner", "avatar", "certificate"}:
            return UploadSessionCreated(mode="proxy", reason="该媒体尚未启用直传")
        if image and (not settings.object_storage_direct_image_upload_enabled or payload.mime_type not in
                      {"image/jpeg", "image/png", "image/webp"}):
            return UploadSessionCreated(mode="proxy", reason="该图片使用既有上传方式")
        allowed = {"image/jpeg", "image/png", "image/webp", "application/pdf"} if certificate else (self.effective.allowed_image_type_set() if image else self.effective.allowed_video_type_set())
        extensions = {"image/jpeg": "jpg", "image/png": "png", "image/webp": "webp", "application/pdf": "pdf"} if image or certificate else VIDEO_EXTENSIONS
        if payload.mime_type not in allowed or payload.mime_type not in extensions:
            raise AppError(status_code=400, code=codes.FILE_TYPE_NOT_ALLOWED, message="媒体类型不允许")
        max_mb = self.effective.max_file_size_mb() if certificate else (self.effective.max_image_size_mb() if image else self.effective.max_video_size_mb())
        if payload.expected_size > max_mb * 1024 * 1024:
            raise AppError(status_code=400, code=codes.FILE_SIZE_EXCEEDED, message="媒体超过当前大小限制")
        enabled = settings.object_storage_direct_image_upload_enabled if image or certificate else settings.object_storage_direct_video_upload_enabled
        if not enabled or settings.effective_object_storage_provider() != "tencent-cos":
            return UploadSessionCreated(mode="proxy", reason="该媒体直传未启用")
        token = uuid4().hex
        prefix = (settings.object_storage_prefix_images if image or (certificate and payload.mime_type.startswith("image/")) else settings.object_storage_prefix_files if certificate else settings.object_storage_prefix_video).strip("/")
        resource = {"brand_logo": "brand-logos", "banner": "banners", "avatar": "user-avatars", "certificate": "brand-certificates"}.get(payload.media_kind, "tiles")
        row = self.repo.create(owner_id=actor.id, idempotency_key=payload.client_idempotency_key,
            media_kind=payload.media_kind, business_id=payload.business_id, expected_size=payload.expected_size,
            mime_type=payload.mime_type, part_size=PART_SIZE, mode="cos_direct",
            temporary_key=f"{settings.object_storage_prefix_temp.strip('/')}/direct-upload/{token}/source",
            stable_key=f"{prefix}/default/{resource}/{('pending' if certificate else payload.business_id) or 'pending'}/direct-upload/{token}.{extensions[payload.mime_type]}",
            now=self.clock())
        self.db.commit()
        if row["state"] == "created":
            self._initialize(row)
        return UploadSessionCreated(mode="cos_direct", session=self.query(row["id"], actor))

    def _initialize(self, row):
        row = self.repo.reserve_initialization(row, now=self.clock())
        self.db.commit()
        upload_id = None
        gateway = self.gateway_factory()
        try:
            gateway.require_versioning()
            if row["expected_size"] > row["part_size"]:
                upload_id = gateway.initiate(row["temporary_key"], row["mime_type"])
            self.repo.activate(row, upload_id=upload_id, now=self.clock())
            self.db.commit()
        except Exception:
            self.db.rollback()
            try:
                self.repo.release_initialization(row, now=self.clock())
                self.db.commit()
            except UploadSessionConflict:
                self.db.rollback()
            # If a concurrent cancellation won, do not leave a known multipart active.
            if upload_id:
                gateway.abort(row["temporary_key"], upload_id)
            raise

    def query(self, session_id, actor):
        return self.status(self._get(session_id, actor))

    def authorize(self, session_id, actor, part_number=None):
        row = self._get(session_id, actor, active=True)
        if row["state"] != "uploading":
            raise UploadSessionConflict("Upload is not accepting bytes")
        if row["upload_id"]:
            if part_number is None:
                raise UploadSessionConflict("Multipart authorization requires a part")
            length = part_length(row["expected_size"], row["part_size"], part_number)
        else:
            if part_number is not None:
                raise UploadSessionConflict("Simple upload has no parts")
            length = row["expected_size"]
        now = self.clock()
        seconds = min(900, int((datetime.fromisoformat(row["expires_at"]) - now).total_seconds()))
        if seconds <= 0:
            raise AppError(status_code=409, code=codes.UPLOAD_SESSION_EXPIRED, message="上传会话已过期")
        self.db.rollback()  # release read snapshot before network, recheck afterwards
        url = self.gateway_factory().authorize(row["temporary_key"], length=length, expires=seconds,
            upload_id=row["upload_id"], part_number=part_number)
        latest = self._get(session_id, actor, active=True)
        if latest["state"] != "uploading" or latest["version"] != row["version"]:
            raise UploadSessionConflict("Upload changed while authorizing")
        return UploadAuthorization(url=url, length=length, part_number=part_number,
            expires_at=utc_timestamp(now + timedelta(seconds=seconds)))

    def renew(self, session_id, actor):
        row = self._get(session_id, actor, active=True)
        if row["state"] == "created":
            self._initialize(row)
            row = self._get(session_id, actor, active=True)
        if row["state"] != "uploading":
            raise UploadSessionConflict("Upload cannot be renewed")
        authorization = None if row["upload_id"] else self.authorize(session_id, actor)
        return UploadSessionRenewed(session=self.status(row), authorization=authorization)

    def confirm(self, session_id, actor):
        row = self._get(session_id, actor)
        if row["state"] in {"ready", "bound", "processing"}:
            return self.status(row)
        row = self._get(session_id, actor, active=True)
        if row["state"] == "verifying" and row["lease_expires_at"] > utc_timestamp(self.clock()):
            return self.status(row)
        if row["state"] == "failed" and row["error_code"] != str(codes.STORAGE_UNAVAILABLE):
            raise UploadSessionConflict("Invalid content requires a new upload")
        row = self.repo.claim(row, "verifying", now=self.clock())
        self.db.commit()
        gateway = self.gateway_factory()
        try:
            if row["source_version_id"]:
                source = gateway.inspect(row["temporary_key"], version_id=row["source_version_id"], expected_size=row["expected_size"])
            elif row["upload_id"]:
                source = gateway.complete(row["temporary_key"], row["upload_id"], expected_size=row["expected_size"], part_size=row["part_size"])
            else:
                source = gateway.inspect(row["temporary_key"], expected_size=row["expected_size"])
            # Pin the source before any content check or server-side copy.
            row = self.repo.checkpoint(row, now=self.clock(), source_version_id=source.version_id,
                source_etag=source.etag, actual_size=source.size,
                integrity_hash="crc64:" + source.crc64 if source.crc64 else None)
            self.db.commit()
            if source.content_type != row["mime_type"]:
                raise UploadObjectMismatch("Object MIME differs from declaration")
            if row["media_kind"] == "certificate" and row["mime_type"] == "application/pdf":
                prefix = gateway.read_prefix(source)
                if not prefix.startswith(b"%PDF-"):
                    raise UploadObjectMismatch("Certificate PDF signature differs from declaration")
            if row["media_kind"] == "sku_video":
                validate_video_prefix(gateway.read_prefix(source), row["mime_type"])

            row = self.repo.heartbeat(row, now=self.clock())
            self.db.commit()
            stable = gateway.copy_stable(source, row["stable_key"])
            if row["mime_type"] in {"image/jpeg", "image/png", "image/webp"}:
                row = self.repo.checkpoint(row, now=self.clock(), stable_version_id=stable.version_id,
                    actual_mime_type=row["mime_type"])
                row = self.repo.queue_processing(row, now=self.clock(), metadata={
                    "thumbnail_target_kib": self.effective.thumbnail_max_size_kb(),
                    "display_target_kib": self.effective.display_max_size_kb(), "attempt": 0})
            else:
                row = self.repo.finish(row, "ready", now=self.clock(), stable_version_id=stable.version_id,
                    actual_mime_type=row["mime_type"], error_code=None)
            self.db.commit()
            return self.status(row)
        except (AppError, UploadObjectMismatch) as exc:
            self.db.rollback()
            code = exc.code if isinstance(exc, AppError) else codes.UPLOAD_OBJECT_MISMATCH
            try:
                self.repo.finish(row, "failed", now=self.clock(), error_code=str(code))
                self.db.commit()
            except UploadSessionConflict:
                self.db.rollback()  # cancellation or lease takeover must remain authoritative
            raise

    def retry_processing(self, session_id, actor):
        row = self._get(session_id, actor, active=True)
        if row["state"] in {"processing", "ready", "bound"}:
            return self.status(row)
        if row["state"] != "failed" or row["error_code"] != "30084":
            raise UploadSessionConflict("No failed image processing task")
        metadata = json.loads(row["variants_json"] or "{}")
        metadata.update(attempt=0, failure=None)
        row = self.repo.queue_processing(row, now=self.clock(), metadata=metadata)
        self.db.commit()
        return self.status(row)

    def cancel(self, session_id, actor):
        row = self._get(session_id, actor)
        row = self.repo.cancel(row, now=self.clock())
        self.db.commit()  # persist the terminal state even when COS abort fails
        if row["upload_id"]:
            self.gateway_factory().abort(row["temporary_key"], row["upload_id"])
        return self.status(row)
