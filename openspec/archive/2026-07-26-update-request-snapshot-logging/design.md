## Context

REQ-0071 已评审通过，要求在既有 `product-usage-logging` 能力上增强 API 请求日志。当前正式 spec 已覆盖 request_id、method、path、status code、duration、client type、操作者上下文、metadata、管理端日志 API 与详情抽屉，但 metadata 仍偏摘要化，不能稳定表达 route template、query 白名单、body schema 摘要、业务资源 ID、环境、请求开始/结束时间和脱敏状态。

该变更涉及后端请求日志 middleware、日志服务、日志仓储、SQLite/MySQL schema、Pydantic Schema、管理端日志详情 API、Web 管理端日志详情抽屉、OpenAPI / Orval 与测试治理。REQ 提供了低保真 HTML 原型：`issues/requirements/archive/REQ-0071-request-snapshot-logging/prototype/web/request-snapshot-log-detail.html`。

## Goals / Non-Goals

**Goals:**

- 定义统一 Request Snapshot 字段契约，并作为请求日志 metadata 或结构化字段的一部分持久化。
- 在请求日志采集链路中补齐 route template、query 白名单摘要、body schema 摘要、资源标识、响应结果、操作者、客户端、环境与时间信息。
- 以后端白名单、敏感字段黑名单、脱敏和截断策略作为最终安全边界。
- 扩展管理端日志详情 API 与抽屉展示，让管理员无需从多个字段拼接排障上下文。
- 同步 API、数据库、OpenAPI / Orval、文档和测试要求。

**Non-Goals:**

- 不保存完整原始请求体、完整响应体或未脱敏 Header。
- 不引入外部 APM、链路追踪平台、消息队列或日志全文检索。
- 不对历史日志做批量回填。
- 不统一接入 Nginx access log、容器 stdout、数据库慢查询等运维级日志。
- 不把前端脱敏作为安全边界。

## Decisions

### D1. UI 策略：DS 结构化增强

采用 Design System 结构化增强，而非 CSS Port。低保真 HTML 原型只表达信息分组，不作为像素级 Golden Reference；实现阶段 SHALL 复用现有 `/admin/logs` 日志详情抽屉、Admin Shell、shadcn 基础组件和 semantic token。

理由：

- REQ 的核心是日志字段契约和安全治理，不是全新页面视觉。
- 正式 spec 已有日志详情抽屉和管理端日志审计页要求，继续在现有结构中追加 Snapshot 分组风险最低。
- 避免为低保真 HTML 复制局部 CSS，造成与现有管理端列表/抽屉样式漂移。

### D2. Snapshot 作为结构化 metadata 契约

Request Snapshot SHOULD 以 `request_snapshot` 或等价对象嵌入请求日志详情响应，并可存储在 `request_logs.metadata` 或等价结构化字段中。实现阶段 MAY 选择 JSON metadata 扩展或新增列，但 API 响应必须暴露稳定字段结构。

建议字段分组：

- 请求信息：`method`、`path`、`route_template`、`request_id`
- 输入摘要：`query`、`body_schema_summary`、`redaction_summary`
- 业务资源：`resource_type`、`resource_id`、`id_source`
- 响应结果：`status_code`、`error_code`、`duration_ms`、`error_summary`
- 操作者 / 客户端：`actor_user_id`、`actor_username`、`client_type`、`ip_summary`、`user_agent_summary`
- 环境与时间：`environment`、`started_at`、`finished_at`

理由：

- 保留 metadata 的灵活性，同时通过 API Schema 约束字段，减少跨端和前后端漂移。
- 可兼容 SQLite demo 与 MySQL production；是否新增索引或列可在实现阶段基于查询需求决定。

### D3. Route template 获取与降级

实现阶段优先从 FastAPI route match 结果或 request scope 中获取 `route_template`。如果 middleware 所在时机无法稳定获取模板，系统 MUST 记录明确降级值，例如 `unknown`、`unmatched` 或等价枚举，而不是用带 query string 的原始 path 伪装模板。

理由：

- route template 是错误聚合和统计分析关键字段。
- 明确降级值比猜测字符串更利于排障，也更安全。

### D4. Query / Body 白名单与敏感过滤

query 与 body MUST 由后端统一白名单、敏感字段黑名单、类型摘要、长度截断和脱敏函数处理。上传、登录、认证、系统设置等敏感接口采用更严格白名单。

理由：

- 前端无法作为可信安全边界。
- 日志需要可排障但不能持久化原始敏感 body。

### D5. 契约同步

任何实现字段变化都必须同步：

- SQLite schema 与 MySQL schema / migration
- Pydantic response schema
- OpenAPI 与 Orval generated client
- `docs/03-api-index.md`、`docs/04-database-design.md` 和适用错误码文档
- 后端和前端测试

理由：

- REQ-0071 直接扩展日志 API 响应与存储契约，跳过任一同步点都会造成管理端或生产环境漂移。

## Conflict Resolution

| 来源 | 内容 | 决策 |
|---|---|---|
| HTML 原型 | 展示 Request Snapshot 分组与 JSON 辅助视图 | 采纳信息架构，不做像素级 CSS Port |
| prototype context | 入口沿用日志审计页，不新增导航层级 | 采纳 |
| acceptance.md | Snapshot 缺失字段或 metadata 异常时页面不可崩溃 | 采纳并写入 spec |
| `rules/ui-design.md` | 管理端复用模板、semantic token、日志页结构 | 采纳 |
| 正式 spec | 已有日志详情抽屉展示基础信息、请求信息、操作者与客户端、操作上下文、事件属性和 metadata JSON | 保留并 MODIFIED，新增 Request Snapshot 分组 |

## Risks / Trade-offs

- [Risk] middleware 获取 route template 时机不稳定 → Mitigation: 设计降级枚举，并在测试中覆盖 matched 与 unmatched 路由。
- [Risk] Snapshot 字段过多导致 metadata 膨胀 → Mitigation: body 只存 schema 摘要、长度和安全字段，长字段截断，禁止完整 body/response。
- [Risk] SQLite 与 MySQL JSON 行为差异 → Mitigation: 查询仍优先依赖索引列；JSON 主要用于详情展示，生产查询字段需评估索引或冗余列。
- [Risk] 敏感字段漏记 → Mitigation: 建立黑名单测试，覆盖 Authorization、Cookie、password、token、DSN、MinIO secret、raw filename。
- [Risk] Web 管理端只展示 JSON 可读性差 → Mitigation: 详情抽屉必须提供结构化分组，JSON 仅作为辅助视图。

## Migration Plan

1. 扩展后端 Snapshot builder 和脱敏策略，先在测试中锁定敏感字段不落库。
2. 扩展日志存储结构或 metadata schema，补齐 SQLite/MySQL migration。
3. 扩展日志详情 Pydantic Schema 与 API 响应。
4. 生成 OpenAPI / Orval 并更新管理端日志详情抽屉。
5. 同步 API/数据库/错误码文档与测试。
6. 若生产发现字段量或性能风险，保持 API 字段兼容，回滚具体采集字段或降级为更严格白名单。

## Open Questions

- 各接口 query/body 字段白名单是集中配置、路由装饰器配置，还是由日志 service 内部映射维护？
- `environment` 使用现有配置字段还是新增日志环境枚举？
- `resource_type` / `resource_id` 与既有 `entity_type` / `entity_id` 是否统一命名，或在 API 中同时兼容？

