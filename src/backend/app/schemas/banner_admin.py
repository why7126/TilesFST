"""Admin banner management schemas."""

from __future__ import annotations

from pydantic import BaseModel, Field


class BannerAdminSummary(BaseModel):
    total: int
    filtered_count: int
    online_count: int
    pending_count: int


class BannerAdminItem(BaseModel):
    id: int
    title: str
    display_client: str
    position: str
    image_object_key: str
    image_url: str
    image_source: str
    sku_gallery_asset_id: int | None = None
    jump_type: str
    sku_id: int | None = None
    external_url: str | None = None
    topic_id: int | None = None
    sort_order: int
    valid_from: str | None = None
    valid_to: str | None = None
    status: str
    time_status: str | None = None
    remark: str | None = None
    created_at: str
    updated_at: str


class BannerAdminListData(BaseModel):
    items: list[BannerAdminItem]
    page: int
    page_size: int
    total: int
    summary: BannerAdminSummary


class BannerCreateRequest(BaseModel):
    title: str = Field(..., min_length=1, max_length=100)
    display_client: str
    position: str
    image_object_key: str
    image_source: str
    sku_gallery_asset_id: int | None = None
    jump_type: str
    sku_id: int | None = None
    external_url: str | None = None
    topic_id: int | None = None
    sort_order: int = 100
    valid_from: str | None = None
    valid_to: str | None = None
    remark: str | None = Field(None, max_length=500)


class BannerUpdateRequest(BaseModel):
    title: str = Field(..., min_length=1, max_length=100)
    display_client: str
    position: str
    image_object_key: str
    image_source: str
    sku_gallery_asset_id: int | None = None
    jump_type: str
    sku_id: int | None = None
    external_url: str | None = None
    topic_id: int | None = None
    sort_order: int
    valid_from: str | None = None
    valid_to: str | None = None
    remark: str | None = Field(None, max_length=500)


class TopicAdminItem(BaseModel):
    id: int
    code: str
    title: str
    status: str
    cover_object_key: str | None = None
    cover_url: str | None = None


class TopicAdminListData(BaseModel):
    items: list[TopicAdminItem]
    total: int
