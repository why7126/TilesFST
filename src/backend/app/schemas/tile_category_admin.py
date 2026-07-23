"""Admin tile category management schemas."""

from __future__ import annotations

from pydantic import BaseModel, Field


class TileCategoryAdminSummary(BaseModel):
    total: int
    enabled_count: int
    bound_sku_total: int
    max_level: int = 2


class TileCategoryAdminItem(BaseModel):
    id: int
    parent_id: int | None = None
    name: str
    code: str
    sort_order: int
    level: int
    description: str | None = None
    status: str
    sku_count: int
    path: str
    created_at: str
    updated_at: str


class TileCategoryAdminListData(BaseModel):
    items: list[TileCategoryAdminItem]
    page: int
    page_size: int
    total: int
    summary: TileCategoryAdminSummary


class TileCategoryTreeNode(BaseModel):
    id: int
    name: str
    code: str
    level: int
    status: str
    sku_count: int
    children: list["TileCategoryTreeNode"] = Field(default_factory=list)


class TileCategoryCreateRequest(BaseModel):
    parent_id: int | None = None
    name: str = Field(..., description="最多 10 个字符，仅允许中文、英文和数字")
    sort_order: int
    description: str | None = Field(None, max_length=200)
    status: str = "ENABLED"


class TileCategoryUpdateRequest(BaseModel):
    name: str = Field(..., description="最多 10 个字符，仅允许中文、英文和数字")
    sort_order: int
    description: str | None = Field(None, max_length=200)


TileCategoryTreeNode.model_rebuild()
