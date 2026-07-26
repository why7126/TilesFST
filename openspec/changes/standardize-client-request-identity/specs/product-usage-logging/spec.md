## ADDED Requirements

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
