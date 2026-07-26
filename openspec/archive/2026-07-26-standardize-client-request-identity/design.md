## Context

`REQ-0072-client-request-identity-standard` 已评审通过，父需求为 `REQ-0024-product-usage-logging`。当前系统已有请求日志、usage events、日志审计列表和详情抽屉，但跨端普通 API 请求的客户端类型与客户端请求标识仍不统一：

- Web 管理端和店主 Web 前台的 API client 需要统一注入客户端来源和客户端请求标识。
- 微信小程序 usage events 已可表达 `wechat_miniapp`，但普通 API 请求仍可能因为缺失请求头被默认归因。
- 后端可信 `request_id` 与客户端生成 ID 的安全边界需要明确。
- 日志审计页需要展示并区分两类 ID，同时保持 `admin-list` 横切一致性。

本 Change 只创建 OpenSpec 工件，不写 `src/`。实现必须经 `/opsx-apply` 或 Sprint apply。

## Goals / Non-Goals

**Goals:**

- 统一三类客户端来源：`web_admin`、`web_catalog`、`wechat_miniapp`。
- 明确客户端传入请求标识只能作为 `client_request_id` 或等价独立字段保存，不得默认覆盖后端可信 `request_id`。
- 后端继续生成可信 `request_id`，并通过响应头 `x-request-id` 返回。
- Web 管理端、店主 Web 前台和微信小程序请求封装都能注入客户端类型与客户端请求标识。
- 日志审计列表 / 详情抽屉展示客户端类型、后端可信 `request_id` 和客户端请求 ID，并保持复制反馈无布局位移。
- API、数据库、OpenAPI、Orval、docs 和测试同步覆盖新增契约。

**Non-Goals:**

- 不引入 OpenTelemetry、Jaeger、APM 或外部分布式链路追踪平台。
- 不把客户端传入的 `x-request-id` 当作服务端最终可信 request id。
- 不保存 Authorization Header、Cookie、Token、密码、真实密钥、完整敏感请求体或原始客户数据。
- 不改变日志保留周期、日志清理策略或对象存储策略。
- 不新增独立日志审计页面，只增强既有 `/admin/logs` 字段和交互。

## Decisions

### D1. UI 策略：Design System 模板增强

选择 Design System / `AdminListPage` 等价模板增强，而不是 CSS Port。

理由：

- REQ 原型表达的是既有日志审计列表和详情抽屉字段补充，不是新页面重建。
- `openspec/specs/web-client` 已要求 `/admin/logs` 参与管理端列表页横切一致性。
- 复制反馈、分页 DOM、指标卡 DOM 与 fixed toast 应复用既有管理端列表页规范。

替代方案：

- CSS Port：适合全新页面或高保真 HTML 迁移。本需求只有字段与交互补充，使用 CSS Port 会扩大样式面。

### D2. 后端可信 ID 与客户端 ID 分离

后端每次请求继续生成可信 `request_id`，响应头使用 `x-request-id` 返回。客户端请求标识统一保存为 `client_request_id` 或等价字段，来源可为 `x-client-request-id`、请求体 `client_request_id` 或经实现确认的兼容头，但不得默认覆盖服务端可信 ID。

理由：

- 客户端字段可伪造，不能作为服务端链路事实源。
- 分离字段可同时支持服务端排障和前端动作关联。
- 日志审计可清晰展示 Trusted Request ID 与 Client Request ID，减少误读。

替代方案：

- 接受客户端 `x-request-id` 并透传为服务端 request id：排障体验简单，但安全边界不清晰，且容易污染可信日志链路。

### D3. 客户端类型枚举统一

统一枚举为：

- `web_admin`
- `web_catalog`
- `wechat_miniapp`

后端对缺失或未知值采用受控降级：记录为 `unknown` 或现有安全默认值，但必须可通过测试发现三端正常封装不会触发降级。

### D4. 小程序 fallback 重试标识

同一小程序用户动作触发 fallback base URL 重试时，应复用同一个 `client_request_id`；如果重试已经跨越用户动作边界，则重新生成。该策略用于把同一次动作的多次尝试聚合到同一客户端请求线索下，同时后端每次 HTTP 请求仍拥有独立可信 `request_id`。

### D5. 行为事件关联策略

行为事件可携带相关后端 `request_id` 或客户端请求 ID。若事件在主业务请求之前产生，可以先携带客户端请求 ID；若主业务响应已返回，则可补充后端可信 `request_id`。usage event 上报失败不得阻断主业务流程。

### D6. 契约同步策略

若实现新增日志字段、查询参数、响应字段、请求头说明或响应头说明，必须同步：

- OpenAPI 导出；
- Orval 生成客户端；
- `docs/03-api-index.md`；
- `docs/04-database-design.md`；
- 适用错误码文档；
- 后端、Web、小程序测试。

### D7. 客户端请求标识筛选策略

本期不新增独立 `client_request_id` 查询参数。日志审计仍复用既有 `keyword` 与 `path_or_request_id` 查询入口，其中后端模糊匹配范围扩展为 API path、服务端可信 `request_id`、`client_request_id` 与 `task_trace_id`。

理由：

- 管理端已有“路径 / Request ID”筛选入口，避免为低频排障字段新增一列筛选控件导致列表筛选区拥挤。
- `client_request_id` 已作为独立列和索引持久化，后续如需要精确筛选参数，可通过新的 OpenSpec Change 扩展 API 契约。
- 当前验收重点是三端注入、可信 ID 边界、列表 / 详情展示和复制反馈。

## Conflict Resolution

原型优先级按 `HTML > PNG > context.md > acceptance.md > ui-design.md > openspec/specs`。

| 来源 | 结论 |
|---|---|
| `prototype/web/client-request-identity.html` | 最高优先级可视参考；展示 `client_type`、`request_id`、`client_request_id`、fixed toast、分页 DOM 与详情抽屉字段分组。 |
| PNG | 当前无 PNG；不阻塞 Change 创建，后续实现可按验收导出截图。 |
| `prototype/web/client-request-identity-context.md` | 明确该原型是既有日志审计字段补充，不是新增独立页面。 |
| `acceptance.md` | 功能 AC 与横切 AC 均与原型一致。 |
| `rules/ui-design.md` | 管理端列表优先复用模板、semantic token、fixed toast。 |

冲突处理结论：后续实现以现有 `/admin/logs` 页面为承载，不新增页面；TSX/CSS 中不得按原型裸 Hex 复制样式，必须映射到现有 Design System semantic token。

## Risks / Trade-offs

- [Risk] 前端、小程序和后端对请求头命名理解不一致 → Mitigation: OpenSpec tasks 中固定请求头/字段名确认步骤，并补充三端测试。
- [Risk] 客户端 ID 被误用为可信 request id → Mitigation: spec 明确字段分离，日志审计文案区分 Trusted Request ID 与 Client Request ID。
- [Risk] 数据库迁移在 SQLite/MySQL 漂移 → Mitigation: 同步 schema、migration、MySQL drift 测试和数据库文档。
- [Risk] 日志审计表格列增加导致布局拥挤 → Mitigation: 列表短 ID 截断，详情展示完整值，复制获取完整 ID，并保留分页 / fixed toast 横切 AC。
- [Risk] 小程序 fallback 重试产生多条 request id 难以关联 → Mitigation: 同一用户动作复用 `client_request_id`，后端可信 request id 仍逐请求独立。

## Migration Plan

1. 后端先扩展请求日志模型和 middleware，确保可信 `request_id` 响应头不回归。
2. 增加 `client_request_id` 或等价字段的 SQLite/MySQL schema、migration、repository 和服务层读写。
3. Web 管理端与店主 Web 前台请求封装注入客户端类型和客户端请求 ID。
4. 小程序统一 request 封装注入 `wechat_miniapp` 和客户端请求 ID，并实现 fallback 重试复用策略。
5. 日志审计列表 / 详情抽屉展示字段、复制反馈和筛选策略。
6. 同步 OpenAPI / Orval / docs / tests。

Rollback：若前端或小程序请求头注入异常，后端仍生成可信 `request_id` 并按受控默认值记录客户端类型；可临时关闭客户端 ID 展示但不得关闭可信 request id 生成和响应头返回。

## Open Questions

- 最终客户端请求标识请求头命名是否固定为 `x-client-request-id`，以及是否兼容历史 `x-request-id` 输入。
- 日志列表本期不新增独立 `client_request_id` 筛选参数，复用 `keyword` / `path_or_request_id` 模糊检索；若需要精确筛选参数，另走 follow-up Change。
- 是否需要独立动作级 `interaction_id`。本 Change 不默认引入；若产品确认需要，应另行 capture follow-up。
