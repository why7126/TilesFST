"""Business references accepted by the media authorization endpoints."""

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

MediaResource = Literal["sku_image", "sku_video", "brand_logo", "banner_image", "certificate", "avatar", "upload_session", "store_logo"]
MediaVariant = Literal["thumbnail", "display", "original"]


class MediaReadReference(BaseModel):
    model_config = ConfigDict(extra="forbid")

    resource_type: MediaResource
    resource_id: str = Field(min_length=1, max_length=64, pattern=r"^[a-zA-Z0-9_-]+$")
    media_id: int | None = Field(default=None, ge=1)
    variant: MediaVariant = "original"


class MediaReadRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    items: list[MediaReadReference] = Field(min_length=1, max_length=50)
    mode: Literal["auto", "proxy"] = "auto"


class MediaReadDescriptor(BaseModel):
    media_ref: str
    variant: MediaVariant
    url: str
    head_url: str | None = None
    expires_at: datetime | None = None
    read_mode: Literal["direct", "external", "proxy"]
    degraded: bool = False
    content_type: str | None = None
    size_bytes: int | None = None


class MediaReadError(BaseModel):
    code: int
    message: str


class MediaReadItem(BaseModel):
    reference: MediaReadReference
    status: Literal["ready", "unavailable", "failed"]
    descriptor: MediaReadDescriptor | None = None
    error: MediaReadError | None = None


class MediaReadData(BaseModel):
    server_time: datetime
    items: list[MediaReadItem]
