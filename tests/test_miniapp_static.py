from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MINIAPP = ROOT / "src" / "miniapp"


def _read(path: str) -> str:
    return (MINIAPP / path).read_text(encoding="utf-8")


def test_miniapp_routes_cover_home_search_detail_store_and_tabbar() -> None:
    config = json.loads(_read("app.json"))

    assert "pages/index/index" in config["pages"]
    assert "pages/search/index" in config["pages"]
    assert "pages/tile-detail/index" in config["pages"]
    assert "pages/store-info/index" in config["pages"]
    assert "pages/favorites/index" in config["pages"]
    assert "pages/certificates/index" in config["pages"]
    assert "pages/product-list/index" in config["pages"]
    assert [item["text"] for item in config["tabBar"]["list"]] == [
        "首页",
        "分类",
        "找砖",
        "收藏",
        "证书",
    ]
    assert config["tabBar"]["custom"] is True
    for item in config["tabBar"]["list"]:
        assert item["iconPath"].startswith("assets/tabbar/")
        assert item["selectedIconPath"].startswith("assets/tabbar/")
        assert (MINIAPP / item["iconPath"]).exists()
        assert (MINIAPP / item["selectedIconPath"]).exists()
    assert (MINIAPP / "custom-tab-bar/index.wxml").exists()
    assert (MINIAPP / "custom-tab-bar/index.wxss").exists()


def test_miniapp_home_detail_search_smoke_contracts() -> None:
    home_ts = _read("pages/index/index.ts")
    search_ts = _read("pages/search/index.ts")
    detail_ts = _read("pages/tile-detail/index.ts")
    store_ts = _read("pages/store-info/index.ts")

    assert "/api/v1/miniapp/home" in home_ts
    assert "/api/v1/miniapp/search/suggestions" in search_ts
    assert "/api/v1/miniapp/search?" in search_ts
    assert "DEBOUNCE_MS = 300" in search_ts
    assert "suggestionSeq" in search_ts
    assert "miniapp_search_recent_keywords_v1" in search_ts
    assert "search_filter_apply" in search_ts
    assert "/api/v1/miniapp/skus/${id}" in detail_ts
    assert "/api/v1/miniapp/products/${id}" in detail_ts
    assert "legacyToSkuDetail" in detail_ts
    assert "home_share" in home_ts
    assert "miniapp_home_search_click" in home_ts
    assert "miniapp_home_quick_entry_click" in home_ts
    assert "miniapp_home_waterfall_load" in home_ts
    assert "miniapp_home_waterfall_load_failed" in home_ts
    assert "miniapp_home_waterfall_end_reached" in home_ts
    assert "miniapp_home_favorite_visual_click" in home_ts
    assert "sku_detail_view" in detail_ts
    assert "sku_share_click" in detail_ts
    assert "sku_favorite" in detail_ts
    assert "sku_unfavorite" in detail_ts
    assert "sku_brand_click" in detail_ts
    assert "sku_recommend_click" in detail_ts
    assert "sku_load_error" in detail_ts
    assert "home_contact_click" in store_ts


def test_miniapp_local_api_base_urls_cover_default_and_docker_override() -> None:
    app_js = _read("app.js")
    app_ts = _read("app.ts")
    api_js = _read("services/api.js")
    api_ts = _read("services/api.ts")
    project_config = json.loads(_read("project.config.json"))
    private_config = json.loads(_read("project.private.config.json"))

    assert "apiBaseUrl: 'http://localhost:8000'" in app_js
    assert "apiFallbackBaseUrls: ['http://127.0.0.1:8010', 'http://localhost:8010']" in app_js
    assert "apiFallbackBaseUrls: ['http://127.0.0.1:8010', 'http://localhost:8010']" in app_ts
    assert "function baseUrls()" in api_js
    assert "function baseUrls(): string[]" in api_ts
    assert "tryRequest(index + 1)" in api_js
    assert "function normalizeMediaUrls" in api_js
    assert "value.indexOf('/media/') === 0" in api_js
    assert "resolve(normalizeMediaUrls(body.data, currentBaseUrl))" in api_js
    assert project_config["setting"]["urlCheck"] is False
    assert private_config["setting"]["urlCheck"] is False


def test_miniapp_runtime_entry_scripts_are_not_empty_templates() -> None:
    critical_pages = [
        "pages/index/index",
        "pages/search/index",
        "pages/tile-detail/index",
        "pages/store-info/index",
        "pages/category/index",
        "pages/product-list/index",
        "pages/favorites/index",
        "pages/certificates/index",
    ]

    for page in critical_pages:
        js_source = _read(f"{page}.js")
        ts_source = _read(f"{page}.ts")

        assert "Page({" in js_source
        assert "data: {\n\n  }" not in js_source
        assert "onLoad(options) {\n\n  }" not in js_source
        assert len(js_source) > 0.45 * len(ts_source)


def test_miniapp_runtime_js_avoids_preview_incompatible_syntax() -> None:
    for path in MINIAPP.rglob("*.js"):
        source = path.read_text(encoding="utf-8")

        assert "?." not in source, f"{path} uses optional chaining"
        assert "??" not in source, f"{path} uses nullish coalescing"


def test_miniapp_home_runtime_entry_loads_home_data_and_interactions() -> None:
    home_js = _read("pages/index/index.js")
    home_wxml = _read("pages/index/index.wxml")

    assert "loading: true" in home_js
    assert "home: null" in home_js
    assert "errorDetail: ''" in home_js
    assert "allProducts: []" in home_js
    assert "productsHasMore: true" in home_js
    assert "loadHome()" in home_js
    assert "loadAllProducts(reset)" in home_js
    assert "this.loadHome()" in home_js
    assert "this.loadAllProducts(true)" in home_js
    assert "/api/v1/miniapp/home" in home_js
    assert "/api/v1/miniapp/products?page=" in home_js
    assert "error.attempts" in home_js
    assert "诊断：{{errorDetail}}" in home_wxml
    assert "openSearch()" in home_js
    assert "openStoreInfo()" in home_js
    assert "openQuickEntry(event)" in home_js
    assert "openBanner(event)" in home_js
    assert "openProduct(event)" in home_js
    assert "retryAllProducts()" in home_js
    assert "mergeProducts(existing, incoming)" in home_js
    assert "onImageError(event)" in home_js
    assert "home_share" in home_js
    assert "miniapp_home_waterfall_load" in home_js


def test_miniapp_home_custom_navigation_excludes_store_info_and_fake_system_controls() -> None:
    home_config = json.loads(_read("pages/index/index.json"))
    home_wxml = _read("pages/index/index.wxml")
    nav_wxml = _read("components/custom-navigation/index.wxml")
    nav_wxss = _read("components/custom-navigation/index.wxss")
    nav_js = _read("components/custom-navigation/index.js")
    home_ts = _read("pages/index/index.ts")
    home_js = _read("pages/index/index.js")

    assert home_config["navigationStyle"] == "custom"
    assert home_config["usingComponents"]["custom-navigation"] == "../../components/custom-navigation/index"
    assert "navigationStyle" not in json.loads(_read("app.json"))["window"]
    assert '<view class="page">' in home_wxml
    assert '<custom-navigation' in home_wxml
    assert 'variant="home"' in home_wxml
    assert "store-name" in home_wxml
    assert "logo-src" in home_wxml

    assert "store-logo" in nav_wxml
    assert "store-name" in nav_wxml
    assert "store-subtitle" in nav_wxml
    assert "back-hit-area" in nav_wxml
    assert "wx:if=\"{{variant !== 'home'}}\"" in nav_wxml
    assert "native-action-reserve" in nav_wxml
    assert "store-link" not in nav_wxml
    assert "门店信息" not in nav_wxml
    assert "openStoreInfo" not in nav_wxml
    assert "position: fixed" in nav_wxss
    assert "z-index: 30" in nav_wxss
    assert "align-items: center" in nav_wxss
    assert "height: 106px" in nav_js
    assert "reserveStyle: 'width: 92px; flex-basis: 92px;'" in nav_js
    assert "height: 88rpx" in nav_wxss
    assert "flex: 0 0 76rpx" in nav_wxss
    assert "justify-content: center" in nav_wxss
    assert "align-self: center" in nav_wxss
    assert "wx.getSystemInfoSync()" in nav_js
    assert "wx.getMenuButtonBoundingClientRect" in nav_js
    assert "onShareAppMessage()" in home_ts
    assert "onShareAppMessage()" in home_js

    forbidden_lookalikes = [
        "mini-capsule",
        "capsule",
        "share-control",
        "close-control",
        "share-button",
        "close-button",
        "system-close",
        "system-share",
    ]
    home_source = "\n".join([home_wxml, nav_wxml, nav_wxss])
    for token in forbidden_lookalikes:
        assert token not in home_source


def test_miniapp_global_custom_navigation_covers_subpages_and_back_fallback() -> None:
    covered_pages = [
        ("pages/search/index", "搜索"),
        ("pages/tile-detail/index", "商品详情"),
        ("pages/category/index", "全部分类"),
        ("pages/product-list/index", "{{title}}"),
        ("pages/favorites/index", "{{title}}"),
        ("pages/certificates/index", "{{title}}"),
        ("pages/store-info/index", "门店信息"),
    ]
    nav_js = _read("components/custom-navigation/index.js")
    nav_ts = _read("components/custom-navigation/index.ts")
    nav_wxml = _read("components/custom-navigation/index.wxml")
    nav_wxss = _read("components/custom-navigation/index.wxss")

    assert "Component({" in nav_js
    assert "variant: { type: String, value: 'subpage' }" in nav_js
    assert "getCurrentPages()" in nav_js
    assert "pages.length > 1" in nav_js
    assert "wx.navigateBack" in nav_js
    assert "wx.switchTab({ url: '/pages/index/index' })" in nav_js
    assert "wx.reLaunch({ url: '/pages/index/index' })" in nav_js
    assert "wx.getSystemInfoSync()" in nav_ts
    assert "wx.getMenuButtonBoundingClientRect" in nav_ts
    assert "systemInfo.windowWidth - menuButton.left + 8" in nav_ts
    assert "back-hit-area" in nav_wxml
    assert "subpage-title" in nav_wxml
    assert "native-action-reserve" in nav_wxml
    assert "width: 88rpx" in nav_wxss
    assert "height: 88rpx" in nav_wxss
    assert "min-width: 184rpx" in nav_wxss

    for page, title in covered_pages:
        config = json.loads(_read(f"{page}.json"))
        wxml = _read(f"{page}.wxml")

        assert config["navigationStyle"] == "custom"
        assert config["usingComponents"]["custom-navigation"] == "../../components/custom-navigation/index"
        assert "<custom-navigation" in wxml
        assert f'title="{title}"' in wxml

    search_wxml = _read("pages/search/index.wxml")
    assert "nav-btn" not in search_wxml
    assert "open-type=\"share\"" in _read("pages/tile-detail/index.wxml")
    assert "skuId=${product.product_id}&source=share" in _read("pages/tile-detail/index.js")


def test_miniapp_category_page_covers_tree_cache_navigation_and_states() -> None:
    category_js = _read("pages/category/index.js")
    category_ts = _read("pages/category/index.ts")
    category_wxml = _read("pages/category/index.wxml")
    category_wxss = _read("pages/category/index.wxss")

    assert "/api/v1/miniapp/categories/tree?depth=2" in category_ts
    assert "miniapp_category_tree_cache_v1" in category_js
    assert "miniapp_category_page_state_v1" in category_js
    assert "category_page_view" in category_js
    assert "primary_category_click" in category_js
    assert "secondary_category_click" in category_js
    assert "openSearch" in category_js
    assert "sourcePage=category" in category_js
    assert "category_load_failed" in category_js
    assert "CLICK_DEBOUNCE_MS = 300" in category_js
    assert "页面打开失败，请重试" in category_js
    assert "网络异常，已展示缓存" in category_js
    assert "getTabBar" in category_js
    assert "scroll-top=\"{{leftScrollTop}}\"" in category_wxml
    assert "scroll-top=\"{{rightScrollTop}}\"" in category_wxml
    assert "binderror=\"onImageError\"" not in category_wxml
    assert "onImageError" not in category_js
    assert "secondary-image" not in category_wxml
    assert "该分类暂未配置二级分类" in category_wxml
    assert "skeleton-shell" in category_wxml
    assert "brand-header" not in category_wxml
    assert "store-logo" not in category_wxml
    assert "page-title-row" not in category_wxml
    assert ".page-title-row" not in category_wxss
    assert "search-box" in category_wxml
    assert "/pages/product-list/index?categoryId=" in category_js
    assert "商品卡片" not in category_wxml
    assert "价格" not in category_wxml
    assert "热门分类" not in category_wxml
    assert "width: 196rpx" in category_wxss
    assert "grid-template-columns: repeat(3, minmax(0, 1fr))" in category_wxss
    assert "aspect-ratio: 1 / 1" not in category_wxss
    assert ".secondary-image" not in category_wxss
    assert "min-height: 96rpx" in category_wxss
    assert "min-height: 112rpx" in category_wxss
    assert "background: #18160F" in category_wxss
    assert "color: #C8A055" in category_wxss
    assert ".brand-header" not in category_wxss
    assert ".search-box" in category_wxss


def test_miniapp_product_list_page_carries_category_navigation() -> None:
    app_config = json.loads(_read("app.json"))
    product_list_js = _read("pages/product-list/index.js")
    product_list_ts = _read("pages/product-list/index.ts")
    product_list_wxml = _read("pages/product-list/index.wxml")
    product_list_wxss = _read("pages/product-list/index.wxss")

    assert "pages/product-list/index" in app_config["pages"]
    assert "categoryId" in product_list_js
    assert "categoryName" in product_list_js
    assert "brandId" in product_list_js
    assert "keyword" in product_list_js
    assert "priceRange" in product_list_js
    assert "filter_type=category" in product_list_js
    assert "filter_value=" in product_list_js
    assert "pageSize" in product_list_js
    assert "product_list_page_view" in product_list_js
    assert "product_list_item_exposure" in product_list_js
    assert "product_list_item_click" in product_list_js
    assert "product_list_filter_open" in product_list_js
    assert "product_list_filter_apply" in product_list_js
    assert "product_list_sort_change" in product_list_js
    assert "product_list_refresh" in product_list_js
    assert "product_list_load_more" in product_list_js
    assert "product_list_load_failed" in product_list_js
    assert "filterSnapshot" in product_list_js
    assert "mergeProducts" in product_list_js
    assert "onPullDownRefresh" in product_list_js
    assert "onReachBottom" in product_list_js
    assert "/api/v1/miniapp/products?" in product_list_ts
    assert "wx.setNavigationBarTitle" in product_list_js
    assert "/pages/tile-detail/index?skuId=" in product_list_js
    assert "分类商品加载失败，请重试" in product_list_js
    assert "该分类暂未上架商品" in product_list_js
    assert "list-header" not in product_list_wxml
    assert "list-header" not in product_list_wxss
    assert "product-card" in product_list_wxml
    assert "filter-drawer" in product_list_wxml
    assert "sort-tabs" in product_list_wxml
    assert "activeFilterChips" in product_list_wxml
    assert "加载更多失败，点击重试" in product_list_js
    assert "收藏" not in product_list_wxml
    assert "购物车" not in product_list_wxml
    assert "立即购买" not in product_list_wxml
    assert "询价" not in product_list_wxml
    assert "background: #18160F" in product_list_wxss
    assert "color: #C8A055" in product_list_wxss
    assert "env(safe-area-inset-bottom)" in product_list_wxss
    assert "min-height: 88rpx" in product_list_wxss


def test_miniapp_home_images_have_runtime_fallback_handlers() -> None:
    home_wxml = _read("pages/index/index.wxml")
    home_js = _read("pages/index/index.js")

    assert 'binderror="onImageError"' in home_wxml
    assert "<swiper" in home_wxml
    assert 'wx:for="{{home.banners}}"' in home_wxml
    assert 'src="{{item.image_url}}"' in home_wxml
    assert 'data-key="home.banners[{{index}}].image_url"' in home_wxml
    assert 'src="{{item.cover_image || imageFallback}}"' in home_wxml
    assert 'data-key="home.new_products[{{index}}].cover_image"' in home_wxml
    assert 'data-key="home.hot_products[{{index}}].cover_image"' in home_wxml
    assert 'data-key="allProducts[{{index}}].cover_image"' in home_wxml
    assert "imageFallback: '/assets/tile-placeholder.png'" in home_js
    assert "this.setData({ [key]: this.data.imageFallback })" in home_js


def test_miniapp_sku_detail_page_covers_media_favorite_share_and_empty_states() -> None:
    detail_js = _read("pages/tile-detail/index.js")
    detail_ts = _read("pages/tile-detail/index.ts")
    detail_wxml = _read("pages/tile-detail/index.wxml")
    detail_wxss = _read("pages/tile-detail/index.wxss")

    assert "/api/v1/miniapp/skus/${id}?client_id=" in detail_ts
    assert "/api/v1/miniapp/skus/${product.product_id}/favorite" in detail_ts
    assert "wx.previewImage" in detail_ts
    assert "wx.createVideoContext" in detail_ts
    assert "onHide()" in detail_ts
    assert "previous = product.favorite" in detail_js
    assert "'product.favorite': previous" in detail_js
    assert "sku_media_swipe" in detail_js
    assert "sku_image_preview" in detail_js
    assert "sku_video_play" in detail_js
    assert "sku_share_click" in detail_js
    assert "sku_recommend_click" in detail_js
    assert "商品暂不可查看" in detail_js
    assert "skeleton" in detail_wxml
    assert "<swiper" in detail_wxml
    assert "<video" in detail_wxml
    assert "media-count" in detail_wxml
    assert "品牌" in detail_wxml
    assert "action-icon" in detail_wxml
    assert "分享给客户" in detail_wxml
    assert "同系列推荐" in detail_wxml
    assert "同品牌推荐" in detail_wxml
    assert "购物车" not in detail_wxml
    assert "立即购买" not in detail_wxml
    assert "库存" not in detail_wxml
    assert "grid-template-columns: repeat(3, minmax(0, 1fr))" in detail_wxss
    assert "height: 88rpx" in detail_wxss
    assert "padding: 0" in detail_wxss
    assert "background: transparent" in detail_wxss
    assert "border-radius: 28rpx" in detail_wxss
    assert "env(safe-area-inset-bottom)" in detail_wxss
    assert "min-height: 88rpx" in detail_wxss


def test_miniapp_home_matches_prototype_structure_and_visual_tokens() -> None:
    home_wxml = _read("pages/index/index.wxml")
    home_wxss = _read("pages/index/index.wxss")

    for token in [
        "search-box",
        "hero-button",
        "hero-dots",
        "shortcut-icon",
        "visual-heart",
        "waterfall",
        "load-more",
    ]:
        assert token in home_wxml

    for title in ["选瓷砖", "品牌馆", "新品榜", "热销榜"]:
        assert title in home_wxml or title in _read("pages/index/index.js")

    assert (MINIAPP / "assets/logos/product-logo.png").exists()
    assert "mini-capsule" not in home_wxml
    assert "brand-logo" not in home_wxml
    assert "到店咨询" not in home_wxml
    assert "到店询价" not in home_wxml

    for token in [
        "background: #18160F",
        "background: #211E16",
        "color: #C8A055",
        "color: #EDE8DF",
        "grid-template-columns: repeat(4, 1fr)",
        "grid-template-columns: repeat(2, 1fr)",
        "column-count: 2",
        "background: rgba(24,22,15,0.88)",
    ]:
        assert token in home_wxss


def test_miniapp_custom_tabbar_has_larger_text_and_icons() -> None:
    tabbar_wxml = _read("custom-tab-bar/index.wxml")
    tabbar_wxss = _read("custom-tab-bar/index.wxss")
    tabbar_js = _read("custom-tab-bar/index.js")

    assert "tabbar-icon" in tabbar_wxml
    assert "tabbar-text" in tabbar_wxml
    assert "wx.switchTab" in tabbar_js
    assert "收藏" in tabbar_js
    assert "证书" in tabbar_js
    assert "font-size: 24rpx" in tabbar_wxss
    assert "width: 46rpx" in tabbar_wxss
    assert "height: 46rpx" in tabbar_wxss
    assert "grid-template-columns: repeat(5, 1fr)" in tabbar_wxss


def test_miniapp_scope_excludes_favorite_appointment_and_admin_config() -> None:
    source = "\n".join(
        path.read_text(encoding="utf-8")
        for path in MINIAPP.rglob("*.*")
        if path.suffix in {".js", ".ts", ".json", ".wxml", ".wxss", ".md"}
    )

    forbidden_terms = [
        "appointment",
        "预约",
        "inquiry",
        "询价规则",
        "admin-config",
        "后台配置",
        "user-profile",
        "用户画像",
        "favorite_api",
        "favorite_list",
        "certificate_api",
    ]
    for term in forbidden_terms:
        assert term not in source


def test_miniapp_styles_keep_primary_tappable_targets_at_least_44pt() -> None:
    css = "\n".join(path.read_text(encoding="utf-8") for path in MINIAPP.rglob("*.wxss"))

    assert "min-height: 88rpx" in css
    assert "env(safe-area-inset-bottom)" in css
    assert "overflow: hidden" in css
