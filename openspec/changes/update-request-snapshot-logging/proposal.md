## Why

当前 API 请求日志已记录 request_id、method、path、状态码、耗时、操作者和客户端等摘要字段，但 metadata 主要停留在 query/path 摘要，无法稳定还原一次业务请求的输入上下文。REQ-0071 要求建立统一 Request Snapshot，在不保存原始敏感 body 的前提下，为前台 Web、后台管理端与微信小程序请求提供一致、可审计、可排障的请求快照。

## What Changes

- 为 API 请求日志新增统一 Request Snapshot 契约，覆盖请求信息、输入摘要、业务资源、响应结果、操作者 / 客户端、环境与时间。
- 扩展请求日志采集要求，补齐 route template、query 白名单摘要、body schema 摘要、资源 ID、error code、请求开始时间和响应结束时间。
- 明确 query/body 白名单、敏感字段黑名单、脱敏、截断和后端安全边界，禁止保存 Authorization、Cookie、密码、Token、真实密钥、数据库 DSN、MinIO AccessKey/SecretKey、内部路径、原始文件名和原始敏感 body。
- 扩展管理端日志详情抽屉，按结构化分组展示 Request Snapshot，并在字段缺失或 metadata 异常时保持基础日志信息可见。
- 要求实现阶段同步 SQLite / MySQL schema、Pydantic Schema、日志 API 响应、OpenAPI / Orval、API/数据库文档和测试。
- 不接入外部 APM、链路追踪平台、日志全文检索、历史日志回填或运维级日志统一采集。

## Capabilities

### New Capabilities

- 无。

### Modified Capabilities

- `product-usage-logging`: 增强 API 请求日志采集、日志存储与保留、管理端日志查询 API、日志详情抽屉、OpenAPI / Orval 与文档治理要求，以支持统一 Request Snapshot。

## Impact

- 后端：请求日志 middleware、日志服务、日志仓储、请求脱敏策略、错误上下文摘要。
- API：管理端日志详情响应需要暴露 Request Snapshot 结构；如新增字段必须同步 OpenAPI 与 Orval。
- 数据库：可能扩展 `request_logs.metadata` 结构或新增结构化字段；需同步 SQLite demo schema 与 MySQL production schema。
- Web 管理端：日志详情抽屉需展示 Snapshot 分组和结构化 JSON / 字段视图。
- 小程序 / 店主 Web：请求来源和 client type 需与统一 Snapshot 字段兼容。
- 安全：以后端白名单、敏感字段黑名单、脱敏和截断作为最终安全边界。
- 测试：需覆盖敏感字段不落库、错误请求可排障、跨端字段兼容、日志详情空态、权限和分页性能边界。
