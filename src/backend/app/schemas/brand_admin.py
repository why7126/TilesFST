"""Admin brand management schemas."""

from __future__ import annotations

from pydantic import BaseModel, Field


class BrandAdminSummary(BaseModel):
    total: int
    enabled_count: int
    disabled_count: int
    unlinked_sku_count: int


class BrandAdminItem(BaseModel):
    id: int
    name: str
    sort_order: int
    short_name: str | None = None
    english_name: str | None = None
    logo_object_key: str | None = None
    logo_url: str | None = None
    description: str | None = None
    status: str
    sku_count: int
    created_at: str
    updated_at: str


class BrandAdminListData(BaseModel):
    items: list[BrandAdminItem]
    page: int
    page_size: int
    total: int
    summary: BrandAdminSummary


class BrandCreateRequest(BaseModel):
    name: str = Field(..., min_length=1, max_length=50)
    sort_order: int
    short_name: str | None = Field(None, max_length=30)
    english_name: str | None = Field(None, max_length=80)
    logo_object_key: str | None = None
    description: str | None = Field(None, max_length=500)


class BrandUpdateRequest(BaseModel):
    name: str = Field(..., min_length=1, max_length=50)
    sort_order: int
    short_name: str | None = Field(None, max_length=30)
    english_name: str | None = Field(None, max_length=80)
    logo_object_key: str | None = None
    description: str | None = Field(None, max_length=500)
