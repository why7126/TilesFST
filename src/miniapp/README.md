---
purpose: 微信小程序源码说明
content: 说明本目录职责、边界和AI新增文件规则
source: AI自动生成，人工确认
update_method: 目录职责变化时更新
created_at: 2026-07-16 13:40:44
updated_at: 2026-07-19 02:17:59
note: AI新增文件前必须确认目录边界
---

# 微信小程序源码说明

本目录职责请参考 `rules/directory-structure.md`。

## 运行入口策略

当前小程序采用同步运行脚本策略：`.ts` 文件保留类型化源码意图，微信开发者工具实际加载的 `.js` 文件必须同步包含对应页面的业务数据、生命周期和交互方法。

关键页面包括首页、搜索页、商品详情页和门店信息页。修改这些页面时必须同时维护同目录 `.js`，并运行 `tests/test_miniapp_static.py`，避免空模板 `.js` 覆盖已实现的 `.ts` 逻辑。

## 首页数据与视觉实现

首页通过 `GET /api/v1/miniapp/home` 获取门店摘要、Banner、快捷入口、服务区、新品推荐和热门推荐。

- Banner 使用后台管理端 Banner 管理数据；后端仅聚合已上线、展示端为 `MINIAPP_HOME`（小程序首页）、展示位置为 `MINIAPP_HOME_CAROUSEL`（小程序首页轮播）、且在有效期内的 Banner。小程序首页通过 `swiper` 使用 Banner `image_url` 渲染轮播图；没有可用 Banner 时降级展示本地黑金品牌 Hero。
- 新品推荐、热门推荐卡片使用 SKU 主图字段 `cover_image`；缺少主图时降级为 `/assets/tile-placeholder.png`。
- 商品价格展示使用后端格式化字段 `price_display`；已维护价格显示为 `¥xx.xx`，未维护或非正价格显示为 `价格待维护`，不再展示“到店咨询”。
- 首页左上角产品 Logo 使用 `src/miniapp/assets/logos/product-logo.png`，来源于 Web 公共 Logo 资源 `src/web/public/logos/64x64.png`。

## 搜索组件与页面

搜索入口组件位于 `components/search-entry/`，支持关键词、清空、提交、取消、禁用态、`scope` 与 `sourcePage`。搜索页 `pages/search/index.*` 通过 `GET /api/v1/miniapp/search/home`、`GET /api/v1/miniapp/search/suggestions` 和 `GET /api/v1/miniapp/search` 实现搜索首页、300ms 实时联想、结果 Tab、SKU 卡片、筛选抽屉、无结果和失败重试。

- 最近搜索仅使用本机 storage `miniapp_search_recent_keywords_v1`，最多 20 条，重复关键词去重置顶。
- 最近浏览仅使用本机 storage `miniapp_recent_browsing_v1`，最多 10 条；接口返回的最近浏览只作为兜底展示。
- 搜索埋点通过 `track()` 上报 `search_page_view`、`search_input`、`search_suggestion_exposure`、`search_suggestion_click`、`search_submit`、`search_result_exposure`、`search_result_click`、`search_filter_apply`、`search_no_result`、`search_history_click`、`search_history_delete`、`search_history_clear`；埋点失败不得阻断搜索主流程。
- 本期不包含管理端搜索配置中心、后台热门词维护、同义词维护、自然语言词典维护、搜索统计管理页或 `/api/admin/search/*`。

## 商品列表页

商品列表页位于 `pages/product-list/index.*`，用于承接分类、搜索、品牌、新品榜和热销榜等入口。页面通过 `GET /api/v1/miniapp/products` 携带 `categoryId`、`keyword`、`brandId`、`spec`、`priceRange`、`sort`、`page` 和 `pageSize` 获取公开 SKU、分页状态和筛选 facets。

- 列表容器统一处理首屏骨架屏、下拉刷新、上拉加载更多、无更多、空状态、错误状态和加载更多失败重试。
- 商品卡片仅展示主图、商品名称、SKU 编码、品牌、规格、参考价格和辅助分类信息；整卡点击进入 SKU 详情页，不提供收藏、询价、购物车、立即购买、在线下单或联系商家快捷按钮。
- 底部筛选抽屉支持品牌、分类、规格和价格区间，排序支持默认、最新、价格升序和价格降序；筛选或排序变更后重置分页并重新请求第一页。
- 商品列表埋点通过 `track()` 上报 `product_list_page_view`、`product_list_item_exposure`、`product_list_item_click`、`product_list_filter_open`、`product_list_filter_apply`、`product_list_sort_change`、`product_list_refresh`、`product_list_load_more`、`product_list_load_failed`；埋点失败不得阻断列表加载、筛选、排序、刷新、加载更多或详情跳转。
- 本期不包含 Web 管理端商品列表组件、店主 Web 商品列表、后台商品管理列表、购物车、询价、在线下单或收藏能力。

## 自定义 TabBar

当前小程序启用 `app.json` 的 `tabBar.custom=true`，底部导航由 `src/miniapp/custom-tab-bar/` 组件渲染。

- 图标资源位于 `src/miniapp/assets/tabbar/`。
- 底部导航文字字号为 `24rpx`，图标尺寸为 `46rpx`。
- 新增、删除或重排 Tab 时，必须同时维护 `app.json` 的 `tabBar.list` 与 `custom-tab-bar/index.js` 中的 `tabs`。

## 本地调试

- `project.config.json` 与 `project.private.config.json` 均关闭 `urlCheck`，用于本地 HTTP 后端调试。
- API 基础地址按 `http://localhost:8000`、`http://127.0.0.1:8010`、`http://localhost:8010` 顺序降级探测。
- 后端代码变更后需重新构建运行镜像，例如 `docker compose up -d --build backend`，否则微信开发者工具可能仍访问到旧接口。
- 小程序静态与首页聚合回归检查：`uv run pytest tests/test_miniapp_static.py tests/test_miniapp_home.py`。
