---
change_id: update-search-experience-unification
created_at: 2026-08-27 00:19:59
updated_at: 2026-08-28 15:10:59
---

## 设计概览

本 Change 将 REQ-0128 落为跨小程序、管理端列表、后端查询能力和观测口径的 OpenSpec 设计。核心原则是“统一入口、复用完整搜索页、列表内搜索不越界、管理端列表体验一致、行为链路可验收”。

## Requirement Readiness Report

| 项 | 结论 |
|---|---|
| REQ 状态 | `in_sprint`，已通过 `/req-review` 并纳入 `sprint-026` |
| 主文档 | `requirement.md` 已存在 |
| 用户故事 | `user-stories.md` 已存在 |
| 业务流程 | `business-flow.md` 已存在 |
| 验收标准 | `acceptance.md` 已存在，包含功能、UI、数据接口与观测 AC |
| Trace | `trace.md` 已存在，`iteration: sprint-026` |
| Prototype | 存在 `prototype/miniapp/prototype-context.md` 与 `prototype/web/context.md`，无 HTML/PNG |
| 结论 | ready |

## 影响分析

```yaml
impact:
  backend: true
  web: true
  miniapp: true
  admin: true
  database: possible_index_only
  storage: false
  api: true
capabilities:
  new: []
  modified:
    - miniapp-search
    - miniapp-home
    - miniapp-category-list-page
    - miniapp-brand-list-page
    - miniapp-certificate-list-page
    - miniapp-product-list-page
    - favorite-list-page
    - xl-admin-page-acceptance-template
    - product-usage-logging
change_type: update
```

## 产品数据采集与链路观测声明

```yaml
product_data_collection_observability:
  status: applicable
  affected_layers:
    - usage_events
    - request_logs
    - web_request_wrapper
    - miniapp_request_wrapper
    - api
  reason: 搜索入口点击、搜索提交、联想曝光/点击、结果曝光/点击、无结果、列表筛选和重置均是可命名用户行为，并会触发小程序或管理端业务 API 查询。
  validation: Change 必须声明稳定事件名、来源页面、scope、关键词脱敏摘要、结果数量、筛选条件摘要、behavior_trace_id / behavior_event_id / client_request_id 透传；普通搜索默认 Task Trace N/A，复杂长耗时查询需重新评估。
```

关键词、筛选条件和错误摘要不得保存 Authorization、Cookie、Token、密码、完整请求体、完整响应体、本机绝对路径、真实密钥或完整对象 key。请求日志只保存脱敏查询摘要、分页、结果数量、状态码和耗时等安全字段。

## 原型冲突报告

| 来源 | 状态 | 结论 |
|---|---|---|
| `prototype/miniapp/prototype-context.md` | 存在 context，无 HTML/PNG | 作为小程序入口位置、scope、sourcePage 和列表策略的最高事实源 |
| `prototype/web/context.md` | 存在 context，无 HTML/PNG | 作为管理端列表搜索一致性的最高事实源 |
| `acceptance.md` | 已补齐 AC | 作为可测试验收口径 |
| `rules/ui-design.md` | 已读取 | 约束 Web 管理端 semantic token 和小程序暗色旗舰风 |
| 既有 spec | 存在冲突 | `miniapp-product-list-page` 和 `miniapp-certificate-list-page` 旧规格要求不展示搜索入口，本 Change 通过 MODIFIED Requirements 调整 |

Conflict Resolution:

- 小程序完整搜索仍由 `/pages/search/index` 承接，不把完整搜索结果页嵌入每个列表。
- 搜索结果页非 SKU 结果不得继续使用会产生重复文案的通用信息模板；品牌结果按“图片 / 品牌名称 / SKU 数量”渲染，证书结果按“图片 / 证书名称 / 品牌 / 证书类型”渲染。
- 搜索结果页 SKU 数量面向用户统一展示为“x 个 SKU”，不展示“公开”内部可见性限定词。
- 搜索结果页综合 Tab 内容流按“最佳匹配 / 品牌 / 证书 / SKU”展示；顶部 Tab 顺序保持“综合 / 品牌 / SKU / 证书”，避免扰动高频 SKU Tab 入口。
- 搜索结果页分页优先随下滑自动加载；综合 Tab 采用“品牌 / 证书首屏固定，SKU 后续页无限追加”的 MVP 策略。自动加载下一页时不得用整页 loading 覆盖已展示结果，底部仅展示轻量加载状态或“已加载全部”，且不展示黄色“加载更多”主按钮。
- 商品列表页保持轻量双列浏览，但允许提供当前上下文搜索路径、跳转完整搜索页调整关键词或在当前列表范围搜索；不得新增复杂筛选抽屉或排序 tabs。
- 证书列表页按证书名称、品牌名称、证书类型枚举或中文类型标签在当前证书列表内过滤，保持证书卡片布局，不跳完整搜索结果页；旧“不展示搜索框”约束被本 Change 替换。
- 收藏列表页收敛为当前收藏范围内搜索，保持收藏卡片布局；搜索空态提供清空关键词和继续浏览商品路径，不再提供显著的全局搜索调整入口。
- 底部 Tab「全部分类」页保持纯分类浏览，不展示搜索入口；用户可通过分类进入商品列表后在商品列表上下文继续搜索。
- 品牌列表页搜索不跳完整搜索结果页，采用当前页品牌字段过滤：前端复用 `search-entry` 输入模式，请求 `/api/v1/miniapp/brands?keyword=...`，后端仅匹配品牌名称、品牌简称和品牌英文名；搜索态隐藏品牌 Banner 和 Hero 兜底，清空关键词后恢复完整品牌列表和 Banner。

## UI Contract

| 项 | 合同 |
|---|---|
| 事实源优先级 | `prototype-context.md` > `acceptance.md` > `rules/ui-design.md` > `docs/knowledge-base/best-practices/admin-list-page-consistency.md` > 既有 spec |
| 小程序页面与入口 | 首页和商品列表保留完整搜索页路径；品牌、证书、收藏列表页提供当前页输入过滤；全部分类页不展示搜索入口；完整搜索进入 `/pages/search/index` |
| 管理端页面与入口 | 品牌、类目、SKU、规格、Banner、证书、用户、日志主要列表保持统一搜索区、筛选区、重置、表格和分页顺序 |
| 信息架构 | 小程序搜索入口靠近页面标题、首屏主要内容或列表标题；管理端搜索入口位于列表筛选区，搜索/筛选变化后页码回到第一页 |
| 视觉 token | Web 管理端使用 Design System semantic token，不新增裸 Hex；小程序沿用暗色旗舰风、品牌金强调和既有 `search-entry` 视觉 |
| 交互状态 | 覆盖输入、提交、清空、取消、disabled、loading、empty、error、retry、debounce、并发旧响应丢弃 |
| 图标与文案 | 搜索入口文案必须区分全局搜索和当前列表搜索；管理端重置文案与既有列表模板一致 |
| Mock/API 边界 | 优先复用现有搜索页、现有列表 API 或纯前端过滤；新增 API 参数必须在实现任务中列出请求、响应、错误码、OpenAPI、Orval 和测试 |
| 权限规则 | 管理端搜索只返回当前用户有权查看的数据；小程序仅返回公开可见商品、品牌、类目和证书 |
| 一致性参照 | 管理端列表遵守 admin-list best practice：真实分页、`page-summary` + `page-right`、fixed toast、DS confirm、nowrap、sticky 操作列 |

## API 与数据库策略

- 小程序全局搜索优先复用 `/api/v1/miniapp/search` 或等价搜索 API。
- `/api/v1/miniapp/search` 的品牌分区和品牌最佳匹配 SHALL 返回可展示 `logo_url`；证书分区和证书最佳匹配 SHALL 返回 `file_url`、`thumbnail_url`、`brand_name`、`certificate_type` 和 `certificate_type_label`，但 SHALL NOT 暴露内部对象 key。
- `/api/v1/miniapp/search` 的综合 Tab 和 SKU Tab 第 2 页及后续页 SHALL 使用轻量 SKU-only 响应，跳过品牌、证书、facets、推荐词和最佳匹配等首屏摘要型查询；前端 SHALL 按 `entity_type` 合并分区，避免后续页覆盖首屏品牌 / 证书结果。
- `/api/v1/miniapp/search` 首屏响应 SHALL 避免同步调用搜索首页数据；`recommended_keywords` 使用轻量默认推荐词或空数组返回，不通过 `get_search_home()` 拉取热门商品，也不触发逐商品 `hot_score metadata LIKE` 分支。首页带关键词进入搜索页时，小程序 SHALL 跳过无必要的 `/api/v1/miniapp/search/home` 请求；用户清空关键词回到搜索首页时再加载搜索首页数据。
- `/api/v1/miniapp/search` 首屏 SHALL 按当前 Tab 执行最小查询集合：综合 Tab 只查询品牌、证书和 SKU，品牌 Tab 只查询品牌，证书 Tab 只查询证书，SKU Tab 只查询 SKU；当前 UI 不展示 facets、类目 named 和规格 named，因此首屏 SHALL 返回空 facets 并跳过相关聚合查询。
- `/api/v1/miniapp/search` 在关键词精确匹配启用品牌名称、品牌简称或品牌英文名时 SHALL 先形成品牌快路径；SKU 列表和 SKU count 使用该品牌 ID 过滤，避免继续使用 SKU 名称、编码、品牌、规格、表面、色系和类目等多字段 `OR LIKE` 主路径。未命中品牌快路径时，保留通用关键词召回逻辑。
- `/api/v1/miniapp/search` SHALL 通过 `Server-Timing` 响应头暴露安全的服务端分段耗时，包括品牌识别、SKU list、SKU count、品牌 named、证书查询和搜索构建总耗时；该响应头只包含阶段名和毫秒数，不包含关键词原文、SQL、内部对象 key、请求体或结果明细。
- 小程序列表型 SKU 卡片 SHALL 使用约定的缩略图 / 展示图 URL 组装列表图片，不在首页新品/热销、商品列表、搜索首页最近浏览/热门商品、完整搜索结果或 SKU 详情推荐中逐卡片同步调用对象存储存在性探测；缺失素材由小程序图片 fallback 和详情页媒体加载策略兜底。详情主媒体、Banner、证书详情和品牌 Hero 保留存在性探测。
- 搜索 SKU 查询 SHALL 避免逐商品扫描 `usage_events.metadata` 计算热度；如后续需要“热度排序”，应通过预聚合或可索引字段独立设计。
- 小程序列表内搜索优先复用现有列表 API 的 `keyword`、`categoryId`、`brandId`、`section`、`page` 和 `page_size` 等参数；品牌列表页通过 `/api/v1/miniapp/brands` 的 `keyword` 参数仅匹配品牌名称、品牌简称和品牌英文名，搜索态不返回 Banner；证书列表页通过 `/api/v1/miniapp/certificates` 的 `keyword` 参数匹配证书名称、品牌名称、证书类型枚举和中文类型标签；收藏列表页为本机收藏数据前端过滤，不新增后端 API。
- 管理端品牌、类目、SKU、规格、Banner、证书、用户、日志等列表优先复用现有 keyword/filter/page/page_size；若页面缺少后端 keyword 支持，必须新增参数并同步 OpenAPI、Orval、API 文档和测试。
- 默认不新增数据库表，不调整保留周期；如出现性能证据要求普通索引，必须同步 SQLite/MySQL schema、迁移、数据库文档和测试。

## 测试策略

- 小程序：覆盖 `search-entry` 入口/输入模式、首页搜索入口、品牌/证书/收藏列表内搜索、商品列表搜索路径、全部分类页无搜索入口、搜索页承接、空态/错误态、`.ts` 与 `.js` 运行入口一致。
- 管理端：覆盖代表性列表的 keyword 输入、防抖或提交、筛选重置、页码重置、真实 total、空态、权限边界和 admin-list 横切 DOM。
- 后端 API：覆盖新增或调整的查询参数校验、长度限制、枚举、分页、权限过滤、错误响应、品牌词搜索 SKU `brand_id` 快路径、搜索接口 `Server-Timing` 分段耗时响应头、列表型 SKU 卡片构建不探测对象存储和 request log 摘要。
- Orval：API contract 变化时运行 OpenAPI 导出与 Orval 生成，并检查生成物未手写修改。
- 观测：覆盖稳定事件名、关键词脱敏、请求链路 ID 透传、行为事件与请求日志关联、普通搜索 Task Trace N/A。

## 非目标

- 不引入 Elasticsearch、向量搜索、外部搜索服务或复杂分词引擎。
- 不新增搜索词运营后台、搜索词报表、同义词、纠错或结果高亮。
- 不把完整搜索结果页嵌入所有列表页。
- 不新增管理端高级查询 DSL、保存筛选方案或跨表高级检索。
- 不调整 Docker Compose、对象存储和媒体上传链路。
