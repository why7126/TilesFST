# 产品使用行为日志规范

## Purpose
定义产品使用行为埋点、API 请求日志、日志存储、管理端日志审计查询与详情展示能力，确保排障、安全审计和产品行为分析有统一、可检索、可脱敏的事实来源。
## Requirements
### Requirement: API 请求日志采集
系统 SHALL 采集 API 请求日志摘要与统一 Request Snapshot，用于运维排障、审计链路关联和跨端请求上下文还原。

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

#### Scenario: 生成统一 Request Snapshot
- **WHEN** 可采集 API 请求完成
- **THEN** 系统 SHALL 为该请求生成统一 Request Snapshot
- **AND** Snapshot SHALL 至少包含 method、path、route template、query 白名单摘要、body schema 摘要、业务资源标识、status code、error code、duration、操作者、客户端、环境、请求开始时间和响应结束时间
- **AND** Snapshot SHALL 关联对应 request id。

#### Scenario: route template 获取与降级
- **WHEN** 系统采集 Request Snapshot 的路由上下文
- **THEN** Snapshot SHALL 同时记录实际 path 和 FastAPI route template 或等价路由模板
- **AND** 当 route template 无法稳定识别时，Snapshot SHALL 使用明确降级状态而不是使用带查询串的 path 冒充模板。

#### Scenario: query 和 body 摘要脱敏
- **WHEN** 系统采集 Request Snapshot 输入上下文
- **THEN** query 参数 SHALL 按后端白名单采集
- **AND** body SHALL 仅保存 schema 摘要、字段类型、字段数量、长度、业务安全字段或脱敏结果
- **AND** Snapshot SHALL NOT 保存 Authorization、Cookie、密码、Token、真实密钥、数据库 DSN、MinIO AccessKey、MinIO SecretKey、内部路径、原始文件名或原始敏感 body。

#### Scenario: 业务资源标识
- **WHEN** 请求可从 path、query、body 或业务上下文识别业务资源
- **THEN** Request Snapshot SHALL 记录 resource type 与 resource id 或等价 entity type 与 entity id
- **AND** 当资源无法可靠识别时，Snapshot SHALL 使用空值或未识别状态，不得凭不可靠字符串猜测。

#### Scenario: 跨端 Snapshot 字段兼容
- **WHEN** 请求来自后台管理端、店主 Web 展示端、微信小程序或后端内部客户端
- **THEN** Snapshot SHALL 使用兼容字段结构
- **AND** client type SHALL 能区分 `web_admin`、`web_catalog`、`miniapp`、`backend` 或后续明确终端
- **AND** 某终端无法提供的字段 SHALL 使用兼容空值。

### Requirement: 产品使用行为事件采集
系统 SHALL 按人工定义的事件字典采集产品使用行为事件。事件字典 SHALL 支持 Web 管理端既有事件，并 SHALL 支持微信小程序首页、首页样式信息架构优化、分类页、商品列表页、商品详情、搜索、收藏列表、品牌详情页、商品卡片组件和品牌卡片组件的详情访问、分享、咨询、快捷入口、瀑布流、搜索交互、收藏交互、品牌入口、卡片曝光、卡片点击和安全降级事件，用于小程序热销推荐统计、分类入口效果分析、搜索体验分析、收藏行为分析、品牌入口效果分析和后续产品优先级判断。

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

#### Scenario: 小程序收藏列表行为事件
- **WHEN** 微信小程序用户浏览收藏页、点击收藏项、取消收藏、点击空状态行动入口或收藏页加载失败
- **THEN** 系统 SHALL 接受已登记或等价预留的 `favorite_list_page_view`、`favorite_list_item_click`、`favorite_list_remove`、`favorite_list_empty_action_click` 和 `favorite_list_load_failed` 事件
- **AND** 事件 SHALL 仅携带 terminal、objectType、objectId、index、sourcePage、hasLogin、resultCount、requestId、client type 和必要页面上下文
- **AND** 事件 SHALL NOT 包含手机号、地址、客户姓名、Authorization header、Cookie、raw payload、raw object key、密钥、`.env` 内容或其它不必要个人敏感信息
- **AND** 埋点失败 SHALL NOT 阻断收藏页浏览、跳转或取消收藏主流程。

#### Scenario: 小程序品牌详情页行为事件
- **WHEN** 微信小程序用户浏览品牌详情页、切换 Tab、加载品牌商品、加载更多品牌商品、加载品牌证书、点击证书或发生对应加载失败
- **THEN** 系统 SHALL 接受已登记或等价预留的 `brand_detail_view`、`brand_detail_tab_click`、`brand_products_load`、`brand_products_load_more`、`brand_products_load_failed`、`brand_certificates_load`、`brand_certificates_load_failed` 和 `brand_certificate_click` 事件
- **AND** 事件 SHALL 仅携带 sourcePage、sourceModule、brandId、brandName、tab、page、pageSize、resultCount、index、requestId、client type 和必要页面上下文
- **AND** 事件 SHALL NOT 包含手机号、地址、客户姓名、Authorization header、Cookie、raw payload、raw object key、内部备注或其它不必要个人敏感信息
- **AND** 埋点失败 SHALL NOT 阻断品牌页加载、Tab 切换、商品跳转、证书预览或详情跳转。

#### Scenario: 小程序商品卡片组件行为事件
- **WHEN** 微信小程序商品卡片发生曝光、可用点击、不可用点击或图片加载失败
- **THEN** 系统 SHALL 接受已登记或等价预留的 `product_card_exposure`、`product_card_click`、`product_card_unavailable_click` 和 `product_card_image_failed` 事件
- **AND** 事件 SHALL 仅携带 skuId、skuCode、sourcePage、sourceModule、listContext、index、categoryId、brandId、keyword、requestId、client type 和必要上下文
- **AND** 事件 SHALL NOT 包含手机号、Authorization header、Cookie、raw payload、raw object key、内部备注或其它不必要个人敏感信息
- **AND** 埋点失败 SHALL NOT 阻断商品卡片展示或详情跳转。

#### Scenario: 小程序品牌卡片组件行为事件
- **WHEN** 微信小程序品牌卡片发生可用点击、不可用点击或图片加载失败
- **THEN** 系统 SHALL 接受已登记或等价预留的 `brand_card_click`、`brand_card_unavailable_click` 和 `brand_card_image_failed` 事件
- **AND** 事件 SHALL 仅携带 brandId、brandName、sourcePage、sourceModule、skuId、listContext、index、requestId、unavailableReason、client type 和必要上下文
- **AND** 事件 SHALL NOT 包含手机号、Authorization header、Cookie、raw payload、raw object key、内部备注或其它不必要个人敏感信息
- **AND** 埋点失败 SHALL NOT 阻断品牌卡片展示、品牌详情跳转或 fallback 跳转。

#### Scenario: 小程序事件字典防漂移
- **WHEN** 小程序新增或修改 `track()` 事件
- **THEN** 系统 SHALL 通过测试、静态校验或等价机制发现小程序事件名未在后端事件字典中登记的情况
- **AND** 对动态事件名调用点 SHALL 维护代表性样例并纳入测试
- **AND** 测试 SHALL 同时覆盖未知事件仍被拒绝和禁止字段仍被拒绝。

### Requirement: 日志存储与保留
系统 SHALL 将 request logs、Request Snapshot 与 usage events 存储在关系型存储中，并提供可查询索引和保留周期治理。

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

#### Scenario: Request Snapshot 存储兼容
- **WHEN** 系统持久化 Request Snapshot
- **THEN** Snapshot SHALL 存储为 JSON metadata 或等价结构化字段
- **AND** SQLite demo schema 与 MySQL production schema SHALL 保持兼容
- **AND** 实现阶段 SHALL 明确哪些 Snapshot 字段需要索引、冗余列或仅用于详情展示。

#### Scenario: Snapshot 存储失败不阻断主流程
- **WHEN** Request Snapshot 采集或持久化失败但主业务请求已经完成
- **THEN** 系统 SHALL NOT 因日志采集失败改变主业务响应结果
- **AND** 系统 SHALL 记录可观测错误摘要，且该摘要 SHALL NOT 暴露敏感信息。

### Requirement: 管理端日志查询 API
系统 SHALL 提供仅管理员可用的日志列表与详情查询 API，并在日志详情中返回统一 Request Snapshot。

#### Scenario: 管理员查询日志列表
- **WHEN** 已认证 admin 调用 `GET /api/v1/admin/logs`
- **THEN** 系统 SHALL 返回统一响应，包含分页日志项、total、page、page_size 和指标摘要。

#### Scenario: 支持日志列表筛选
- **WHEN** admin 按日志类型、时间范围、操作者、client type、status code 或 result、resource id、path、keyword、request id 或 task trace id 筛选
- **THEN** 系统 SHALL 仅返回匹配日志，并按最新优先排序。

#### Scenario: 操作者筛选保持 actor_user_id 语义
- **WHEN** admin 通过日志审计页面选择某个操作者候选后查询日志
- **THEN** 日志列表 API SHALL 使用该用户的稳定 `actor_user_id` 作为过滤条件
- **AND** API SHALL NOT 将用户显示名称、昵称或账号字符串解释为 `actor_user_id`
- **AND** API SHALL 保持既有 `actor_user_id` 查询参数兼容。

#### Scenario: 管理员查询日志详情
- **WHEN** 已认证 admin 针对已存在日志调用 `GET /api/v1/admin/logs/{id}`
- **THEN** 系统 SHALL 返回基础信息、请求信息、操作者与客户端、操作上下文、事件属性和 metadata 等详情分组。

#### Scenario: 日志详情返回 Request Snapshot
- **WHEN** 已认证 admin 查询包含 Request Snapshot 的请求日志详情
- **THEN** 日志详情 API SHALL 返回结构化 Request Snapshot
- **AND** Snapshot SHALL 包含请求信息、输入摘要、业务资源、响应结果、操作者与客户端、环境与时间分组或等价字段
- **AND** Snapshot 缺失字段 SHALL 使用空值、未采集状态或等价可展示表达。

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
- **AND** 页面 SHALL 展示日志类型、时间范围、状态或结果、操作者、Task Trace ID、路径 / Request ID 筛选。
- **AND** 时间范围 SHALL 提供最近5分钟、最近10分钟、最近30分钟、最近1小时、最近3小时、最近6小时、最近12小时、最近1天、最近2天、最近3天和最近7天，不提供全部时间选项。
- **AND** 状态或结果筛选 SHALL 使用下拉选择交互，支持成功、失败和常见 HTTP 状态码精确筛选，且 SHALL 至少包含 `422 参数校验错误`。

#### Scenario: 操作者筛选使用可搜索单选下拉

- **WHEN** admin 使用 `/admin/logs` 的操作者筛选项
- **THEN** 页面 SHALL 提供单选可搜索下拉，而不是要求 admin 直接输入 User ID
- **AND** 下拉 SHALL 支持按用户名称和账号搜索操作者候选
- **AND** 候选项 SHALL 只展示两行：第一行账号 `username`，第二行用户名称 `display_name || username`
- **AND** 候选项 SHALL 使用账号行区分同名用户。

#### Scenario: 操作者筛选查询日志

- **WHEN** admin 在操作者下拉中选择一个用户候选
- **THEN** 页面 SHALL 使用该用户的 `id` 作为 `actor_user_id` 请求日志列表
- **AND** 页面 SHALL NOT 将用户名称或账号字符串作为 `actor_user_id` 传给日志列表 API
- **AND** 筛选变化 SHALL 将当前页重置为 1 并重新查询。

#### Scenario: 操作者筛选清空与重置

- **WHEN** admin 清空操作者筛选或点击页面重置
- **THEN** 页面 SHALL 清除 `actor_user_id` 过滤条件
- **AND** 日志列表 SHALL 按全部操作者和其他默认筛选条件重新查询。

#### Scenario: 操作者候选异常状态

- **WHEN** 操作者候选正在加载、无匹配结果或加载失败
- **THEN** 页面 SHALL 在下拉或等价控件区域展示清晰状态
- **AND** 候选加载失败 SHALL NOT 阻止 admin 使用日志类型、时间范围、状态、Task Trace ID、路径 / Request ID 等其他筛选
- **AND** 候选加载失败反馈 SHALL 与日志列表查询失败反馈可区分。

#### Scenario: 日志表格支持排障

- **WHEN** admin 查看日志行
- **THEN** 表格 SHALL 展示时间、类型、事件或摘要、操作者账号、客户端、状态或结果、耗时、Task Trace、request id 和详情操作。
- **AND** 操作者列 SHALL 使用 `actor_username` 单行展示，不展示用户名称。
- **AND** Task Trace 与 request id 列 SHALL 均以单行短 ID 加复制操作展示。
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
- **AND** 前端测试 SHALL 覆盖列表渲染、筛选、操作者候选搜索、操作者选择、清空、重置、候选无结果、候选加载失败、同名用户区分、request_id 复制成功、Clipboard API 不可用兜底、复制写入失败兜底、详情抽屉、forbidden 状态和分页结构。

### Requirement: 日志详情抽屉
系统 SHALL 在右侧抽屉中展示日志详情和 Request Snapshot，且不丢失列表上下文。

#### Scenario: 打开详情抽屉
- **WHEN** admin 选择日志行详情操作
- **THEN** 页面 SHALL 打开右侧抽屉，并在抽屉背后保留可见列表上下文。

#### Scenario: 详情分组匹配原型
- **WHEN** 详情抽屉可见
- **THEN** 抽屉 SHALL 分组展示基础信息、请求信息、操作者与客户端、操作上下文、事件属性和 metadata JSON。

#### Scenario: Request Snapshot 结构化展示
- **WHEN** 详情抽屉展示包含 Request Snapshot 的日志
- **THEN** 抽屉 SHALL 结构化展示请求信息、输入摘要、业务资源、响应结果、操作者与客户端、环境与时间
- **AND** JSON 视图 SHALL 作为辅助查看方式，不得作为唯一展示方式
- **AND** 敏感字段被忽略或脱敏时 SHALL 展示脱敏状态摘要但不得展示敏感原文。

#### Scenario: Snapshot 空态与异常展示
- **WHEN** Snapshot 字段缺失、metadata 为空或 metadata JSON 解析失败
- **THEN** 日志详情抽屉 SHALL 继续展示核心日志字段
- **AND** 缺失 Snapshot 字段 SHALL 展示未采集、空值或等价空态
- **AND** 页面 SHALL NOT 崩溃。

#### Scenario: 关闭抽屉
- **WHEN** admin 点击关闭、点击遮罩或按下 Escape
- **THEN** 抽屉 SHALL 关闭，并保留当前筛选和分页状态。

#### Scenario: metadata 脱敏且可滚动
- **WHEN** 抽屉展示 metadata
- **THEN** metadata SHALL 使用等宽字体可滚动区域展示
- **AND** 敏感字段 SHALL 被脱敏或省略。

### Requirement: OpenAPI、Orval 与文档治理

系统 SHALL 保持产品使用日志相关 API、数据库、Request Snapshot、文档和生成客户端产物同步。

#### Scenario: 生成 API 契约
- **WHEN** 后端日志 API 被实现或变更
- **THEN** OpenAPI SHALL 暴露 response models、summaries、descriptions 和 tags
- **AND** Orval SHALL 生成对应 Web client methods。

#### Scenario: Request Snapshot 契约同步
- **WHEN** 日志详情 API 新增或修改 Request Snapshot 字段
- **THEN** OpenAPI SHALL 暴露 Snapshot response schema、字段说明、枚举值和空值语义
- **AND** Orval SHALL 生成或更新对应 Web client types
- **AND** generated files SHALL NOT be hand-edited。

#### Scenario: Task Trace 契约同步
- **WHEN** 日志列表、日志详情或上传响应新增 `task_trace_id`、任务摘要或任务时间线字段
- **THEN** OpenAPI SHALL 暴露这些字段
- **AND** Orval SHALL 生成或更新对应 Web client types
- **AND** generated files SHALL NOT be hand-edited。

#### Scenario: 文档保持同步
- **WHEN** 日志能力被实现
- **THEN** `docs/03-api-index.md`、`docs/04-database-design.md` 和适用的错误码文档 SHALL 描述新增 endpoints、schemas、tables 和 errors。

#### Scenario: Snapshot 文档保持同步
- **WHEN** Request Snapshot 被实现
- **THEN** `docs/03-api-index.md` SHALL 描述日志详情响应中的 Snapshot schema
- **AND** `docs/04-database-design.md` SHALL 描述 Snapshot 存储方式、索引或不索引字段理由
- **AND** 适用错误码文档 SHALL 描述新增或复用的错误码。

#### Scenario: 校验与测试覆盖能力
- **WHEN** 实现完成
- **THEN** 后端和前端测试 SHALL 覆盖新增或修改的日志 API、任务时间线字段、权限、脱敏、筛选和错误场景。

#### Scenario: Snapshot 测试覆盖能力
- **WHEN** Request Snapshot 实现完成
- **THEN** 后端测试 SHALL 覆盖 route template 获取与降级、query 白名单、body schema 摘要、敏感字段不落库、错误请求上下文、SQLite/MySQL schema 兼容和日志采集失败不阻断主流程
- **AND** 前端测试 SHALL 覆盖 Snapshot 分组展示、JSON 辅助视图、空态、metadata 解析失败、权限边界和详情抽屉可滚动可关闭。

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

### Requirement: 任务链路追踪

系统 SHALL 为可追踪业务任务提供 Task Trace 模型，支持任务标识、任务节点、状态、耗时、错误码、资源关联、安全脱敏，并覆盖上传之外的长耗时、多步骤、跨服务、异步、批量、媒体处理、复杂保存和复杂查询类任务型业务接口。

#### Scenario: 生成任务追踪标识
- **WHEN** 用户发起需要追踪的业务任务
- **THEN** 系统 SHALL 生成或确认 `task_trace_id`
- **AND** `task_trace_id` SHALL NOT 包含用户原始文件名、手机号、密钥、业务敏感信息或可枚举自增序列。

#### Scenario: 记录任务节点
- **WHEN** 任务进入关键处理节点
- **THEN** 系统 SHALL 记录 task span
- **AND** span SHALL 至少包含 `task_trace_id`、`task_type`、`span_name`、`status`、开始时间和耗时或结束时间。

#### Scenario: 任务状态可推导
- **WHEN** 任务结束、失败、超时、取消或批量任务部分成功
- **THEN** 系统 SHALL 将任务状态标记为 `success`、`failed`、`timeout`、`cancelled` 或 `partial_success`
- **AND** 进行中的任务 SHALL 可标记为 `processing`。

#### Scenario: 任务节点关联请求
- **WHEN** task span 发生在某个 HTTP 请求生命周期中
- **THEN** span SHALL 关联对应 `request_id`
- **AND** 同一 `task_trace_id` MAY 关联多个 request id。

#### Scenario: 子请求和异步任务继承任务上下文
- **WHEN** 一个用户操作触发子请求、后台 worker 或异步任务
- **THEN** 子请求、后台 worker 或异步任务 SHALL 继承原始用户操作的 `task_trace_id`
- **AND** 无法继承时 SHALL 记录降级 span 或明确的关联缺失原因。

#### Scenario: 任务失败可诊断
- **WHEN** 任务节点失败
- **THEN** span SHALL 记录统一错误码或失败摘要
- **AND** SHALL NOT 暴露 Authorization、Cookie、AccessKey、SecretKey、数据库 DSN、`.env` 内容、真实客户数据、内部绝对路径或完整敏感请求体。

#### Scenario: 批量任务部分成功可诊断
- **WHEN** 批量任务出现部分成功
- **THEN** 系统 SHALL 记录成功数、失败数和失败分类摘要
- **AND** 任务最终状态 SHALL 可表达为 `partial_success` 或等价可查询状态。

#### Scenario: 任务追踪持久化可查询
- **WHEN** 系统持久化 task trace 或 task span
- **THEN** 持久化结构 SHALL 支持按 `task_trace_id`、`task_type` 和创建时间查询
- **AND** SQLite demo 与 MySQL production SHALL 使用兼容 schema。

### Requirement: 客户端请求身份标准
系统 SHALL 在 API 请求日志与 usage events 中统一记录客户端类型、后端可信 `request_id` 与客户端请求标识，并保持三者语义边界清晰。

#### Scenario: 后端生成可信 request_id 并返回响应头
- **WHEN** 任一受日志采集覆盖的 API 请求进入后端
- **THEN** 系统 SHALL 为该请求生成服务端可信 `request_id`
- **AND** 响应 SHALL 通过 `x-request-id` 或等价文档化响应头返回该可信 `request_id`
- **AND** 请求日志、错误响应上下文和异常日志 SHALL 使用同一个可信 `request_id`。

#### Scenario: 客户端请求标识独立保存
- **WHEN** 客户端通过 `x-client-request-id`、请求体 `client_request_id` 或文档化等价字段传入客户端请求标识
- **THEN** 系统 SHALL 将其保存为独立 `client_request_id` 或等价字段
- **AND** 系统 SHALL NOT 默认使用客户端传入值覆盖服务端可信 `request_id`
- **AND** 日志详情 SHALL 能区分后端可信 `request_id` 与客户端请求标识。

#### Scenario: 客户端请求标识校验
- **WHEN** 客户端请求标识缺失、超长、包含控制字符或格式非法
- **THEN** 系统 SHALL 忽略、截断或按文档化策略降级该客户端请求标识
- **AND** 系统 SHALL 继续生成服务端可信 `request_id`
- **AND** 系统 SHALL NOT 因客户端请求标识非法返回 500 或写入不可解析 metadata。

#### Scenario: 客户端类型枚举归一
- **WHEN** Web 管理端、店主 Web 前台或微信小程序发起普通 API 请求
- **THEN** 请求日志 SHALL 分别记录 `web_admin`、`web_catalog` 或 `wechat_miniapp`
- **AND** usage events SHALL 使用同一客户端类型枚举
- **AND** 客户端类型 SHALL NOT 作为认证授权依据。

### Requirement: 客户端请求身份日志审计展示
系统 SHALL 在日志审计能力中展示客户端请求身份信息，支持排障而不泄露敏感字段。

#### Scenario: 日志列表展示请求身份摘要
- **WHEN** admin 查看 `/admin/logs` 日志列表
- **THEN** 表格 SHALL 展示客户端类型和后端可信 `request_id`
- **AND** 表格 MAY 展示短格式客户端请求标识
- **AND** 长 ID SHALL 截断展示，完整值 SHALL 可通过复制、详情抽屉或等价方式获取。

#### Scenario: 日志详情展示两类请求 ID
- **WHEN** admin 打开日志详情抽屉
- **THEN** 详情 SHALL 展示后端可信 `request_id`
- **AND** 详情 SHALL 展示客户端请求标识，若不存在则展示空值或等价缺省状态
- **AND** 字段命名或说明 SHALL 避免将客户端请求标识误读为服务端可信链路 ID。

#### Scenario: 客户端请求标识筛选策略
- **WHEN** 日志审计实现 `client_request_id` 筛选
- **THEN** 日志查询 API SHALL 使用索引或等价优化过滤该字段
- **AND** OpenAPI、Orval 和文档 SHALL 同步该查询参数
- **AND** 若本期不实现筛选，design 或验收记录 SHALL 明确说明原因。

#### Scenario: 敏感字段不进入日志身份字段
- **WHEN** 系统记录请求身份相关日志或 usage events
- **THEN** 系统 SHALL NOT 存储 Authorization Header、Cookie、Token、密码、真实密钥、MinIO AccessKey/SecretKey、数据库 DSN、完整敏感请求体或 `.env` 内容
- **AND** 前端脱敏 SHALL NOT 被视为安全边界。

### Requirement: 请求身份测试与文档同步
系统 SHALL 为客户端请求身份补充后端、Web、小程序、API 契约、数据库和文档同步验证。

#### Scenario: 后端请求日志测试覆盖
- **WHEN** 后端测试运行
- **THEN** 测试 SHALL 覆盖 `web_admin`、`web_catalog`、`wechat_miniapp` 三类客户端类型解析
- **AND** 测试 SHALL 覆盖客户端请求标识缺失、非法、超长时仍生成可信 `request_id` 并返回响应头。

#### Scenario: 数据库与文档同步
- **WHEN** 实现新增 `client_request_id` 或等价持久化字段
- **THEN** SQLite schema、MySQL schema、迁移、索引和数据库文档 SHALL 同步更新
- **AND** MySQL drift 测试或等价校验 SHALL 覆盖该字段。

#### Scenario: 日志 API 契约同步
- **WHEN** 日志列表或详情 API 新增请求身份字段或筛选参数
- **THEN** OpenAPI SHALL 暴露对应请求、响应和响应头契约
- **AND** Orval SHALL 生成对应 Web client types
- **AND** generated files SHALL NOT be hand-edited。

### Requirement: 任务型接口 Task Trace 覆盖策略

系统 SHALL 定义任务型接口判定标准，并为首批接入 Task Trace 的业务接口输出可执行清单。

#### Scenario: 生成首批任务型接口清单
- **WHEN** 实现 REQ-0074
- **THEN** 系统 SHALL 输出首批 Task Trace 接入接口清单
- **AND** 清单 SHALL 至少评估保存 SKU、批量操作、导入导出、媒体处理、异步任务和复杂查询六类场景。

#### Scenario: 首批清单包含接入信息
- **WHEN** 某个候选接口被列入首批清单
- **THEN** 清单 SHALL 标注任务类型、接入优先级、关键步骤、预期 span、是否异步、是否批量、是否涉及对象存储或外部依赖。

#### Scenario: 未纳入首批的候选接口有后续排期
- **WHEN** 候选接口未纳入首批接入范围
- **THEN** 清单 SHALL 记录未接入原因和后续排期建议。

#### Scenario: 同步任务记录关键步骤
- **WHEN** 同步任务型接口被接入 Task Trace
- **THEN** 系统 SHALL 至少记录请求接收、输入校验、业务处理、持久化或外部调用、响应或任务结束 span。

#### Scenario: 异步任务记录关键步骤
- **WHEN** 异步任务型接口被接入 Task Trace
- **THEN** 系统 SHALL 至少记录 `async_dispatch`、`worker_start`、`worker_process`、`worker_persist_result`、`worker_finished` 或 `worker_failed` 等等价 span。

#### Scenario: 批量任务记录关键步骤
- **WHEN** 批量任务型接口被接入 Task Trace
- **THEN** 系统 SHALL 至少记录批量解析、批量校验、单项处理、成功 / 失败计数、失败分类摘要和最终结果 span。

#### Scenario: Task Trace helper 封装接入
- **WHEN** 业务服务写入任务 span
- **THEN** 系统 SHALL 通过 Task Trace helper、service 或等价封装生成、透传、绑定上下文和写入 span
- **AND** 路由层 SHALL NOT 直接拼 SQL 或直接持久化 task span。

### Requirement: 管理端复杂任务追踪反馈

系统 SHALL 在管理端复杂任务成功、失败、处理中或部分成功反馈中展示或提供可复制的 `task_trace_id`，并允许管理员进入日志审计查看任务时间线。

#### Scenario: 复杂任务反馈展示追踪标识
- **WHEN** 管理端复杂任务返回 `task_trace_id`
- **THEN** 页面 SHALL 在任务反馈区域展示该追踪标识或复制入口
- **AND** 展示 SHALL 不挤占主要业务表单区域。

#### Scenario: 复制追踪标识不造成布局位移
- **WHEN** 管理员复制 `task_trace_id`
- **THEN** 页面 SHALL 使用 fixed toast 或等价固定层展示成功、失败或兜底反馈
- **AND** 反馈 SHALL NOT 造成页面布局位移。

#### Scenario: 无追踪标识保持兼容
- **WHEN** 复杂任务响应中没有 `task_trace_id`
- **THEN** 页面 SHALL 保持原有交互
- **AND** SHALL NOT 显示空追踪组件或空错误态。

#### Scenario: 失败摘要安全展示
- **WHEN** 管理端展示复杂任务失败反馈
- **THEN** 页面 SHALL 只展示安全错误码、脱敏摘要和可复制追踪标识
- **AND** SHALL NOT 展示内部路径、堆栈、原始请求体或敏感 metadata。

#### Scenario: 日志审计入口可达
- **WHEN** 管理员从复杂任务反馈进入日志审计
- **THEN** 日志审计 SHALL 可按 `task_trace_id` 查询或展示同一任务的时间线。

### Requirement: 管理端链路观测聚合 API

系统 SHALL 提供仅管理员可用的链路观测聚合查询能力，用于按同一筛选口径返回请求日志、行为事件、审计操作和 Task Trace 的摘要、分布、排行与追踪结果。

#### Scenario: 管理员查询链路观测摘要
- **WHEN** 已认证 admin 使用时间范围、日志类型、客户端、任务类型、接口路径、状态或结果筛选链路观测数据
- **THEN** 系统 SHALL 返回统一响应 envelope
- **AND** 响应 SHALL 包含总日志量、API 错误数、API 错误率、慢请求数、任务成功率、慢任务数和审计操作数
- **AND** 所有摘要指标 SHALL 与同一组筛选条件保持一致。

#### Scenario: 返回 Task Trace 观测指标
- **WHEN** admin 查询链路观测数据且存在 Task Trace 数据
- **THEN** 系统 SHALL 返回任务状态分布、任务成功率、失败任务数量和任务耗时分布或等价分桶
- **AND** SHALL 返回慢任务排行，包含任务类型、耗时、状态、触发来源和 `task_trace_id`
- **AND** SHALL 返回最慢 span 排行，包含 span 名称、任务类型、耗时、结果和关联 `task_trace_id`。

#### Scenario: 返回请求与接口错误观测指标
- **WHEN** admin 查询链路观测数据且存在请求日志
- **THEN** 系统 SHALL 按接口路径、方法和状态码统计请求量、错误量和错误率
- **AND** SHALL 返回慢请求排行，包含路径、方法、状态码、耗时、客户端和 `request_id`
- **AND** SHALL 返回失败原因分布，优先使用错误码、异常摘要或业务失败原因。

#### Scenario: 返回客户端与行为分布
- **WHEN** admin 查询链路观测数据且存在行为事件或请求来源
- **THEN** 系统 SHALL 返回客户端分布，覆盖 `web_admin`、`web_catalog`、`miniapp`、`backend` 和未识别客户端
- **AND** 系统 SHALL 返回行为事件分布，包含事件类型、模块、结果和失败原因。

#### Scenario: 追踪 ID 精确查询
- **WHEN** admin 使用 `request_id` 或 `task_trace_id` 精确查询链路观测数据
- **THEN** 系统 SHALL 返回对应日志详情、Task Trace 时间线或相关记录集合所需的跳转 ID
- **AND** 未命中时 SHALL 返回空集合和可识别空态原因，而不是系统错误。

#### Scenario: 聚合查询权限与脱敏
- **WHEN** employee、店主端客户端、小程序用户或匿名用户调用链路观测聚合接口
- **THEN** 系统 SHALL 使用已文档化的 forbidden 响应拒绝访问
- **AND** 响应 SHALL NOT 暴露 Authorization、Cookie、Token、密码、真实密钥、数据库 DSN、`.env` 内容、真实客户数据、内部绝对路径、完整请求体或完整响应体。

#### Scenario: 聚合查询性能边界
- **WHEN** 系统计算链路观测摘要、分布或排行
- **THEN** 系统 SHALL 使用 Repository 或统一数据访问层执行数据库聚合、索引查询或分页 Top N 查询
- **AND** SHALL NOT 在过滤前将全部日志、行为事件、审计操作或 Task Trace 记录加载到内存
- **AND** SQLite demo 与 MySQL production SHALL 使用兼容查询和 schema。

### Requirement: 链路观测契约同步

系统 SHALL 在实现链路观测聚合 API 时同步维护 API、OpenAPI、Orval、文档、错误码、数据库说明和测试契约。

#### Scenario: OpenAPI 与 Orval 同步
- **WHEN** 新增或修改管理端链路观测聚合 API、响应 Schema 或查询参数
- **THEN** OpenAPI SHALL 暴露 response models、summaries、descriptions 和 tags
- **AND** Orval SHALL 生成对应 Web client methods 和 types
- **AND** generated files SHALL NOT be hand-edited。

#### Scenario: API 与数据库文档同步
- **WHEN** 链路观测实现新增 endpoint、schema、索引、聚合字段或错误码
- **THEN** `docs/03-api-index.md`、`docs/04-database-design.md` 和适用的错误码文档 SHALL 描述新增 endpoints、schemas、tables、indexes 和 errors。

#### Scenario: 测试覆盖
- **WHEN** 链路观测聚合 API 实现完成
- **THEN** 后端测试 SHALL 覆盖聚合摘要、筛选、权限、脱敏、空数据、追踪 ID 命中 / 未命中、SQLite 和 MySQL 兼容口径
- **AND** 若 Web 管理端页面消费该聚合接口，前端测试 SHALL 覆盖页面渲染、筛选刷新、排行下钻、复制反馈、加载失败、无权限、空态、分页结构、fixed toast 和移动端 smoke。

### Requirement: 审计日志任务链路关联

系统 SHALL 让审计操作日志支持可选 Task Trace 关联，使敏感操作可从 audit log 串联到主请求、任务节点和日志审计详情。

#### Scenario: 审计写入接口接收任务上下文
- **WHEN** 后端服务调用 `AuditLogRepository.insert()` 或等价审计写入入口并提供合法 `task_trace_id` 与 `task_type`
- **THEN** 系统 SHALL 将 `task_trace_id` 与 `task_type` 持久化到 `audit_logs`
- **AND** 审计基础字段、操作者、资源、动作、结果和脱敏 metadata SHALL 保持原有写入语义。

#### Scenario: 无任务上下文保持兼容
- **WHEN** 审计操作没有任务上下文或调用方未提供 `task_trace_id`
- **THEN** 系统 SHALL 正常写入审计日志
- **AND** `task_trace_id` 与 `task_type` SHALL 为空
- **AND** 日志列表、详情和权限行为 SHALL NOT 回归。

#### Scenario: 首批敏感操作清单
- **WHEN** 实现 REQ-0075
- **THEN** 系统 SHALL 梳理并记录首批审计写入点接入清单
- **AND** 清单 SHALL 至少评估系统设置、品牌证书、媒体或上传、SKU、Banner 等管理端敏感操作。

#### Scenario: 任务型审计操作复用任务标识
- **WHEN** 敏感操作发生在已有 Task Trace 上下文中
- **THEN** 审计日志 SHALL 复用当前请求或任务上下文中的 `task_trace_id`
- **AND** 同一业务任务触发的多条审计日志 SHALL 可通过同一个 `task_trace_id` 关联。

#### Scenario: 审计日志任务查询使用结构化字段
- **WHEN** admin 使用 `task_trace_id` 查询 audit 类型日志
- **THEN** 系统 SHALL 使用结构化字段和索引友好条件查询
- **AND** 系统 SHALL NOT 以 metadata 无界模糊扫描作为主查询路径。

#### Scenario: audit 类型日志详情展示任务链路
- **WHEN** admin 打开一条存在 `task_trace_id` 的 audit 类型日志详情
- **THEN** 日志详情 SHALL 展示 Task Trace 分组或等价任务链路入口
- **AND** 分组 SHALL 包含 `task_trace_id`、`task_type`、任务状态、关键节点摘要或任务时间线。

#### Scenario: 任务字段不参与权限判断
- **WHEN** 前端或客户端提交 `task_trace_id`、`task_type` 或资源相关字段
- **THEN** 系统 SHALL NOT 将这些字段作为权限判断依据
- **AND** 权限判断 SHALL 继续基于认证上下文、角色和服务端资源校验。

#### Scenario: 审计 metadata 安全脱敏
- **WHEN** 系统写入或展示带 Task Trace 的 audit log metadata
- **THEN** metadata SHALL 过滤 Authorization、Cookie、Token、密码、AccessKey、SecretKey、数据库 DSN、`.env` 内容、内部绝对路径和真实客户数据
- **AND** 审计写入失败或 Task Trace 关联失败 SHALL NOT 泄露内部路径、堆栈、对象存储凭证或未脱敏 metadata。

#### Scenario: 审计字段 schema 一致
- **WHEN** 实现或验证审计日志任务链路关联
- **THEN** SQLite demo 与 MySQL production 的 `audit_logs` SHALL 均包含兼容的 `task_trace_id` 与 `task_type` 字段
- **AND** 若 schema 或索引不一致，系统 SHALL 同步 schema、migration、数据库文档和测试。

#### Scenario: 契约与生成物同步
- **WHEN** 日志列表或详情 API 为 audit 类型日志新增或确认任务摘要字段
- **THEN** OpenAPI SHALL 暴露相关字段
- **AND** Orval SHALL 生成或更新对应 Web client types
- **AND** generated files SHALL NOT be hand-edited。

### Requirement: 审计日志任务链路管理端横切验收

系统 SHALL 在管理端日志审计页面实现 audit log Task Trace 展示时遵守管理端列表页一致性与 REQ-0075 原型策略。

#### Scenario: 分页 DOM 对齐管理端基准
- **WHEN** 日志审计列表新增或调整 `task_trace_id` 展示、筛选或复制能力
- **THEN** 分页 DOM SHALL 对齐用户管理基准
- **AND** 左侧 SHALL 使用 `.page-summary`
- **AND** 右侧 SHALL 使用 `.page-right` 页码与每页条数组合。

#### Scenario: 指标卡 DOM 保持一致
- **WHEN** 日志审计指标摘要因任务链路新增或调整
- **THEN** 指标卡 SHALL 使用 `.metric-label`、`.metric-value`、`.metric-desc` 结构
- **AND** SHALL NOT 仅复用外层卡片后用裸 `strong` 或 `span` 承载数值与说明。

#### Scenario: 复制和查询反馈不造成布局位移
- **WHEN** admin 查询、复制 `task_trace_id` 或打开日志详情
- **THEN** 成功、失败或兜底反馈 SHALL 使用 fixed toast 或等价固定层
- **AND** 页面头部、筛选区、指标区和表格 SHALL NOT 因反馈产生纵向位移。

#### Scenario: 不使用 window confirm
- **WHEN** 实现日志审计列表和详情中的 Task Trace 操作
- **THEN** Web client SHALL NOT 调用 `window.confirm`
- **AND** 若后续新增清理、删除、导出等危险操作，系统 SHALL 使用 Design System confirm modal。

#### Scenario: 日志页 smoke 覆盖任务分组
- **WHEN** 实现完成
- **THEN** Web 测试或 smoke SHALL 覆盖 1440x1024 与移动端管理端视口下的分页、筛选、复制反馈和详情抽屉 Task Trace 分组
- **AND** UI SHALL 使用 Design System semantic token。

### Requirement: Task Trace 主请求关联模型
系统 SHALL 为 Task Trace 建立主请求、子请求与 span 的强关联模型，确保任务链路可以从主请求进入 Task Trace，也可以从 Task Trace span 回到对应请求日志。

#### Scenario: Task Trace 记录触发主请求
- **WHEN** API 请求触发一个 Task Trace
- **THEN** 系统 SHALL 记录触发该 Task Trace 的主请求 `request_id`
- **AND** 该字段语义 SHALL 为 `parent_request_id`
- **AND** `parent_request_id` SHALL 来自后端请求上下文，不得信任前端传入值。

#### Scenario: parent_request_id 存储可查询
- **WHEN** 系统持久化 Task Trace 任务摘要
- **THEN** 系统 SHALL 使用独立字段或等价结构化字段保存 `parent_request_id`
- **AND** OpenSpec design SHALL 说明采用独立字段还是 metadata 结构化字段
- **AND** 查询路径 SHALL 索引友好，不得以无界 metadata 模糊扫描作为主查询方式。

#### Scenario: 一个主请求触发多个 Task Trace
- **WHEN** 一个主请求触发多个 Task Trace
- **THEN** 系统 SHALL 保留一对多关联
- **AND** 管理端日志详情 SHALL 能区分多个任务摘要。

#### Scenario: span 写入当前 request_id
- **WHEN** task span 发生在某个 HTTP 请求生命周期中
- **THEN** span SHALL 写入当前请求的 `request_id`
- **AND** 同一 `task_trace_id` SHALL 能关联多个 request id。

#### Scenario: 内部 span 缺少请求上下文
- **WHEN** task span 是无直接 HTTP 请求上下文的后端内部节点
- **THEN** span SHALL 保留 `task_trace_id`、span 顺序、状态和耗时
- **AND** span MAY 继承 `parent_request_id` 或将 `request_id` 标为空
- **AND** API 和页面 SHALL 不展示误导性请求跳转。

#### Scenario: 任务型接口统一透传 task_trace_id
- **WHEN** 任务型接口创建、处理或上报任务节点
- **THEN** request logs、usage events、audit logs、Task Trace 和 task spans SHALL 使用同一个 `task_trace_id` 串联
- **AND** 后端 SHALL 校验前端携带的 `task_trace_id` 格式、权限边界和任务归属。

#### Scenario: 缺失或非法 task_trace_id 不破坏请求日志
- **WHEN** 任务型接口收到缺失或非法 `task_trace_id`
- **THEN** 主请求日志 SHALL 仍然落库
- **AND** 系统 SHALL 返回或记录明确的可观测错误摘要。

#### Scenario: 日志详情支持双向定位
- **WHEN** admin 查看带有 `request_id` 或 `task_trace_id` 的日志详情
- **THEN** 日志详情 SHALL 能从主请求 `request_id` 展示关联 Task Trace 摘要或入口
- **AND** Task Trace 时间线 SHALL 展示 span 关联的 `request_id`
- **AND** admin SHALL 能从 span 的 `request_id` 定位到对应请求日志详情。

#### Scenario: 历史缺失字段安全兜底
- **WHEN** 历史日志缺少 `task_trace_id`、Task Trace 缺少 `parent_request_id` 或 span 缺少 `request_id`
- **THEN** API 和页面 SHALL 安全兜底
- **AND** SHALL NOT 展示空状态错误或误导性关联。

#### Scenario: 上传首批验证主请求关联
- **WHEN** admin 上传图片、视频或文件
- **THEN** 上传主请求 SHALL 生成或绑定 `task_trace_id`
- **AND** Task Trace SHALL 记录上传主请求的 `request_id` 为 `parent_request_id`
- **AND** 上传相关 span SHALL 至少覆盖后端接收、文件校验、对象存储写入、数据库落库和响应返回节点
- **AND** 有请求上下文的上传 span SHALL 写入当前 API 请求的 `request_id`。

#### Scenario: 追踪字段不作为权限依据
- **WHEN** 系统使用 `request_id`、`parent_request_id` 或 `task_trace_id` 定位日志或任务
- **THEN** 这些字段 SHALL 仅用于追踪与定位
- **AND** SHALL NOT 作为权限判断依据
- **AND** 任务链路查询 SHALL 仅系统管理员可访问。

#### Scenario: 追踪数据保持安全脱敏
- **WHEN** 系统记录 Task Trace、span 或关联日志 metadata
- **THEN** 系统 SHALL NOT 存储 Authorization、Cookie、AccessKey、SecretKey、数据库 DSN、`.env` 内容、真实客户数据、内部绝对路径或完整敏感请求体。

#### Scenario: 契约与生成物同步
- **WHEN** 日志详情、任务追踪 API、上传响应或数据模型新增 `parent_request_id`、span `request_id` 或任务摘要字段
- **THEN** OpenAPI SHALL 暴露这些字段
- **AND** Orval SHALL 生成或更新对应 Web client types
- **AND** generated files SHALL NOT be hand-edited
- **AND** `docs/03-api-index.md`、`docs/04-database-design.md` 和适用错误码文档 SHALL 同步更新。

#### Scenario: media-upload 横切验收
- **WHEN** 实现涉及图片、视频或文件上传链路
- **THEN** 上传控件 SHALL 保持 `idle → uploading → done / failed` 状态机
- **AND** 上传成功后同会话 SHALL 即时回显媒体结果
- **AND** 上传失败 SHALL 在控件内展示错误，不能只依赖全局 toast
- **AND** Docker Web 入口 `http://localhost:3000` SHALL 覆盖小文件成功和超限文件统一错误码验收
- **AND** 上传链路 SHALL 继续走后端鉴权和对象存储适配层，不得前端直连未授权对象存储或写入 legacy `data/uploads/`。

