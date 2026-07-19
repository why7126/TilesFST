"""Public WeChat miniapp APIs."""

from __future__ import annotations

from typing import Annotated, Literal

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.repositories.miniapp_home_repository import MiniappHomeRepository
from app.repositories.system_settings_repository import SystemSettingsRepository
from app.schemas.common import ApiResponse, VALIDATION_ERROR_RESPONSE
from app.schemas.miniapp_home import (
    MiniappCategoryTreeData,
    MiniappHomeData,
    MiniappProductDetail,
    MiniappProductListData,
    MiniappSearchData,
    MiniappSearchHomeData,
    MiniappSearchSuggestionsData,
    MiniappSkuDetailData,
    MiniappSkuFavoriteData,
    MiniappSkuFavoriteRequest,
)
from app.services.miniapp_home_service import MiniappHomeService

router = APIRouter()


def get_miniapp_home_service(db: Session = Depends(get_db)) -> MiniappHomeService:
    return MiniappHomeService(
        MiniappHomeRepository(db),
        SystemSettingsRepository(db),
    )


@router.get(
    "/home",
    response_model=ApiResponse[MiniappHomeData],
    responses=VALIDATION_ERROR_RESPONSE,
    summary="小程序首页聚合数据",
    description="返回小程序首页公开展示所需的门店摘要、Banner、快捷入口、服务区、新品和热销商品。",
)
def get_home(
    service: Annotated[MiniappHomeService, Depends(get_miniapp_home_service)],
) -> ApiResponse[MiniappHomeData]:
    return ApiResponse(data=service.get_home())


@router.get(
    "/products",
    response_model=ApiResponse[MiniappProductListData],
    responses=VALIDATION_ERROR_RESPONSE,
    summary="小程序公开商品搜索",
)
def search_products(
    service: Annotated[MiniappHomeService, Depends(get_miniapp_home_service)],
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=50),
    page_size_camel: int | None = Query(None, alias="pageSize", ge=1, le=50),
    keyword: str | None = Query(None, max_length=80),
    category_id: int | None = Query(None, alias="categoryId", ge=1),
    brand_id: int | None = Query(None, alias="brandId", ge=1),
    spec: str | None = Query(None, max_length=80),
    price_range: str | None = Query(None, alias="priceRange", max_length=40),
    sort: Literal["default", "latest", "price_asc", "price_desc"] = Query("default"),
    filter_type: Literal["space", "spec", "style", "color", "category", "all"] | None = Query(None),
    filter_value: str | None = Query(None, max_length=80),
    section: Literal["new", "hot"] | None = Query(None),
) -> ApiResponse[MiniappProductListData]:
    return ApiResponse(
        data=service.search_products(
            page=page,
            page_size=page_size_camel or page_size,
            keyword=keyword,
            category_id=category_id,
            brand_id=brand_id,
            spec=spec,
            price_range=price_range,
            sort=sort,
            filter_type=filter_type,
            filter_value=filter_value,
            section=section,
        )
    )


@router.get(
    "/search/home",
    response_model=ApiResponse[MiniappSearchHomeData],
    responses=VALIDATION_ERROR_RESPONSE,
    summary="小程序搜索首页数据",
    description="返回热门搜索词与最近浏览兜底数据；最近搜索由小程序本机保存。",
)
def get_search_home(
    service: Annotated[MiniappHomeService, Depends(get_miniapp_home_service)],
) -> ApiResponse[MiniappSearchHomeData]:
    return ApiResponse(data=service.get_search_home())


@router.get(
    "/search/suggestions",
    response_model=ApiResponse[MiniappSearchSuggestionsData],
    responses=VALIDATION_ERROR_RESPONSE,
    summary="小程序搜索实时联想",
    description="返回 SKU、品牌、类目、规格和关键词建议；证书不参与实时联想。",
)
def suggest_search(
    service: Annotated[MiniappHomeService, Depends(get_miniapp_home_service)],
    keyword: str = Query(..., min_length=1, max_length=80),
    scope: str = Query("all", max_length=80),
    limit: int = Query(8, ge=6, le=10),
    request_id: str | None = Query(None, max_length=128),
) -> ApiResponse[MiniappSearchSuggestionsData]:
    return ApiResponse(
        data=service.suggest_search(
            keyword=keyword,
            scope=scope,
            limit=limit,
            request_id=request_id,
        )
    )


@router.get(
    "/search",
    response_model=ApiResponse[MiniappSearchData],
    responses=VALIDATION_ERROR_RESPONSE,
    summary="小程序完整搜索",
    description="返回综合、SKU、品牌、类目、证书 Tab、分区结果、筛选 facets 与分页信息。",
)
def search_all(
    service: Annotated[MiniappHomeService, Depends(get_miniapp_home_service)],
    keyword: str = Query(..., min_length=1, max_length=80),
    tab: Literal["all", "sku", "brand", "category", "certificate"] = Query("all"),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=50),
    brand: str | None = Query(None, max_length=80),
    category: str | None = Query(None, max_length=80),
    spec: str | None = Query(None, max_length=80),
    price_min: float | None = Query(None, ge=0),
    price_max: float | None = Query(None, ge=0),
    request_id: str | None = Query(None, max_length=128),
) -> ApiResponse[MiniappSearchData]:
    return ApiResponse(
        data=service.search_all(
            keyword=keyword,
            active_tab=tab,
            page=page,
            page_size=page_size,
            brand=brand,
            category=category,
            spec=spec,
            price_min=price_min,
            price_max=price_max,
            request_id=request_id,
        )
    )


@router.get(
    "/categories/tree",
    response_model=ApiResponse[MiniappCategoryTreeData],
    responses=VALIDATION_ERROR_RESPONSE,
    summary="小程序公开分类树",
    description="返回最多两级启用分类、排序字段、二级分类安全缩略图 URL 和分类数据版本号。",
)
def get_category_tree(
    service: Annotated[MiniappHomeService, Depends(get_miniapp_home_service)],
    depth: int = Query(2, ge=1, le=2),
) -> ApiResponse[MiniappCategoryTreeData]:
    return ApiResponse(data=service.get_category_tree(depth=depth))


@router.get(
    "/products/{product_id}",
    response_model=ApiResponse[MiniappProductDetail],
    responses=VALIDATION_ERROR_RESPONSE,
    summary="小程序公开商品详情",
)
def get_product_detail(
    product_id: int,
    service: Annotated[MiniappHomeService, Depends(get_miniapp_home_service)],
) -> ApiResponse[MiniappProductDetail]:
    return ApiResponse(data=service.get_product_detail(product_id))


@router.get(
    "/skus/{sku_id}",
    response_model=ApiResponse[MiniappSkuDetailData],
    responses=VALIDATION_ERROR_RESPONSE,
    summary="小程序 SKU 详情聚合数据",
    description="返回单个公开 SKU 的主体、媒体、品牌、收藏状态、分享数据和相关推荐。",
)
def get_sku_detail(
    sku_id: int,
    service: Annotated[MiniappHomeService, Depends(get_miniapp_home_service)],
    client_id: str | None = Query(None, max_length=128),
) -> ApiResponse[MiniappSkuDetailData]:
    return ApiResponse(data=service.get_sku_detail(sku_id, client_id=client_id))


@router.put(
    "/skus/{sku_id}/favorite",
    response_model=ApiResponse[MiniappSkuFavoriteData],
    responses=VALIDATION_ERROR_RESPONSE,
    summary="小程序 SKU 收藏状态",
    description="按 SKU 粒度幂等设置收藏或取消收藏，使用小程序客户端标识隔离收藏事实。",
)
def set_sku_favorite(
    sku_id: int,
    payload: MiniappSkuFavoriteRequest,
    service: Annotated[MiniappHomeService, Depends(get_miniapp_home_service)],
) -> ApiResponse[MiniappSkuFavoriteData]:
    return ApiResponse(
        data=service.set_sku_favorite(
            sku_id,
            client_id=payload.client_id,
            favorite=payload.favorite,
        )
    )
