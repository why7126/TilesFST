"""Admin tile spec management schemas."""

from __future__ import annotations

from pydantic import BaseModel, Field


class TileSpecAdminSummary(BaseModel):
    total: int
    enabled_count: int
    disabled_count: int
    unlinked_sku_count: int


class TileSpecAdminItem(BaseModel):
    id: int
    width_mm: int
    length_mm: int
    thickness_mm: float | None = None
    unit: str
    display_name: str
    sort_order: int
    status: str
    sku_count: int
    remark: str | None = None
    created_at: str
    updated_at: str


class TileSpecAdminListData(BaseModel):
    items: list[TileSpecAdminItem]
    page: int
    page_size: int
    total: int
    summary: TileSpecAdminSummary


class TileSpecCreateRequest(BaseModel):
    width_mm: int = Field(..., ge=1, le=9999)
    length_mm: int = Field(..., ge=1, le=9999)
    thickness_mm: float | None = Field(None, ge=0)
    sort_order: int = Field(..., ge=1)
    remark: str | None = Field(None, max_length=200)


class TileSpecUpdateRequest(BaseModel):
    width_mm: int = Field(..., ge=1, le=9999)
    length_mm: int = Field(..., ge=1, le=9999)
    thickness_mm: float | None = Field(None, ge=0)
    sort_order: int = Field(..., ge=1)
    remark: str | None = Field(None, max_length=200)
