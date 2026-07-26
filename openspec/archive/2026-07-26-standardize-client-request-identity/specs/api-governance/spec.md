## ADDED Requirements

### Requirement: 请求身份 API 契约治理
API 治理 SHALL 记录跨端请求身份相关请求头、响应头、OpenAPI 和 Orval 同步要求。

#### Scenario: 请求头契约文档化
- **WHEN** 后端支持客户端类型和客户端请求标识请求头
- **THEN** API 文档 SHALL 记录 `x-client-type` 或等价字段的允许值
- **AND** API 文档 SHALL 记录客户端请求标识字段名、长度限制和安全边界
- **AND** API 文档 SHALL 明确客户端请求标识不会默认覆盖服务端可信 `request_id`。

#### Scenario: 响应头契约文档化
- **WHEN** 后端 API 返回可信 request id
- **THEN** OpenAPI、API 文档或等价契约说明 SHALL 记录 `x-request-id` 响应头
- **AND** 该响应头 SHALL 表示服务端可信 `request_id`。

#### Scenario: OpenAPI 与 Orval 同步
- **WHEN** 日志 API 新增请求身份字段、查询参数或响应头说明
- **THEN** OpenAPI SHALL 暴露对应 schema、parameters、headers 或 descriptions
- **AND** Orval SHALL 生成或更新 Web client types
- **AND** generated files SHALL NOT be hand-edited。

#### Scenario: 参数校验错误保持统一响应
- **WHEN** 客户端请求标识格式、长度或字符集非法且后端选择返回参数错误
- **THEN** 响应 SHALL 使用统一 `{ code, message, data }` 错误信封
- **AND** 错误详情 SHALL NOT 暴露 Authorization、Cookie、Token、密码、真实密钥、数据库 DSN、完整客户端请求标识原文或内部绝对路径。
