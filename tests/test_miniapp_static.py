from __future__ import annotations

import json
from pathlib import Path

from path_helpers import resolve_change_file


ROOT = Path(__file__).resolve().parents[1]
MINIAPP = ROOT / "src" / "miniapp"
SKILLS = ROOT / ".agents" / "skills"


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
    assert "pages/brand-list/index" in config["pages"]
    assert "pages/brand-detail/index" in config["pages"]
    assert [item["text"] for item in config["tabBar"]["list"]] == [
        "首页",
        "分类",
        "品牌",
        "证书",
        "收藏",
    ]
    assert config["tabBar"]["custom"] is True
    for item in config["tabBar"]["list"]:
        assert item["iconPath"].startswith("assets/tabbar/")
        assert item["selectedIconPath"].startswith("assets/tabbar/")
        assert (MINIAPP / item["iconPath"]).exists()
        assert (MINIAPP / item["selectedIconPath"]).exists()
    brand_tab = next(item for item in config["tabBar"]["list"] if item["text"] == "品牌")
    assert brand_tab["iconPath"] == "assets/tabbar/brand-default.png"
    assert brand_tab["selectedIconPath"] == "assets/tabbar/brand-active.png"
    certificate_tab = next(item for item in config["tabBar"]["list"] if item["text"] == "证书")
    favorite_tab = next(item for item in config["tabBar"]["list"] if item["text"] == "收藏")
    assert certificate_tab["iconPath"] == "assets/tabbar/certificate-default.png"
    assert certificate_tab["selectedIconPath"] == "assets/tabbar/certificate-active.png"
    assert favorite_tab["iconPath"] == "assets/tabbar/favorite-default.png"
    assert favorite_tab["selectedIconPath"] == "assets/tabbar/favorite-active.png"
    assert certificate_tab["iconPath"] != favorite_tab["iconPath"]
    assert certificate_tab["selectedIconPath"] != favorite_tab["selectedIconPath"]
    assert (MINIAPP / "custom-tab-bar/index.wxml").exists()
    assert (MINIAPP / "custom-tab-bar/index.wxss").exists()


def test_miniapp_home_detail_search_smoke_contracts() -> None:
    home_ts = _read("pages/index/index.ts")
    search_ts = _read("pages/search/index.ts")
    detail_ts = _read("pages/tile-detail/index.ts")
    store_ts = _read("pages/store-info/index.ts")
    brand_list_ts = _read("pages/brand-list/index.ts")
    brand_detail_ts = _read("pages/brand-detail/index.ts")
    brand_detail_wxml = _read("pages/brand-detail/index.wxml")
    brand_detail_wxss = _read("pages/brand-detail/index.wxss")

    assert "/api/v1/miniapp/home" in home_ts
    assert "/api/v1/miniapp/search/suggestions" in search_ts
    assert "/api/v1/miniapp/search?" in search_ts
    assert "DEBOUNCE_MS = 300" in search_ts
    assert "suggestionSeq" in search_ts
    assert "miniapp_search_recent_keywords_v1" in search_ts
    assert "search_filter_apply" in search_ts
    assert "/api/v1/miniapp/skus/${id}" in detail_ts
    assert "/api/v1/miniapp/products/${id}" in detail_ts
    assert "/api/v1/miniapp/brands?page=" in brand_list_ts
    assert "/api/v1/miniapp/brands/${this.data.brandId}" in brand_detail_ts
    assert "/api/v1/miniapp/brands/${this.data.brandId}/certificates" in brand_detail_ts
    assert "/api/v1/miniapp/products?brandId=${this.data.brandId}" in brand_detail_ts
    assert "legacyToSkuDetail" in detail_ts
    assert "home_share" in home_ts
    assert "miniapp_home_search_click" in home_ts
    assert "miniapp_home_quick_entry_click" in home_ts
    assert "miniapp_home_waterfall_load" in home_ts
    assert "miniapp_home_waterfall_load_failed" in home_ts
    assert "miniapp_home_waterfall_end_reached" in home_ts
    assert "sku_detail_view" in detail_ts
    assert "sku_share_click" in detail_ts
    assert "sku_favorite" in detail_ts
    assert "sku_unfavorite" in detail_ts
    assert 'source-module="sku-detail-brand"' in _read("pages/tile-detail/index.wxml")
    assert "sku_recommend_click" in detail_ts
    assert "sku_load_error" in detail_ts
    assert "brand_list_page_view" in brand_list_ts
    assert "brand_list_carousel_click" in brand_list_ts
    assert "brand_list_card_click" in brand_list_ts
    assert "brand_detail_view" in brand_detail_ts
    assert "brand_detail_tab_click" in brand_detail_ts
    assert "brand_certificate_click" in brand_detail_ts
    assert "normalizeCertificate" in brand_detail_ts
    assert "return brand?.brand_name || '品牌主页';" in brand_detail_ts
    assert "brand?.brand_short_name || brand?.brand_name" not in brand_detail_ts
    assert 'class="brand-overlay"' in brand_detail_wxml
    assert brand_detail_wxml.index('class="brand-logo-frame') < brand_detail_wxml.index('class="brand-overlay"')
    assert "height: 380rpx" in brand_detail_wxss
    assert ".brand-hero {\n  margin-top: 12rpx;\n  padding: 0;" in brand_detail_wxss
    assert "brand-meta" not in brand_detail_wxml
    assert "product_count}} 款商品" not in brand_detail_wxml
    assert 'class="tab-scroll"' in brand_detail_wxml
    assert ".tab-scroll" in brand_detail_wxss
    assert 'class="certificate-grid"' in brand_detail_wxml
    assert 'class="file-frame {{item.file_kind}}"' in brand_detail_wxml
    assert ".type-badge" in brand_detail_wxss
    assert "home_contact_click" in store_ts


def test_miniapp_local_api_base_urls_cover_default_and_docker_override() -> None:
    app_js = _read("app.js")
    app_ts = _read("app.ts")
    api_js = _read("services/api.js")
    api_ts = _read("services/api.ts")
    env_js = _read("utils/env.js")
    env_ts = _read("utils/env.ts")
    project_config = json.loads(_read("project.config.json"))
    private_config = json.loads(_read("project.private.config.json"))

    for source in [env_js, env_ts]:
        assert "environment: 'development'" in source
        assert "apiBaseUrl: 'http://127.0.0.1:8010'" in source
        assert "apiFallbackBaseUrls: ['http://localhost:8010', 'http://localhost:8000']" in source
        assert "environment: 'production'" in source
        assert "apiBaseUrl: 'https://tilesfst.wjoyhappy.site'" in source
        assert any(
            marker in source
            for marker in [
                "return 'development'",
                "return 'production'",
                "envVersion === 'develop' ? 'development' : 'production'",
            ]
        )
    assert "environment: miniappApiConfig.environment" in app_js
    assert "apiBaseUrl: miniappApiConfig.apiBaseUrl" in app_js
    assert "apiFallbackBaseUrls: miniappApiConfig.apiFallbackBaseUrls" in app_ts
    assert "const DEFAULT_BASE_URL = miniappApiConfig.apiBaseUrl" in api_js
    assert "const DEFAULT_BASE_URL = miniappApiConfig.apiBaseUrl" in api_ts
    assert "function baseUrls()" in api_js
    assert "function baseUrls(): string[]" in api_ts
    assert "tryRequest(index + 1)" in api_js
    assert "res.statusCode >= 500 && index + 1 < urls.length" in api_js
    assert "function normalizeMediaUrls" in api_js
    assert "value.indexOf('/media/') === 0" in api_js
    assert "resolve(normalizeMediaUrls(body.data, currentBaseUrl))" in api_js
    is_prod_strategy = "return 'production'" in env_js and "return 'production'" in env_ts
    assert project_config["setting"]["urlCheck"] is False
    assert private_config["setting"]["urlCheck"] is (True if is_prod_strategy else False)


def test_miniapp_environment_command_skills_exist() -> None:
    for command in [
        "miniapp-env",
        "miniapp-check",
        "miniapp-prepare",
        "miniapp-confirm",
        "miniapp-restore",
    ]:
        source = (SKILLS / command / "SKILL.md").read_text(encoding="utf-8")
        assert f'name: "{command}"' in source
        assert "rules/agent-context-budget.md" in source

    for command in ["miniapp-env", "miniapp-check", "miniapp-prepare", "miniapp-restore"]:
        source = (SKILLS / command / "SKILL.md").read_text(encoding="utf-8")
        assert "project.private.config.json" in source
        assert "urlCheck" in source


def test_miniapp_env_script_manages_devtools_url_check() -> None:
    script = (ROOT / "scripts" / "miniapp-env.py").read_text(encoding="utf-8")

    assert "PROJECT_PRIVATE_CONFIG" in script
    assert "_set_devtools_url_check(strategy == \"prod\")" in script
    assert "\"expected_urlCheck\": True if strategy == \"prod\" else False" in script


def test_miniapp_runtime_entry_scripts_are_not_empty_templates() -> None:
    critical_pages = [
        "pages/index/index",
        "pages/search/index",
        "pages/tile-detail/index",
        "pages/store-info/index",
        "pages/category/index",
        "pages/product-list/index",
        "pages/brand-list/index",
        "pages/brand-detail/index",
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

    component_entries = [
        "components/product-card/index",
        "components/brand-card/index",
        "components/custom-navigation/index",
    ]
    for component in component_entries:
        js_source = _read(f"{component}.js")
        ts_source = _read(f"{component}.ts")

        assert "Component({" in js_source
        assert len(js_source) > 0.45 * len(ts_source)


def test_miniapp_category_secondary_names_support_long_labels() -> None:
    category_wxml = _read("pages/category/index.wxml")
    category_wxss = _read("pages/category/index.wxss")
    category_ts = _read("pages/category/index.ts")
    category_js = _read("pages/category/index.js")

    assert 'class="secondary-grid"' in category_wxml
    assert 'class="secondary-card"' in category_wxml
    assert '<view class="secondary-name">{{item.name}}</view>' in category_wxml
    assert "grid-template-columns: repeat(3, minmax(0, 1fr));" in category_wxss
    assert ".secondary-card {\n  min-width: 0;\n  min-height: 132rpx;" in category_wxss
    assert ".secondary-name {\n  width: 100%;" in category_wxss
    assert "line-height: 36rpx;" in category_wxss
    assert "white-space: normal;" in category_wxss
    assert "word-break: break-all;" in category_wxss
    assert "-webkit-line-clamp: 2;" in category_wxss
    assert ".secondary-name" in category_wxss
    secondary_name_block = category_wxss.split(".secondary-name {", 1)[1].split("}", 1)[0]
    assert "white-space: nowrap" not in secondary_name_block
    assert "text-overflow: ellipsis" not in secondary_name_block

    for source in [category_ts, category_js]:
        assert "categoryLevel=secondary&sourcePage=category" in source
        assert "categoryName=${encodeURIComponent(name)}" in source
        assert "rightScrollTop: 0" in source
        assert "this.data.categories.length && savedState.currentPrimaryId" in source
        assert "分类加载失败，请检查网络后重试" in source


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


def test_miniapp_home_recommendation_entries_route_to_product_list() -> None:
    home_ts = _read("pages/index/index.ts")
    home_js = _read("pages/index/index.js")
    home_wxml = _read("pages/index/index.wxml")

    for source in [home_ts, home_js]:
        assert "/pages/product-list/index?section=${entry.section}" in source
        assert "/pages/product-list/index?section=${section}" in source
        assert "/pages/search/index?section=" not in source
        assert "wx.navigateTo({ url: '/pages/search/index' })" in source
        assert "/pages/search/index?keyword=${encodeURIComponent" in source

    assert 'bindtap="openQuickEntry"' in home_wxml
    assert 'bindtap="openSection" data-section="new"' in home_wxml
    assert 'bindtap="openSection" data-section="hot"' in home_wxml


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
    assert "store-name" not in home_wxml
    assert "subtitle=" not in home_wxml
    assert "logo-src" in home_wxml

    assert "store-logo" in nav_wxml
    assert "store-name" in nav_wxml
    assert "store-subtitle" in nav_wxml
    assert "菲尚特瓷砖馆" in nav_wxml
    assert "质感空间，由砖而生" in nav_wxml
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


def test_miniapp_home_share_add_guide_uses_native_menu_reserve_and_session_dismissal() -> None:
    app_js = _read("app.js")
    app_ts = _read("app.ts")
    home_wxml = _read("pages/index/index.wxml")
    home_wxss = _read("pages/index/index.wxss")
    home_js = _read("pages/index/index.js")
    home_ts = _read("pages/index/index.ts")

    for source in [app_js, app_ts]:
        assert "miniapp_share_add_guide_session_closed_v1" in source
        assert "wx.removeStorageSync('miniapp_share_add_guide_session_closed_v1')" in source

    assert 'wx:if="{{shareAddGuideVisible}}"' in home_wxml
    assert 'class="share-add-guide"' in home_wxml
    assert "点击右上角" in home_wxml
    assert "添加到我的小程序，方便下次找回" in home_wxml
    assert 'class="guide-copy-line first-line"' in home_wxml
    assert 'class="guide-copy-line second-line"' in home_wxml
    assert 'class="guide-menu-dots"' in home_wxml
    assert home_wxml.count('class="guide-dot small"') == 2
    assert home_wxml.count('class="guide-dot large"') == 1
    assert 'bindtap="dismissShareAddGuide"' in home_wxml
    assert 'class="guide-dismiss"' in home_wxml
    assert "open-type=\"share\"" not in home_wxml

    for source in [home_js, home_ts]:
        assert "SHARE_ADD_GUIDE_SESSION_KEY" in source
        assert "shareAddGuideDismissedInSession" in source
        assert "prepareShareAddGuide()" in source
        assert "resolveShareAddGuideStyle()" in source
        assert "dismissShareAddGuide()" in source
        assert "wx.getStorageSync(SHARE_ADD_GUIDE_SESSION_KEY)" in source
        assert "wx.setStorageSync(SHARE_ADD_GUIDE_SESSION_KEY, 'closed')" in source
        assert "wx.getMenuButtonBoundingClientRect" in source
        assert "menuButton.bottom + 8" in source
        assert "systemInfo.windowWidth - menuButton.right + 44" in source
        assert "shareAddGuideVisible: !shareAddGuideDismissedInSession && !storageClosed" in source
        assert "shareAddGuideVisible: false" in source

    assert ".share-add-guide" in home_wxss
    assert ".guide-menu-dots" in home_wxss
    assert ".guide-dot.small" in home_wxss
    assert ".guide-dot.large" in home_wxss
    assert "position: fixed" in home_wxss
    assert "z-index: 32" in home_wxss
    assert "width: 500rpx" in home_wxss
    assert "max-width: calc(100vw - 48rpx)" in home_wxss
    assert "white-space: nowrap" in home_wxss
    assert "padding: 16rpx 76rpx 16rpx 24rpx" in home_wxss
    assert "width: 64rpx" in home_wxss
    assert "height: 64rpx" in home_wxss
    assert "overflow-x: hidden" in home_wxss
    assert "min-height: 76rpx" in home_wxss
    assert "guide-copy-line.second-line" in home_wxss

    forbidden_lookalikes = [
        "mini-capsule",
        "share-control",
        "close-control",
        "share-button",
        "close-button",
        "system-close",
        "system-share",
    ]
    guide_source = "\n".join([home_wxml, home_wxss])
    for token in forbidden_lookalikes:
        assert token not in guide_source


def test_miniapp_global_custom_navigation_covers_subpages_and_back_fallback() -> None:
    covered_pages = [
        ("pages/tile-detail/index", "商品详情"),
        ("pages/category/index", "全部分类"),
        ("pages/product-list/index", "{{title}}"),
        ("pages/brand-list/index", "品牌列表"),
        ("pages/brand-detail/index", "{{title}}"),
        ("pages/favorites/index", "收藏列表"),
        ("pages/certificates/index", "证书列表"),
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
    assert "subpage-subtitle" not in nav_wxml
    assert ".subpage-subtitle" not in nav_wxss
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
        assert "subtitle=" not in wxml

    search_wxml = _read("pages/search/index.wxml")
    search_config = json.loads(_read("pages/search/index.json"))
    assert search_config["navigationStyle"] == "custom"
    assert search_config["usingComponents"]["custom-navigation"] == "../../components/custom-navigation/index"
    assert search_config["usingComponents"]["search-entry"] == "../../components/search-entry/index"
    assert '<custom-navigation title="{{searchMode == \'result\' ? normalizedKeyword : \'搜索\'}}" />' in search_wxml
    assert "<search-entry" in search_wxml
    assert "nav-btn" not in search_wxml
    assert "open-type=\"share\"" in _read("pages/tile-detail/index.wxml")
    assert "skuId=${product.product_id}&source=share" in _read("pages/tile-detail/index.js")


def test_miniapp_search_matches_req0046_prototype_structure() -> None:
    search_wxml = _read("pages/search/index.wxml")
    search_wxss = _read("pages/search/index.wxss")
    search_js = _read("pages/search/index.js")
    entry_wxml = _read("components/search-entry/index.wxml")
    entry_wxss = _read("components/search-entry/index.wxss")
    entry_js = _read("components/search-entry/index.js")
    home_wxss = _read("pages/index/index.wxss")

    assert "<search-entry" in search_wxml
    assert 'wx:if="{{searchMode != \'result\'}}"' in search_wxml
    assert 'show-back="{{false}}"' in search_wxml
    assert 'bind:input="onSearchEntryInput"' in search_wxml
    assert 'bind:submit="onSearchEntrySubmit"' in search_wxml
    assert 'bind:cancel="cancelSearch"' in search_wxml
    assert "entry-back" in entry_wxml
    assert "entry-shell" in entry_wxml
    assert "entry-clear" in entry_wxml
    assert "entry-submit" not in entry_wxml
    assert "entry-icon" not in entry_wxml
    assert "event.detail.value" in entry_js
    assert "keyword," in entry_js
    assert "searchMode: 'home'" in search_js
    assert "searchMode: normalized ? 'suggest' : 'home'" in search_js
    assert "searchMode: 'result'" in search_js
    assert 'wx:elif="{{searchMode == \'suggest\'}}"' in search_wxml
    for token in [
        "min-height: 88rpx",
        "padding: 0 16rpx 0 28rpx",
        "border-radius: 44rpx",
        "background: #211E16",
        "border: 2rpx solid rgba(255,255,255,0.07)",
    ]:
        assert token in entry_wxss
        assert token in home_wxss
    assert "min-width: 112rpx" not in entry_wxss

    for token in ["最近搜索", "热门搜索"]:
        assert token in search_wxml
    assert "最近浏览" not in search_wxml
    assert 'source-module="recent_browsing"' not in search_wxml
    assert 'bindtap="deleteHistory"' in search_wxml
    assert 'bindtap="clearHistory"' in search_wxml

    assert "suggest-type\">历史" not in search_wxml
    for token in ["品牌", "SKU", "group_label"]:
        assert token in search_wxml or token in search_js
    assert "品牌 / SKU / 类目规格 / 搜索建议" not in search_wxml
    assert "item.entity_type === 'sku' || item.entity_type === 'brand'" in search_js
    assert "brandSuggestions" in search_js
    assert "skuSuggestions" in search_js
    assert 'wx:for="{{brandSuggestions}}"' in search_wxml
    assert 'wx:for="{{skuSuggestions}}"' in search_wxml
    assert "certificate" in search_js
    assert "suggestionGroupLabel" in search_js

    assert 'title="{{searchMode == \'result\' ? normalizedKeyword : \'搜索\'}}"' in search_wxml
    assert "const order = ['all', 'brand', 'sku', 'certificate']" in search_js
    assert "{ value: 'category', label: '类目', count: 0 }" not in search_js
    for token in ["综合", "SKU", "品牌", "证书"]:
        assert token in search_js
    assert "result-section" in search_wxml
    assert "displaySections" in search_js
    assert 'wx:for="{{displaySections}}"' in search_wxml
    assert "orderDisplaySections" in search_js
    assert "['brand', 'sku', 'certificate']" in search_js
    assert "section-result-product-card" in search_wxml
    assert "section-card-image-frame" in search_wxml
    assert "section-card-price" in search_wxml
    assert 'wx:if="{{activeTab == \'all\' && bestMatch}}"' in search_wxml
    assert "bestMatch.entity_type == 'sku'" in search_wxml
    assert 'data-item="{{bestMatch}}"' in search_wxml
    assert 'wx:if="{{activeTab == \'all\'}}"' in search_wxml
    assert 'wx:elif="{{activeDisplaySection}}"' in search_wxml
    assert "activeDisplaySection" in search_js
    assert "(section.count || 0) > 0 && (section.items || []).length > 0" in search_js
    assert 'wx:if="{{item.entity_type == \'sku\'}}"' in search_wxml
    assert 'source-module="section_sku"' in search_wxml
    assert 'product="{{sectionItem}}"' in search_wxml
    assert "sections: data.sections || []" in search_js
    assert "hasResults" in search_js
    assert "searchResultCount" in search_js
    assert 'wx:elif="{{!hasResults}}"' in search_wxml
    assert "openSectionItem" in search_js
    assert "仅以扁平 SKU 列表" not in search_wxml

    assert 'class="filter-line"' not in search_wxml
    assert 'class="quick-filters"' not in search_wxml
    assert 'class="filter-btn"' not in search_wxml
    assert 'class="filter-drawer"' not in search_wxml
    assert 'bindtap="openFilterDrawer"' not in search_wxml
    assert 'bindtap="selectFacet"' not in search_wxml
    assert 'bindtap="selectPriceRange"' not in search_wxml
    assert 'bindtap="applyFilters"' not in search_wxml

    for token in ["empty-icon", "检查商品名称或型号", "缩短关键词", "替换相近品牌"]:
        assert token in search_wxml
    assert "检查 SKU 编码" not in search_wxml
    assert "sectionItem.sku_code" not in search_wxml
    forbidden_empty_actions = ["联系商家", "提交找砖", "购物车", "在线下单", "客服找砖"]
    for token in forbidden_empty_actions:
        assert token not in search_wxml

    for token in [
        "env(safe-area-inset-top)",
        "min-height: 88rpx",
    ]:
        assert token in search_wxss


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
    assert "primary_category_product_list_click" in category_js
    assert "openPrimaryProducts" in category_js
    assert "sourcePage=category" in category_js
    assert "categoryLevel=primary" in category_js
    assert "categoryLevel=secondary" in category_js
    assert "lastPrimaryProductClickAt" in category_js
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
    assert "search-box" not in category_wxml
    assert "openSearch" not in category_js
    assert "/pages/search/index" not in category_js
    assert 'bindtap="openPrimaryProducts"' in category_wxml
    assert "primary-product-entry" in category_wxml
    assert "查看全部商品" in category_wxml
    assert "/pages/product-list/index?categoryId=" in category_js
    assert "商品卡片" not in category_wxml
    assert "价格" not in category_wxml
    assert "热门分类" not in category_wxml
    assert "width: 196rpx" in category_wxss
    assert "grid-template-columns: repeat(3, minmax(0, 1fr))" in category_wxss
    assert "aspect-ratio: 1 / 1" not in category_wxss
    assert ".secondary-image" not in category_wxss
    assert "min-height: 132rpx" in category_wxss
    assert "white-space: normal" in category_wxss
    assert "-webkit-line-clamp: 2" in category_wxss
    assert "min-height: 112rpx" in category_wxss
    assert "background: #18160F" in category_wxss
    assert "color: #C8A055" in category_wxss
    assert ".secondary-heading" in category_wxss
    assert ".primary-product-entry" in category_wxss
    assert "min-width: 168rpx" in category_wxss
    assert "justify-content: flex-end" in category_wxss
    assert "color: rgba(237,232,223,0.5)" in category_wxss
    assert ".brand-header" not in category_wxss
    assert ".search-box" not in category_wxss


def test_miniapp_product_list_page_carries_category_navigation() -> None:
    app_config = json.loads(_read("app.json"))
    product_list_js = _read("pages/product-list/index.js")
    product_list_ts = _read("pages/product-list/index.ts")
    product_list_wxml = _read("pages/product-list/index.wxml")
    product_list_wxss = _read("pages/product-list/index.wxss")

    assert "pages/product-list/index" in app_config["pages"]
    assert "categoryId" in product_list_js
    assert "categoryName" in product_list_js
    assert "categoryLevel" in product_list_js
    assert "CATEGORY_LEVELS" in product_list_js
    assert "brandId" in product_list_js
    assert "keyword" in product_list_js
    assert "priceRange" not in product_list_js
    assert "filter_type=category" in product_list_js
    assert "filter_value=" in product_list_js
    assert "this.data.categoryName && !this.data.categoryId ? 'filter_type=category'" in product_list_js
    assert "this.data.categoryName && !this.data.categoryId ? `filter_value=${encodeURIComponent(this.data.categoryName)}`" in product_list_js
    assert "shouldKeepCategoryLevel" in product_list_js
    assert "categoryLevel=" in product_list_ts
    assert "sort=default" in product_list_js
    assert "pageSize" in product_list_js
    assert "product_list_page_view" in product_list_js
    assert "product_list_item_exposure" in product_list_js
    assert "product_list_item_click" in product_list_js
    assert "product_list_filter_open" not in product_list_js
    assert "product_list_filter_apply" not in product_list_js
    assert "product_list_sort_change" not in product_list_js
    assert "product_list_refresh" in product_list_js
    assert "product_list_load_more" in product_list_js
    assert "product_list_load_failed" in product_list_js
    assert "filterSnapshot" not in product_list_js
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
    assert 'density="grid"' in product_list_wxml
    assert "search-box" not in product_list_wxml
    assert "filter-drawer" not in product_list_wxml
    assert "sort-tabs" not in product_list_wxml
    assert "activeFilterChips" not in product_list_wxml
    assert "openSearch" not in product_list_js
    assert "openFilter" not in product_list_js
    assert "changeSort" not in product_list_js
    assert "clearFilters" not in product_list_js
    assert "加载更多失败，点击重试" in product_list_js
    assert "收藏" not in product_list_wxml
    assert "购物车" not in product_list_wxml
    assert "立即购买" not in product_list_wxml
    assert "询价" not in product_list_wxml
    assert "background: #18160F" in product_list_wxss
    assert "color: #C8A055" in product_list_wxss
    assert "env(safe-area-inset-bottom)" in product_list_wxss
    assert "grid-template-columns: repeat(2, minmax(0, 1fr))" in product_list_wxss
    assert ".filter-drawer" not in product_list_wxss
    assert ".sort-tabs" not in product_list_wxss
    assert "min-height: 88rpx" in product_list_wxss


def test_miniapp_wechat_share_pages_cover_friend_timeline_and_runtime_sync() -> None:
    target_pages = [
        "pages/index/index",
        "pages/tile-detail/index",
        "pages/product-list/index",
        "pages/brand-detail/index",
    ]

    for page in target_pages:
        ts_source = _read(f"{page}.ts")
        js_source = _read(f"{page}.js")

        assert "onShareAppMessage()" in ts_source
        assert "onShareTimeline()" in ts_source
        assert "onShareAppMessage()" in js_source
        assert "onShareTimeline()" in js_source
        assert "wechat_friend" in ts_source
        assert "wechat_timeline" in ts_source
        assert "wechat_friend" in js_source
        assert "wechat_timeline" in js_source
        assert "Authorization" not in ts_source
        assert "Cookie" not in ts_source
        assert "raw_payload" not in ts_source
        assert "raw_object_key" not in ts_source

    home_ts = _read("pages/index/index.ts")
    home_js = _read("pages/index/index.js")
    detail_ts = _read("pages/tile-detail/index.ts")
    detail_js = _read("pages/tile-detail/index.js")
    product_list_ts = _read("pages/product-list/index.ts")
    product_list_js = _read("pages/product-list/index.js")
    brand_detail_ts = _read("pages/brand-detail/index.ts")
    brand_detail_js = _read("pages/brand-detail/index.js")

    for source in [home_ts, home_js]:
        assert "HOME_SHARE_PATH = '/pages/index/index?source=share'" in source
        assert "trackHomeShare" in source
        assert "query: 'source=share'" in source

    for source in [detail_ts, detail_js]:
        assert "trackSkuShare" in source
        assert "skuShareTitle" in source
        assert "skuShareImage" in source
        assert "skuId=${encodeURIComponent(String(skuId || 0))}&source=share" in source
        assert "pagePath(skuId, 'share')" in source
        assert "this.data.imageFallback" in source

    for source in [product_list_ts, product_list_js]:
        assert "PRODUCT_LIST_SHARE_KEYS" in source
        assert "buildShareQuery" in source
        assert "encodeShareValue" in source
        assert "sourcePage: 'share'" in source
        assert "product_list_share_click" in source
        assert "share_path" in source
        assert "categoryName" in source
        assert "keyword" in source
        assert "section" in source
        assert "requestId" in source

    expected_order = [
        "'categoryId'",
        "'categoryLevel'",
        "'categoryName'",
        "'brandId'",
        "'keyword'",
        "'section'",
        "'sourcePage'",
    ]
    last_index = -1
    for token in expected_order:
        index = product_list_js.index(token)
        assert index > last_index
        last_index = index
    assert "page=" not in product_list_js[product_list_js.index("PRODUCT_LIST_SHARE_KEYS"):product_list_js.index("function requestId")]
    assert "pageSize" not in product_list_js[product_list_js.index("PRODUCT_LIST_SHARE_KEYS"):product_list_js.index("function requestId")]
    assert "requestId" not in product_list_js[product_list_js.index("PRODUCT_LIST_SHARE_KEYS"):product_list_js.index("function requestId")]

    for source in [brand_detail_ts, brand_detail_js]:
        assert "brandSharePath" in source
        assert "brand_detail_share_click" in source
        assert "brandId=${encodeURIComponent(String(this.data.brandId || 0))}&source=share" in source
        assert "this.data.imageFallback" in source


def test_miniapp_wechat_share_evidence_records_static_and_follow_up_boundaries() -> None:
    evidence_path = resolve_change_file(
        ROOT,
        "add-miniapp-wechat-share-pages",
        "implementation/share-evidence.md",
    )
    evidence = evidence_path.read_text(encoding="utf-8")

    for page in [
        "pages/index/index?source=share",
        "pages/tile-detail/index?skuId=1&source=share",
        "pages/product-list/index?keyword=%E5%AE%A2%E5%8E%85&sourcePage=share",
        "pages/brand-detail/index?brandId=1&source=share",
    ]:
        assert page in evidence
    for viewport in ["320pt", "375pt", "430pt"]:
        assert viewport in evidence
    assert "static_review" in evidence
    assert "real_device_follow_up" in evidence
    assert "not reported as DevTools or real-device pass" in evidence
    for forbidden in ["Authorization", "Cookie", ".env", "raw object key"]:
        assert forbidden in evidence


def test_miniapp_certificate_list_page_replaces_placeholder_with_public_list() -> None:
    certificate_js = _read("pages/certificates/index.js")
    certificate_ts = _read("pages/certificates/index.ts")
    certificate_wxml = _read("pages/certificates/index.wxml")
    certificate_wxss = _read("pages/certificates/index.wxss")
    certificate_json = json.loads(_read("pages/certificates/index.json"))

    assert certificate_json["navigationStyle"] == "custom"
    assert certificate_json["usingComponents"]["custom-navigation"] == "../../components/custom-navigation/index"
    assert '<custom-navigation title="证书列表" />' in certificate_wxml
    assert "证书功能建设中" not in certificate_js
    assert "功能建设中" not in certificate_wxml
    assert "/api/v1/miniapp/certificates?" in certificate_ts
    assert "/api/v1/miniapp/certificates?" in certificate_js
    assert "PAGE_SIZE = 12" in certificate_js
    assert "onPullDownRefresh" in certificate_js
    assert "onReachBottom" in certificate_js
    assert "loadingMore" in certificate_js
    assert "mergeCertificates" in certificate_js
    assert "loadMoreError" in certificate_js
    assert "加载更多失败，点击重试" in certificate_js
    assert "暂无公开证书" in certificate_wxml
    assert "没有符合筛选条件的证书" not in certificate_js
    assert "搜索证书" not in certificate_wxml
    assert 'bindinput="onKeywordInput"' not in certificate_wxml
    assert 'bindconfirm="submitSearch"' not in certificate_wxml
    assert 'bindchange="onTypeChange"' not in certificate_wxml
    assert 'bindchange="onBrandChange"' not in certificate_wxml
    assert 'bindchange="onValidityChange"' not in certificate_wxml
    assert 'bindtap="clearFilters"' not in certificate_wxml
    assert "certificateType=" not in certificate_js
    assert "brandId=" not in certificate_js
    assert "validityStatus=" not in certificate_js
    assert "facets" not in certificate_js
    assert "wx.previewImage" in certificate_js
    assert "wx.downloadFile" in certificate_js
    assert "wx.openDocument" in certificate_js
    assert "wx.setClipboardData" in certificate_js
    assert 'binderror="onImageError"' in certificate_wxml
    assert "image_failed" in certificate_js
    assert "certificate_list_page_view" in certificate_js
    assert "certificate_search" not in certificate_js
    assert "certificate_filter_apply" not in certificate_js
    assert "certificate_click" in certificate_js
    assert "certificate_preview_click" in certificate_js
    assert "certificate_load_failed" in certificate_js
    assert "Authorization" not in certificate_js
    assert "Cookie" not in certificate_js
    assert ".env" not in certificate_js
    assert "file_key" not in certificate_wxml
    assert "background: #18160F" in certificate_wxss
    assert "color: #C8A055" in certificate_wxss
    assert "env(safe-area-inset-bottom)" in certificate_wxss
    assert "certificate-grid" in certificate_wxml
    assert "grid-template-columns: repeat(2, minmax(0, 1fr))" in certificate_wxss
    assert "aspect-ratio: 1 / 0.7" in certificate_wxss
    assert "-webkit-line-clamp: 2" in certificate_wxss
    assert "{{item.certificate_name}}" in certificate_wxml
    assert "{{item.brand_name}}" in certificate_wxml
    assert "{{item.certificate_type_label}}" in certificate_wxml
    assert "certificate_no" not in certificate_wxml
    assert "issuer" not in certificate_wxml
    assert "validity_status_label" not in certificate_wxml


def test_miniapp_product_card_component_contract_and_reuse() -> None:
    card_js = _read("components/product-card/index.js")
    card_ts = _read("components/product-card/index.ts")
    card_wxml = _read("components/product-card/index.wxml")
    card_wxss = _read("components/product-card/index.wxss")
    product_list_wxml = _read("pages/product-list/index.wxml")
    search_wxml = _read("pages/search/index.wxml")
    home_wxml = _read("pages/index/index.wxml")
    detail_js = _read("pages/tile-detail/index.js")

    assert "Component({" in card_js
    assert "normalizeProduct" in card_ts
    assert "未命名商品" in card_js
    assert "品牌待确认" in card_js
    assert "规格待补充" in card_js
    assert "暂无" in card_js
    assert "暂无参考价" not in card_js
    assert "function priceText" in card_js
    assert "value === 0" in card_js
    assert "legacyNoPriceText" in card_js
    assert "点击进入 SKU 详情" not in card_js
    assert "product_card_exposure" in card_js
    assert "product_card_click" in card_js
    assert "product_card_image_failed" in card_js
    assert "product_card_unavailable_click" in card_js
    assert "NAV_LOCK_MS = 800" in card_js
    assert "queryPair('sourcePage'" in card_js
    assert "queryPair('sourceModule'" in card_js
    assert "queryPair('requestId'" in card_js
    assert 'binderror="onImageError"' in card_wxml
    assert "{{normalized.productName}}" in card_wxml
    assert "{{normalized.brandName}}" in card_wxml
    assert "{{normalized.specification}}" in card_wxml
    assert "参考价格" in card_wxml
    assert "normalized.skuCode}} · {{normalized.specification" not in card_wxml
    assert "product-status" not in card_wxml
    assert "product-tags" not in card_wxml
    assert "-webkit-line-clamp: 2" in card_wxss
    assert "aspect-ratio: 1 / 0.86" in card_wxss
    assert "min-height: 188rpx" in card_wxss

    assert product_list_wxml.count("<product-card") == 1
    assert 'density="grid"' in product_list_wxml
    assert search_wxml.count("<product-card") >= 3
    assert home_wxml.count("<product-card") == 3
    assert "visual-heart" not in home_wxml
    assert "sourceModule" in detail_js
    assert "listContext" in detail_js
    assert "requestId" in detail_js


def test_miniapp_home_images_have_runtime_fallback_handlers() -> None:
    home_wxml = _read("pages/index/index.wxml")
    home_js = _read("pages/index/index.js")

    assert 'binderror="onImageError"' in home_wxml
    assert "<swiper" in home_wxml
    assert 'wx:for="{{home.banners}}"' in home_wxml
    assert 'src="{{item.image_url}}"' in home_wxml
    assert 'data-key="home.banners[{{index}}].image_url"' in home_wxml
    assert 'image-fallback="{{imageFallback}}"' in home_wxml
    assert "imageFallback: '/assets/tile-placeholder.png'" in home_js
    assert "this.setData({ [key]: this.data.imageFallback })" in home_js


def test_miniapp_sku_detail_page_covers_media_favorite_share_and_empty_states() -> None:
    detail_js = _read("pages/tile-detail/index.js")
    detail_ts = _read("pages/tile-detail/index.ts")
    detail_wxml = _read("pages/tile-detail/index.wxml")
    detail_wxss = _read("pages/tile-detail/index.wxss")
    detail_json = json.loads(_read("pages/tile-detail/index.json"))

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
    assert detail_json["usingComponents"]["brand-card"] == "../../components/brand-card/index"
    assert "skeleton" in detail_wxml
    assert "<swiper" in detail_wxml
    assert detail_wxml.index('<view class="summary">') < detail_wxml.index('<view class="brand-card-wrap">')
    assert detail_wxml.index('<view class="brand-card-wrap">') < detail_wxml.index('<view class="panel-title">商品参数</view>')
    assert "{{product.sku_code}}" not in detail_wxml[detail_wxml.index('<view class="summary">'):detail_wxml.index('<view class="brand-card-wrap">')]
    assert "SKU 编码" not in detail_wxml
    assert "<video" in detail_wxml
    assert 'src="{{item.url}}"' in detail_wxml
    assert 'poster="{{item.cover_url || \'\'}}"' in detail_wxml
    assert "poster=\"{{item.cover_url || product.cover_image || imageFallback}}\"" not in detail_wxml
    assert 'bindplay="onVideoPlay"' in detail_wxml
    assert 'binderror="onMediaError"' in detail_wxml
    assert 'autoplay="{{false}}"' in detail_wxml
    assert 'autoplay="{{!mediaPaused}}"' in detail_wxml
    assert "this.setData({ mediaPaused: true })" in detail_js
    assert "wx.createVideoContext(`sku-video-${item.media_id}`, this).pause()" in detail_js
    assert "视频暂时无法播放" in detail_js
    assert "media-count" in detail_wxml
    assert "<brand-card" in detail_wxml
    assert 'hint="查看品牌主页"' in detail_wxml
    assert 'source-module="sku-detail-brand"' in detail_wxml
    assert 'bindtap="openBrand"' not in detail_wxml
    assert "openBrand()" not in detail_js
    assert "openBrand()" not in detail_ts
    assert "sku-detail-bottom-bar" not in detail_js
    assert "sku-detail-bottom-bar" not in detail_ts
    assert "brandNavigating" not in detail_js
    assert "brandNavigating" not in detail_ts
    assert "sku_brand_click" not in detail_js
    assert "sku_brand_click" not in detail_ts
    assert "brand-logo" not in detail_wxml
    assert "action-icon" in detail_wxml
    assert detail_wxml.count('class="action-btn') == 1
    assert detail_wxml.count('class="share-btn"') == 1
    assert detail_wxml.index('bindtap="toggleFavorite"') < detail_wxml.index('open-type="share"')
    bottom_actions = detail_wxml[detail_wxml.index('<view wx:if="{{product}}" class="actions">'):]
    assert ">品牌</text>" not in bottom_actions
    assert "分享给客户" in detail_wxml
    assert "同系列推荐" in detail_wxml
    assert "同品牌推荐" in detail_wxml
    assert "购物车" not in detail_wxml
    assert "立即购买" not in detail_wxml
    assert "库存" not in detail_wxml
    assert "grid-template-columns: minmax(0, 0.78fr) minmax(0, 1.22fr)" in detail_wxss
    assert "repeat(3, minmax(0, 1fr))" not in detail_wxss
    assert "height: 88rpx" in detail_wxss
    assert "padding: 0" in detail_wxss
    assert "background: transparent" in detail_wxss
    assert "border-radius: 28rpx" in detail_wxss
    assert "env(safe-area-inset-bottom)" in detail_wxss
    assert "min-height: 88rpx" in detail_wxss


def test_miniapp_favorite_list_page_uses_local_storage_and_states() -> None:
    app_config = json.loads(_read("app.json"))
    favorites_js = _read("pages/favorites/index.js")
    favorites_ts = _read("pages/favorites/index.ts")
    favorites_wxml = _read("pages/favorites/index.wxml")
    favorites_wxss = _read("pages/favorites/index.wxss")
    product_list_js = _read("pages/product-list/index.js")
    product_list_wxml = _read("pages/product-list/index.wxml")
    detail_js = _read("pages/tile-detail/index.js")
    detail_ts = _read("pages/tile-detail/index.ts")

    assert "pages/favorites/index" in app_config["pages"]
    assert any(item["pagePath"] == "pages/favorites/index" and item["text"] == "收藏" for item in app_config["tabBar"]["list"])
    for source in [favorites_js, favorites_ts, detail_js, detail_ts]:
        assert "miniapp_favorite_skus_v1" in source
    for source in [favorites_js, favorites_ts]:
        assert "normalizeFavoriteItem" in source
        assert "item.objectId || item.sku_id || item.product_id" in source
        assert "readFavorites" in source
        assert "writeFavorites" in source
        assert "favorite_list_page_view" in source
        assert "favorite_list_item_click" in source
        assert "favorite_list_remove" in source
        assert "favorite_list_empty_action_click" in source
        assert "favorite_list_load_failed" in source
        assert "hasLogin: false" in source
        assert "Authorization" not in source
        assert "/api/v1/miniapp/skus/${id}/favorite" in source
        assert "favorite: false" in source

    assert '<custom-navigation title="收藏列表" />' in favorites_wxml
    assert '<view wx:if="{{total > 0}}" class="summary">' in favorites_wxml
    assert "已收藏商品：{{total}}" in favorites_wxml
    assert "当前收藏保存在本机" not in favorites_wxml
    assert "guestHint" not in favorites_js
    assert "guestHint" not in favorites_ts
    assert "status == 'empty'" in favorites_wxml
    assert "status == 'error'" in favorites_wxml
    assert "loadingMore" in favorites_wxml
    assert "loadMoreError" in favorites_wxml
    assert 'bindtap="openItem"' in favorites_wxml
    assert 'data-id="{{item.objectId || item.sku_id || item.product_id}}"' in favorites_wxml
    assert 'catchtap="removeItem"' in favorites_wxml
    assert ">♥</button>" in favorites_wxml
    assert ">♡</button>" not in favorites_wxml
    assert "/pages/tile-detail/index?skuId=${id}&source=favorites" in favorites_js
    assert "target: 'product_list'" in favorites_js
    assert "wx.navigateTo({ url: '/pages/product-list/index?sourcePage=favorites' })" in favorites_js
    assert "wx.switchTab({ url: '/pages/category/index' })" not in favorites_js
    assert "title: '全部商品'" in product_list_js
    assert " : '全部商品')" in product_list_js
    assert '<custom-navigation title="{{title}}" />' in product_list_wxml
    assert 'density="grid"' in product_list_wxml
    assert "env(safe-area-inset-bottom)" in favorites_wxss
    assert "min-height: 88rpx" in favorites_wxss
    assert "background: #18160F" in favorites_wxss
    assert "color: #C8A055" in favorites_wxss
    assert "syncLocalFavorite(product, true)" in detail_js
    assert "syncLocalFavorite(product, nextFavorite)" in detail_js
    assert "syncLocalFavorite(product, true)" in detail_ts
    assert "syncLocalFavorite(product, nextFavorite)" in detail_ts


def test_miniapp_brand_list_page_covers_carousel_grid_entry_and_tracking() -> None:
    app_config = json.loads(_read("app.json"))
    tabbar_js = _read("custom-tab-bar/index.js")
    home_js = _read("pages/index/index.js")
    brand_js = _read("pages/brand-list/index.js")
    brand_ts = _read("pages/brand-list/index.ts")
    brand_wxml = _read("pages/brand-list/index.wxml")
    brand_wxss = _read("pages/brand-list/index.wxss")
    brand_json = json.loads(_read("pages/brand-list/index.json"))

    assert app_config["tabBar"]["list"][2]["pagePath"] == "pages/brand-list/index"
    assert app_config["tabBar"]["list"][2]["text"] == "品牌"
    assert "text: '品牌'" in tabbar_js
    assert "brand-default.png" in tabbar_js
    assert "brand-active.png" in tabbar_js
    assert "find-default.png" not in tabbar_js
    assert "pagePath: '/pages/brand-list/index'" in tabbar_js
    assert "{ key: 'brand', title: '品牌', icon: '▣', url: '/pages/brand-list/index' }" in home_js
    assert "/pages/find/index" not in home_js

    assert brand_json["navigationStyle"] == "custom"
    assert brand_json["usingComponents"]["custom-navigation"] == "../../components/custom-navigation/index"
    assert brand_json["usingComponents"]["brand-card"] == "../../components/brand-card/index"
    assert '<custom-navigation title="品牌列表" />' in brand_wxml
    assert "/api/v1/miniapp/brands?page=" in brand_ts
    assert "/api/v1/miniapp/brands?page=" in brand_js
    assert "brand_list_page_view" in brand_js
    assert "brand_list_carousel_click" in brand_js
    assert "brand_list_card_click" in brand_js
    assert "authorization" not in brand_js
    assert "cookie" not in brand_js
    assert "object_key" not in brand_js
    assert "<swiper" in brand_wxml
    assert "autoplay" in brand_wxml
    assert "circular" in brand_wxml
    assert 'indicator-active-color="#C8A055"' in brand_wxml
    assert "brand-grid" in brand_wxml
    assert "<brand-card" in brand_wxml
    assert 'density="grid"' in brand_wxml
    assert " 个商品" in brand_wxml
    assert "item.product_count + ' 个公开商品'" not in brand_wxml
    assert "暂无内容" in brand_wxml
    assert 'bindtap="onBrandTap"' in brand_wxml
    assert "status == 'loading'" in brand_wxml
    assert "status == 'empty'" in brand_wxml
    assert "status == 'error'" in brand_wxml
    assert "grid-template-columns: repeat(2, minmax(0, 1fr))" in brand_wxss
    assert "env(safe-area-inset-bottom)" in brand_wxss
    assert "min-height: 244rpx" in brand_wxss
    assert "padding: 28rpx 28rpx calc(132rpx + env(safe-area-inset-bottom))" in brand_wxss
    assert "overflow: hidden" in brand_wxss
    assert "height: 300rpx" in brand_wxss
    assert "left: 28rpx" in brand_wxss
    assert "right: 28rpx" in brand_wxss
    assert "min-height: 560rpx" in brand_wxss


def test_miniapp_brand_card_component_contract_and_states() -> None:
    brand_js = _read("components/brand-card/index.js")
    brand_ts = _read("components/brand-card/index.ts")
    brand_wxml = _read("components/brand-card/index.wxml")
    brand_wxss = _read("components/brand-card/index.wxss")
    brand_json = json.loads(_read("components/brand-card/index.json"))

    assert brand_json["component"] is True
    for source in [brand_js, brand_ts]:
        assert "brand_entry_path" in source
        assert "fallbackSearchPath" in source
        assert "encodeURIComponent(cleanParam(brandName))" in source
        assert "brand_card_click" in source
        assert "brand_card_image_failed" in source
        assert "brand_card_unavailable_click" in source
        assert "sourcePage" in source
        assert "sourceModule" in source
        assert "skuId" in source
        assert "listContext" in source
        assert "requestId" in source
        assert "NAV_LOCK_MS = 800" in source
        assert "暂无内容" in source
        assert "品牌内容暂不可查看" not in source
        assert "/api/v1/" not in source
        assert "request<" not in source
        assert "request(" not in source

    assert 'bindtap="openBrand"' in brand_wxml
    assert 'binderror="onImageError"' in brand_wxml
    assert "brand-logo-empty" in brand_wxml
    assert "normalized.fallbackText" in brand_wxml
    assert "normalized.brandName" in brand_wxml
    assert "normalized.hint" in brand_wxml
    assert "density == 'grid'" in brand_wxml
    assert "grid-template-columns: 64rpx minmax(0, 1fr) 28rpx" in brand_wxss
    assert ".brand-card.grid" in brand_wxss
    assert "min-height: 244rpx" in brand_wxss
    assert "min-height: 104rpx" in brand_wxss
    assert "text-overflow: ellipsis" in brand_wxss
    assert ".brand-card.unavailable" in brand_wxss
    assert "width: 64rpx" in brand_wxss


def test_miniapp_home_matches_prototype_structure_and_visual_tokens() -> None:
    home_wxml = _read("pages/index/index.wxml")
    home_wxss = _read("pages/index/index.wxss")

    for token in [
        "search-box",
        "hero-button",
        "hero-dots",
        "shortcut-icon",
        "waterfall",
        "load-more",
    ]:
        assert token in home_wxml

    for title in ["选瓷砖", "品牌", "新品榜", "热销榜"]:
        assert title in home_wxml or title in _read("pages/index/index.js")

    assert (MINIAPP / "assets/logos/product-logo.png").exists()
    assert "mini-capsule" not in home_wxml
    assert "search-icon" not in home_wxml
    assert "search-action" not in home_wxml
    assert ".search-action" not in home_wxss
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
        "background: rgba(24,22,15,0.88)",
    ]:
        assert token in home_wxss
    assert "column-count: 2" not in home_wxss


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
        "certificate_api",
    ]
    for term in forbidden_terms:
        assert term not in source


def test_miniapp_styles_keep_primary_tappable_targets_at_least_44pt() -> None:
    css = "\n".join(path.read_text(encoding="utf-8") for path in MINIAPP.rglob("*.wxss"))

    assert "min-height: 88rpx" in css
    assert "env(safe-area-inset-bottom)" in css
    assert "overflow: hidden" in css
