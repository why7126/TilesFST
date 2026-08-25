"""Admin tile SKU management schemas."""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field, model_validator

DEFAULT_RECALL_PIN_SORT_ORDER = 9999

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
    thumbnail_url: str | None = None
    display_url: str | None = None
    original_url: str | None = None
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
    recall_pin_sort_order: int = DEFAULT_RECALL_PIN_SORT_ORDER
    recall_pin_starts_at: str | None = None
    recall_pin_ends_at: str | None = None
    status: TileSkuStatus
    main_image_url: str | None = None
    main_image_thumbnail_url: str | None = None
    main_image_display_url: str | None = None
    main_image_original_url: str | None = None
    image_count: int = 0
    video_count: int = 0
    has_main_image: bool = False
    material_completeness: MaterialCompleteness
    images: list[TileSkuImageItem] = Field(default_factory=list)
    videos: list[TileSkuVideoItem] = Field(default_factory=list)
    published_at: str | None = None
    created_at: str
    updated_at: str
    task_trace_id: str | None = None
    task_type: str | None = None


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
    recall_pin_sort_order: int | None = DEFAULT_RECALL_PIN_SORT_ORDER
    recall_pin_starts_at: str | None = None
    recall_pin_ends_at: str | None = None
    images: list[TileSkuImageInput] = Field(default_factory=list)
    videos: list[TileSkuVideoInput] = Field(default_factory=list)

    @model_validator(mode="after")
    def validate_recall_pin_config(self) -> "TileSkuCreateRequest":
        _validate_recall_pin_config(
            self.recall_pin_sort_order,
            self.recall_pin_starts_at,
            self.recall_pin_ends_at,
        )
        return self


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
    recall_pin_sort_order: int | None = None
    recall_pin_starts_at: str | None = None
    recall_pin_ends_at: str | None = None
    images: list[TileSkuImageInput] | None = None
    videos: list[TileSkuVideoInput] | None = None

    @model_validator(mode="after")
    def validate_recall_pin_config(self) -> "TileSkuUpdateRequest":
        _validate_recall_pin_config(
            self.recall_pin_sort_order,
            self.recall_pin_starts_at,
            self.recall_pin_ends_at,
        )
        return self


def _validate_recall_pin_config(
    sort_order: int | None,
    starts_at: str | None,
    ends_at: str | None,
) -> None:
    if sort_order is not None and sort_order <= 0:
        raise ValueError("召回排序值必须为正整数")
    if starts_at and ends_at and starts_at > ends_at:
        raise ValueError("召回置顶开始时间不能晚于结束时间")
