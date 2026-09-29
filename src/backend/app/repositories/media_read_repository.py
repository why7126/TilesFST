"""Resolve registered business media; never authorize a caller-supplied object key."""

from dataclasses import dataclass
from datetime import UTC, datetime
import json

from sqlalchemy.orm import Session

from app.repositories.system_settings_repository import SystemSettingsRepository
from app.repositories.banner_repository import BannerRepository
from app.repositories.brand_certificate_repository import BrandCertificateRepository
from app.repositories.brand_repository import BrandRepository
from app.repositories.miniapp_home_repository import MiniappHomeRepository
from app.repositories.tile_sku_repository import TileSkuRepository
from app.repositories.user_repository import UserRecord, UserRepository
from app.schemas.media_read import MediaReadReference
from app.modules.media.upload_sessions import UploadSessionRepository, UploadSessionNotFound


@dataclass(frozen=True)
class OwnedMedia:
    reference: str
    is_image: bool
    exact_variant: str | None = None


class MediaReadRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def resolve(self, ref: MediaReadReference, actor: UserRecord | None) -> OwnedMedia | None:
        admin = actor is not None and actor.role in {"admin", "employee"} and actor.status == "active"
        if ref.resource_type == "store_logo":
            if ref.resource_id != "store" or ref.media_id is not None:
                return None
            setting = SystemSettingsRepository(self.db).get("miniapp.logo_url")
            return OwnedMedia(setting.value.strip(), True) if setting and setting.value.strip() else None
        if ref.resource_type == "upload_session":
            if not admin or ref.media_id is not None:
                return None
            try:
                row = UploadSessionRepository(self.db).get(ref.resource_id, actor.id)
            except UploadSessionNotFound:
                return None
            # Bound objects are read through current business visibility, not a stale upload grant.
            if row["state"] != "ready" or datetime.fromisoformat(row["expires_at"]) <= datetime.now(UTC):
                return None
            if row["media_kind"] == "certificate" and actor.role != "admin":
                return None
            image = (row["actual_mime_type"] or "").startswith("image/")
            key = row["stable_key"]
            if ref.variant != "original":
                if not image:
                    return None
                output = json.loads(row["variants_json"] or "{}").get("outputs", {}).get(ref.variant)
                if not output:
                    return None
                key = output["key"]
            return OwnedMedia(key, image, ref.variant)
        if ref.resource_type == "avatar":
            # Employees may read their own avatar; user management belongs to admins.
            if not actor or not (actor.id == ref.resource_id or (admin and actor.role == "admin")):
                return None
            user = UserRepository(self.db).get_by_id(ref.resource_id)
            return OwnedMedia(user.avatar_object_key, True) if user and user.avatar_object_key and ref.media_id is None else None
        if not ref.resource_id.isdecimal():
            return None
        resource_id = int(ref.resource_id)
        if not 0 < resource_id <= 9223372036854775807:
            return None
        public = MiniappHomeRepository(self.db)
        if ref.resource_type in {"sku_image", "sku_video"}:
            repo = TileSkuRepository(self.db)
            resource = repo.get_by_id(resource_id) if admin else public.get_product(resource_id)
            if resource is None:
                return None
            image = ref.resource_type == "sku_image"
            records = repo.list_images(resource_id) if image else repo.list_videos(resource_id)
            media = next((item for item in records if item.id == ref.media_id), None)
            if ref.media_id is None and image:
                media = next((item for item in records if item.is_main), None)
            return OwnedMedia(media.object_key or getattr(media, "url", ""), image) if media else None
        if ref.resource_type == "brand_logo":
            brand = BrandRepository(self.db).get_by_id(resource_id) if admin else public.get_public_brand(resource_id)
            return OwnedMedia(brand.logo_object_key, True) if brand and brand.logo_object_key and ref.media_id is None else None
        if ref.resource_type == "banner_image":
            banner = BannerRepository(self.db).get_by_id(resource_id)
            if not banner or ref.media_id is not None:
                return None
            if not admin and not any(item.id == resource_id for item in public.list_public_banners(position=banner.position)):
                return None
            return OwnedMedia(banner.image_object_key, True) if banner.image_object_key else None
        if ref.resource_type == "certificate":
            if not admin and public.get_public_certificate_detail(resource_id) is None:
                return None
            certificate = BrandCertificateRepository(self.db).get_by_id(resource_id)
            if not certificate or certificate.deleted_at:
                return None
            media = certificate
            if ref.media_id is not None:
                media = next((item for item in public.list_public_certificate_images(resource_id) if item.id == ref.media_id), None)
            elif ref.variant != "original":
                # Card references identify the certificate, whose current main image may
                # coexist with a legacy PDF attachment. Original without media_id is the PDF.
                images = public.list_public_certificate_images(resource_id)
                media = images[0] if images else certificate
            if media is None:
                return None
            return OwnedMedia(media.file_key or media.file_url, (media.file_mime_type or "").startswith("image/"))
        return None
