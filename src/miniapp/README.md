---
purpose: 微信小程序源码说明
content: 说明本目录职责、边界和AI新增文件规则
source: AI自动生成，人工确认
update_method: 目录职责变化时更新
created_at: 2026-07-16 13:40:44
updated_at: 2026-08-28 10:13:06
note: AI新增文件前必须确认目录边界
---

# 微信小程序源码说明

本目录职责请参考 `rules/directory-structure.md`。

## 运行入口策略

当前小程序采用同步运行脚本策略：`.ts` 文件保留类型化源码意图，微信开发者工具实际加载的 `.js` 文件必须同步包含对应页面的业务数据、生命周期和交互方法。

关键页面包括首页、搜索页、商品详情页和门店信息页。修改这些页面时必须同时维护同目录 `.js`，并运行 `tests/test_miniapp_static.py`，避免空模板 `.js` 覆盖已实现的 `.ts` 逻辑。

## 首页数据与视觉实现

首页通过 `GET /api/v1/miniapp/home` 获取门店摘要、Banner、快捷入口、服务区、新品推荐和热门推荐。

- Banner 使用后台管理端 Banner 管理数据；后端仅聚合已上线、展示端为 `MINIAPP_HOME`（管理端显示“小程序”）、且在有效期内的 Banner。小程序首页只读取 `MINIAPP_HOME_CAROUSEL`（首页轮播），品牌列表页只读取 `MINIAPP_BRAND_LIST_CAROUSEL`（品牌列表页轮播），品牌列表页无轮播数据时不使用首页轮播兜底。小程序 Banner 轮播图属于首屏大图展示位，目标规格为 `display`；首页与品牌列表页均通过 `swiper` 优先使用 Banner `display_url`，缺失或不可读时降级到 `thumbnail_url`，再降级到安全视图占位；不得请求原图、preview、旧 `url`、语义不明 `image_url` 或不存在的本地静态占位图，并支持 `product`、`brand`、`search`、`store`、`none` 跳转类型；`brand` 使用 `target_id` 跳转 `pages/brand-detail/index?brandId=...`。没有可用 Banner 时首页降级展示本地黑金品牌 Hero。
- 新品推荐、热门推荐卡片使用 SKU 主图字段 `cover_image`；缺少主图时由 `components/product-card/` 展示内置文字占位，不请求本地占位图片或原图。两者在首页均使用横向滑动列表和 `components/product-card/` 的 `compact` 密度，保持一致的卡片点击、详情跳转和来源上下文传参。
- 商品价格展示使用后端格式化字段 `price_display`；已维护价格显示为 `¥xx.xx`，未维护、非正或旧无价文案显示为 `暂无`，不再展示旧咨询类文案。
- 首页左上角产品 Logo 使用 `src/miniapp/assets/logos/product-logo.png`，来源于 Web 公共 Logo 资源 `src/web/public/logos/64x64.png`。

## 搜索组件与页面

搜索入口组件位于 `components/search-entry/`，支持关键词、清空、提交、取消、禁用态、`scope` 与 `sourcePage`。搜索页 `pages/search/index.*` 通过 `GET /api/v1/miniapp/search/home`、`GET /api/v1/miniapp/search/suggestions` 和 `GET /api/v1/miniapp/search` 实现搜索首页、300ms 实时联想、结果 Tab、最佳匹配、品牌/SKU/证书卡片、无结果和失败重试。

- 底部 Tab「全部分类」页不展示搜索入口，保持一级 / 二级分类双栏浏览；用户进入商品列表后可在商品列表上下文继续搜索或调整关键词。
- 最近搜索仅使用本机 storage `miniapp_search_recent_keywords_v1`，最多 20 条，重复关键词去重置顶。
- 搜索首页仅展示最近搜索和热门搜索，不展示最近浏览模块；最近搜索支持单条删除和清空，清空按钮需与搜索框右侧对齐。
- 关键词联想只展示品牌与 SKU 两组，不展示最近搜索、普通关键词、类目、规格或证书。
- 搜索结果页不展示搜索框、快捷筛选、筛选按钮或筛选抽屉；Tab 展示顺序为综合、品牌、SKU、证书，小程序端不展示类目 Tab。
- 综合 Tab 只在有结果时展示分区：最多 1 条最佳匹配，其后按品牌、证书、SKU 顺序展示非 0 条分区；品牌/SKU/证书单独 Tab 内直接展示卡片内容，不再显示“品牌/SKU/证书 x 条”的分区标题。
- 综合 Tab 加载更多采用“品牌 / 证书首屏固定，SKU 持续追加”的 MVP 策略；第 2 页及后续页只追加 SKU 分区内容，不覆盖已展示的最佳匹配、品牌和证书结果。自动加载下一页时结果列表保持可见，底部仅显示轻量加载或完成状态，不展示黄色“加载更多”主按钮。
- SKU 结果复用 `components/product-card/`；品牌与证书结果使用与 SKU 卡片一致的一行卡片式视觉，但保留品牌/证书自身跳转行为。
- `best_match` 可返回 SKU、品牌或证书：SKU 编码或名称直接命中优先，其次品牌名精确命中，最后证书名称或证书编号精确命中；都不满足时为空。
- 搜索埋点通过 `track()` 上报 `search_page_view`、受防抖控制的 `search_input`、`search_suggestion_exposure`、`search_suggestion_click`、`search_submit`、集合语义的 `search_result_exposure`、`search_result_click`、`search_filter_apply`、`search_no_result`、`search_history_click`、`search_history_delete`、`search_history_clear`；埋点失败不得阻断搜索主流程。
- 本期不包含管理端搜索配置中心、后台热门词维护、同义词维护、自然语言词典维护、搜索统计管理页或 `/api/admin/search/*`。

## 商品列表页

商品列表页位于 `pages/product-list/index.*`，用于承接分类、搜索、品牌、新品榜和热销榜等入口。页面通过 `GET /api/v1/miniapp/products` 携带 `categoryId`、`categoryLevel`、`keyword`、`brandId`、`spec`、`priceRange`、`sort`、`page` 和 `pageSize` 获取公开 SKU、分页状态和筛选 facets；`categoryLevel=primary` 表示一级分类聚合，`categoryLevel=secondary` 表示二级分类精确查询。

- 列表容器统一处理首屏骨架屏、下拉刷新、上拉加载更多、无更多、空状态、错误状态和加载更多失败重试。
- 商品卡片仅展示主图、SKU 名称、品牌、规格和参考价格；整卡点击进入 SKU 详情页，不提供收藏、询价、购物车、立即购买、在线下单或联系商家快捷按钮。
- 品牌、分类和普通关键词入口在 `sort=default` 时由后端按 `COALESCE(published_at, created_at) ASC, id ASC` 返回，保持与品牌主页商品 Tab 一致；首页全部产品、新品榜、热销榜、价格排序和搜索页显式相关性排序保持各自策略。
- 底部筛选抽屉支持品牌、分类、规格和价格区间，排序支持默认、最新、价格升序和价格降序；筛选或排序变更后重置分页并重新请求第一页。
- 商品列表支持微信朋友分享和朋友圈分享，分享路径只保留 `categoryId`、`categoryLevel`、`categoryName`、`brandId`、`keyword`、`section`、`sourcePage` 白名单参数，中文参数必须编码，缺少可选参数时降级为可浏览列表。
- 商品列表埋点通过 `track()` 上报 `product_list_page_view`、`product_list_item_click`、`product_list_filter_open`、`product_list_filter_apply`、`product_list_sort_change`、`product_list_refresh`、`product_list_load_more`、`product_list_load_failed`、`product_list_share_click`；SKU 级曝光以 `product-card` 的 `product_card_exposure` 为主口径，并按页面、模块、列表上下文、关键词、`requestId` 和 SKU 去重；埋点失败不得阻断列表加载、筛选、排序、刷新、加载更多、详情跳转或分享。
- 本期不包含 Web 管理端商品列表组件、店主 Web 商品列表、后台商品管理列表、购物车、询价、在线下单或收藏能力。

## 商品详情页

商品详情页位于 `pages/tile-detail/index.*`，通过 `GET /api/v1/miniapp/skus/{sku_id}` 获取公开 SKU 详情聚合数据，并在旧接口兼容场景降级请求 `GET /api/v1/miniapp/products/{product_id}`。

- 页面展示大媒体区、商品摘要、品牌入口、商品参数、同系列推荐、同品牌推荐和底部收藏/分享操作。
- 商品详情页顶部图片轮播普通展示使用详情接口 `media[].display_url`，缺少展示图时仅可降级到 `thumbnail_url` 或本地占位图 `/assets/logos/product-logo.png`，不得把 `media[].url` 原图作为冷加载展示兜底；后端应只返回已存在且可读的 `display_url` / `thumbnail_url`，派生展示图缺失时由端侧占位图兜底。点击预览使用 `original_url`、`preview_url` 或等价高清 URL。商品列表、商品卡片和推荐位仍保留 `.thumb` 或等价轻量图片策略；Banner 作为首屏大图展示位优先消费 `.display`。轮播高度使用视口宽度约束的更高媒体区，首屏仍需露出商品名称或关键商品信息。
- 商品备注说明来自后端 `remark` 公开字段；小程序需过滤空值、`null`、`undefined` 占位值，并作为 `商品参数` 模块内的 `备注说明` 参数行展示，不得单独渲染独立“备注说明”模块。
- 商品详情页不得在摘要区展示 SKU 编码；SKU 编码、类目、规格、色系、表面工艺和备注说明等信息统一进入商品参数模块。
- 商品详情埋点通过 `track()` 上报 `sku_detail_view`、`sku_media_swipe`、`sku_image_preview`、`sku_video_play`、`sku_favorite`、`sku_unfavorite`、`sku_recommend_click`、`sku_share_click` 和 `sku_load_error`；埋点失败不得阻断详情浏览、媒体预览、收藏、分享或推荐跳转。

## 品牌入口页与品牌主页

品牌入口页位于 `pages/brand-list/index.*`，通过 `GET /api/v1/miniapp/brands` 获取品牌列表页轮播和启用品牌列表。页面顶部复用 `search-entry` 输入模式，按品牌名称、品牌简称和品牌英文名在当前品牌列表内过滤；搜索请求携带 `keyword`，搜索结果保持品牌列表页卡片布局，不跳完整搜索结果页；搜索态隐藏品牌列表页 Banner 和黑金品牌画廊兜底，清空关键词后恢复完整品牌列表和 Banner。顶部 Hero 保持品牌列表页 Banner 数据、指示器、自动播放和点击行为不变；无 Banner 时展示黑金品牌画廊兜底。轮播下方使用“品牌矩阵”单列卡片：卡片上半区作为品牌入口，展示圆形 Logo、品牌名称、`x 款商品` 和进入箭头；卡片下半区直接展示该品牌所有上架商品绑定的末级类目名称，不额外展示“按类目快速识别”或“全部类目 · 点击查看该品牌下的类目商品”等说明文案。类目来自响应 `leaf_categories`，小程序端按类目名称去重后全部折行展示，不使用 `+N` 折叠；类目胶囊区采用两列固定布局，左右列分别左对齐，类目名称超出胶囊宽度时单行省略，不换行、不撑破边框；类目胶囊字号比品牌名称小 2rpx，避免在移动端过弱；无类目时仅在类目区展示轻量 `暂无类目`。点击品牌卡片上半区进入 `pages/brand-detail/index?brandId=...`；点击类目标签进入 `pages/product-list/index?brandId=...&categoryId=...&categoryLevel=secondary&categoryName=...&sourcePage=brand-list-category`，不展示“公开”字样。

品牌主页位于 `pages/brand-detail/index.*`，通过 `GET /api/v1/miniapp/brands/{brand_id}` 获取品牌图片、品牌名称、英文名、简介、商品数和证书数；导航栏标题必须使用品牌名称 `brand_name`，不得使用品牌简称。顶部品牌文案以浮层形式覆盖在品牌 Hero 图片上，不展示“x 个商品 / x 个证书”数量行；顶部品牌图位属于首屏 Hero 大图展示位，普通展示优先使用 `brand_hero_display_url`，缺失或不可读时降级到 `brand_hero_thumbnail_url`，再降级到安全视图占位或品牌名占位，不请求 `brand_logo_url` 原图、preview、旧 `url`、语义不明 `image_url` 或不存在的本地静态占位图。品牌列表、品牌卡和详情页品牌入口等小 Logo 场景仍只消费 `brand_logo_thumbnail_url`。商品 Tab 复用 `GET /api/v1/miniapp/products?brandId=...` 和 `components/product-card/`，接口默认按 `published_at ASC, id ASC` 返回当前品牌公开 SKU，历史 `published_at` 空值由后端使用 `created_at` 兜底；小程序端只按接口返回顺序首屏展示和加载更多，不做端侧重排。证书 Tab 通过 `GET /api/v1/miniapp/brands/{brand_id}/certificates` 获取当前品牌可公开证书，卡片样式保持与证书列表页一致，卡片主点击进入 `pages/certificate-detail/index?certificateId=...`，文件预览能力下沉到证书详情页。

- 后端只返回启用品牌、公开 SKU 和可见证书，不暴露后台备注、审计字段、对象存储原始 key、Authorization header、Cookie 或敏感配置。启用品牌即使商品数为 0，也必须允许进入品牌主页；品牌详情接口返回 `product_count=0`，商品 Tab 展示空态，不得将 0 商品品牌误判为“暂不可查看”。
- 品牌入口页和品牌主页均使用 `custom-navigation`，需要按 `docs/knowledge-base/best-practices/miniapp-custom-navigation.md` 记录 DevTools 320/375/390/430 pt evidence；真机不可用时标记 blocked 或 follow_up。
- 品牌主页 Tab 样式需与搜索结果页“综合 / 品牌”等 Tab 保持一致；证书 Tab 的证书卡片需与 `pages/certificates/index.*` 的证书卡片保持一致。
- 品牌主页支持微信朋友分享和朋友圈分享，分享路径保留 `brandId` 与 `source=share`，标题优先使用品牌名称，图片优先使用公开品牌 Logo 并降级到本地占位图。
- 品牌页埋点通过 `track()` 上报 `brand_list_page_view`、`brand_list_carousel_click`、`brand_list_card_click`、`brand_detail_view`、`brand_detail_tab_click`、`brand_products_load`、`brand_certificates_load`、`brand_certificate_click` 和 `brand_detail_share_click`；埋点失败不得阻断页面加载、Tab 切换、证书详情跳转或分享。

## 证书列表页

证书列表页位于 `pages/certificates/index.*`，通过 `GET /api/v1/miniapp/certificates` 获取所有可公开证书，页面标题固定为“证书列表”。页面顶部复用 `search-entry` 输入模式，按证书名称、品牌名称、证书类型枚举或中文类型标签在当前证书列表页过滤；请求支持 `page`、`pageSize` 和 `keyword`，搜索结果保持证书卡片布局，不跳完整搜索结果页。页面不提供管理端证书类型筛选、品牌筛选、有效状态筛选或复杂筛选抽屉。

- 列表采用一行 2 个证书卡片；卡片文本仅展示证书名称、品牌名称和证书类型，不展示证书编号、签发方或有效期状态。
- 证书列表卡片主点击进入 `pages/certificate-detail/index?certificateId=...`，不直接绑定为文件预览。
- 页面需覆盖首屏加载、下拉刷新、触底加载更多、无更多、暂无公开证书、网络失败、加载更多失败和图片失败降级状态。
- 证书列表埋点通过 `track()` 上报 `certificate_list_page_view`、`certificate_list_load`、`certificate_list_refresh`、`certificate_list_load_more`、`list_search_submit`、`list_search_reset`、`certificate_click` 和 `certificate_load_failed`；搜索提交和清空需在请求成功后带 `resultCount`、`requestId`、`page_path`、`sourcePage`、`scope` 和 `client_type` 上报。埋点和日志不得记录 `file_key`、Authorization header、Cookie、`.env` 内容、本机路径或后台备注。

## 证书详情页

证书详情页位于 `pages/certificate-detail/index.*`，通过 `GET /api/v1/miniapp/certificates/{certificate_id}` 加载单张公开证书。页面复用商品详情页的大媒体区、信息分区、品牌入口、分享和错误态结构，但不得展示价格、收藏、推荐、购物车、购买、库存、促销或询价能力。

- 顶部媒体区优先展示主图；多图按主图优先、排序值和 ID 展示，图片可通过 `wx.previewImage` 从当前图开始预览。
- PDF 或未知文件使用稳定文件占位，通过 `wx.downloadFile` + `wx.openDocument` 打开；失败时展示稳定错误提示，不复制文件链接。
- 页面标题固定为“证书详情”；证书名称面板只展示证书类型和证书名称，不重复展示品牌名称。
- 证书信息模块展示证书类型、证书编号、发证机构、有效状态和备注说明，不展示有效期；备注说明来自后端 `remark` 公开字段，空值或占位值以安全占位处理。
- 品牌入口复用 `components/brand-card/`，使用后端返回的 `brand_entry_path` 和 `brand_logo_thumbnail_url` 展示所属品牌；证书详情页传入 `sourcePage=certificate_detail`、`sourceModule=brand_entry`、`certificateId` 和 `requestId`，普通展示不得 fallback 到品牌 Logo 原图。分享路径携带 `certificateId` 与 `source=share`；分享直达无页面栈时由 `custom-navigation` 返回兜底到首页。
- 页面不提供底部固定“预览文件”或“分享证书”交互按钮；图片/PDF 预览通过媒体区域触发，分享保留微信原生分享生命周期。
- 详情页埋点通过 `track()` 上报 `certificate_detail_view`、`certificate_detail_media_switch`、`certificate_detail_image_preview`、`certificate_detail_file_open`、`brand_card_click`、`certificate_detail_share_click` 和 `certificate_detail_load_failed`；不得记录原始对象 key、内部备注、Authorization header、Cookie、`.env` 内容、本机路径或个人隐私。

## 收藏列表页

收藏列表页位于 `pages/favorites/index.*`，使用本机 storage `miniapp_favorite_skus_v1` 展示用户已收藏 SKU。页面顶部复用 `search-entry` 输入模式，只在当前收藏范围内按商品名称、SKU 编码、品牌、类目和规格过滤；搜索结果保持收藏卡片布局，不跳完整搜索结果页。搜索空态说明“收藏范围内没有找到”并提供清空关键词路径，不展示显著的“去全局搜索调整”主按钮。

- 收藏页保留收藏项点击、取消收藏、失效对象降级、加载更多、加载失败和空收藏引导浏览商品路径。
- 收藏页搜索提交和清空通过 `track()` 上报 `list_search_submit`、`list_search_reset`，需包含 `resultCount`、`requestId`、`page_path`、`sourcePage`、`scope` 和 `client_type`；埋点失败不得阻断收藏列表浏览、搜索、清空或取消收藏。

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
- `/miniapp-prepare` 的 prod 策略、`urlCheck=true`、静态测试和生产 smoke 属于自动门禁；DevTools Network 与体验版 Network 属于待人工执行的 release/miniapp checklist，不得在未执行时写作自动通过。
- DevTools Network evidence 应记录微信开发者工具版本、基础库版本、运行策略、`urlCheck`、页面路径、请求域名、HTTP 状态、业务响应状态和资源加载结论，并说明不等同于体验版或真机网络验收。
- 体验版 Network evidence 应确认最新体验版入口、重新扫码、生产 API 域名、首页或列表页加载、详情页或媒体资源加载结论；无法执行时只能记录 `blocked`、`follow_up` 或明确的 `not_applicable`。
- Network evidence 记录不得包含 token、Cookie、Authorization header、`.env`、真实密钥、真实客户数据、未脱敏隐私或完整网络日志。
- `project.config.json` 默认关闭 `urlCheck` 用于本地 HTTP 后端调试；`project.private.config.json` 可在发布验证时打开 `urlCheck`，提交正式版前需在微信公众平台配置生产域名合法域名。
- 后端代码变更后需重新构建运行镜像，例如 `docker compose up -d --build tilesfst-backend`，否则微信开发者工具可能仍访问到旧接口。
- 小程序静态与首页聚合回归检查：`uv run pytest tests/test_miniapp_static.py tests/test_miniapp_home.py`。
