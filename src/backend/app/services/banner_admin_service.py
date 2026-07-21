"""Admin banner management business logic."""

from __future__ import annotations

import re
from datetime import UTC, datetime
from urllib.parse import urlparse

from app.core.exceptions import (
    AuthInvalidRequestError,
    BannerDeleteForbiddenError,
    BannerExternalUrlInvalidError,
    BannerJumpTargetInvalidError,
    BannerNotFoundError,
    BannerTitleDuplicatedError,
)
from app.repositories.banner_repository import BannerRecord, BannerRepository, compute_time_status
from app.repositories.topic_repository import TopicRepository
from app.schemas.banner_admin import (
    BannerAdminItem,
    BannerAdminListData,
    BannerAdminSummary,
    BannerCreateRequest,
    BannerUpdateRequest,
)

VALID_PAGE_SIZES = frozenset({10, 20, 50})

MINIAPP_DISPLAY_CLIENT = "MINIAPP_HOME"
MINIAPP_HOME_CAROUSEL_POSITION = "MINIAPP_HOME_CAROUSEL"
MINIAPP_BRAND_LIST_CAROUSEL_POSITION = "MINIAPP_BRAND_LIST_CAROUSEL"

DISPLAY_CLIENT_POSITIONS: dict[str, frozenset[str]] = {
    MINIAPP_DISPLAY_CLIENT: frozenset(
        {MINIAPP_HOME_CAROUSEL_POSITION, MINIAPP_BRAND_LIST_CAROUSEL_POSITION}
    ),
}

DEFAULT_POSITION: dict[str, str] = {
    MINIAPP_DISPLAY_CLIENT: MINIAPP_HOME_CAROUSEL_POSITION,
}

JUMP_TYPES = frozenset({"SKU_DETAIL", "BRAND_DETAIL", "EXTERNAL_LINK", "TOPIC_PAGE", "NO_JUMP"})
IMAGE_SOURCES = frozenset(
    {"sku_main_image", "sku_gallery_image", "custom_upload", "topic_cover", "brand_logo"}
)
BANNER_STATUSES = frozenset({"DRAFT", "ONLINE", "OFFLINE", "EXPIRED"})

_HTTPS_PATTERN = re.compile(r"^https://", re.IGNORECASE)


def _media_url(object_key: str | None) -> str | None:
    if not object_key:
        return None
    return f"/media/{object_key}"


def _normalize_optional(value: str | None, *, max_len: int) -> str | None:
    if value is None:
        return None
    trimmed = value.strip()
    if not trimmed:
        return None
    return trimmed[:max_len]


def _parse_dt(value: str | None) -> datetime | None:
    if not value:
        return None
    try:
        dt = datetime.fromisoformat(value.replace("Z", "+00:00"))
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=UTC)
        return dt
    except ValueError:
        return None


class BannerAdminService:
    def __init__(
        self,
        banner_repo: BannerRepository,
        topic_repo: TopicRepository,
    ) -> None:
        self._banners = banner_repo
        self._topics = topic_repo

    @staticmethod
    def to_item(banner: BannerRecord) -> BannerAdminItem:
        return BannerAdminItem(
            id=banner.id,
            title=banner.title,
            display_client=banner.display_client,
            position=banner.position,
            image_object_key=banner.image_object_key,
            image_url=_media_url(banner.image_object_key) or "",
            image_source=banner.image_source,
            sku_gallery_asset_id=banner.sku_gallery_asset_id,
            jump_type=banner.jump_type,
            sku_id=banner.sku_id,
            external_url=banner.external_url,
            topic_id=banner.topic_id,
            brand_id=banner.brand_id,
            sort_order=banner.sort_order,
            valid_from=banner.valid_from,
            valid_to=banner.valid_to,
            status=banner.status,
            time_status=compute_time_status(
                status=banner.status,
                valid_from=banner.valid_from,
                valid_to=banner.valid_to,
            ),
            remark=banner.remark,
            created_at=banner.created_at,
            updated_at=banner.updated_at,
        )

    @staticmethod
    def validate_display_client_position(display_client: str, position: str) -> None:
        if display_client not in DISPLAY_CLIENT_POSITIONS:
            raise AuthInvalidRequestError("当前仅支持小程序首页轮播和品牌列表页轮播")
        if position not in DISPLAY_CLIENT_POSITIONS[display_client]:
            raise AuthInvalidRequestError("当前仅支持小程序首页轮播和品牌列表页轮播")

    @staticmethod
    def validate_title(title: str) -> str:
        trimmed = title.strip()
        if not trimmed:
            raise AuthInvalidRequestError("Banner 标题不能为空")
        if len(trimmed) > 100:
            raise AuthInvalidRequestError("Banner 标题不能超过 100 个字符")
        return trimmed

    @staticmethod
    def validate_sort_order(sort_order: int) -> None:
        if sort_order < 1:
            raise AuthInvalidRequestError("排序必须为正整数")

    @staticmethod
    def validate_external_url(url: str) -> str:
        trimmed = url.strip()
        if not _HTTPS_PATTERN.match(trimmed):
            raise BannerExternalUrlInvalidError()
        parsed = urlparse(trimmed)
        if parsed.scheme.lower() != "https" or not parsed.netloc:
            raise BannerExternalUrlInvalidError()
        return trimmed

    def validate_jump_and_image(
        self,
        *,
        jump_type: str,
        sku_id: int | None,
        external_url: str | None,
        topic_id: int | None,
        brand_id: int | None,
        image_source: str,
        image_object_key: str,
        sku_gallery_asset_id: int | None,
    ) -> None:
        if jump_type not in JUMP_TYPES:
            raise BannerJumpTargetInvalidError("跳转类型无效")
        if image_source not in IMAGE_SOURCES:
            raise BannerJumpTargetInvalidError("图片来源无效")
        if not image_object_key.strip():
            raise BannerJumpTargetInvalidError("Banner 图片不能为空")

        if jump_type == "SKU_DETAIL":
            if sku_id is None:
                raise BannerJumpTargetInvalidError("SKU 详情跳转必须选择 SKU")
            if not self._banners.sku_exists(sku_id):
                raise BannerJumpTargetInvalidError("关联 SKU 不存在")
            if external_url or topic_id is not None or brand_id is not None:
                raise BannerJumpTargetInvalidError("SKU 详情跳转不能包含其他跳转目标")
            self._validate_sku_image(sku_id, image_source, sku_gallery_asset_id, image_object_key)
            return

        if jump_type == "BRAND_DETAIL":
            if brand_id is None:
                raise BannerJumpTargetInvalidError("品牌详情跳转必须选择品牌")
            if not self._banners.brand_exists(brand_id):
                raise BannerJumpTargetInvalidError("关联品牌不存在或未启用")
            if sku_id is not None or external_url or topic_id is not None:
                raise BannerJumpTargetInvalidError("品牌详情跳转不能包含其他跳转目标")
            self._validate_brand_image(brand_id, image_source, sku_gallery_asset_id, image_object_key)
            return

        if jump_type == "EXTERNAL_LINK":
            if not external_url:
                raise BannerJumpTargetInvalidError("外部链接跳转必须填写 URL")
            self.validate_external_url(external_url)
            if sku_id is not None or topic_id is not None or brand_id is not None:
                raise BannerJumpTargetInvalidError("外部链接跳转不能包含其他跳转目标")
            if image_source != "custom_upload":
                raise BannerJumpTargetInvalidError("外部链接 Banner 必须使用自定义上传图片")
            if sku_gallery_asset_id is not None:
                raise BannerJumpTargetInvalidError("外部链接 Banner 不能引用 SKU 图库")
            return

        if jump_type == "TOPIC_PAGE":
            if topic_id is None:
                raise BannerJumpTargetInvalidError("专题页跳转必须选择专题")
            if not self._topics.is_enabled(topic_id):
                raise BannerJumpTargetInvalidError("专题不存在或未启用")
            if sku_id is not None or external_url or brand_id is not None:
                raise BannerJumpTargetInvalidError("专题页跳转不能包含其他跳转目标")
            return

        if jump_type == "NO_JUMP":
            if sku_id is not None or external_url or topic_id is not None or brand_id is not None:
                raise BannerJumpTargetInvalidError("无跳转 Banner 不能配置跳转目标")
            if sku_gallery_asset_id is not None and image_source != "custom_upload":
                raise BannerJumpTargetInvalidError("无跳转 Banner 图片配置无效")

    def _validate_sku_image(
        self,
        sku_id: int,
        image_source: str,
        sku_gallery_asset_id: int | None,
        image_object_key: str,
    ) -> None:
        if image_source == "sku_main_image":
            main_key = self._banners.get_sku_main_image_key(sku_id)
            if not main_key:
                raise BannerJumpTargetInvalidError("SKU 无主图，请切换图片来源")
            if main_key != image_object_key:
                raise BannerJumpTargetInvalidError("SKU 主图引用不一致")
            if sku_gallery_asset_id is not None:
                raise BannerJumpTargetInvalidError("SKU 主图不能设置图库资产 ID")
            return

        if image_source == "sku_gallery_image":
            if sku_gallery_asset_id is None:
                raise BannerJumpTargetInvalidError("SKU 图库引用必须选择图库资产")
            image = self._banners.get_tile_image(sku_gallery_asset_id)
            if image is None or int(image["tile_id"]) != sku_id:
                raise BannerJumpTargetInvalidError("SKU 图库资产不存在或不属于该 SKU")
            if image["object_key"] != image_object_key:
                raise BannerJumpTargetInvalidError("SKU 图库引用不一致")
            return

        if image_source == "custom_upload":
            if sku_gallery_asset_id is not None:
                raise BannerJumpTargetInvalidError("自定义上传不能设置图库资产 ID")
            return

        raise BannerJumpTargetInvalidError("SKU 详情 Banner 图片来源无效")

    def _validate_brand_image(
        self,
        brand_id: int,
        image_source: str,
        sku_gallery_asset_id: int | None,
        image_object_key: str,
    ) -> None:
        if image_source == "brand_logo":
            logo_key = self._banners.get_brand_logo_key(brand_id)
            if not logo_key:
                raise BannerJumpTargetInvalidError("品牌无 Logo，请切换图片来源")
            if logo_key != image_object_key:
                raise BannerJumpTargetInvalidError("品牌 Logo 引用不一致")
            if sku_gallery_asset_id is not None:
                raise BannerJumpTargetInvalidError("品牌 Logo 不能设置 SKU 图库资产 ID")
            return

        if image_source == "custom_upload":
            if sku_gallery_asset_id is not None:
                raise BannerJumpTargetInvalidError("自定义上传不能设置图库资产 ID")
            return

        raise BannerJumpTargetInvalidError("品牌详情 Banner 图片来源无效")

    @staticmethod
    def validate_validity(valid_from: str | None, valid_to: str | None) -> None:
        from_dt = _parse_dt(valid_from)
        to_dt = _parse_dt(valid_to)
        if valid_from and from_dt is None:
            raise AuthInvalidRequestError("有效期开始时间格式无效")
        if valid_to and to_dt is None:
            raise AuthInvalidRequestError("有效期结束时间格式无效")
        if from_dt and to_dt and from_dt > to_dt:
            raise AuthInvalidRequestError("有效期开始时间不能晚于结束时间")

    def list_banners(
        self,
        *,
        page: int,
        page_size: int,
        keyword: str | None,
        display_client: str | None,
        status: str | None,
        time_status: str | None,
    ) -> BannerAdminListData:
        if page_size not in VALID_PAGE_SIZES:
            page_size = 10
        if page < 1:
            page = 1
        if status and status not in BANNER_STATUSES:
            status = None
        if time_status and time_status not in {"ACTIVE", "PENDING", "EXPIRED"}:
            time_status = None
        if display_client and display_client not in DISPLAY_CLIENT_POSITIONS:
            display_client = MINIAPP_DISPLAY_CLIENT

        result = self._banners.list_banners(
            page=page,
            page_size=page_size,
            keyword=keyword.strip() if keyword else None,
            display_client=display_client,
            status=status,
            time_status=time_status,
        )
        summary = result.summary
        return BannerAdminListData(
            items=[self.to_item(b) for b in result.items],
            page=page,
            page_size=page_size,
            total=result.total,
            summary=BannerAdminSummary(
                total=summary["total"],
                filtered_count=summary["filtered_count"],
                online_count=summary["online_count"],
                pending_count=summary["pending_count"],
            ),
        )

    def get_banner(self, banner_id: int) -> BannerAdminItem:
        banner = self._banners.get_by_id(banner_id)
        if banner is None:
            raise BannerNotFoundError()
        return self.to_item(banner)

    def create_banner(self, payload: BannerCreateRequest) -> BannerAdminItem:
        title = self.validate_title(payload.title)
        self.validate_display_client_position(payload.display_client, payload.position)
        self.validate_sort_order(payload.sort_order)
        self.validate_validity(payload.valid_from, payload.valid_to)
        self.validate_jump_and_image(
            jump_type=payload.jump_type,
            sku_id=payload.sku_id,
            external_url=payload.external_url,
            topic_id=payload.topic_id,
            brand_id=payload.brand_id,
            image_source=payload.image_source,
            image_object_key=payload.image_object_key,
            sku_gallery_asset_id=payload.sku_gallery_asset_id,
        )
        if self._banners.get_by_unique_key(payload.display_client, payload.position, title):
            raise BannerTitleDuplicatedError()

        banner = self._banners.create(
            title=title,
            display_client=payload.display_client,
            position=payload.position,
            image_object_key=payload.image_object_key.strip(),
            image_source=payload.image_source,
            sku_gallery_asset_id=payload.sku_gallery_asset_id,
            jump_type=payload.jump_type,
            sku_id=payload.sku_id,
            external_url=_normalize_optional(payload.external_url, max_len=500),
            topic_id=payload.topic_id,
            brand_id=payload.brand_id,
            sort_order=payload.sort_order,
            valid_from=payload.valid_from,
            valid_to=payload.valid_to,
            remark=_normalize_optional(payload.remark, max_len=500),
        )
        return self.to_item(banner)

    def update_banner(self, banner_id: int, payload: BannerUpdateRequest) -> BannerAdminItem:
        banner = self._banners.get_by_id(banner_id)
        if banner is None:
            raise BannerNotFoundError()

        title = self.validate_title(payload.title)
        self.validate_display_client_position(payload.display_client, payload.position)
        self.validate_sort_order(payload.sort_order)
        self.validate_validity(payload.valid_from, payload.valid_to)
        self.validate_jump_and_image(
            jump_type=payload.jump_type,
            sku_id=payload.sku_id,
            external_url=payload.external_url,
            topic_id=payload.topic_id,
            brand_id=payload.brand_id,
            image_source=payload.image_source,
            image_object_key=payload.image_object_key,
            sku_gallery_asset_id=payload.sku_gallery_asset_id,
        )
        if self._banners.get_by_unique_key(
            payload.display_client, payload.position, title, exclude_id=banner_id
        ):
            raise BannerTitleDuplicatedError()

        updated = self._banners.update(
            banner_id,
            title=title,
            display_client=payload.display_client,
            position=payload.position,
            image_object_key=payload.image_object_key.strip(),
            image_source=payload.image_source,
            sku_gallery_asset_id=payload.sku_gallery_asset_id,
            jump_type=payload.jump_type,
            sku_id=payload.sku_id,
            external_url=_normalize_optional(payload.external_url, max_len=500),
            topic_id=payload.topic_id,
            brand_id=payload.brand_id,
            sort_order=payload.sort_order,
            valid_from=payload.valid_from,
            valid_to=payload.valid_to,
            remark=_normalize_optional(payload.remark, max_len=500),
        )
        assert updated is not None
        return self.to_item(updated)

    def online_banner(self, banner_id: int) -> BannerAdminItem:
        banner = self._banners.get_by_id(banner_id)
        if banner is None:
            raise BannerNotFoundError()

        ts = compute_time_status(
            status=banner.status,
            valid_from=banner.valid_from,
            valid_to=banner.valid_to,
        )
        if ts == "EXPIRED":
            raise BannerJumpTargetInvalidError("Banner 已过期，无法上线")

        self.validate_jump_and_image(
            jump_type=banner.jump_type,
            sku_id=banner.sku_id,
            external_url=banner.external_url,
            topic_id=banner.topic_id,
            brand_id=banner.brand_id,
            image_source=banner.image_source,
            image_object_key=banner.image_object_key,
            sku_gallery_asset_id=banner.sku_gallery_asset_id,
        )
        self.validate_sort_order(banner.sort_order)
        self.validate_validity(banner.valid_from, banner.valid_to)

        updated = self._banners.update_status(banner_id, "ONLINE")
        assert updated is not None
        return self.to_item(updated)

    def offline_banner(self, banner_id: int) -> BannerAdminItem:
        banner = self._banners.get_by_id(banner_id)
        if banner is None:
            raise BannerNotFoundError()
        updated = self._banners.update_status(banner_id, "OFFLINE")
        assert updated is not None
        return self.to_item(updated)

    def delete_banner(self, banner_id: int) -> None:
        banner = self._banners.get_by_id(banner_id)
        if banner is None:
            raise BannerNotFoundError()
        if banner.status == "ONLINE":
            raise BannerDeleteForbiddenError()
        self._banners.delete(banner_id)
