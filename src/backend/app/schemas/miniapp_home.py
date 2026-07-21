"""Public WeChat miniapp home and product schemas."""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field


class MiniappStoreSummary(BaseModel):
    name: str
    logo_url: str | None = None
    description: str | None = None
    address: str | None = None


class MiniappBannerItem(BaseModel):
    id: int
    title: str
    subtitle: str | None = None
    image_url: str
    jump_type: Literal["none", "product", "brand", "search", "store"]
    target_id: int | None = None
    search_keyword: str | None = None


class MiniappShortcutItem(BaseModel):
    key: Literal["select", "brand", "new", "hot"]
    title: str
    filter_type: str
    filter_value: str | None = None


class MiniappServiceItem(BaseModel):
    key: str
    title: str
    description: str
    action_type: Literal["none", "copy_wechat", "phone"]
    action_value: str | None = None


class MiniappProductCard(BaseModel):
    product_id: int
    product_name: str
    sku_code: str
    cover_image: str | None = None
    specification: str
    category_name: str | None = None
    brand_name: str | None = None
    style_tags: list[str] = Field(default_factory=list)
    applicable_spaces: list[str] = Field(default_factory=list)
    color_family: str | None = None
    price_display: str
    is_new: bool = False
    is_hot: bool = False


class MiniappSearchFacetOption(BaseModel):
    value: str
    label: str
    count: int
    selected: bool = False


class MiniappSearchFacets(BaseModel):
    brands: list[MiniappSearchFacetOption] = Field(default_factory=list)
    categories: list[MiniappSearchFacetOption] = Field(default_factory=list)
    specs: list[MiniappSearchFacetOption] = Field(default_factory=list)
    price_ranges: list[MiniappSearchFacetOption] = Field(default_factory=list)


class MiniappHomeData(BaseModel):
    store: MiniappStoreSummary
    banners: list[MiniappBannerItem]
    shortcuts: list[MiniappShortcutItem]
    services: list[MiniappServiceItem]
    new_products: list[MiniappProductCard]
    hot_products: list[MiniappProductCard]


class MiniappProductListData(BaseModel):
    items: list[MiniappProductCard]
    total: int
    page: int
    page_size: int
    has_more: bool = False
    facets: MiniappSearchFacets = Field(default_factory=MiniappSearchFacets)


class MiniappBrandCard(BaseModel):
    brand_id: int
    brand_name: str
    brand_short_name: str | None = None
    english_name: str | None = None
    brand_logo_url: str | None = None
    brand_entry_path: str
    product_count: int = 0
    description: str | None = None
    available: bool = True


class MiniappBrandListData(BaseModel):
    banners: list[MiniappBannerItem]
    items: list[MiniappBrandCard]
    total: int
    page: int
    page_size: int
    has_more: bool = False


class MiniappBrandDetailData(MiniappBrandCard):
    product_path: str
    certificate_count: int = 0


class MiniappBrandCertificateItem(BaseModel):
    certificate_id: int
    certificate_name: str
    certificate_type: str | None = None
    certificate_no: str | None = None
    issuer: str | None = None
    brand_name: str
    file_url: str


class MiniappBrandCertificateListData(BaseModel):
    items: list[MiniappBrandCertificateItem]
    total: int


class MiniappCertificateItem(BaseModel):
    certificate_id: int
    certificate_name: str
    certificate_type: str | None = None
    certificate_type_label: str
    certificate_no: str | None = None
    issuer: str | None = None
    brand_id: int
    brand_name: str
    file_url: str | None = None
    file_name: str | None = None
    file_mime_type: str | None = None
    file_kind: Literal["image", "pdf", "unknown"]
    effective_date: str | None = None
    expiry_date: str | None = None
    validity_status: Literal["PERMANENT", "VALID", "EXPIRING_SOON", "EXPIRED", "UNSET"]
    validity_status_label: str


class MiniappCertificateListData(BaseModel):
    items: list[MiniappCertificateItem]
    total: int
    page: int
    page_size: int
    has_more: bool = False


class MiniappSearchSuggestion(BaseModel):
    id: str
    text: str
    entity_type: Literal["keyword", "sku", "brand", "category", "spec"]
    target_id: int | None = None
    target_path: str | None = None
    scope: str = "all"


class MiniappSearchSuggestionsData(BaseModel):
    keyword: str
    normalized_keyword: str
    request_id: str
    suggestions: list[MiniappSearchSuggestion]


class MiniappSearchSection(BaseModel):
    entity_type: Literal["sku", "brand", "category", "certificate"]
    title: str
    count: int
    items: list[dict[str, object]] = Field(default_factory=list)


class MiniappSearchData(BaseModel):
    keyword: str
    normalized_keyword: str
    request_id: str
    active_tab: Literal["all", "sku", "brand", "category", "certificate"]
    tabs: list[MiniappSearchFacetOption]
    best_match: dict[str, object] | None = None
    sections: list[MiniappSearchSection]
    facets: MiniappSearchFacets
    items: list[MiniappProductCard]
    total: int
    page: int
    page_size: int
    has_more: bool = False
    recommended_keywords: list[str] = Field(default_factory=list)


class MiniappSearchHomeData(BaseModel):
    hot_keywords: list[str]
    recent_browsing: list[MiniappProductCard]


class MiniappCategoryChildItem(BaseModel):
    id: int
    name: str
    cover_url: str = Field(alias="coverUrl")
    sort: int

    model_config = {"populate_by_name": True}


class MiniappCategoryTreeItem(BaseModel):
    id: int
    name: str
    sort: int
    children: list[MiniappCategoryChildItem] = Field(default_factory=list)


class MiniappCategoryTreeData(BaseModel):
    version: str
    items: list[MiniappCategoryTreeItem]


class MiniappProductDetail(MiniappProductCard):
    images: list[str] = Field(default_factory=list)
    videos: list[str] = Field(default_factory=list)
    surface_finish: str | None = None
    share_title: str


class MiniappSkuMediaItem(BaseModel):
    media_id: int
    media_type: Literal["image", "video"]
    url: str
    preview_url: str | None = None
    cover_url: str | None = None
    sort_order: int
    is_main: bool = False
    duration_seconds: float | None = None


class MiniappSkuBrandInfo(BaseModel):
    brand_id: int
    brand_name: str
    brand_short_name: str | None = None
    brand_logo_url: str | None = None
    brand_entry_path: str | None = None
    available: bool = True


class MiniappSkuShareInfo(BaseModel):
    title: str
    path: str
    image_url: str | None = None
    summary: str


class MiniappSkuDetailData(MiniappProductCard):
    brand: MiniappSkuBrandInfo
    media: list[MiniappSkuMediaItem] = Field(default_factory=list)
    image_count: int = 0
    video_count: int = 0
    category_path: list[str] = Field(default_factory=list)
    parameters: list[dict[str, str]] = Field(default_factory=list)
    remark: str | None = None
    surface_finish: str | None = None
    favorite: bool = False
    same_series_recommendations: list[MiniappProductCard] = Field(default_factory=list)
    same_brand_recommendations: list[MiniappProductCard] = Field(default_factory=list)
    share: MiniappSkuShareInfo


class MiniappSkuFavoriteRequest(BaseModel):
    client_id: str = Field(min_length=1, max_length=128)
    favorite: bool


class MiniappSkuFavoriteData(BaseModel):
    sku_id: int
    favorite: bool
