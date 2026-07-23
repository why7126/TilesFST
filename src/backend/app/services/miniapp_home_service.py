"""Public miniapp home aggregation service."""

from __future__ import annotations

from datetime import UTC, datetime, timedelta

from app.core.exceptions import TileSkuNotFoundError
from app.repositories.miniapp_home_repository import (
    MiniappBannerRecord,
    MiniappCategoryRecord,
    MiniappHomeRepository,
    MiniappProductRecord,
)
from app.repositories.system_settings_repository import SystemSettingsRepository
from app.schemas.miniapp_home import (
    MiniappBannerItem,
    MiniappBrandCard,
    MiniappBrandCertificateItem,
    MiniappBrandCertificateListData,
    MiniappBrandDetailData,
    MiniappBrandListData,
    MiniappCategoryChildItem,
    MiniappCertificateItem,
    MiniappCertificateListData,
    MiniappCategoryTreeData,
    MiniappCategoryTreeItem,
    MiniappHomeData,
    MiniappSkuBrandInfo,
    MiniappSkuDetailData,
    MiniappSkuFavoriteData,
    MiniappSkuMediaItem,
    MiniappSkuShareInfo,
    MiniappProductCard,
    MiniappProductDetail,
    MiniappProductListData,
    MiniappSearchData,
    MiniappSearchFacetOption,
    MiniappSearchFacets,
    MiniappSearchHomeData,
    MiniappSearchSection,
    MiniappSearchSuggestion,
    MiniappSearchSuggestionsData,
    MiniappServiceItem,
    MiniappShortcutItem,
    MiniappStoreSummary,
)


class MiniappHomeService:
    def __init__(
        self,
        repo: MiniappHomeRepository,
        settings_repo: SystemSettingsRepository,
    ) -> None:
        self._repo = repo
        self._settings_repo = settings_repo

    def get_home(self) -> MiniappHomeData:
        new_products, _ = self._repo.list_products(page=1, page_size=6, only_new=True)
        if len(new_products) < 3:
            new_products, _ = self._repo.list_products(page=1, page_size=6)
        hot_products, _ = self._repo.list_products(page=1, page_size=6, hot_first=True)
        return MiniappHomeData(
            store=self._store_summary(),
            banners=[
                self._to_banner_item(item)
                for item in self._repo.list_public_banners(position="MINIAPP_HOME_CAROUSEL")
            ],
            shortcuts=self._shortcuts(),
            services=self._services(),
            new_products=[self._to_product_card(item, force_new=True) for item in new_products],
            hot_products=[self._to_product_card(item, force_hot=True) for item in hot_products],
        )

    def get_brand_list(self, *, page: int, page_size: int) -> MiniappBrandListData:
        items, total = self._repo.list_public_brands(page=page, page_size=page_size)
        return MiniappBrandListData(
            banners=[
                self._to_banner_item(item)
                for item in self._repo.list_public_banners(
                    position="MINIAPP_BRAND_LIST_CAROUSEL"
                )
            ],
            items=[self._to_brand_card(item) for item in items],
            total=total,
            page=page,
            page_size=page_size,
            has_more=page * page_size < total,
        )

    def get_brand_detail(self, brand_id: int) -> MiniappBrandDetailData:
        record = self._repo.get_public_brand(brand_id)
        if record is None:
            raise TileSkuNotFoundError("品牌不存在或暂不可查看")
        card = self._to_brand_card(record)
        certificates = self._repo.list_public_brand_certificates(brand_id=brand_id)
        return MiniappBrandDetailData(
            **card.model_dump(),
            product_path=f"/pages/product-list/index?brandId={record.id}&sourcePage=brand-detail",
            certificate_count=len(certificates),
        )

    def get_brand_certificates(self, brand_id: int) -> MiniappBrandCertificateListData:
        if self._repo.get_public_brand(brand_id) is None:
            raise TileSkuNotFoundError("品牌不存在或暂不可查看")
        items = self._repo.list_public_brand_certificates(brand_id=brand_id)
        return MiniappBrandCertificateListData(
            items=[
                MiniappBrandCertificateItem(
                    certificate_id=item.id,
                    certificate_name=item.name,
                    certificate_type=item.type,
                    certificate_no=item.certificate_no,
                    issuer=item.issuer,
                    brand_name=item.brand_name,
                    file_url=item.file_url,
                )
                for item in items
            ],
            total=len(items),
        )

    def list_certificates(
        self,
        *,
        page: int,
        page_size: int,
    ) -> MiniappCertificateListData:
        items, total = self._repo.list_public_certificates(
            page=page,
            page_size=page_size,
        )
        return MiniappCertificateListData(
            items=[self._to_certificate_item(item) for item in items],
            total=total,
            page=page,
            page_size=page_size,
            has_more=page * page_size < total,
        )

    def get_category_tree(self, *, depth: int = 2) -> MiniappCategoryTreeData:
        categories = self._repo.list_enabled_categories_for_tree(depth=min(max(depth, 1), 2))
        roots = [item for item in categories if item.level == 1 and item.parent_id is None]
        children_by_parent: dict[int, list[MiniappCategoryRecord]] = {}
        for item in categories:
            if item.level != 2 or item.parent_id is None:
                continue
            children_by_parent.setdefault(item.parent_id, []).append(item)
        return MiniappCategoryTreeData(
            version=_category_tree_version(categories),
            items=[
                MiniappCategoryTreeItem(
                    id=root.id,
                    name=root.name,
                    sort=root.sort_order,
                    children=[
                        MiniappCategoryChildItem(
                            id=child.id,
                            name=child.name,
                            cover_url="/media/miniapp/category-placeholder.webp",
                            sort=child.sort_order,
                        )
                        for child in children_by_parent.get(root.id, [])
                    ],
                )
                for root in roots
            ],
        )

    def search_products(
        self,
        *,
        page: int,
        page_size: int,
        keyword: str | None,
        category_id: int | None,
        category_level: str | None,
        brand_id: int | None,
        spec: str | None,
        price_range: str | None,
        sort: str,
        filter_type: str | None,
        filter_value: str | None,
        section: str | None,
    ) -> MiniappProductListData:
        price_min, price_max = _parse_price_range(price_range)
        items, total = self._repo.list_products(
            page=page,
            page_size=page_size,
            keyword=keyword,
            category_id=category_id,
            category_level=category_level,
            brand_id=brand_id,
            spec=spec,
            price_min=price_min,
            price_max=price_max,
            sort=sort,
            filter_type=filter_type,
            filter_value=filter_value,
            only_new=section == "new",
            hot_first=section == "hot",
        )
        facets = self._product_facets(
            keyword=keyword,
            category_id=category_id,
            category_level=category_level,
            brand_id=brand_id,
            spec=spec,
            price_min=price_min,
            price_max=price_max,
        )
        return MiniappProductListData(
            items=[self._to_product_card(item, force_new=section == "new") for item in items],
            total=total,
            page=page,
            page_size=page_size,
            has_more=page * page_size < total,
            facets=facets,
        )

    def get_search_home(self) -> MiniappSearchHomeData:
        hot_products, _ = self._repo.list_products(page=1, page_size=10, hot_first=True)
        hot_keywords = _unique_non_empty(
            ["岩板", "柔光砖", "800×800", "客厅", "菲尚特"]
            + [item.brand_name for item in hot_products]
            + [item.category_name for item in hot_products]
            + [item.spec_name or item.size for item in hot_products]
        )[:10]
        return MiniappSearchHomeData(
            hot_keywords=hot_keywords,
            recent_browsing=[
                self._to_product_card(item, force_hot=item.hot_score > 0) for item in hot_products[:10]
            ],
        )

    def suggest_search(
        self,
        *,
        keyword: str,
        scope: str,
        limit: int,
        request_id: str | None,
    ) -> MiniappSearchSuggestionsData:
        normalized = _normalize_keyword(keyword)
        suggestions: list[MiniappSearchSuggestion] = []
        if not _meets_suggestion_threshold(normalized):
            return MiniappSearchSuggestionsData(
                keyword=keyword,
                normalized_keyword=normalized,
                request_id=request_id or _request_id(normalized),
                suggestions=[],
            )
        named = self._repo.list_search_named_results(keyword=normalized)
        for entity_type in ["brand"]:
            for item in named[entity_type]:
                target_path = _target_path(entity_type, item.id, item.name)
                suggestions.append(
                    MiniappSearchSuggestion(
                        id=f"{entity_type}-{item.id}",
                        text=item.name,
                        entity_type=entity_type,  # type: ignore[arg-type]
                        target_id=item.id if item.id else None,
                        target_path=target_path,
                        scope=scope or "all",
                    )
                )
        products, _ = self._repo.list_search_products(
            keyword=normalized,
            page=1,
            page_size=min(limit, 10),
            brand=None,
            category=scope if scope not in {"", "all"} else None,
            spec=None,
            price_min=None,
            price_max=None,
        )
        for item in products:
            suggestions.append(
                MiniappSearchSuggestion(
                    id=f"sku-{item.id}",
                    text=item.name,
                    entity_type="sku",
                    target_id=item.id,
                    target_path=f"/pages/tile-detail/index?skuId={item.id}",
                    scope=scope or "all",
                )
            )
        return MiniappSearchSuggestionsData(
            keyword=keyword,
            normalized_keyword=normalized,
            request_id=request_id or _request_id(normalized),
            suggestions=_dedupe_suggestions(suggestions)[: min(limit, 10)],
        )

    def search_all(
        self,
        *,
        keyword: str,
        active_tab: str,
        page: int,
        page_size: int,
        brand: str | None,
        category: str | None,
        spec: str | None,
        price_min: float | None,
        price_max: float | None,
        request_id: str | None,
    ) -> MiniappSearchData:
        normalized = _normalize_keyword(keyword)
        selected_tab = active_tab if active_tab in {"all", "sku", "brand", "category", "certificate"} else "all"
        products, product_total = self._repo.list_search_products(
            keyword=normalized,
            page=page,
            page_size=page_size,
            brand=brand,
            category=category,
            spec=spec,
            price_min=price_min,
            price_max=price_max,
        )
        named = self._repo.list_search_named_results(keyword=normalized)
        certificates = self._repo.list_search_certificates(keyword=normalized)
        product_cards = [self._to_product_card(item, force_hot=item.hot_score > 0) for item in products]
        sections = [
            MiniappSearchSection(
                entity_type="sku",
                title="SKU",
                count=product_total,
                items=[item.model_dump() for item in product_cards[:8]],
            ),
            MiniappSearchSection(
                entity_type="brand",
                title="品牌",
                count=len(named["brand"]),
                items=[item.__dict__ for item in named["brand"]],
            ),
            MiniappSearchSection(
                entity_type="category",
                title="类目",
                count=len(named["category"]),
                items=[item.__dict__ for item in named["category"]],
            ),
            MiniappSearchSection(
                entity_type="certificate",
                title="证书",
                count=len(certificates),
                items=[item.__dict__ for item in certificates],
            ),
        ]
        visible_sections = [
            section for section in sections if selected_tab == "all" or section.entity_type == selected_tab
        ]
        facets = self._search_facets(normalized, brand=brand, category=category, spec=spec)
        tabs = [
            MiniappSearchFacetOption(
                value="all",
                label="综合",
                count=product_total + len(named["brand"]) + len(named["category"]) + len(certificates),
                selected=selected_tab == "all",
            ),
            MiniappSearchFacetOption(value="sku", label="SKU", count=product_total, selected=selected_tab == "sku"),
            MiniappSearchFacetOption(
                value="brand", label="品牌", count=len(named["brand"]), selected=selected_tab == "brand"
            ),
            MiniappSearchFacetOption(
                value="category",
                label="类目",
                count=len(named["category"]),
                selected=selected_tab == "category",
            ),
            MiniappSearchFacetOption(
                value="certificate",
                label="证书",
                count=len(certificates),
                selected=selected_tab == "certificate",
            ),
        ]
        best_match = self._best_match(named["brand"], certificates, product_cards, normalized)
        return MiniappSearchData(
            keyword=keyword,
            normalized_keyword=normalized,
            request_id=request_id or _request_id(normalized),
            active_tab=selected_tab,  # type: ignore[arg-type]
            tabs=tabs,
            best_match=best_match,
            sections=visible_sections,
            facets=facets,
            items=product_cards,
            total=product_total,
            page=page,
            page_size=page_size,
            has_more=page * page_size < product_total,
            recommended_keywords=self.get_search_home().hot_keywords[:6],
        )

    def _search_facets(
        self,
        keyword: str,
        *,
        brand: str | None,
        category: str | None,
        spec: str | None,
    ) -> MiniappSearchFacets:
        raw = self._repo.list_search_facets(keyword=keyword)
        return MiniappSearchFacets(
            brands=[
                MiniappSearchFacetOption(
                    value=item.name,
                    label=item.name,
                    count=item.count,
                    selected=item.name == brand,
                )
                for item in raw["brands"]
            ],
            categories=[
                MiniappSearchFacetOption(
                    value=item.name,
                    label=item.name,
                    count=item.count,
                    selected=item.name == category,
                )
                for item in raw["categories"]
            ],
            specs=[
                MiniappSearchFacetOption(
                    value=item.name,
                    label=item.name,
                    count=item.count,
                    selected=item.name == spec,
                )
                for item in raw["specs"]
            ],
            price_ranges=[
                MiniappSearchFacetOption(value="0-100", label="100 元以下", count=0),
                MiniappSearchFacetOption(value="100-200", label="100-200 元", count=0),
                MiniappSearchFacetOption(value="200-", label="200 元以上", count=0),
            ],
        )

    def _product_facets(
        self,
        *,
        keyword: str | None,
        category_id: int | None,
        category_level: str | None,
        brand_id: int | None,
        spec: str | None,
        price_min: float | None,
        price_max: float | None,
    ) -> MiniappSearchFacets:
        raw = self._repo.list_product_facets(
            keyword=keyword,
            category_id=category_id,
            category_level=category_level,
            brand_id=brand_id,
            spec=spec,
            price_min=price_min,
            price_max=price_max,
        )
        return MiniappSearchFacets(
            brands=[
                MiniappSearchFacetOption(
                    value=str(item.id),
                    label=item.name,
                    count=item.count,
                    selected=item.id == brand_id,
                )
                for item in raw["brands"]
            ],
            categories=[
                MiniappSearchFacetOption(
                    value=str(item.id),
                    label=item.name,
                    count=item.count,
                    selected=item.id == category_id,
                )
                for item in raw["categories"]
            ],
            specs=[
                MiniappSearchFacetOption(
                    value=item.name,
                    label=item.name,
                    count=item.count,
                    selected=item.name == spec,
                )
                for item in raw["specs"]
            ],
            price_ranges=[
                MiniappSearchFacetOption(
                    value=value,
                    label=label,
                    count=0,
                    selected=(price_min, price_max) == _parse_price_range(value),
                )
                for value, label in [
                    ("0-100", "100 元以下"),
                    ("100-200", "100-200 元"),
                    ("200-", "200 元以上"),
                ]
            ],
        )

    def get_product_detail(self, product_id: int) -> MiniappProductDetail:
        record = self._repo.get_product(product_id)
        if record is None:
            raise TileSkuNotFoundError("商品不存在或未公开")
        card = self._to_product_card(record, force_hot=record.hot_score > 0)
        images = self._repo.list_product_images(product_id)
        return MiniappProductDetail(
            **card.model_dump(),
            images=[self._media_url(image) for image in images]
            or ([self._media_url(record.main_image_url)] if record.main_image_url else []),
            videos=[self._media_url(video) for video in self._repo.list_product_videos(product_id)],
            surface_finish=record.surface_finish,
            share_title=f"{record.brand_name} {record.name}".strip(),
        )

    def get_sku_detail(self, sku_id: int, *, client_id: str | None = None) -> MiniappSkuDetailData:
        record = self._repo.get_product(sku_id)
        if record is None:
            raise TileSkuNotFoundError("商品暂不可查看")
        card = self._to_product_card(record, force_hot=record.hot_score > 0)
        media = self._media_items(record)
        image_count = sum(1 for item in media if item.media_type == "image")
        video_count = sum(1 for item in media if item.media_type == "video")
        series = self._repo.list_same_series_products(record)
        series_ids = {item.id for item in series}
        brand_recommendations = self._repo.list_same_brand_products(
            record,
            exclude_ids=series_ids,
        )
        favorite = (
            self._repo.is_favorite(client_id=client_id.strip(), product_id=sku_id)
            if client_id and client_id.strip()
            else False
        )
        share_image = media[0].url if media else (
            self._media_url(record.main_image_url) if record.main_image_url else None
        )
        return MiniappSkuDetailData(
            **card.model_dump(),
            brand=MiniappSkuBrandInfo(
                brand_id=record.brand_id,
                brand_name=record.brand_name,
                brand_short_name=record.brand_short_name,
                brand_logo_url=self._media_url(record.brand_logo_object_key)
                if record.brand_logo_object_key
                else None,
                brand_entry_path=f"/pages/brand-detail/index?brandId={record.brand_id}",
                available=True,
            ),
            media=media,
            image_count=image_count,
            video_count=video_count,
            category_path=_category_path(record.category_path, record.category_name),
            parameters=self._parameters(record),
            remark=None,
            surface_finish=record.surface_finish,
            favorite=favorite,
            same_series_recommendations=[
                self._to_product_card(item, force_hot=item.hot_score > 0) for item in series
            ],
            same_brand_recommendations=[
                self._to_product_card(item, force_hot=item.hot_score > 0)
                for item in brand_recommendations
            ],
            share=MiniappSkuShareInfo(
                title=f"{record.brand_name} {record.name}",
                path=f"/pages/tile-detail/index?skuId={record.id}&source=share",
                image_url=share_image,
                summary=f"{record.brand_name} · {card.price_display}",
            ),
        )

    def set_sku_favorite(
        self,
        sku_id: int,
        *,
        client_id: str,
        favorite: bool,
    ) -> MiniappSkuFavoriteData:
        if self._repo.get_product(sku_id) is None:
            raise TileSkuNotFoundError("商品暂不可查看")
        saved = self._repo.set_favorite(
            client_id=client_id.strip(),
            product_id=sku_id,
            favorite=favorite,
        )
        return MiniappSkuFavoriteData(sku_id=sku_id, favorite=saved)

    def _store_summary(self) -> MiniappStoreSummary:
        return MiniappStoreSummary(
            name=self._setting("miniapp.store_name", "菲尚特瓷砖馆"),
            logo_url=self._setting("miniapp.logo_url", None),
            description=self._setting("miniapp.store_description", "质感空间，由砖而生"),
            address=self._setting("miniapp.store_address", None),
        )

    def _services(self) -> list[MiniappServiceItem]:
        phone = self._setting("miniapp.contact_phone", None)
        wechat = self._setting("miniapp.contact_wechat", "FeishangteTiles")
        services = [
            MiniappServiceItem(
                key="authentic",
                title="正品保障",
                description="甄选品牌瓷砖资料，放心选材",
                action_type="none",
            ),
            MiniappServiceItem(
                key="selection",
                title="免费选砖",
                description="按空间、规格、风格快速筛选",
                action_type="none",
            ),
        ]
        if phone:
            services.append(
                MiniappServiceItem(
                    key="phone",
                    title="联系门店",
                    description="电话咨询门店选砖建议",
                    action_type="phone",
                    action_value=phone,
                )
            )
        elif wechat:
            services.append(
                MiniappServiceItem(
                    key="wechat",
                    title="联系门店",
                    description="复制微信号咨询门店选砖建议",
                    action_type="copy_wechat",
                    action_value=wechat,
                )
            )
        return services

    @staticmethod
    def _shortcuts() -> list[MiniappShortcutItem]:
        return [
            MiniappShortcutItem(key="select", title="选瓷砖", filter_type="all"),
            MiniappShortcutItem(key="brand", title="品牌馆", filter_type="brand"),
            MiniappShortcutItem(key="new", title="新品榜", filter_type="section", filter_value="new"),
            MiniappShortcutItem(key="hot", title="热销榜", filter_type="section", filter_value="hot"),
        ]

    def _to_banner_item(self, record: MiniappBannerRecord) -> MiniappBannerItem:
        jump_type = "none"
        target_id = None
        search_keyword = None
        if record.jump_type in {"SKU_DETAIL", "PRODUCT", "product"} and record.sku_id:
            jump_type = "product"
            target_id = record.sku_id
        elif record.jump_type in {"BRAND_DETAIL", "BRAND", "brand"} and record.brand_id:
            jump_type = "brand"
            target_id = record.brand_id
        elif record.jump_type in {"TOPIC", "SEARCH", "search"}:
            jump_type = "search"
            search_keyword = record.title
        elif record.jump_type in {"STORE", "store"}:
            jump_type = "store"
        return MiniappBannerItem(
            id=record.id,
            title=record.title,
            subtitle=None,
            image_url=self._media_url(record.image_object_key),
            jump_type=jump_type,
            target_id=target_id,
            search_keyword=search_keyword,
        )

    @staticmethod
    def _to_certificate_item(record) -> MiniappCertificateItem:
        status = _certificate_validity_status(record)
        return MiniappCertificateItem(
            certificate_id=record.id,
            certificate_name=record.name,
            certificate_type=record.type,
            certificate_type_label=_certificate_type_label(record.type),
            certificate_no=record.certificate_no,
            issuer=record.issuer,
            brand_id=record.brand_id or 0,
            brand_name=record.brand_name,
            file_url=record.file_url,
            file_name=record.file_name,
            file_mime_type=record.file_mime_type,
            file_kind=_certificate_file_kind(record.file_mime_type, record.file_url, record.file_name),
            effective_date=record.effective_date,
            expiry_date=record.expiry_date,
            validity_status=status,
            validity_status_label=_VALIDITY_STATUS_LABELS[status],
        )

    def _to_brand_card(self, record) -> MiniappBrandCard:
        return MiniappBrandCard(
            brand_id=record.id,
            brand_name=record.name,
            brand_short_name=record.short_name,
            english_name=record.english_name,
            brand_logo_url=self._media_url(record.logo_object_key) if record.logo_object_key else None,
            brand_entry_path=f"/pages/brand-detail/index?brandId={record.id}",
            product_count=record.product_count,
            description=_public_summary(record.description),
            available=True,
        )

    def _media_items(self, record: MiniappProductRecord) -> list[MiniappSkuMediaItem]:
        media = self._repo.list_product_media(record.id)
        if not media and record.main_image_url:
            url = self._media_url(record.main_image_url)
            return [
                MiniappSkuMediaItem(
                    media_id=0,
                    media_type="image",
                    url=url,
                    preview_url=url,
                    sort_order=0,
                    is_main=True,
                )
            ]
        items: list[MiniappSkuMediaItem] = []
        for item in media:
            url = self._media_url(item.url)
            items.append(
                MiniappSkuMediaItem(
                    media_id=item.id,
                    media_type="video" if item.media_type == "video" else "image",
                    url=url,
                    preview_url=url if item.media_type == "image" else None,
                    cover_url=None,
                    sort_order=item.sort_order,
                    is_main=item.is_main,
                    duration_seconds=item.duration_seconds,
                )
            )
        return items

    @staticmethod
    def _parameters(record: MiniappProductRecord) -> list[dict[str, str]]:
        return [
            {"label": "类目", "value": " / ".join(_category_path(record.category_path, record.category_name))},
            {"label": "规格", "value": record.spec_name or record.size or "—"},
            {"label": "主色系", "value": record.color_family or "—"},
            {"label": "表面工艺", "value": record.surface_finish or "—"},
        ]

    def _to_product_card(
        self,
        record: MiniappProductRecord,
        *,
        force_new: bool = False,
        force_hot: bool = False,
    ) -> MiniappProductCard:
        is_new = force_new or _is_recent(record.created_at)
        return MiniappProductCard(
            product_id=record.id,
            product_name=record.name,
            sku_code=record.sku_code,
            cover_image=self._media_url(record.main_image_url) if record.main_image_url else None,
            specification=record.spec_name or record.size,
            category_name=record.category_name,
            brand_name=record.brand_name,
            style_tags=[record.surface_finish] if record.surface_finish else [],
            applicable_spaces=[record.category_name] if record.category_name else [],
            color_family=record.color_family,
            price_display=_price_display(record.reference_price),
            is_new=is_new,
            is_hot=force_hot or record.hot_score > 0,
        )

    @staticmethod
    def _best_match(
        brands: list[object],
        certificates: list[object],
        product_cards: list[MiniappProductCard],
        normalized_keyword: str,
    ) -> dict[str, object] | None:
        keyword = normalized_keyword.strip().lower()
        if not keyword:
            return None
        for card in product_cards:
            sku_code = (card.sku_code or "").strip().lower()
            product_name = (card.product_name or "").strip().lower()
            if sku_code == keyword or sku_code.startswith(keyword):
                data = card.model_dump()
                data["entity_type"] = "sku"
                return data
            if product_name == keyword or product_name.startswith(keyword):
                data = card.model_dump()
                data["entity_type"] = "sku"
                return data
        for brand in brands:
            brand_name = str(getattr(brand, "name", "") or "").strip()
            if brand_name.lower() == keyword:
                brand_id = getattr(brand, "id", None)
                return {
                    "entity_type": "brand",
                    "id": brand_id,
                    "name": brand_name,
                    "title": brand_name,
                    "count": getattr(brand, "count", 0),
                    "target_path": _target_path("brand", brand_id, brand_name),
                }
        for certificate in certificates:
            name = str(getattr(certificate, "name", "") or "").strip()
            certificate_no = str(getattr(certificate, "certificate_no", "") or "").strip()
            if name.lower() == keyword or (certificate_no and certificate_no.lower() == keyword):
                return {
                    "entity_type": "certificate",
                    "id": getattr(certificate, "id", None),
                    "name": name,
                    "title": name,
                    "certificate_no": getattr(certificate, "certificate_no", None),
                    "issuer": getattr(certificate, "issuer", None),
                    "brand_name": getattr(certificate, "brand_name", None),
                    "file_url": getattr(certificate, "file_url", None),
                    "target_path": f"/pages/search/index?keyword={normalized_keyword}&tab=certificate",
                }
        return None

    def _setting(self, key: str, default: str | None) -> str | None:
        record = self._settings_repo.get(key)
        if record is None:
            return default
        value = record.value.strip()
        return value or default

    @staticmethod
    def _media_url(object_key: str) -> str:
        return object_key if object_key.startswith(("/", "http://", "https://")) else f"/media/{object_key}"


def _price_display(value: float | None) -> str:
    if value is None or value <= 0:
        return "暂无"
    return f"¥{value:.2f}"


_CERTIFICATE_TYPE_LABELS = {
    "QUALITY": "质量认证",
    "INSPECTION": "检测报告",
    "GREEN_BUILDING": "绿色建材",
    "HONOR": "荣誉资质",
    "OTHER": "其他证书",
}

_VALIDITY_STATUS_LABELS = {
    "PERMANENT": "长期有效",
    "VALID": "有效",
    "EXPIRING_SOON": "即将到期",
    "EXPIRED": "已过期",
    "UNSET": "未设置有效期",
}


def _certificate_type_label(value: str | None) -> str:
    return _CERTIFICATE_TYPE_LABELS.get(value or "", "其他证书")


def _certificate_file_kind(
    mime_type: str | None,
    file_url: str | None,
    file_name: str | None,
) -> str:
    value = " ".join([mime_type or "", file_url or "", file_name or ""]).lower()
    if "pdf" in value:
        return "pdf"
    if any(token in value for token in ["image/", ".jpg", ".jpeg", ".png", ".webp", ".gif"]):
        return "image"
    return "unknown"


def _certificate_validity_status(record) -> str:
    if record.is_permanent:
        return "PERMANENT"
    if not record.expiry_date:
        return "UNSET"
    try:
        expiry = datetime.fromisoformat(str(record.expiry_date).replace("Z", "+00:00")).date()
    except ValueError:
        return "UNSET"
    today = datetime.now(UTC).date()
    if expiry < today:
        return "EXPIRED"
    if expiry <= today + timedelta(days=30):
        return "EXPIRING_SOON"
    return "VALID"


def _parse_price_range(value: str | None) -> tuple[float | None, float | None]:
    cleaned = (value or "").strip()
    if not cleaned:
        return None, None
    if "-" not in cleaned:
        return None, None
    raw_min, raw_max = cleaned.split("-", 1)
    try:
        price_min = float(raw_min) if raw_min else None
        price_max = float(raw_max) if raw_max else None
    except ValueError:
        return None, None
    if price_min is not None and price_min < 0:
        return None, None
    if price_max is not None and price_max < 0:
        return None, None
    if price_min is not None and price_max is not None and price_min > price_max:
        return None, None
    return price_min, price_max


def _category_path(path: str | None, fallback: str | None) -> list[str]:
    cleaned = [item for item in (path or "").replace(">", "/").split("/") if item]
    if cleaned:
        return cleaned
    return [fallback] if fallback else []


def _category_tree_version(categories: list[MiniappCategoryRecord]) -> str:
    if not categories:
        return "empty"
    latest = max(item.updated_at or item.created_at for item in categories)
    return f"{len(categories)}-{latest}"


def _is_recent(value: str) -> bool:
    try:
        created = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return False
    if created.tzinfo is None:
        created = created.replace(tzinfo=UTC)
    return created >= datetime.now(UTC) - timedelta(days=90)


def _normalize_keyword(value: str) -> str:
    return " ".join(value.strip().split())[:80]


def _request_id(keyword: str) -> str:
    stamp = int(datetime.now(UTC).timestamp() * 1000)
    suffix = abs(hash(keyword)) % 10000
    return f"search-{stamp}-{suffix}"


def _meets_suggestion_threshold(value: str) -> bool:
    if not value:
        return False
    return len(value) >= 1 if any("\u4e00" <= char <= "\u9fff" for char in value) else len(value) >= 2


def _unique_non_empty(values: list[str | None]) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for value in values:
        cleaned = (value or "").strip()
        if cleaned and cleaned not in seen:
            seen.add(cleaned)
            result.append(cleaned)
    return result


def _public_summary(value: str | None) -> str | None:
    cleaned = " ".join((value or "").split())
    if not cleaned:
        return None
    return cleaned[:36]


def _target_path(entity_type: str, entity_id: int, name: str) -> str:
    if entity_type == "category":
        return f"/pages/product-list/index?categoryId={entity_id}&categoryName={name}"
    return f"/pages/search/index?keyword={name}&tab={entity_type}"


def _dedupe_suggestions(items: list[MiniappSearchSuggestion]) -> list[MiniappSearchSuggestion]:
    seen: set[tuple[str, str]] = set()
    result: list[MiniappSearchSuggestion] = []
    for item in items:
        key = (item.entity_type, item.text)
        if key in seen:
            continue
        seen.add(key)
        result.append(item)
    return result
