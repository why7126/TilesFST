"""Admin brand certificate business logic."""

from __future__ import annotations

import json
from datetime import UTC, date, datetime, timedelta

from app.core.exceptions import (
    AuthInvalidRequestError,
    BrandCertificateDateInvalidError,
    BrandCertificateFileRequiredError,
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
from app.schemas.brand_certificate_admin import (
    BrandCertificateCreateRequest,
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
            file_name=record.file_name,
            file_mime_type=record.file_mime_type,
            file_size_bytes=record.file_size_bytes,
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
    ) -> BrandCertificateItem:
        values = self._validate_payload(payload)
        if self._repo.get_by_brand_and_name(brand_id=payload.brand_id, name=values["name"]):
            raise BrandCertificateNameDuplicatedError()
        record = self._repo.create(values)
        self._audit(actor_user_id, "brand_certificate_create", record, "新增品牌证书")
        return self.to_item(record)

    def update_certificate(
        self,
        certificate_id: int,
        payload: BrandCertificateUpdateRequest,
        *,
        actor_user_id: str | None,
    ) -> BrandCertificateItem:
        existing = self._repo.get_by_id(certificate_id)
        if existing is None:
            raise BrandCertificateNotFoundError()
        values = self._validate_payload(payload)
        duplicated = self._repo.get_by_brand_and_name(
            brand_id=payload.brand_id,
            name=values["name"],
            exclude_id=certificate_id,
        )
        if duplicated is not None:
            raise BrandCertificateNameDuplicatedError()
        record = self._repo.update(certificate_id, values)
        assert record is not None
        self._audit(actor_user_id, "brand_certificate_update", record, "编辑品牌证书")
        return self.to_item(record)

    def show_certificate(self, certificate_id: int, *, actor_user_id: str | None) -> BrandCertificateItem:
        record = self._repo.get_by_id(certificate_id)
        if record is None:
            raise BrandCertificateNotFoundError()
        updated = self._repo.set_visibility(certificate_id, True)
        assert updated is not None
        self._audit(actor_user_id, "brand_certificate_show", updated, "显示品牌证书")
        return self.to_item(updated)

    def hide_certificate(self, certificate_id: int, *, actor_user_id: str | None) -> BrandCertificateItem:
        record = self._repo.get_by_id(certificate_id)
        if record is None:
            raise BrandCertificateNotFoundError()
        updated = self._repo.set_visibility(certificate_id, False)
        assert updated is not None
        self._audit(actor_user_id, "brand_certificate_hide", updated, "隐藏品牌证书")
        return self.to_item(updated)

    def delete_certificate(self, certificate_id: int, *, actor_user_id: str | None) -> None:
        record = self._repo.get_by_id(certificate_id)
        if record is None:
            raise BrandCertificateNotFoundError()
        deleted = self._repo.soft_delete(certificate_id)
        if not deleted:
            raise BrandCertificateNotFoundError()
        self._audit(actor_user_id, "brand_certificate_delete", record, "删除品牌证书")

    def _validate_payload(
        self,
        payload: BrandCertificateCreateRequest | BrandCertificateUpdateRequest,
    ) -> dict:
        brand = self._brand_repo.get_by_id(payload.brand_id)
        if brand is None:
            raise BrandNotFoundError()
        name = payload.name.strip()
        if not name:
            raise AuthInvalidRequestError("证书名称不能为空")
        if payload.file is None:
            raise BrandCertificateFileRequiredError()
        if not payload.file.file_key or not payload.file.file_url:
            raise BrandCertificateFileRequiredError()
        effective_date = None if payload.is_permanent else payload.effective_date
        expiry_date = None if payload.is_permanent else payload.expiry_date
        effective = _parse_date(effective_date)
        expiry = _parse_date(expiry_date)
        if not payload.is_permanent and expiry is None:
            raise BrandCertificateDateInvalidError("非长期有效证书必须填写到期日期")
        if effective and expiry and expiry < effective:
            raise BrandCertificateDateInvalidError()
        return {
            "brand_id": payload.brand_id,
            "name": name,
            "sort_order": payload.sort_order,
            "type": payload.type,
            "certificate_no": _normalize_optional(payload.certificate_no, max_len=120),
            "issuer": _normalize_optional(payload.issuer, max_len=120),
            "file_url": payload.file.file_url,
            "file_key": payload.file.file_key,
            "file_name": payload.file.file_name,
            "file_mime_type": payload.file.file_mime_type,
            "file_size_bytes": payload.file.file_size_bytes,
            "is_permanent": int(payload.is_permanent),
            "effective_date": effective_date,
            "expiry_date": expiry_date,
            "is_visible": int(payload.is_visible),
            "remark": _normalize_optional(payload.remark, max_len=500),
        }

    def _audit(
        self,
        actor_user_id: str | None,
        action_type: str,
        record: BrandCertificateRecord,
        action_label: str,
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
        )
