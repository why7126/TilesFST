"""Admin brand certificate schemas."""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field, model_validator

CertificateType = Literal[
    "QUALITY",
    "INSPECTION",
    "GREEN_BUILDING",
    "HONOR",
    "OTHER",
]
CertificateValidityStatus = Literal[
    "PERMANENT",
    "VALID",
    "EXPIRING_SOON",
    "EXPIRED",
    "UNSET",
]
CertificateDisplayStatus = Literal["VISIBLE", "HIDDEN"]


class BrandCertificateFile(BaseModel):
    file_url: str = Field(..., min_length=1, max_length=768)
    file_key: str = Field(..., min_length=1, max_length=512)
    file_name: str = Field(..., min_length=1, max_length=255)
    file_mime_type: str = Field(..., min_length=1, max_length=128)
    file_size_bytes: int = Field(..., ge=1)


class BrandCertificateSummary(BaseModel):
    total: int
    valid_count: int
    expiring_soon_count: int
    expired_count: int


class BrandCertificateItem(BaseModel):
    id: int
    brand_id: int
    brand_name: str
    name: str
    sort_order: int
    type: CertificateType
    certificate_no: str | None = None
    issuer: str | None = None
    file_url: str
    file_key: str
    file_name: str
    file_mime_type: str
    file_size_bytes: int
    is_permanent: bool
    effective_date: str | None = None
    expiry_date: str | None = None
    validity_status: CertificateValidityStatus
    is_visible: bool
    display_status: CertificateDisplayStatus
    remark: str | None = None
    created_at: str
    updated_at: str


class BrandCertificateListData(BaseModel):
    items: list[BrandCertificateItem]
    page: int
    page_size: int
    total: int
    summary: BrandCertificateSummary


class BrandCertificateMutationRequest(BaseModel):
    brand_id: int = Field(..., ge=1)
    name: str = Field(..., min_length=1, max_length=120)
    sort_order: int = Field(..., ge=1)
    type: CertificateType
    certificate_no: str | None = Field(None, max_length=120)
    issuer: str | None = Field(None, max_length=120)
    file: BrandCertificateFile
    is_permanent: bool = False
    effective_date: str | None = Field(None, max_length=32)
    expiry_date: str | None = Field(None, max_length=32)
    is_visible: bool = True
    remark: str | None = Field(None, max_length=500)

    @model_validator(mode="after")
    def validate_dates(self) -> "BrandCertificateMutationRequest":
        if self.is_permanent:
            self.effective_date = None
            self.expiry_date = None
        return self


class BrandCertificateCreateRequest(BrandCertificateMutationRequest):
    pass


class BrandCertificateUpdateRequest(BrandCertificateMutationRequest):
    pass
