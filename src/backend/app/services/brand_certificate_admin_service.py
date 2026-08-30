"""Admin brand certificate business logic."""

from __future__ import annotations

import json
from datetime import UTC, date, datetime, timedelta

from app.core.exceptions import (
    AuthInvalidRequestError,
    BrandCertificateDateInvalidError,
    BrandCertificateFileRequiredError,
    BrandCertificateImageReferenceInvalidError,
    BrandCertificateMainImageInvalidError,
    BrandCertificateNameDuplicatedError,
    BrandCertificateNotFoundError,
    BrandNotFoundError,
)
from app.repositories.audit_log_repository import AuditLogRepository
from app.repositories.brand_certificate_repository import (
    BrandCertificateRecord,
    BrandCertificateRepository,
)
from app.repositories.brand_repository import BrandRepository
from app.modules.media.business_media import formalize_business_media_object, is_pending_business_media_key
from app.modules.media.storage import same_directory_thumbnail_object_key
from app.schemas.brand_certificate_admin import (
    BrandCertificateCreateRequest,
    BrandCertificateFile,
    BrandCertificateImage,
    BrandCertificateItem,
    BrandCertificateListData,
    BrandCertificateSummary,
    BrandCertificateUpdateRequest,
    CertificateValidityStatus,
)

VALID_PAGE_SIZES = frozenset({20, 50, 100})
CERTIFICATE_TYPES = {"QUALITY", "INSPECTION", "GREEN_BUILDING", "HONOR", "OTHER"}
VALIDITY_STATUSES = {"PERMANENT", "VALID", "EXPIRING_SOON", "EXPIRED", "UNSET"}
DISPLAY_STATUSES = {"VISIBLE", "HIDDEN"}
CERTIFICATE_IMAGE_MIME_TYPES = {"image/jpeg", "image/jpg", "image/png", "image/webp"}
MAX_CERTIFICATE_IMAGES = 9


def _normalize_optional(value: str | None, *, max_len: int) -> str | None:
    if value is None:
        return None
    trimmed = value.strip()
    if not trimmed:
        return None
    return trimmed[:max_len]


def _parse_date(value: str | None) -> date | None:
    if not value:
        return None
    try:
        return date.fromisoformat(value[:10])
    except ValueError as exc:
        raise BrandCertificateDateInvalidError() from exc


def _is_backend_media_reference(file_key: str, file_url: str) -> bool:
    if not file_key or not file_url:
        return False
    if "://" in file_key or file_key.startswith("/"):
        return False
    if ".." in file_key.split("/"):
        return False
    return file_url == f"/media/{file_key}"


def _thumbnail_url(file_key: str, file_mime_type: str | None) -> str | None:
    if file_mime_type not in CERTIFICATE_IMAGE_MIME_TYPES:
        return None
    return f"/media/{same_directory_thumbnail_object_key(file_key)}"


class BrandCertificateAdminService:
    def __init__(
        self,
        repo: BrandCertificateRepository,
        brand_repo: BrandRepository,
        audit_repo: AuditLogRepository,
    ) -> None:
        self._repo = repo
        self._brand_repo = brand_repo
        self._audit_repo = audit_repo

    @staticmethod
    def validity_status(record: BrandCertificateRecord) -> CertificateValidityStatus:
        if record.is_permanent:
            return "PERMANENT"
        expiry = _parse_date(record.expiry_date)
        if expiry is None:
            return "UNSET"
        today = datetime.now(UTC).date()
        if expiry < today:
            return "EXPIRED"
        if expiry <= today + timedelta(days=30):
            return "EXPIRING_SOON"
        return "VALID"

    @classmethod
    def to_item(cls, record: BrandCertificateRecord) -> BrandCertificateItem:
        images = [
            BrandCertificateImage(
                file_url=image.file_url,
                file_key=image.file_key,
                thumbnail_url=_thumbnail_url(image.file_key, image.file_mime_type),
                file_name=image.file_name,
                file_mime_type=image.file_mime_type,
                file_size_bytes=image.file_size_bytes,
                is_main=image.is_main,
                sort_order=image.sort_order,
            )
            for image in record.images
        ]
        if not images and record.file_mime_type in CERTIFICATE_IMAGE_MIME_TYPES:
            images = [
                BrandCertificateImage(
                    file_url=record.file_url,
                    file_key=record.file_key,
                    thumbnail_url=_thumbnail_url(record.file_key, record.file_mime_type),
                    file_name=record.file_name,
                    file_mime_type=record.file_mime_type,
                    file_size_bytes=record.file_size_bytes,
                    is_main=True,
                    sort_order=0,
                )
            ]
        main_image = next((image for image in images if image.is_main), images[0] if images else None)
        return BrandCertificateItem(
            id=record.id,
            brand_id=record.brand_id,
            brand_name=record.brand_name,
            name=record.name,
            sort_order=record.sort_order,
            type=record.type,
            certificate_no=record.certificate_no,
            issuer=record.issuer,
            file_url=record.file_url,
            file_key=record.file_key,
            thumbnail_url=_thumbnail_url(record.file_key, record.file_mime_type),
            file_name=record.file_name,
            file_mime_type=record.file_mime_type,
            file_size_bytes=record.file_size_bytes,
            images=images,
            main_image=main_image,
            is_permanent=record.is_permanent,
            effective_date=record.effective_date,
            expiry_date=record.expiry_date,
            validity_status=cls.validity_status(record),
            is_visible=record.is_visible,
            display_status="VISIBLE" if record.is_visible else "HIDDEN",
            remark=record.remark,
            created_at=record.created_at,
            updated_at=record.updated_at,
        )

    def list_certificates(
        self,
        *,
        page: int,
        page_size: int,
        keyword: str | None,
        brand_id: int | None,
        certificate_type: str | None,
        validity_status: str | None,
        display_status: str | None,
    ) -> BrandCertificateListData:
        page = max(1, page)
        if page_size not in VALID_PAGE_SIZES:
            page_size = 20
        if certificate_type and certificate_type not in CERTIFICATE_TYPES:
            certificate_type = None
        if display_status and display_status not in DISPLAY_STATUSES:
            display_status = None
        if validity_status and validity_status not in VALIDITY_STATUSES:
            validity_status = None

        result = self._repo.list_certificates(
            page=page,
            page_size=page_size,
            keyword=keyword.strip() if keyword else None,
            brand_id=brand_id,
            certificate_type=certificate_type,
            display_status=display_status,
        )
        items = [self.to_item(record) for record in result.items]
        if validity_status:
            items = [item for item in items if item.validity_status == validity_status]

        summary_statuses = [self.validity_status(record) for record in result.summary_rows]
        return BrandCertificateListData(
            items=items,
            page=page,
            page_size=page_size,
            total=result.total if not validity_status else len(items),
            summary=BrandCertificateSummary(
                total=len(result.summary_rows),
                valid_count=sum(1 for status in summary_statuses if status in {"PERMANENT", "VALID"}),
                expiring_soon_count=summary_statuses.count("EXPIRING_SOON"),
                expired_count=summary_statuses.count("EXPIRED"),
            ),
        )

    def get_certificate(self, certificate_id: int) -> BrandCertificateItem:
        record = self._repo.get_by_id(certificate_id)
        if record is None:
            raise BrandCertificateNotFoundError()
        return self.to_item(record)

    def create_certificate(
        self,
        payload: BrandCertificateCreateRequest,
        *,
        actor_user_id: str | None,
        task_trace_id: str | None = None,
        task_type: str | None = None,
    ) -> BrandCertificateItem:
        values, images = self._validate_payload(payload)
        if self._repo.get_by_brand_and_name(brand_id=payload.brand_id, name=values["name"]):
            raise BrandCertificateNameDuplicatedError()
        record = self._repo.create(values, images)
        record = self._formalize_certificate_media_if_needed(record)
        self._audit(actor_user_id, "brand_certificate_create", record, "新增品牌证书", task_trace_id, task_type)
        return self.to_item(record)

    def update_certificate(
        self,
        certificate_id: int,
        payload: BrandCertificateUpdateRequest,
        *,
        actor_user_id: str | None,
        task_trace_id: str | None = None,
        task_type: str | None = None,
    ) -> BrandCertificateItem:
        existing = self._repo.get_by_id(certificate_id)
        if existing is None:
            raise BrandCertificateNotFoundError()
        values, images = self._validate_payload(payload)
        duplicated = self._repo.get_by_brand_and_name(
            brand_id=payload.brand_id,
            name=values["name"],
            exclude_id=certificate_id,
        )
        if duplicated is not None:
            raise BrandCertificateNameDuplicatedError()
        record = self._repo.update(certificate_id, values, images)
        assert record is not None
        record = self._formalize_certificate_media_if_needed(record)
        self._audit(actor_user_id, "brand_certificate_update", record, "编辑品牌证书", task_trace_id, task_type)
        return self.to_item(record)

    def _formalize_certificate_media_if_needed(
        self,
        record: BrandCertificateRecord,
    ) -> BrandCertificateRecord:
        changed = False
        file_key = record.file_key
        file_url = record.file_url
        if is_pending_business_media_key(record.file_key):
            is_image = record.file_mime_type in CERTIFICATE_IMAGE_MIME_TYPES
            usage = "images" if is_image else "files"
            media_kind = "image" if is_image else "file"
            file_key = formalize_business_media_object(
                object_key=record.file_key,
                resource_type="brand-certificates",
                business_id=record.id,
                usage=usage,
                media_kind=media_kind,
            )
            file_url = f"/media/{file_key}"
            changed = True

        images: list[dict] = []
        for image in record.images:
            image_key = image.file_key
            image_url = image.file_url
            if is_pending_business_media_key(image.file_key):
                image_key = formalize_business_media_object(
                    object_key=image.file_key,
                    resource_type="brand-certificates",
                    business_id=record.id,
                    usage="images",
                    media_kind="image",
                )
                image_url = f"/media/{image_key}"
                changed = True
            images.append(
                {
                    "file_url": image_url,
                    "file_key": image_key,
                    "file_name": image.file_name,
                    "file_mime_type": image.file_mime_type,
                    "file_size_bytes": image.file_size_bytes,
                    "is_main": int(image.is_main),
                    "sort_order": image.sort_order,
                }
            )

        if not changed:
            return record

        updated = self._repo.update(
            record.id,
            {
                "brand_id": record.brand_id,
                "name": record.name,
                "sort_order": record.sort_order,
                "type": record.type,
                "certificate_no": record.certificate_no,
                "issuer": record.issuer,
                "file_url": file_url,
                "file_key": file_key,
                "file_name": record.file_name,
                "file_mime_type": record.file_mime_type,
                "file_size_bytes": record.file_size_bytes,
                "is_permanent": int(record.is_permanent),
                "effective_date": record.effective_date,
                "expiry_date": record.expiry_date,
                "is_visible": int(record.is_visible),
                "remark": record.remark,
            },
            images,
        )
        assert updated is not None
        return updated

    def show_certificate(
        self,
        certificate_id: int,
        *,
        actor_user_id: str | None,
        task_trace_id: str | None = None,
        task_type: str | None = None,
    ) -> BrandCertificateItem:
        record = self._repo.get_by_id(certificate_id)
        if record is None:
            raise BrandCertificateNotFoundError()
        updated = self._repo.set_visibility(certificate_id, True)
        assert updated is not None
        self._audit(actor_user_id, "brand_certificate_show", updated, "显示品牌证书", task_trace_id, task_type)
        return self.to_item(updated)

    def hide_certificate(
        self,
        certificate_id: int,
        *,
        actor_user_id: str | None,
        task_trace_id: str | None = None,
        task_type: str | None = None,
    ) -> BrandCertificateItem:
        record = self._repo.get_by_id(certificate_id)
        if record is None:
            raise BrandCertificateNotFoundError()
        updated = self._repo.set_visibility(certificate_id, False)
        assert updated is not None
        self._audit(actor_user_id, "brand_certificate_hide", updated, "隐藏品牌证书", task_trace_id, task_type)
        return self.to_item(updated)

    def delete_certificate(
        self,
        certificate_id: int,
        *,
        actor_user_id: str | None,
        task_trace_id: str | None = None,
        task_type: str | None = None,
    ) -> None:
        record = self._repo.get_by_id(certificate_id)
        if record is None:
            raise BrandCertificateNotFoundError()
        deleted = self._repo.soft_delete(certificate_id)
        if not deleted:
            raise BrandCertificateNotFoundError()
        self._audit(actor_user_id, "brand_certificate_delete", record, "删除品牌证书", task_trace_id, task_type)

    def _validate_payload(
        self,
        payload: BrandCertificateCreateRequest | BrandCertificateUpdateRequest,
    ) -> tuple[dict, list[dict]]:
        brand = self._brand_repo.get_by_id(payload.brand_id)
        if brand is None:
            raise BrandNotFoundError()
        name = payload.name.strip()
        if not name:
            raise AuthInvalidRequestError("证书名称不能为空")
        images = self._normalize_images(payload.images)
        fallback_file = payload.file or self._main_image_as_file(images)
        if fallback_file is None:
            raise BrandCertificateFileRequiredError()
        if not fallback_file.file_key or not fallback_file.file_url:
            raise BrandCertificateFileRequiredError()
        if not _is_backend_media_reference(fallback_file.file_key, fallback_file.file_url):
            raise BrandCertificateImageReferenceInvalidError("证书文件引用无效")
        effective_date = None if payload.is_permanent else payload.effective_date
        expiry_date = None if payload.is_permanent else payload.expiry_date
        effective = _parse_date(effective_date)
        expiry = _parse_date(expiry_date)
        if not payload.is_permanent and expiry is None:
            raise BrandCertificateDateInvalidError("非长期有效证书必须填写到期日期")
        if effective and expiry and expiry < effective:
            raise BrandCertificateDateInvalidError()
        return (
            {
                "brand_id": payload.brand_id,
                "name": name,
                "sort_order": payload.sort_order,
                "type": payload.type,
                "certificate_no": _normalize_optional(payload.certificate_no, max_len=120),
                "issuer": _normalize_optional(payload.issuer, max_len=120),
                "file_url": fallback_file.file_url,
                "file_key": fallback_file.file_key,
                "file_name": fallback_file.file_name,
                "file_mime_type": fallback_file.file_mime_type,
                "file_size_bytes": fallback_file.file_size_bytes,
                "is_permanent": int(payload.is_permanent),
                "effective_date": effective_date,
                "expiry_date": expiry_date,
                "is_visible": int(payload.is_visible),
                "remark": _normalize_optional(payload.remark, max_len=500),
            },
            images,
        )

    def _normalize_images(self, images: list[BrandCertificateImage]) -> list[dict]:
        if len(images) > MAX_CERTIFICATE_IMAGES:
            raise BrandCertificateMainImageInvalidError(f"证书图片最多支持 {MAX_CERTIFICATE_IMAGES} 张")
        if not images:
            return []
        main_count = sum(1 for image in images if image.is_main)
        if main_count != 1:
            raise BrandCertificateMainImageInvalidError()
        normalized: list[dict] = []
        for index, image in enumerate(sorted(images, key=lambda item: item.sort_order)):
            if image.file_mime_type not in CERTIFICATE_IMAGE_MIME_TYPES:
                raise BrandCertificateImageReferenceInvalidError("证书图片仅支持 JPG、PNG、WebP")
            if not _is_backend_media_reference(image.file_key, image.file_url):
                raise BrandCertificateImageReferenceInvalidError()
            normalized.append(
                {
                    "file_url": image.file_url,
                    "file_key": image.file_key,
                    "file_name": image.file_name,
                    "file_mime_type": image.file_mime_type,
                    "file_size_bytes": image.file_size_bytes,
                    "is_main": int(image.is_main),
                    "sort_order": index,
                }
            )
        return normalized

    @staticmethod
    def _main_image_as_file(images: list[dict]) -> BrandCertificateFile | None:
        main_image = next((image for image in images if image["is_main"]), None)
        if main_image is None:
            return None
        return BrandCertificateFile(
            file_url=main_image["file_url"],
            file_key=main_image["file_key"],
            file_name=main_image["file_name"],
            file_mime_type=main_image["file_mime_type"],
            file_size_bytes=main_image["file_size_bytes"],
        )

    def _audit(
        self,
        actor_user_id: str | None,
        action_type: str,
        record: BrandCertificateRecord,
        action_label: str,
        task_trace_id: str | None = None,
        task_type: str | None = None,
    ) -> None:
        self._audit_repo.insert(
            actor_user_id=actor_user_id,
            domain="brand_certificate",
            action_type=action_type,
            summary=f"{action_label}: {record.brand_name} / {record.name}",
            metadata=json.dumps(
                {
                    "brand_id": record.brand_id,
                    "certificate_id": record.id,
                    "certificate_name": record.name,
                    "action": action_type,
                },
                ensure_ascii=False,
            ),
            task_trace_id=task_trace_id,
            task_type=task_type,
        )
