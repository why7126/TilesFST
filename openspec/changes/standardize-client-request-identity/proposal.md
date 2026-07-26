## Why

当前产品使用日志已经记录 `request_id` 与 `client_type`，但 Web 管理端、店主 Web 前台和微信小程序普通 API 请求尚未统一携带客户端类型与客户端请求标识，导致请求日志和行为事件之间的跨端归因不稳定。需要在既有日志审计能力上补齐客户端请求身份规范，明确后端可信 `request_id` 与客户端生成标识的边界。

## What Changes

- 统一客户端类型枚举与请求头约定，覆盖 `web_admin`、`web_catalog`、`wechat_miniapp`。
- 后端继续生成可信 `request_id` 并通过响应头返回，同时将客户端请求标识保存为独立 `client_request_id` 或等价字段，不默认覆盖服务端可信 ID。
- Web 管理端、店主 Web 前台和微信小程序统一请求封装注入客户端类型与客户端请求标识。
- 日志审计列表和详情展示后端可信 `request_id`、客户端请求标识和客户端类型，并保持复制交互、分页 DOM、fixed toast 与既有管理端列表规范一致。
- 行为事件可携带相关请求标识，用于从用户行为追溯到业务请求；上报失败不阻断主流程。
- 同步 OpenAPI / Orval / API 文档 / 数据库文档 / 测试，覆盖新增或变更的请求头、响应头、日志字段、筛选能力和错误场景。
- 不引入外部分布式链路追踪平台，不保存敏感 Header、Cookie、Token、密码、密钥或完整敏感请求体。

## Capabilities

### New Capabilities

- 无。

### Modified Capabilities

- `product-usage-logging`: 补充客户端请求身份、客户端请求标识存储、日志审计展示与测试契约。
- `web-client`: 补充 Web 管理端和店主 Web 前台请求封装、日志审计字段展示、复制反馈和管理端列表横切约束。
- `api-governance`: 补充跨端请求头、响应头和生成客户端同步治理要求。

## Impact

- 后端：请求日志 middleware、日志 schema / repository / service、usage event 上下文、日志查询 API。
- Web 管理端：Axios 或等价 API client、`/admin/logs` 列表与详情抽屉、复制交互、Vitest 覆盖。
- 店主 Web 前台：公开 API client 请求头注入和 smoke / 测试覆盖。
- 微信小程序：统一 request 封装、普通 API 请求客户端类型注入、fallback base URL 重试标识策略。
- API / Orval：如新增请求头、响应头、日志字段或筛选参数，需要同步 OpenAPI 与生成客户端。
- 数据库：如新增 `client_request_id` 字段或索引，需要同步 SQLite/MySQL schema、迁移与数据库文档。
- 文档与测试：同步 `docs/03-api-index.md`、`docs/04-database-design.md`、API governance / error code 文档和后端、前端、小程序测试。
