"""Admin tile SKU management schemas."""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field

SaveMode = Literal["draft", "create"]
TileSkuStatus = Literal["PUBLISHED", "DRAFT", "NEEDS_COMPLETION", "DISABLED"]
MaterialCompleteness = Literal[
    "complete", "missing_main_image", "missing_images", "missing_videos"
]


class TileSkuImageInput(BaseModel):
    object_key: str
    url: str
    is_main: bool = False
    sort_order: int = 0


class TileSkuVideoInput(BaseModel):
    object_key: str
    file_name: str
    file_size_bytes: int | None = None
    duration_seconds: float | None = None
    sort_order: int = 0


class TileSkuImageItem(BaseModel):
    id: int
    object_key: str
    url: str
    is_main: bool
    sort_order: int


class TileSkuVideoItem(BaseModel):
    id: int
    object_key: str
    url: str
    file_name: str
    file_size_bytes: int | None = None
    duration_seconds: float | None = None
    sort_order: int


class TileSkuAdminItem(BaseModel):
    id: int
    name: str
    sku_code: str
    brand_id: int
    brand_name: str
    category_id: int
    category_name: str
    spec_id: int | None = None
    size: str
    surface_finish: str
    color_family: str | None = None
    reference_price: float | None = None
    remark: str | None = None
    status: TileSkuStatus
    main_image_url: str | None = None
    image_count: int = 0
    video_count: int = 0
    has_main_image: bool = False
    material_completeness: MaterialCompleteness
    images: list[TileSkuImageItem] = Field(default_factory=list)
    videos: list[TileSkuVideoItem] = Field(default_factory=list)
    created_at: str
    updated_at: str


class TileSkuAdminSummary(BaseModel):
    total: int
    published_count: int
    needs_completion_count: int
    draft_count: int


class TileSkuAdminListData(BaseModel):
    items: list[TileSkuAdminItem]
    pagination: dict[str, int]
    summary: TileSkuAdminSummary


class TileSkuCreateRequest(BaseModel):
    save_mode: SaveMode = "create"
    name: str
    sku_code: str | None = None
    brand_id: int | None = None
    category_id: int | None = None
    spec_id: int | None = None
    size: str | None = None
    surface_finish: str | None = None
    color_family: str | None = None
    reference_price: float = 0.0
    remark: str | None = None
    images: list[TileSkuImageInput] = Field(default_factory=list)
    videos: list[TileSkuVideoInput] = Field(default_factory=list)


class TileSkuUpdateRequest(BaseModel):
    name: str | None = None
    sku_code: str | None = None
    brand_id: int | None = None
    category_id: int | None = None
    spec_id: int | None = None
    size: str | None = None
    surface_finish: str | None = None
    color_family: str | None = None
    reference_price: float | None = None
    remark: str | None = None
    images: list[TileSkuImageInput] | None = None
    videos: list[TileSkuVideoInput] | None = None
