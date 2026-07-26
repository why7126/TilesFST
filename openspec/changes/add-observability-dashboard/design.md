## Context

`REQ-0076-observability-dashboard` 已评审通过，目标是在 `REQ-0024-product-usage-logging` 的日志审计列表、详情抽屉、基础指标和 Task Trace 时间线基础上，新增“日志审计 + 链路观测”排障工作流。

当前正式 spec `product-usage-logging` 已覆盖：

- `GET /api/v1/admin/logs` 日志列表、筛选、分页和基础 summary；
- `GET /api/v1/admin/logs/{id}` 日志详情；
- `/admin/logs` 管理端日志审计页；
- Task Trace 模型、span、`task_trace_id` / `request_id` 关联和安全脱敏；
- OpenAPI、Orval、docs、测试同步要求。

本 Change 只新增 OpenSpec 工件，不写 `src/`。实现必须经 `/opsx-apply add-observability-dashboard`。

## Goals / Non-Goals

**Goals:**

- 提供管理端链路观测仪表，统一展示请求、行为、审计和 Task Trace 的健康摘要。
- 支持任务成功率、慢任务、最慢 span、接口错误率、慢请求、失败原因和客户端分布。
- 支持通过 `request_id` / `task_trace_id` 一键追踪到日志详情、Task Trace 时间线或相关记录集合。
- 增加或扩展管理端日志聚合 API，保持 SQLite demo 与 MySQL production 可运行。
- 将 `admin-list` 知识库横切 AC 写入实现验收，避免分页、指标卡 DOM、toast 和管理端 smoke 回归。

**Non-Goals:**

- 不接入外部 APM、日志平台或 OpenTelemetry 全量分布式追踪。
- 不做实时大屏、告警推送、SLA 报表或自动异常检测。
- 不新增店主 Web 或小程序独立观测页面。
- 不改变对象存储上传链路；只消费已有日志、行为事件和 Task Trace 数据。

## Decisions

### D1. UI 策略：Tailwind DS / 共享管理端组件

采用 `tailwind-ds` 策略：复用现有 Admin Shell、管理端列表页、筛选区、指标卡、表格、分页、详情抽屉和 fixed toast 模式，不做独立 CSS Port。

理由：

- 原型 `prototype/web/observability-dashboard.html` 是结构和信息架构参考，不是必须逐像素 port 的 Golden Reference。
- 需求强调与现有日志审计页融合，复用 DS 更能降低 Dashboard / 列表 / 分页 / toast 回归风险。
- `docs/knowledge-base/best-practices/admin-list-page-consistency.md` 要求指标卡 DOM、分页 DOM 和 fixed toast 对齐用户管理基准。

备选方案：

- CSS Port：适合已有高保真 Golden Reference 的页面，但本需求 PNG 仍待导出，过早 port 会增加后续维护成本。
- 独立图表页面：会弱化日志列表与 Task Trace 下钻，不符合排障工作流。

### D2. 信息架构：优先扩展 `/admin/logs`

第一版优先在现有 `/admin/logs` 下增加“链路观测 / 日志列表 / Task Trace”模式或等价 Tab，而不是新增完全独立页面。

理由：

- 现有日志审计页已承载 `request_id`、`task_trace_id`、详情抽屉和筛选能力。
- 观测仪表需要下钻到日志详情与 Task Trace 时间线，保留同一页面上下文更高效。
- 若后续实现证明页面复杂度过高，可在 design trace 中记录并改为 SYSTEM 分组独立“链路观测”入口，但必须保留与日志审计互跳。

### D3. 聚合接口：新增 dedicated summary endpoint 优先

优先新增 dedicated 管理端聚合接口，例如 `GET /api/v1/admin/logs/observability`；如实现阶段选择扩展现有 `/api/v1/admin/logs` summary，必须在实现 trace 中说明兼容策略。

接口返回 SHOULD 包含：

- `summary`: 总日志量、API 错误数 / 错误率、慢请求数、任务成功率、慢任务数、审计操作数；
- `distributions`: 失败原因、客户端、任务状态、接口错误率；
- `rankings`: 慢任务、最慢 span、慢请求；
- `trace_results`: `request_id` / `task_trace_id` 查询结果或跳转所需 ID。

理由：

- Dedicated endpoint 避免日志列表分页接口变得过重。
- 聚合查询可以独立优化 SQL、索引和缓存策略。
- Orval 生成的 Web client 方法更清晰。

### D4. 数据口径：固定默认范围与可解释阈值

默认时间范围沿用日志审计页的近期排障心智，建议为最近 24 小时；可选范围必须与现有日志审计时间范围兼容，不提供“全部时间”。

慢请求 / 慢任务阈值第一版建议：

- 慢请求：复用现有日志审计慢请求口径或配置项；
- 慢任务：固定阈值或系统设置项均可，但实现 trace 必须记录来源；
- P95 / P99 若数据库层暂不支持，可先用平均耗时、最大耗时和固定分桶替代，并在 UI 文案或 design notes 中说明。

### D5. 安全与性能：数据库聚合优先，敏感字段不出域

聚合必须在 Repository 或统一数据访问层完成，禁止先拉全量日志到应用内过滤。返回数据只允许包含脱敏摘要、统计值、短 ID、跳转 ID 和错误码 / 失败摘要，不得返回完整请求体、响应体、Authorization、Cookie、Token、密码、真实密钥、数据库 DSN、`.env` 内容、真实客户数据或内部绝对路径。

## Conflict Resolution

| 来源 | 优先级 | 结论 |
|---|---:|---|
| `prototype/web/observability-dashboard.html` | 1 | 采用其页面结构：摘要指标、筛选、分布 / 排行、追踪区、明细与分页。 |
| `prototype/web/observability-dashboard-context.md` | 2 | 采用“扩展现有日志审计入口”的信息架构建议。 |
| `acceptance.md` | 3 | 全量转化为 delta spec 场景和 tasks 验收。 |
| `rules/ui-design.md` | 4 | 使用管理端 DS semantic token、既有组件和暗色旗舰风。 |
| `openspec/specs/product-usage-logging/spec.md` | 5 | 本 Change 是增量扩展，不移除现有日志列表、详情、Task Trace 和复制 helper 要求。 |

未发现冲突。若后续 PNG Golden Reference 导出，视觉验收优先级将高于 context 和 acceptance。

## Knowledge-base Refs

- `docs/knowledge-base/best-practices/admin-list-page-consistency.md`
- `docs/knowledge-base/retrospectives/sprint-010-retrospective.md`

## Risks / Trade-offs

- 聚合查询变慢 → 使用数据库聚合、必要索引、时间范围限制和 Top N 排行；禁止前端全量拉取。
- 指标口径与列表不一致 → 所有摘要、分布、排行和明细入口必须共享同一筛选参数解析。
- Task Trace 数据不完整 → 空缺字段以空态或“无关联”呈现，不得误报系统错误。
- 图表库引入增加复杂度 → 第一版可用表格、排行、轻量分布条或既有组件；新增依赖需在实现 trace 中说明。
- 管理端 UI 回归 → 执行 `admin-list` 横切 AC，覆盖分页 DOM、指标卡 DOM、fixed toast、无 `window.confirm` 和 1440x1024 / 移动端 smoke。

## Migration Plan

1. 新增或扩展管理端日志观测聚合 API，并补充 Schema、Service、Repository 和权限测试。
2. 同步 OpenAPI、Orval、`docs/03-api-index.md`、错误码文档和测试夹具。
3. 在 `/admin/logs` 中增加链路观测模式，复用 DS 组件和日志详情 / Task Trace 下钻。
4. 补充前端测试覆盖加载、空态、失败、筛选、追踪 ID 查询、复制、分页 DOM 和 fixed toast。
5. 如数据库需要新增索引，更新 SQLite / MySQL schema、迁移和数据库文档。

Rollback:

- 若聚合接口异常，可关闭或隐藏链路观测模式，保留原日志列表与详情能力。
- API 新增为非破坏性扩展，不应影响既有 `/api/v1/admin/logs` 列表与详情。

## Open Questions

- 最终接口采用 dedicated `/api/v1/admin/logs/observability` 还是扩展现有 summary，由实现阶段结合现有 service 结构确认。
- 慢任务阈值是否来自系统设置，还是本期固定在后端配置常量。
- 是否引入图表库；默认建议先用 DS 指标卡、排行表和轻量分布条完成 MVP。
