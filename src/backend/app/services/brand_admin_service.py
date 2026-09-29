"""Admin brand management business logic."""

from __future__ import annotations

from app.core.exceptions import (
    AuthInvalidRequestError,
    BrandDeleteForbiddenError,
    BrandInvalidSortOrderError,
    BrandNameDuplicatedError,
    BrandNotFoundError,
)
from app.modules.media.upload_binding import VideoUploadBinding
from app.repositories.brand_certificate_repository import BrandCertificateRepository
from app.repositories.brand_repository import BrandRecord, BrandRepository
from app.modules.media.business_media import formalize_business_media_object, is_pending_business_media_key
from app.modules.media.storage import same_directory_thumbnail_object_key
from app.schemas.brand_admin import (
    BrandAdminItem,
    BrandAdminListData,
    BrandAdminSummary,
    BrandCreateRequest,
    BrandUpdateRequest,
)

VALID_PAGE_SIZES = frozenset({20, 50, 100})


def _logo_url(object_key: str | None) -> str | None:
    if not object_key:
        return None
    return f"/media/{object_key}"


def _logo_thumbnail_url(object_key: str | None) -> str | None:
    if not object_key:
        return None
    return f"/media/{same_directory_thumbnail_object_key(object_key)}"


def _normalize_optional(value: str | None, *, max_len: int) -> str | None:
    if value is None:
        return None
    trimmed = value.strip()
    if not trimmed:
        return None
    return trimmed[:max_len]


class BrandAdminService:
    def __init__(
        self,
        repo: BrandRepository,
        certificate_repo: BrandCertificateRepository | None = None,
        actor_id: str | None = None,
    ) -> None:
        self._repo = repo
        self._certificate_repo = certificate_repo
        self._logo_binding = VideoUploadBinding(repo.db, actor_id)

    @staticmethod
    def to_item(brand: BrandRecord) -> BrandAdminItem:
        return BrandAdminItem(
            id=brand.id,
            name=brand.name,
            sort_order=brand.sort_order,
            short_name=brand.short_name,
            english_name=brand.english_name,
            logo_object_key=brand.logo_object_key,
            logo_url=_logo_url(brand.logo_object_key),
            logo_thumbnail_url=_logo_thumbnail_url(brand.logo_object_key),
            description=brand.description,
            status=brand.status,
            sku_count=brand.sku_count,
            created_at=brand.created_at,
            updated_at=brand.updated_at,
        )

    @staticmethod
    def _validate_sort_order(sort_order: int) -> None:
        if sort_order < 1:
            raise BrandInvalidSortOrderError()

    @staticmethod
    def _validate_name(name: str) -> str:
        trimmed = name.strip()
        if not trimmed:
            raise AuthInvalidRequestError("品牌名称不能为空")
        if len(trimmed) > 50:
            raise AuthInvalidRequestError("品牌名称不能超过 50 个字符")
        return trimmed

    def list_brands(
        self,
        *,
        page: int,
        page_size: int,
        keyword: str | None,
        status: str | None,
    ) -> BrandAdminListData:
        if page_size not in VALID_PAGE_SIZES:
            page_size = 20
        if page < 1:
            page = 1
        if status and status not in {"ENABLED", "DISABLED"}:
            status = None

        result = self._repo.list_brands(
            page=page,
            page_size=page_size,
            keyword=keyword.strip() if keyword else None,
            status=status,
        )
        summary = result.summary
        return BrandAdminListData(
            items=[self.to_item(brand) for brand in result.items],
            page=page,
            page_size=page_size,
            total=result.total,
            summary=BrandAdminSummary(
                total=summary["total"],
                enabled_count=summary["enabled_count"],
                disabled_count=summary["disabled_count"],
                unlinked_sku_count=summary["unlinked_sku_count"],
            ),
        )

    def get_brand(self, brand_id: int) -> BrandAdminItem:
        brand = self._repo.get_by_id(brand_id)
        if brand is None:
            raise BrandNotFoundError()
        return self.to_item(brand)

    def create_brand(self, payload: BrandCreateRequest) -> BrandAdminItem:
        if payload.logo_object_key and "/direct-upload/" in payload.logo_object_key:
            return self._save_direct_logo(payload)
        name = self._validate_name(payload.name)
        self._validate_sort_order(payload.sort_order)
        if self._repo.get_by_name(name):
            raise BrandNameDuplicatedError()

        brand = self._repo.create(
            name=name,
            sort_order=payload.sort_order,
            short_name=_normalize_optional(payload.short_name, max_len=30),
            english_name=_normalize_optional(payload.english_name, max_len=80),
            logo_object_key=payload.logo_object_key,
            description=_normalize_optional(payload.description, max_len=500),
        )
        brand = self._formalize_logo_if_needed(brand)
        return self.to_item(brand)

    def update_brand(self, brand_id: int, payload: BrandUpdateRequest) -> BrandAdminItem:
        if payload.logo_object_key and "/direct-upload/" in payload.logo_object_key:
            return self._save_direct_logo(payload, brand_id)
        brand = self._repo.get_by_id(brand_id)
        if brand is None:
            raise BrandNotFoundError()

        name = self._validate_name(payload.name)
        self._validate_sort_order(payload.sort_order)
        existing = self._repo.get_by_name(name, exclude_id=brand_id)
        if existing:
            raise BrandNameDuplicatedError()

        updated = self._repo.update(
            brand_id,
            name=name,
            sort_order=payload.sort_order,
            short_name=_normalize_optional(payload.short_name, max_len=30),
            english_name=_normalize_optional(payload.english_name, max_len=80),
            logo_object_key=payload.logo_object_key,
            description=_normalize_optional(payload.description, max_len=500),
        )
        assert updated is not None
        updated = self._formalize_logo_if_needed(updated)
        return self.to_item(updated)

    def _save_direct_logo(self, payload, brand_id=None):
        name = self._validate_name(payload.name)
        self._validate_sort_order(payload.sort_order)
        binding = self._logo_binding
        media = [{"object_key": payload.logo_object_key}]
        rows = binding.resolve(media, brand_id, media_kind="brand_logo")
        row = rows[0]
        creating = brand_id is None
        if creating and row["bound_business_id"]:
            brand_id = int(row["bound_business_id"])
            if row["state"] == "bound":
                return self.get_brand(brand_id)
        if brand_id is not None and self._repo.get_by_id(brand_id) is None:
            raise BrandNotFoundError()
        if self._repo.get_by_name(name, exclude_id=brand_id):
            raise BrandNameDuplicatedError()
        values = dict(name=name, sort_order=payload.sort_order,
                      short_name=_normalize_optional(payload.short_name, max_len=30),
                      english_name=_normalize_optional(payload.english_name, max_len=80),
                      description=_normalize_optional(payload.description, max_len=500))
        with self._repo.atomic():
            if brand_id is None:
                # A failed copy leaves a disabled reservation with no media reference.
                brand_id = self._repo.create(**values, logo_object_key=None, status="DISABLED").id
            rows = binding.claim(rows, brand_id)
        try:
            rows = binding.copy(rows)
            with self._repo.atomic():
                key = binding.finish(rows, media)[0]["object_key"]
                updated = self._repo.update(brand_id, **values, logo_object_key=key)
                if updated is None:
                    raise BrandNotFoundError()
                if creating:
                    self._repo.update_status(brand_id, "ENABLED")
            binding.record_bound(rows)
            return self.get_brand(brand_id)
        except Exception:
            binding.release(rows)
            raise

    def _formalize_logo_if_needed(self, brand: BrandRecord) -> BrandRecord:
        object_key = brand.logo_object_key
        if not object_key or not is_pending_business_media_key(object_key):
            return brand
        target_key = formalize_business_media_object(
            object_key=object_key,
            resource_type="brand-logos",
            business_id=brand.id,
            usage="logos",
            media_kind="image",
        )
        updated = self._repo.update(
            brand.id,
            name=brand.name,
            sort_order=brand.sort_order,
            short_name=brand.short_name,
            english_name=brand.english_name,
            logo_object_key=target_key,
            description=brand.description,
        )
        assert updated is not None
        return updated

    def enable_brand(self, brand_id: int) -> BrandAdminItem:
        brand = self._repo.get_by_id(brand_id)
        if brand is None:
            raise BrandNotFoundError()
        updated = self._repo.update_status(brand_id, "ENABLED")
        assert updated is not None
        return self.to_item(updated)

    def disable_brand(self, brand_id: int) -> BrandAdminItem:
        brand = self._repo.get_by_id(brand_id)
        if brand is None:
            raise BrandNotFoundError()
        updated = self._repo.update_status(brand_id, "DISABLED")
        assert updated is not None
        return self.to_item(updated)

    def delete_brand(self, brand_id: int) -> None:
        brand = self._repo.get_by_id(brand_id)
        if brand is None:
            raise BrandNotFoundError()
        if self._certificate_repo and self._certificate_repo.count_active_by_brand(brand_id) > 0:
            raise BrandDeleteForbiddenError("品牌存在未删除证书，请先迁移或删除证书")
        if brand.sku_count != 0 or brand.status != "DISABLED":
            raise BrandDeleteForbiddenError()
        self._repo.delete(brand_id)
