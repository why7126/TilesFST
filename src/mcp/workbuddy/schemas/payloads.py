"""Local payload checks; backend remains the business validation authority."""

from pydantic import BaseModel, ConfigDict, Field


class SkuPayload(BaseModel):
    model_config = ConfigDict(extra="allow", strict=True)
    name: str = Field(min_length=1)


class BrandPayload(SkuPayload):
    name: str = Field(min_length=1, max_length=50)
    sort_order: int


class CategoryPayload(BrandPayload):
    name: str = Field(min_length=1, max_length=15)


def payload_model(tool: str):
    if tool in {"create_tile_sku", "update_tile_sku"}:
        return SkuPayload
    if tool == "manage_brand":
        return BrandPayload
    if tool == "manage_category":
        return CategoryPayload
    return None
