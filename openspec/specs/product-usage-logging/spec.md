# 产品使用行为日志规范

## Purpose
定义产品使用行为埋点、API 请求日志、日志存储、管理端日志审计查询与详情展示能力，确保排障、安全审计和产品行为分析有统一、可检索、可脱敏的事实来源。
## Requirements
### Requirement: API 请求日志采集
系统 SHALL 采集 API 请求日志摘要，用于运维排障和审计链路关联。

#### Scenario: 生成或透传 request_id
- **WHEN** 客户端发送 API 请求且未携带 request_id
- **THEN** 系统 SHALL 为该请求生命周期生成 request_id
- **AND** 请求日志 SHALL 存储该 request_id。

#### Scenario: 持久化请求摘要
- **WHEN** API 请求完成
- **THEN** 系统 SHALL 持久化 method、path、status code、毫秒级耗时、request id、client type、可用的操作者上下文、摘要和创建时间。

#### Scenario: 异常请求存储脱敏错误上下文
- **WHEN** API 请求因应用错误或服务端错误失败
- **THEN** 请求日志 SHALL 存储 status code、可用的 error code、错误摘要、request id 和已脱敏 metadata
- **AND** SHALL NOT 存储原始密钥、密码、Authorization header、Cookie 或数据库连接串。

#### Scenario: 默认排除噪声路由
- **WHEN** 请求目标为健康检查、静态资源、Swagger/OpenAPI 文档或媒体直出路由
- **THEN** 系统 SHALL 将该请求排除在默认请求日志采集之外。

### Requirement: 产品使用行为事件采集
系统 SHALL 按人工定义的事件字典采集产品使用行为事件。事件字典 SHALL 支持 Web 管理端既有事件，并 SHALL 支持微信小程序首页、首页样式信息架构优化、商品详情和搜索的详情访问、分享、咨询、快捷入口、瀑布流、搜索交互和安全降级事件，用于小程序热销推荐统计、搜索体验分析和后续产品优先级判断。

#### Scenario: 接受已登记事件
- **WHEN** 客户端提交的 usage event 存在于事件字典且包含全部必填属性
- **THEN** 系统 SHALL 校验该事件
- **AND** 持久化事件，同时写入服务端推导的用户、角色、client type、request id、timestamp、user agent 摘要和 IP 摘要。

#### Scenario: 拒绝未知事件
- **WHEN** 客户端提交的 usage event 未在事件字典中定义
- **THEN** 系统 SHALL 使用已文档化的校验错误拒绝该事件
- **AND** 拒绝埋点 SHALL NOT 中断用户主业务流程。

#### Scenario: 阻断禁止属性
- **WHEN** usage event 包含 token、password、authorization、cookie、raw payload 或 raw filename 等禁止属性
- **THEN** 系统 SHALL 按服务端校验策略在持久化前拒绝或移除这些属性
- **AND** SHALL NOT 将前端脱敏作为安全边界。

#### Scenario: 强制执行 MVP 事件字典
- **WHEN** 实现处理 MVP 事件
- **THEN** 系统 SHALL 至少支持 page_view、search_submit、filter_change、detail_view、copy_request_id、entity_create、entity_update、entity_delete、status_change、media_upload、login_success、login_failed 和 api_error。

#### Scenario: Web 管理端上报行为事件
- **WHEN** 已认证 admin 或 employee 打开任一已登记 Web 管理端页面
- **THEN** Web 客户端 SHALL 通过共享 tracking client 上报 `page_view` usage event，并携带 module、page path、route pattern、page title、entity type 和 entity id。
- **WHEN** 已认证 admin 修改日志审计筛选、执行查询、复制 request id 或打开详情抽屉
- **THEN** Web 客户端 SHALL 通过共享 tracking client 上报对应交互 usage event
- **AND** 埋点失败 SHALL NOT 阻断可见用户流程。

#### Scenario: 小程序首页与商品详情行为事件
- **WHEN** 微信小程序用户浏览商品详情、分享首页、分享商品、点击首页咨询或点击商品咨询
- **THEN** 系统 SHALL 接受已登记的 `product_detail_view`、`home_share`、`product_share`、`home_contact_click`、`product_contact_click` 事件
- **AND** 事件 SHALL 携带必要的商品 ID、页面标识、client type 和时间上下文
- **AND** 事件 SHALL NOT 包含聊天内容、Authorization header、Cookie、原始手机号或其它不必要个人敏感信息
- **AND** 埋点失败 SHALL NOT 阻断小程序浏览、分享或咨询主流程。

#### Scenario: 小程序首页样式与信息架构行为事件
- **WHEN** 微信小程序用户点击首页搜索、快捷入口、新品商品、热销商品、全部产品商品、收藏视觉图标或证书 Tab
- **THEN** 系统 SHALL 接受已登记或等价预留的 `miniapp_home_search_click`、`miniapp_home_quick_entry_click`、`miniapp_home_new_product_click`、`miniapp_home_hot_product_click`、`miniapp_home_waterfall_product_click`、`miniapp_home_favorite_visual_click` 和 `miniapp_certificate_tab_click` 事件
- **AND** 事件 SHALL 仅携带必要的入口标识、商品 ID、页面标识、client type 和时间上下文
- **AND** 事件 SHALL NOT 承诺或写入收藏持久化事实。

#### Scenario: 小程序瀑布流加载行为事件
- **WHEN** 全部产品瀑布流发生首屏加载、下一页加载、加载失败或无更多状态
- **THEN** 系统 SHALL 接受已登记或等价预留的 `miniapp_home_waterfall_load`、`miniapp_home_waterfall_load_failed` 和 `miniapp_home_waterfall_end_reached` 事件
- **AND** 埋点失败 SHALL NOT 阻断瀑布流展示、追加、重试或无更多提示。

#### Scenario: 小程序搜索行为事件
- **WHEN** 微信小程序用户浏览搜索页、输入关键词、看到联想、点击联想、提交搜索、看到搜索结果、点击搜索结果、应用筛选、遇到无结果或操作搜索历史
- **THEN** 系统 SHALL 接受已登记或等价预留的 `search_page_view`、`search_input`、`search_suggestion_exposure`、`search_suggestion_click`、`search_submit`、`search_result_exposure`、`search_result_click`、`search_filter_apply`、`search_no_result`、`search_history_click`、`search_history_delete` 和 `search_history_clear` 事件
- **AND** 事件 SHALL 仅携带 keyword、normalizedKeyword、scope、entityType、resultCount、sourcePage、filterSnapshot、requestId、client type 和时间上下文等必要字段
- **AND** 事件 SHALL NOT 包含手机号、聊天内容、Authorization header、Cookie、raw payload、raw object key 或其它不必要个人敏感信息
- **AND** 埋点失败 SHALL NOT 阻断搜索输入、联想展示、结果展示、筛选、无结果页或历史操作主流程。

### Requirement: 日志存储与保留
系统 SHALL 将 request logs 与 usage events 存储在关系型存储中，并提供可查询索引和保留周期治理。

#### Scenario: 关系型存储支持 demo 与生产
- **WHEN** 应用运行在本地或 Docker demo 模式
- **THEN** 日志 SHALL 使用 SQLite 兼容 schema 存储
- **AND** 当应用运行在 MySQL 生产环境
- **THEN** 日志 SHALL 使用 MySQL 兼容 schema，且不得包含 SQLite-only DDL。

#### Scenario: 常用筛选字段建立索引
- **WHEN** 日志按创建时间、日志类型、操作者、request id、status code 或 path 查询
- **THEN** 系统 SHALL 使用索引或等价优化的数据库访问方式
- **AND** SHALL NOT 在过滤前将全部日志加载到内存。

#### Scenario: 定义保留周期策略
- **WHEN** 评估日志保留周期
- **THEN** request logs 与 usage events SHALL 遵循既有审计保留策略，或遵循明确文档化的专用保留配置。

#### Scenario: metadata 保持可展示
- **WHEN** 日志包含 metadata
- **THEN** 系统 SHALL 在脱敏和截断后以 JSON 或等价可解析结构存储 metadata
- **AND** 若 metadata 解析失败，列表页 SHALL 仍展示核心日志字段。

### Requirement: 管理端日志查询 API
系统 SHALL 提供仅管理员可用的日志列表与详情查询 API。

#### Scenario: 管理员查询日志列表
- **WHEN** 已认证 admin 调用 `GET /api/v1/admin/logs`
- **THEN** 系统 SHALL 返回统一响应，包含分页日志项、total、page、page_size 和指标摘要。

#### Scenario: 支持日志列表筛选
- **WHEN** admin 按日志类型、时间范围、操作者、client type、status code 或 result、resource id、path、keyword 或 request id 筛选
- **THEN** 系统 SHALL 仅返回匹配日志，并按最新优先排序。

#### Scenario: 管理员查询日志详情
- **WHEN** 已认证 admin 针对已存在日志调用 `GET /api/v1/admin/logs/{id}`
- **THEN** 系统 SHALL 返回基础信息、请求信息、操作者与客户端、操作上下文、事件属性和 metadata 等详情分组。

#### Scenario: 拒绝非管理员访问
- **WHEN** employee、店主端客户端、小程序用户或匿名用户调用管理端日志 API
- **THEN** 系统 SHALL 使用已文档化的 forbidden 响应拒绝访问。

#### Scenario: 日志不存在返回 not found
- **WHEN** admin 请求不存在的 log id
- **THEN** 系统 SHALL 返回已文档化的 404 类错误响应。

### Requirement: 使用行为事件接收 API
系统 SHALL 为受支持客户端提供 usage event 接收 API。

#### Scenario: 事件接收成功
- **WHEN** 受支持客户端向 `POST /api/v1/usage-events` 提交合法事件
- **THEN** 系统 SHALL 持久化该事件
- **AND** 返回统一成功响应，且不暴露内部存储细节。

#### Scenario: 事件接收校验失败
- **WHEN** 受支持客户端提交的事件存在属性类型非法、缺少必填字段、长度超限或包含禁止数据
- **THEN** 系统 SHALL 返回已文档化的校验错误
- **AND** 客户端集成 SHALL 将埋点失败视为不阻断主用户流程。

#### Scenario: 控制匿名边界
- **WHEN** 匿名客户端提交 usage event
- **THEN** 系统 SHALL 仅对明确支持的 client type 和 event name 接受事件
- **AND** SHALL NOT 采集敏感个人信息。

### Requirement: 管理端日志审计页面

系统 SHALL 提供 Web 管理端日志审计页面，并对齐产品 v2 Golden Reference。

#### Scenario: 管理员打开日志审计页

- **WHEN** 已认证 admin 打开 `/admin/logs`
- **THEN** 系统 SHALL 在既有 Admin Shell 内渲染日志审计页面
- **AND** SYSTEM sidebar SHALL 展示并激活 `日志审计`。

#### Scenario: 指标与筛选可见

- **WHEN** admin 查看日志审计页
- **THEN** 页面 SHALL 展示 TODAY LOGS、API ERRORS、SLOW REQUESTS 和 SENSITIVE OPS 指标卡
- **AND** 页面 SHALL 展示日志类型、时间范围、操作者、状态或结果、资源或 ID、路径或 request id 筛选。
- **AND** 状态或结果筛选 SHALL 使用下拉选择交互，支持成功、失败和常见 HTTP 状态码精确筛选，且 SHALL 至少包含 `422 参数校验错误`。

#### Scenario: 日志表格支持排障

- **WHEN** admin 查看日志行
- **THEN** 表格 SHALL 展示时间、类型、事件或摘要、操作者、客户端、状态或结果、耗时、request id、复制操作和详情操作。
- **AND** 类型与状态或结果 SHALL 通过不同颜色或等价视觉样式区分不同值，便于管理员快速扫描异常日志。

#### Scenario: request_id 可复制且不造成布局位移

- **WHEN** admin 复制带有 request id 的日志记录
- **THEN** 系统 SHALL 优先将完整 request id 写入系统剪贴板
- **AND** 系统 SHALL 使用 fixed toast 或等价不造成布局位移的反馈展示成功、失败或兜底结果
- **AND** 当 Clipboard API 不存在、浏览器拒绝写入或写入失败时，系统 SHALL 不抛出未捕获错误
- **AND** 系统 SHALL 提供手动复制指引、可选中文本或等价兜底，使 admin 仍可获取完整 request id
- **AND** 系统 SHALL 仅在剪贴板写入成功时记录 `copy_request_id` 成功行为事件。

#### Scenario: employee 不可打开页面

- **WHEN** 已认证 employee 打开 `/admin/logs`
- **THEN** 系统 SHALL 按既有管理端授权模式展示 forbidden 状态或重定向
- **AND** 不暴露日志数据。

#### Scenario: 日志能力测试覆盖

- **WHEN** 实现完成
- **THEN** 后端测试 SHALL 覆盖日志记录、校验、脱敏、权限、筛选和 not-found 行为
- **AND** 前端测试 SHALL 覆盖列表渲染、筛选、request_id 复制成功、Clipboard API 不可用兜底、复制写入失败兜底、详情抽屉、forbidden 状态和分页结构。

### Requirement: 日志详情抽屉
系统 SHALL 在右侧抽屉中展示日志详情，且不丢失列表上下文。

#### Scenario: 打开详情抽屉
- **WHEN** admin 选择日志行详情操作
- **THEN** 页面 SHALL 打开右侧抽屉，并在抽屉背后保留可见列表上下文。

#### Scenario: 详情分组匹配原型
- **WHEN** 详情抽屉可见
- **THEN** 抽屉 SHALL 分组展示基础信息、请求信息、操作者与客户端、操作上下文、事件属性和 metadata JSON。

#### Scenario: 关闭抽屉
- **WHEN** admin 点击关闭、点击遮罩或按下 Escape
- **THEN** 抽屉 SHALL 关闭，并保留当前筛选和分页状态。

#### Scenario: metadata 脱敏且可滚动
- **WHEN** 抽屉展示 metadata
- **THEN** metadata SHALL 使用等宽字体可滚动区域展示
- **AND** 敏感字段 SHALL 被脱敏或省略。

### Requirement: OpenAPI、Orval 与文档治理
系统 SHALL 保持产品使用日志相关 API、数据库、文档和生成客户端产物同步。

#### Scenario: 生成 API 契约
- **WHEN** 后端日志 API 被实现或变更
- **THEN** OpenAPI SHALL 暴露 response models、summaries、descriptions 和 tags
- **AND** Orval SHALL 生成对应 Web client methods。

#### Scenario: 文档保持同步
- **WHEN** 日志能力被实现
- **THEN** `docs/03-api-index.md`、`docs/04-database-design.md` 和适用的错误码文档 SHALL 描述新增 endpoints、schemas、tables 和 errors。

#### Scenario: 校验与测试覆盖能力
- **WHEN** 实现完成
- **THEN** 后端测试 SHALL 覆盖日志记录、校验、脱敏、权限、筛选和 not-found 行为
- **AND** 前端测试 SHALL 覆盖列表渲染、筛选、request_id 复制、详情抽屉、forbidden 状态和分页结构。

### Requirement: 日志审计复制 helper 迁移边界

Product usage logging SHALL preserve the existing `/admin/logs` request id copy behavior when the Web client migrates that interaction to a shared Clipboard copy helper or equivalent normalized pattern.

#### Scenario: request_id 复制成功后埋点

- **WHEN** an admin copies a non-empty request id and Clipboard writing succeeds
- **THEN** the Web client SHALL continue to emit the `copy_request_id` usage event
- **AND** the event SHALL NOT include passwords, tokens, Authorization values, cookies, or unrelated sensitive metadata.

#### Scenario: request_id 复制失败不记录成功事件

- **WHEN** Clipboard API is unavailable, Clipboard writing fails, or the request id is empty
- **THEN** the Web client SHALL NOT emit a successful `copy_request_id` usage event
- **AND** it SHALL show fixed toast or equivalent manual-copy guidance without causing list layout shift.

#### Scenario: request_id 复制测试保持

- **WHEN** the logs page frontend tests run after helper migration
- **THEN** they SHALL cover request id copy success, Clipboard API unavailable fallback, Clipboard write failure fallback, and empty request id behavior
- **AND** they SHALL continue to cover list pagination structure.

### Requirement: 小程序 SKU 详情页行为事件
系统 SHALL 支持微信小程序 SKU 详情页行为事件，用于记录详情浏览、媒体交互、收藏、分享、品牌入口、推荐点击和加载失败，同时遵守统一 usage event 脱敏策略。

#### Scenario: SKU 详情页浏览事件
- **WHEN** 微信小程序 SKU 详情页成功展示
- **THEN** 系统 SHALL 接受已登记或等价预留的 `sku_detail_view` 事件
- **AND** 事件 SHALL 仅携带必要的 SKU ID、页面标识、来源参数、client type 和时间上下文
- **AND** 埋点失败 SHALL NOT 阻断详情页展示。

#### Scenario: SKU 媒体交互事件
- **WHEN** 用户切换媒体、打开图片预览或播放视频
- **THEN** 系统 SHALL 接受已登记或等价预留的 `sku_media_swipe`、`sku_image_preview` 和 `sku_video_play` 事件
- **AND** 事件 SHALL NOT 包含原始 object key、未授权媒体 URL、Authorization header、Cookie 或用户敏感信息。

#### Scenario: SKU 收藏和分享事件
- **WHEN** 用户成功收藏、取消收藏或点击分享 SKU
- **THEN** 系统 SHALL 接受已登记或等价预留的 `sku_favorite`、`sku_unfavorite` 和 `sku_share_click` 事件
- **AND** 收藏事件 SHALL 仅记录 SKU 粒度业务事实和必要上下文
- **AND** 分享事件 SHALL NOT 存储聊天内容、联系人、群信息或原始手机号。

#### Scenario: SKU 品牌和推荐点击事件
- **WHEN** 用户点击品牌入口、同系列推荐或同品牌推荐
- **THEN** 系统 SHALL 接受已登记或等价预留的 `sku_brand_click` 和 `sku_recommend_click` 事件
- **AND** 推荐点击事件 SHALL 携带当前 SKU ID、目标 SKU ID、推荐类型和必要页面上下文。

#### Scenario: SKU 详情加载失败事件
- **WHEN** SKU 详情加载失败、SKU 不存在或网络失败
- **THEN** 系统 SHALL 接受已登记或等价预留的 `sku_load_error` 事件
- **AND** 事件 metadata SHALL 只包含脱敏错误码、失败阶段和必要页面上下文
- **AND** SHALL NOT 持久化原始响应体、token、Cookie、Authorization header 或内部路径。

### Requirement: 小程序商品列表行为事件
系统 SHALL 记录小程序商品列表浏览、曝光、点击、筛选、排序、刷新、加载更多和失败事件，用于分析商品发现效率。

#### Scenario: 商品列表页浏览
- **WHEN** 用户进入商品列表页
- **THEN** 系统 SHALL 记录 `product_list_page_view`
- **AND** 事件 SHALL 包含 sourcePage、categoryId、brandId、keyword、sort、filterSnapshot、pageSize 和 requestId 中适用字段。

#### Scenario: 商品曝光与点击
- **WHEN** 商品卡片曝光或用户点击商品卡片
- **THEN** 系统 SHALL 记录 `product_list_item_exposure` 或 `product_list_item_click`
- **AND** 事件 SHALL 包含 skuId、sourcePage、列表上下文、位置索引和 requestId 中适用字段。

#### Scenario: 筛选和排序事件
- **WHEN** 用户打开筛选、应用筛选或切换排序
- **THEN** 系统 SHALL 记录 `product_list_filter_open`、`product_list_filter_apply` 或 `product_list_sort_change`
- **AND** 事件 SHALL 包含 filterSnapshot、sort、resultCount 和 requestId 中适用字段。

#### Scenario: 刷新与加载更多事件
- **WHEN** 用户触发下拉刷新、上拉加载更多或加载失败
- **THEN** 系统 SHALL 记录 `product_list_refresh`、`product_list_load_more` 或 `product_list_load_failed`
- **AND** 事件 SHALL 包含 page、pageSize、resultCount、errorCode 和 requestId 中适用字段。

#### Scenario: 商品列表事件敏感信息过滤
- **WHEN** 系统记录商品列表行为事件
- **THEN** 事件 SHALL NOT 包含手机号、Authorization header、Cookie、raw payload、原始 object key、内部备注或不必要个人敏感信息。

