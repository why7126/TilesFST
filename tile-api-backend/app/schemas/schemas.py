from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from enum import Enum


class RoleEnum(str, Enum):
    ADMIN = "admin"
    EDITOR = "editor"


class StatTypeEnum(str, Enum):
    VIEW = "view"
    FAVORITE = "favorite"
    SHARE = "share"


class LoginRequest(BaseModel):
    username: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class CategoryBase(BaseModel):
    name: str
    parent_id: Optional[int] = None
    sort_order: int = 0


class CategoryCreate(CategoryBase):
    pass


class CategoryUpdate(CategoryBase):
    pass


class CategoryResponse(CategoryBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


class BrandBase(BaseModel):
    name: str
    logo_url: Optional[str] = None


class BrandCreate(BrandBase):
    pass


class BrandUpdate(BrandBase):
    pass


class BrandResponse(BrandBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


class ProductBase(BaseModel):
    name: str
    model: Optional[str] = None
    description: Optional[str] = None
    price: float
    size: Optional[str] = None
    category_id: Optional[int] = None
    brand_id: Optional[int] = None
    images: Optional[str] = None
    video_url: Optional[str] = None
    is_active: bool = True


class ProductCreate(ProductBase):
    pass


class ProductUpdate(ProductBase):
    pass


class ProductResponse(ProductBase):
    id: int
    created_at: datetime
    updated_at: datetime
    category: Optional[CategoryResponse] = None
    brand: Optional[BrandResponse] = None

    class Config:
        from_attributes = True


class ProductListResponse(BaseModel):
    total: int
    items: List[ProductResponse]


class EmployeeBase(BaseModel):
    username: str
    role: RoleEnum = RoleEnum.EDITOR


class EmployeeCreate(EmployeeBase):
    password: str


class EmployeeUpdate(BaseModel):
    role: Optional[RoleEnum] = None
    password: Optional[str] = None


class EmployeeResponse(BaseModel):
    id: int
    username: str
    role: RoleEnum
    created_at: datetime

    class Config:
        from_attributes = True


class StatisticBase(BaseModel):
    product_id: int
    type: StatTypeEnum
    count: int = 1


class StatisticResponse(StatisticBase):
    id: int
    date: datetime

    class Config:
        from_attributes = True


class StatisticsSummary(BaseModel):
    total_views: int
    total_favorites: int
    total_shares: int


class FileUploadResponse(BaseModel):
    object_key: str
    url: str