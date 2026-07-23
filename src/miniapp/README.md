---
purpose: 微信小程序源码说明
content: 说明本目录职责、边界和AI新增文件规则
source: AI自动生成，人工确认
update_method: 目录职责变化时更新
created_at: 2026-07-16 13:40:44
updated_at: 2026-07-21 22:57:26
note: AI新增文件前必须确认目录边界
---

# 微信小程序源码说明

本目录职责请参考 `rules/directory-structure.md`。

## 运行入口策略

当前小程序采用同步运行脚本策略：`.ts` 文件保留类型化源码意图，微信开发者工具实际加载的 `.js` 文件必须同步包含对应页面的业务数据、生命周期和交互方法。

关键页面包括首页、搜索页、商品详情页和门店信息页。修改这些页面时必须同时维护同目录 `.js`，并运行 `tests/test_miniapp_static.py`，避免空模板 `.js` 覆盖已实现的 `.ts` 逻辑。

## 首页数据与视觉实现

首页通过 `GET /api/v1/miniapp/home` 获取门店摘要、Banner、快捷入口、服务区、新品推荐和热门推荐。

- Banner 使用后台管理端 Banner 管理数据；后端仅聚合已上线、展示端为 `MINIAPP_HOME`（管理端显示“小程序”）、且在有效期内的 Banner。小程序首页只读取 `MINIAPP_HOME_CAROUSEL`（首页轮播），品牌列表页只读取 `MINIAPP_BRAND_LIST_CAROUSEL`（品牌列表页轮播），品牌列表页无轮播数据时不使用首页轮播兜底。小程序首页与品牌列表页均通过 `swiper` 使用 Banner `image_url` 渲染轮播图，并支持 `product`、`brand`、`search`、`store`、`none` 跳转类型；`brand` 使用 `target_id` 跳转 `pages/brand-detail/index?brandId=...`。没有可用 Banner 时首页降级展示本地黑金品牌 Hero。
- 新品推荐、热门推荐卡片使用 SKU 主图字段 `cover_image`；缺少主图时降级为 `/assets/tile-placeholder.png`。两者在首页均使用横向滑动列表和 `components/product-card/` 的 `compact` 密度，保持一致的卡片点击、详情跳转和来源上下文传参。
- 商品价格展示使用后端格式化字段 `price_display`；已维护价格显示为 `¥xx.xx`，未维护、非正或旧无价文案显示为 `暂无`，不再展示旧咨询类文案。
- 首页左上角产品 Logo 使用 `src/miniapp/assets/logos/product-logo.png`，来源于 Web 公共 Logo 资源 `src/web/public/logos/64x64.png`。

## 搜索组件与页面

搜索入口组件位于 `components/search-entry/`，支持关键词、清空、提交、取消、禁用态、`scope` 与 `sourcePage`。搜索页 `pages/search/index.*` 通过 `GET /api/v1/miniapp/search/home`、`GET /api/v1/miniapp/search/suggestions` 和 `GET /api/v1/miniapp/search` 实现搜索首页、300ms 实时联想、结果 Tab、最佳匹配、品牌/SKU/证书卡片、无结果和失败重试。

- 最近搜索仅使用本机 storage `miniapp_search_recent_keywords_v1`，最多 20 条，重复关键词去重置顶。
- 搜索首页仅展示最近搜索和热门搜索，不展示最近浏览模块；最近搜索支持单条删除和清空，清空按钮需与搜索框右侧对齐。
- 关键词联想只展示品牌与 SKU 两组，不展示最近搜索、普通关键词、类目、规格或证书。
- 搜索结果页不展示搜索框、快捷筛选、筛选按钮或筛选抽屉；Tab 展示顺序为综合、品牌、SKU、证书，小程序端不展示类目 Tab。
- 综合 Tab 只在有结果时展示分区：最多 1 条最佳匹配，其后按品牌、SKU、证书顺序展示非 0 条分区；品牌/SKU/证书单独 Tab 内直接展示卡片内容，不再显示“品牌/SKU/证书 x 条”的分区标题。
- SKU 结果复用 `components/product-card/`；品牌与证书结果使用与 SKU 卡片一致的一行卡片式视觉，但保留品牌/证书自身跳转行为。
- `best_match` 可返回 SKU、品牌或证书：SKU 编码或名称直接命中优先，其次品牌名精确命中，最后证书名称或证书编号精确命中；都不满足时为空。
- 搜索埋点通过 `track()` 上报 `search_page_view`、`search_input`、`search_suggestion_exposure`、`search_suggestion_click`、`search_submit`、`search_result_exposure`、`search_result_click`、`search_filter_apply`、`search_no_result`、`search_history_click`、`search_history_delete`、`search_history_clear`；埋点失败不得阻断搜索主流程。
- 本期不包含管理端搜索配置中心、后台热门词维护、同义词维护、自然语言词典维护、搜索统计管理页或 `/api/admin/search/*`。

## 商品列表页

商品列表页位于 `pages/product-list/index.*`，用于承接分类、搜索、品牌、新品榜和热销榜等入口。页面通过 `GET /api/v1/miniapp/products` 携带 `categoryId`、`categoryLevel`、`keyword`、`brandId`、`spec`、`priceRange`、`sort`、`page` 和 `pageSize` 获取公开 SKU、分页状态和筛选 facets；`categoryLevel=primary` 表示一级分类聚合，`categoryLevel=secondary` 表示二级分类精确查询。

- 列表容器统一处理首屏骨架屏、下拉刷新、上拉加载更多、无更多、空状态、错误状态和加载更多失败重试。
- 商品卡片仅展示主图、SKU 名称、品牌、规格和参考价格；整卡点击进入 SKU 详情页，不提供收藏、询价、购物车、立即购买、在线下单或联系商家快捷按钮。
- 底部筛选抽屉支持品牌、分类、规格和价格区间，排序支持默认、最新、价格升序和价格降序；筛选或排序变更后重置分页并重新请求第一页。
- 商品列表支持微信朋友分享和朋友圈分享，分享路径只保留 `categoryId`、`categoryLevel`、`categoryName`、`brandId`、`keyword`、`section`、`sourcePage` 白名单参数，中文参数必须编码，缺少可选参数时降级为可浏览列表。
- 商品列表埋点通过 `track()` 上报 `product_list_page_view`、`product_list_item_exposure`、`product_list_item_click`、`product_list_filter_open`、`product_list_filter_apply`、`product_list_sort_change`、`product_list_refresh`、`product_list_load_more`、`product_list_load_failed`、`product_list_share_click`；埋点失败不得阻断列表加载、筛选、排序、刷新、加载更多、详情跳转或分享。
- 本期不包含 Web 管理端商品列表组件、店主 Web 商品列表、后台商品管理列表、购物车、询价、在线下单或收藏能力。

## 品牌入口页与品牌主页

品牌入口页位于 `pages/brand-list/index.*`，通过 `GET /api/v1/miniapp/brands` 获取品牌列表页轮播和启用品牌卡片列表。品牌卡片一行 2 个，复用 `components/brand-card/`，点击进入 `pages/brand-detail/index?brandId=...`；卡片副文案展示 `x 个商品`，商品数为 0 时展示 `暂无内容`，不展示“公开”字样。

品牌主页位于 `pages/brand-detail/index.*`，通过 `GET /api/v1/miniapp/brands/{brand_id}` 获取品牌图片、品牌名称、英文名、简介、商品数和证书数；导航栏标题必须使用品牌名称 `brand_name`，不得使用品牌简称。顶部品牌文案以浮层形式覆盖在品牌图片上，不展示“x 个商品 / x 个证书”数量行。商品 Tab 复用 `GET /api/v1/miniapp/products?brandId=...` 和 `components/product-card/`；证书 Tab 通过 `GET /api/v1/miniapp/brands/{brand_id}/certificates` 获取当前品牌可公开证书，卡片样式保持与证书列表页一致，并按文件类型使用图片预览或 PDF 打开/复制链接兜底。

- 后端只返回启用品牌、公开 SKU 和可见证书，不暴露后台备注、审计字段、对象存储原始 key、Authorization header、Cookie 或敏感配置。启用品牌即使商品数为 0，也必须允许进入品牌主页；品牌详情接口返回 `product_count=0`，商品 Tab 展示空态，不得将 0 商品品牌误判为“暂不可查看”。
- 品牌入口页和品牌主页均使用 `custom-navigation`，需要按 `docs/knowledge-base/best-practices/miniapp-custom-navigation.md` 记录 DevTools 320/375/430 pt evidence；真机不可用时标记 blocked 或 follow_up。
- 品牌主页 Tab 样式需与搜索结果页“综合 / 品牌”等 Tab 保持一致；证书 Tab 的证书卡片需与 `pages/certificates/index.*` 的证书卡片保持一致。
- 品牌主页支持微信朋友分享和朋友圈分享，分享路径保留 `brandId` 与 `source=share`，标题优先使用品牌名称，图片优先使用公开品牌 Logo 并降级到本地占位图。
- 品牌页埋点通过 `track()` 上报 `brand_list_page_view`、`brand_list_carousel_click`、`brand_list_card_click`、`brand_detail_view`、`brand_detail_tab_click`、`brand_products_load`、`brand_certificates_load`、`brand_certificate_click` 和 `brand_detail_share_click`；埋点失败不得阻断页面加载、Tab 切换、预览、详情跳转或分享。

## 证书列表页

证书列表页位于 `pages/certificates/index.*`，通过 `GET /api/v1/miniapp/certificates` 获取所有可公开证书，页面标题固定为“证书列表”。请求仅支持 `page` 和 `pageSize` 分页参数，不提供搜索框、筛选按钮、筛选抽屉或清空筛选动作。

- 列表采用一行 2 个证书卡片；卡片文本仅展示证书名称、品牌名称和证书类型，不展示证书编号、签发方或有效期状态。
- 证书文件使用后端返回的受控 `file_url`；图片证书使用 `wx.previewImage`，PDF 使用 `wx.downloadFile` + `wx.openDocument`，不可打开时提供复制链接兜底。
- 页面需覆盖首屏加载、下拉刷新、触底加载更多、无更多、暂无公开证书、网络失败、加载更多失败和图片失败降级状态。
- 证书列表埋点通过 `track()` 上报 `certificate_list_page_view`、`certificate_click`、`certificate_preview_click` 和 `certificate_load_failed`；埋点和日志不得记录 `file_key`、Authorization header、Cookie、`.env` 内容、本机路径或后台备注。

## 自定义 TabBar

当前小程序启用 `app.json` 的 `tabBar.custom=true`，底部导航由 `src/miniapp/custom-tab-bar/` 组件渲染。

- 图标资源位于 `src/miniapp/assets/tabbar/`。
- 品牌 Tab 使用 `brand-default.png` / `brand-active.png`，不得复用搜索 `find-*` 图标。
- Tab 展示顺序为首页、分类、品牌、证书、收藏；证书必须位于收藏前。
- 证书 Tab 使用 `certificate-default.png` / `certificate-active.png`，收藏 Tab 使用 `favorite-default.png` / `favorite-active.png`，两者不得复用同一套图标。
- 底部导航文字字号为 `24rpx`，图标尺寸为 `46rpx`。
- 新增、删除或重排 Tab 时，必须同时维护 `app.json` 的 `tabBar.list` 与 `custom-tab-bar/index.js` 中的 `tabs`。

## 本地调试

- 小程序环境配置集中在 `utils/env.*`，通过 `/miniapp-env` 命令族维护，禁止手工只改 `.ts` 或只改 `.js`。
- `/miniapp-env dev`：所有运行形态使用本地 API，基础地址为 `http://127.0.0.1:8010`，并按 `http://localhost:8010`、`http://localhost:8000` 顺序降级探测。
- `/miniapp-env prod`：所有运行形态使用生产 API，基础地址固定为 `https://tilesfst.wjoyhappy.site`，不配置本地 fallback。
- `/miniapp-env auto`：开发版使用本地 API，体验版和正式版使用生产 API；发布后默认恢复到该策略。
- `/miniapp-env dev` 与 `/miniapp-env auto` 会把 `project.private.config.json` 的 `setting.urlCheck` 设为 `false`，用于本地 HTTP 后端调试；`/miniapp-env prod` 与 `/miniapp-prepare` 会设为 `true`，用于生产域名校验。
- `/miniapp-check` 检查当前策略、运行入口同步和生产接口；`/miniapp-prepare` 用于上传体验版/提审前切生产、跑静态测试和生产 smoke；`/miniapp-confirm` 记录体验版/正式版验证结论；`/miniapp-restore` 恢复默认策略。
- `project.config.json` 默认关闭 `urlCheck` 用于本地 HTTP 后端调试；`project.private.config.json` 可在发布验证时打开 `urlCheck`，提交正式版前需在微信公众平台配置生产域名合法域名。
- 后端代码变更后需重新构建运行镜像，例如 `docker compose up -d --build backend`，否则微信开发者工具可能仍访问到旧接口。
- 小程序静态与首页聚合回归检查：`uv run pytest tests/test_miniapp_static.py tests/test_miniapp_home.py`。
