## MODIFIED Requirements

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
