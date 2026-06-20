"""Admin tile SKU management business logic."""

from __future__ import annotations

from app.core.exceptions import (
    AuthInvalidRequestError,
    TileSkuCodeDuplicatedError,
    TileSkuDeleteForbiddenError,
    TileSkuNotFoundError,
    TileSkuPublishForbiddenError,
)
from app.repositories.tile_sku_repository import TileSkuRecord, TileSkuRepository
from app.schemas.tile_sku_admin import (
    MaterialCompleteness,
    TileSkuAdminItem,
    TileSkuAdminListData,
    TileSkuAdminSummary,
    TileSkuCreateRequest,
    TileSkuImageInput,
    TileSkuImageItem,
    TileSkuUpdateRequest,
    TileSkuVideoInput,
    TileSkuVideoItem,
)

VALID_PAGE_SIZES = frozenset({10, 20, 50, 100})


def _video_url(object_key: str) -> str:
    return f"/media/{object_key}"


class TileSkuAdminService:
    def __init__(self, repo: TileSkuRepository) -> None:
        self._repo = repo

    @staticmethod
    def _normalize_optional(value: str | None, *, max_len: int) -> str | None:
        if value is None:
            return None
        trimmed = value.strip()
        if not trimmed:
            return None
        return trimmed[:max_len]

    @staticmethod
    def _normalize_images(images: list[TileSkuImageInput]) -> list[dict]:
        if not images:
            return []
        normalized: list[dict] = []
        main_index: int | None = None
        for idx, img in enumerate(images):
            if img.is_main:
                main_index = idx
            normalized.append(
                {
                    "object_key": img.object_key.strip(),
                    "url": img.url.strip(),
                    "is_main": img.is_main,
                    "sort_order": img.sort_order if img.sort_order else idx,
                }
            )
        if main_index is None and normalized:
            normalized[0]["is_main"] = True
        elif main_index is not None:
            for i, item in enumerate(normalized):
                item["is_main"] = i == main_index
        return normalized

    @staticmethod
    def _normalize_videos(videos: list[TileSkuVideoInput]) -> list[dict]:
        return [
            {
                "object_key": vid.object_key.strip(),
                "file_name": vid.file_name.strip(),
                "file_size_bytes": vid.file_size_bytes,
                "duration_seconds": vid.duration_seconds,
                "sort_order": vid.sort_order if vid.sort_order else idx,
            }
            for idx, vid in enumerate(videos)
        ]

    def _resolve_status_after_save(self, *, has_main_image: bool, save_mode: str) -> str:
        if save_mode == "create" and not has_main_image:
            return "NEEDS_COMPLETION"
        return "DRAFT"

    def _resolve_draft_defaults(
        self,
        payload: TileSkuCreateRequest,
    ) -> tuple[str, int, int, str, str]:
        sku_code = (payload.sku_code or "").strip() or self._repo.generate_draft_sku_code()
        brand_id = payload.brand_id or self._repo.get_first_brand_id()
        category_id = payload.category_id or self._repo.get_first_category_id()
        if brand_id is None:
            raise AuthInvalidRequestError("请先创建品牌后再保存 SKU")
        if category_id is None:
            raise AuthInvalidRequestError("请先创建类目后再保存 SKU")
        size = (payload.size or "").strip() or "-"
        surface_finish = (payload.surface_finish or "").strip() or "-"
        return sku_code, brand_id, category_id, size, surface_finish

    def _validate_create_fields(self, payload: TileSkuCreateRequest) -> None:
        if not payload.name.strip():
            raise AuthInvalidRequestError("SKU 名称不能为空")
        if not (payload.sku_code or "").strip():
            raise AuthInvalidRequestError("SKU 编码不能为空")
        if payload.brand_id is None:
            raise AuthInvalidRequestError("请选择品牌")
        if payload.category_id is None:
            raise AuthInvalidRequestError("请选择类目")
        if not (payload.size or "").strip():
            raise AuthInvalidRequestError("规格尺寸不能为空")
        if not (payload.surface_finish or "").strip():
            raise AuthInvalidRequestError("表面工艺不能为空")
        if not self._repo.brand_exists(payload.brand_id):
            raise AuthInvalidRequestError("所选品牌不存在")
        if not self._repo.category_exists(payload.category_id):
            raise AuthInvalidRequestError("所选类目不存在")

    def _ensure_unique_sku_code(self, sku_code: str, *, exclude_id: int | None = None) -> None:
        existing = self._repo.get_by_sku_code(sku_code, exclude_id=exclude_id)
        if existing:
            raise TileSkuCodeDuplicatedError()

    def to_item(self, record: TileSkuRecord, *, include_media: bool = False) -> TileSkuAdminItem:
        material = self._repo.compute_material_completeness(record)
        images: list[TileSkuImageItem] = []
        videos: list[TileSkuVideoItem] = []
        if include_media:
            images = [
                TileSkuImageItem(
                    id=img.id,
                    object_key=img.object_key,
                    url=img.url,
                    is_main=bool(img.is_main),
                    sort_order=img.sort_order,
                )
                for img in self._repo.list_images(record.id)
            ]
            videos = [
                TileSkuVideoItem(
                    id=vid.id,
                    object_key=vid.object_key,
                    url=_video_url(vid.object_key),
                    file_name=vid.file_name,
                    file_size_bytes=vid.file_size_bytes,
                    duration_seconds=vid.duration_seconds,
                    sort_order=vid.sort_order,
                )
                for vid in self._repo.list_videos(record.id)
            ]
        return TileSkuAdminItem(
            id=record.id,
            name=record.name,
            sku_code=record.sku_code,
            brand_id=record.brand_id,
            brand_name=record.brand_name,
            category_id=record.category_id,
            category_name=record.category_name,
            size=record.size,
            surface_finish=record.surface_finish,
            color_family=record.color_family,
            reference_price=record.reference_price,
            remark=record.remark,
            status=record.status,  # type: ignore[arg-type]
            main_image_url=record.main_image_url,
            image_count=record.image_count,
            video_count=record.video_count,
            has_main_image=record.has_main_image,
            material_completeness=material,  # type: ignore[arg-type]
            images=images,
            videos=videos,
            created_at=record.created_at,
            updated_at=record.updated_at,
        )

    def list_skus(
        self,
        *,
        page: int,
        page_size: int,
        keyword: str | None,
        brand_id: int | None,
        category_id: int | None,
        status: str | None,
        material_completeness: MaterialCompleteness | None,
    ) -> TileSkuAdminListData:
        if page_size not in VALID_PAGE_SIZES:
            raise AuthInvalidRequestError("每页条数仅支持 10、20、50、100")
        items, total = self._repo.list_skus(
            page=page,
            page_size=page_size,
            keyword=keyword,
            brand_id=brand_id,
            category_id=category_id,
            status=status,
            material_completeness=material_completeness,
        )
        summary_raw = self._repo.get_summary()
        return TileSkuAdminListData(
            items=[self.to_item(item) for item in items],
            pagination={
                "page": page,
                "page_size": page_size,
                "total": total,
                "total_pages": (total + page_size - 1) // page_size if total else 0,
            },
            summary=TileSkuAdminSummary(**summary_raw),
        )

    def get_sku(self, tile_id: int) -> TileSkuAdminItem:
        record = self._repo.get_by_id(tile_id)
        if record is None:
            raise TileSkuNotFoundError()
        return self.to_item(record, include_media=True)

    def create_sku(self, payload: TileSkuCreateRequest) -> TileSkuAdminItem:
        name = payload.name.strip()
        if not name:
            raise AuthInvalidRequestError("SKU 名称不能为空")

        if payload.save_mode == "create":
            self._validate_create_fields(payload)
            sku_code = payload.sku_code.strip()  # type: ignore[union-attr]
            brand_id = payload.brand_id  # type: ignore[assignment]
            category_id = payload.category_id  # type: ignore[assignment]
            size = payload.size.strip()  # type: ignore[union-attr]
            surface_finish = payload.surface_finish.strip()  # type: ignore[union-attr]
        else:
            sku_code, brand_id, category_id, size, surface_finish = self._resolve_draft_defaults(
                payload
            )

        self._ensure_unique_sku_code(sku_code)
        images = self._normalize_images(payload.images)
        videos = self._normalize_videos(payload.videos)
        has_main = any(img["is_main"] for img in images)
        status = self._resolve_status_after_save(
            has_main_image=has_main, save_mode=payload.save_mode
        )

        record = self._repo.create_sku(
            name=name,
            sku_code=sku_code,
            brand_id=brand_id,
            category_id=category_id,
            size=size,
            surface_finish=surface_finish,
            color_family=self._normalize_optional(payload.color_family, max_len=50),
            reference_price=payload.reference_price,
            remark=self._normalize_optional(payload.remark, max_len=500),
            status=status,
        )
        if images:
            self._repo.replace_images(record.id, images)
        if videos:
            self._repo.replace_videos(record.id, videos)
        return self.get_sku(record.id)

    def update_sku(self, tile_id: int, payload: TileSkuUpdateRequest) -> TileSkuAdminItem:
        record = self._repo.get_by_id(tile_id)
        if record is None:
            raise TileSkuNotFoundError()

        name = payload.name.strip() if payload.name is not None else record.name
        sku_code = payload.sku_code.strip() if payload.sku_code is not None else record.sku_code
        brand_id = payload.brand_id if payload.brand_id is not None else record.brand_id
        category_id = (
            payload.category_id if payload.category_id is not None else record.category_id
        )
        size = payload.size.strip() if payload.size is not None else record.size
        surface_finish = (
            payload.surface_finish.strip()
            if payload.surface_finish is not None
            else record.surface_finish
        )

        if not name:
            raise AuthInvalidRequestError("SKU 名称不能为空")
        if not sku_code:
            raise AuthInvalidRequestError("SKU 编码不能为空")
        if not size:
            raise AuthInvalidRequestError("规格尺寸不能为空")
        if not surface_finish:
            raise AuthInvalidRequestError("表面工艺不能为空")
        if not self._repo.brand_exists(brand_id):
            raise AuthInvalidRequestError("所选品牌不存在")
        if not self._repo.category_exists(category_id):
            raise AuthInvalidRequestError("所选类目不存在")

        self._ensure_unique_sku_code(sku_code, exclude_id=tile_id)

        status = record.status
        if record.status == "NEEDS_COMPLETION":
            images_for_check = payload.images if payload.images is not None else None
            if images_for_check is not None:
                normalized = self._normalize_images(images_for_check)
                if any(img["is_main"] for img in normalized):
                    status = "DRAFT"

        updated = self._repo.update_sku(
            tile_id,
            name=name,
            sku_code=sku_code,
            brand_id=brand_id,
            category_id=category_id,
            size=size,
            surface_finish=surface_finish,
            color_family=(
                self._normalize_optional(payload.color_family, max_len=50)
                if payload.color_family is not None
                else record.color_family
            ),
            reference_price=(
                payload.reference_price
                if payload.reference_price is not None
                else record.reference_price
            ),
            remark=(
                self._normalize_optional(payload.remark, max_len=500)
                if payload.remark is not None
                else record.remark
            ),
            status=status,
            old_brand_id=record.brand_id,
            old_category_id=record.category_id,
        )

        if payload.images is not None:
            self._repo.replace_images(tile_id, self._normalize_images(payload.images))
        if payload.videos is not None:
            self._repo.replace_videos(tile_id, self._normalize_videos(payload.videos))

        return self.get_sku(updated.id)

    def publish_sku(self, tile_id: int) -> TileSkuAdminItem:
        record = self._repo.get_by_id(tile_id)
        if record is None:
            raise TileSkuNotFoundError()
        if not record.has_main_image:
            raise TileSkuPublishForbiddenError("缺少主图，无法上架")
        if not record.name.strip() or not record.sku_code.strip():
            raise TileSkuPublishForbiddenError()
        if not record.size.strip() or record.size == "-":
            raise TileSkuPublishForbiddenError("规格尺寸不完整，无法上架")
        if not record.surface_finish.strip() or record.surface_finish == "-":
            raise TileSkuPublishForbiddenError("表面工艺不完整，无法上架")
        if record.sku_code.startswith("DRAFT-"):
            raise TileSkuPublishForbiddenError("请先完善 SKU 编码后再上架")
        updated = self._repo.update_status(tile_id, "PUBLISHED")
        return self.to_item(updated)

    def unpublish_sku(self, tile_id: int) -> TileSkuAdminItem:
        record = self._repo.get_by_id(tile_id)
        if record is None:
            raise TileSkuNotFoundError()
        if record.status != "PUBLISHED":
            raise AuthInvalidRequestError("仅已上架 SKU 可下架")
        updated = self._repo.update_status(tile_id, "DISABLED")
        return self.to_item(updated)

    def delete_sku(self, tile_id: int) -> None:
        record = self._repo.get_by_id(tile_id)
        if record is None:
            raise TileSkuNotFoundError()
        if record.status == "PUBLISHED":
            raise TileSkuDeleteForbiddenError()
        self._repo.delete_sku(tile_id, brand_id=record.brand_id, category_id=record.category_id)
