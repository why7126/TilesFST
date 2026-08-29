## 1. 小程序搜索入口与搜索页承接

- [x] 1.1 盘点 `src/miniapp/components/search-entry/` 与 `/pages/search/index` 现有契约，确认入口模式、输入模式、`keyword`、`placeholder`、`scope`、`sourcePage`、disabled、提交、清空和取消事件。
- [x] 1.2 强化首页搜索入口位置与视觉权重，保证入口位于首屏高优先级区域，不遮挡导航、Banner、快捷入口、推荐区和底部 TabBar。
- [x] 1.3 统一首页、商品列表等页面进入 `/pages/search/index` 的跳转参数，保留 `sourcePage`、`scope`、`keyword` 和当前上下文；品牌、证书、收藏列表页采用当前页输入过滤；全部分类页不展示搜索入口。
- [x] 1.4 保持搜索页搜索首页、历史、热门、联想、综合结果、分区结果、无结果和加载更多逻辑不回归。
- [x] 1.5 同步维护小程序 `.ts` 与 `.js` 运行入口，避免体验版加载逻辑漂移。

## 2. 小程序列表搜索路径

- [x] 2.1 全部分类页保持左右双栏分类浏览为主体验，不展示搜索入口；分类进入商品列表后可在商品列表上下文继续搜索。
- [x] 2.2 品牌列表支持按品牌名称、品牌简称和品牌英文名在当前页过滤，搜索态隐藏 Banner，关键词空态、清空恢复和品牌详情跳转保持稳定。
- [x] 2.3 证书列表支持按证书名称、品牌名称或证书类型在当前证书列表页过滤，搜索结果保持证书卡片布局，不跳完整搜索结果页。
- [x] 2.4 商品列表支持当前分类、品牌、section 或关键词上下文下的搜索路径，并在空态中提供返回完整搜索页调整关键词的入口。
- [x] 2.5 收藏页收敛为当前收藏范围搜索，搜索结果保持收藏卡片布局，搜索空态只提供清空关键词或继续浏览商品，不提供全局搜索调整主入口。

## 3. 管理端列表搜索一致性

- [x] 3.1 盘点品牌、类目、SKU、规格、Banner、证书、用户、日志列表的 keyword/filter/page/page_size 支持情况，形成最终 MVP 页面清单。
- [x] 3.2 优先复用 `AdminListPage` 或既有筛选卡片样式，统一搜索输入、筛选区、重置按钮、表格、分页和空态顺序。
- [x] 3.3 搜索、筛选和重置后页码回到第一页，并展示后端真实 total，不使用全量拉取后前端伪分页作为验收依据。
- [x] 3.4 保持权限边界，管理端搜索只返回当前登录用户有权查看的数据。
- [x] 3.5 保持 admin-list 横切 gate：`page-summary` + `page-right`、fixed toast、DS confirm、nowrap、sticky 操作列和窄屏可达性。

## 4. API、Orval 与数据库

- [x] 4.1 对每个纳入页面声明复用现有 API、纯前端过滤或新增后端查询参数的依据。
- [x] 4.2 若新增或调整查询参数，补充后端校验、长度限制、枚举、默认值、错误响应和权限过滤。
- [x] 4.3 API contract 变化时同步 OpenAPI、Orval、`docs/03-api-index.md`、前端调用和测试。
- [x] 4.4 若新增普通索引或检索字段，同步 SQLite/MySQL schema、迁移、`docs/04-database-design.md` 和测试；若不改 DB，记录 N/A 原因。

## 5. 行为事件与请求链路

- [x] 5.1 定义搜索入口点击、搜索输入停顿、搜索提交、联想曝光、联想点击、结果曝光、结果点击、无结果、列表筛选和重置事件名。
- [x] 5.2 行为事件属性包含来源页面、搜索范围、关键词脱敏摘要、结果数量、选中 Tab、筛选条件摘要、请求 ID 或 N/A 原因。
- [x] 5.3 小程序和 Web 管理端请求封装透传 `behavior_trace_id`、`behavior_event_id`、`client_request_id` 或等价字段。
- [x] 5.4 后端 request logs 保存脱敏查询摘要、结果数量、耗时和链路 ID，不保存敏感原文。
- [x] 5.5 普通搜索记录 Task Trace N/A；若实现中出现长耗时复杂查询，补充 Task Trace 声明与验收。

## 6. 验证

- [x] 6.1 小程序静态或交互测试覆盖搜索入口、跳转参数、联想降级、无结果、错误态和 320/375/430 pt 不遮挡。
- [x] 6.2 管理端测试覆盖代表性列表搜索/筛选/重置、分页真实 total、空态、权限和 admin-list 横切 DOM。
- [x] 6.3 后端测试覆盖新增或调整的查询参数、权限过滤、分页和错误响应。
- [x] 6.4 观测测试覆盖事件字典、关键词脱敏、行为链路 ID 透传和 request logs 关联。
- [x] 6.5 运行 `python scripts/validate-product-data-observability-gates.py --change update-search-experience-unification` 或等价聚焦校验。
- [x] 6.6 运行 `python scripts/validate-openspec-language.py`。
- [x] 6.7 运行 `openspec validate update-search-experience-unification --strict`。
- [x] 6.8 运行 `python scripts/sync-workflow-status.py --event opsx.apply --change update-search-experience-unification --sprint auto --dry-run`，确认 Change 已在 `sprint-026` scope。

## 验收返修记录

- [x] 2026-08-27 搜索结果页品牌卡片返修：品牌最佳匹配和品牌分区展示品牌图片或稳定占位、品牌名称和 `x 个 SKU`，去掉“公开 SKU”和重复“最佳匹配 + 品牌名”行。
- [x] 2026-08-27 搜索结果页证书卡片返修：证书最佳匹配和证书分区展示证书图片或稳定占位、证书名称、品牌和证书类型。
- [x] 2026-08-27 搜索结果页加载方式返修：下滑到底自动触发加载更多，并在 loading 或无下一页时避免重复请求。
- [x] 2026-08-27 搜索响应字段返修：品牌结果返回 `logo_url`，证书结果返回 `file_url`、`thumbnail_url`、`brand_name`、`certificate_type`、`certificate_type_label`，不暴露内部对象 key。
- [x] 2026-08-27 搜索结果页二次返修：综合 Tab 按 `entity_type` 合并分区，首屏保留最佳匹配、品牌和证书，后续页只向 SKU 分区追加新 SKU，避免 `displaySections` 被新响应覆盖。
- [x] 2026-08-27 搜索性能二次返修：综合 Tab 和 SKU Tab 第 2 页及后续页返回 SKU-only 轻量响应，跳过品牌、证书、facets、推荐词和最佳匹配查询；搜索 SKU 查询不再逐商品计算 `usage_events.metadata LIKE` 热度分。
- [x] 2026-08-28 搜索结果页三次返修：拆分首屏 `loading` 与底部 `loadingMore`，自动加载下一页时保留已有结果，仅在底部显示“加载更多中...”或“已加载全部”；移除黄色“加载更多”主按钮。
- [x] 2026-08-28 搜索结果页四次返修：综合 Tab 内容流顺序调整为最佳匹配、品牌、证书、SKU；顶部 Tab 顺序保持综合、品牌、SKU、证书，后续页仍只向 SKU 分区追加。
- [x] 2026-08-28 分类列表页范围澄清返修：底部 Tab「全部分类」页移除 `search-entry`、组件注册和搜索跳转逻辑，保留分类双栏浏览与进入商品列表路径。
- [x] 2026-08-28 品牌列表页范围澄清返修：品牌列表页搜索改为 `search-entry` 输入模式当前页过滤，按品牌名称、品牌简称和品牌英文名匹配；搜索结果保持品牌卡片布局，搜索态隐藏 Banner，清空后恢复完整品牌列表和 Banner；后端 `/api/v1/miniapp/brands` 新增 `keyword` 参数并同步 OpenAPI/Orval、API 文档和测试。
- [x] 2026-08-28 品牌列表页搜索埋点返修：`list_search_submit` / `list_search_reset` 改为品牌列表请求成功后上报，补齐 `resultCount`、`requestId`、`page_path`、`sourcePage`、`scope` 和 `client_type`，避免 usage-events 因缺少必填属性返回 400。
- [x] 2026-08-28 证书列表页与收藏列表页搜索范围返修：证书列表页改为 `search-entry` 输入模式当前页过滤，后端 `/api/v1/miniapp/certificates` 新增 `keyword`；收藏列表页保留当前收藏范围过滤并移除全局搜索调整入口；两页搜索提交/清空埋点补齐 usage event 必填属性。
- [x] 2026-08-28 首页搜索入口搜索耗时返修：截图确认 `/api/v1/miniapp/search` 首屏 TTFB 约 3.80s，端侧从首页带关键词进入搜索页时跳过无必要 `/search/home` 请求；后端搜索首屏 `recommended_keywords` 改为轻量默认词，不再同步调用 `get_search_home()` 触发热门商品和 `hot_score metadata LIKE` 分支。
- [x] 2026-08-28 搜索结果页性能继续返修：截图确认 `/api/v1/miniapp/search` 首屏 TTFB 降至约 2.55s 但仍偏慢；综合 Tab 首屏仅查询品牌、证书、SKU 和 best_match 所需数据，移除未展示的 facets、类目 named、规格 named 查询；品牌/证书/SKU 单独 Tab 只执行本 Tab 必要查询。
- [x] 2026-08-28 搜索结果页性能品牌词返修：复测截图确认 `/api/v1/miniapp/search` TTFB 约 2.43s，移除 facets 与类目/规格 named 后改善不明显；新增品牌精确命中快路径，品牌词场景下 SKU 查询和 count 使用 `brand_id` 过滤，避免通用多字段 `OR LIKE` 扫描，并用测试钩子验证不走全字段 SKU LIKE 主路径。
- [x] 2026-08-28 搜索结果页性能定位返修：复测截图显示 `/api/v1/miniapp/search` TTFB 仍约 2.50s；为完整搜索接口补充 `Server-Timing` 响应头，输出品牌识别、SKU list、SKU count、品牌 named、证书查询和总构建耗时，方便在微信开发者工具 Timing 面板定位真实慢段。
- [x] 2026-08-28 搜索结果页卡片构建性能返修：`Server-Timing` 确认 SQL 子阶段仅毫秒级，`search_build` 约 2.77s；搜索结果 SKU 卡片构建改为直接返回约定缩略图 / 展示图 URL，不再逐卡片同步探测对象存储文件存在性，并新增 `search_product_cards` 分段耗时。
- [x] 2026-08-28 列表型 SKU 卡片同类性能返修：小程序首页新品/热销、商品列表、搜索首页最近浏览/热门商品和 SKU 详情推荐统一复用轻量列表卡片，不再逐卡片同步探测对象存储文件存在性；详情主媒体、Banner、证书详情和品牌 Hero 保留存在性探测。
