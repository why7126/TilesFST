"""Public upload control payloads; persistent object/credential fields stay private."""
from typing import Literal
from pydantic import BaseModel, ConfigDict, Field

MediaKind = Literal['avatar', 'brand_logo', 'banner', 'sku_image', 'sku_video', 'certificate']


class UploadSessionCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")
    media_kind: MediaKind
    business_id: int | None = Field(default=None, gt=0)
    expected_size: int = Field(gt=0)
    mime_type: str = Field(min_length=1, max_length=128)
    client_idempotency_key: str = Field(min_length=1, max_length=128, pattern=r'^[A-Za-z0-9_-]+$')


class UploadSessionStatus(BaseModel):
    session_id: str
    state: str
    expires_at: str
    retryable: bool = False
    error_code: int | None = None
    task_trace_id: str | None = None
    mode: Literal['cos_direct'] = 'cos_direct'
    part_size: int
    part_count: int
    media: 'UploadSessionMedia | None' = None


class UploadSessionMedia(BaseModel):
    thumbnail_url: str | None = None
    display_url: str | None = None
    original_url: str | None = None
    processing_warning: bool = False
    object_key: str
    url: str
    mime_type: str
    size: int


class UploadAuthorization(BaseModel):
    url: str
    method: Literal['PUT'] = 'PUT'
    expires_at: str
    length: int
    part_number: int | None = None


class UploadSessionCreated(BaseModel):
    mode: Literal['cos_direct', 'proxy']
    reason: str | None = None
    session: UploadSessionStatus | None = None


class UploadSessionRenewed(BaseModel):
    session: UploadSessionStatus
    authorization: UploadAuthorization | None = None
