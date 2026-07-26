## Context

`REQ-0069-upload-observability-trace-logs` 已建立 Task Trace 能力方向，当前正式 spec `product-usage-logging` 也已有“任务链路追踪”要求：生成 `task_trace_id`、记录 task span、任务状态可推导、span 可关联 `request_id`，并支持任务追踪持久化查询。

`REQ-0073-task-trace-parent-request-model` 是对该能力的补强：现有模型仍缺少 Task Trace 到触发它的主请求 `request_id` 的稳定事实源；span 虽有 `request_id` 语义，但上传记录链路尚未形成强制写入和双向定位验收。此次变更跨后端日志、任务追踪、上传、数据库、管理端日志详情、OpenAPI/Orval 和测试。

## Goals / Non-Goals

**Goals:**

- Task Trace 任务摘要能够稳定记录触发它的主请求 `request_id`，字段语义为 `parent_request_id`。
- 有请求上下文的 task span 必须写入当前 `request_id`。
- 管理端日志详情能够从主请求进入 Task Trace，也能从 Task Trace span 回到请求日志。
- 上传场景首批验证图片、视频、文件上传的主请求、task trace、span 请求关系。
- API、DB、OpenAPI、Orval、文档和测试同步。

**Non-Goals:**

- 不建设完整分布式追踪、外部 APM、Trace Topology 或采样控制台。
- 不回填历史上传任务的 `parent_request_id` 或 span `request_id`。
- 不新增视频转码、压缩、多清晰度或封面生成能力。
- 不新增店主 Web 或小程序任务追踪展示入口。

## Decisions

### D1. `parent_request_id` 优先使用独立字段

优先在 `task_traces` 或等价任务摘要表中新增 `parent_request_id` 独立字段，并建立索引。这样能避免以 metadata 模糊扫描作为主查询路径，也能让日志详情从主请求反查任务摘要时保持稳定。

备选方案是在 metadata 中保存结构化字段。该方案仅作为兼容或过渡选择；若实现选择 metadata，必须定义固定 JSON key、读取兜底和缺失字段兼容，不得依赖临时约定。

### D2. `parent_request_id` 只能来自后端请求上下文

`parent_request_id` 代表触发 Task Trace 的主请求，必须从后端 request context 读取。前端可以携带 `task_trace_id` 用于串联任务，但不能声明或覆盖 `parent_request_id`。这可以避免客户端伪造追踪来源，也能保持审计边界清晰。

### D3. span `request_id` 按请求上下文写入

有 HTTP 请求上下文的 span 必须写入当前 `request_id`。无直接请求上下文的后端内部节点可以继承任务的 `parent_request_id` 或将 `request_id` 标为空，但必须保留 `task_trace_id`、时间顺序、状态、耗时和安全摘要，避免 UI 展示误导性跳转。

### D4. 管理端复用日志详情，不新增页面

本变更复用现有管理端日志审计详情和 `REQ-0069` 的 Task Trace 时间线策略，只补充字段展示与跳转/复制能力。UI 采用 Design System token 与 fixed toast，不新增独立页面或营销式说明区。

## Conflict Resolution

原型优先级：HTML > PNG > `prototype/web/context.md` > acceptance.md > `rules/ui-design.md` > `openspec/specs`。

本 REQ 仅提供 `prototype/web/context.md`，没有独立 HTML/PNG。因此后续实现以 context 和 acceptance 为准：在现有日志详情 Task Trace 分组中补充 `parent_request_id`、span `request_id` 展示、复制和定位；若后续 `/opsx-apply` 发现需要明显布局调整，必须基于 `REQ-0069` 原型补充 HTML/PNG Golden Reference 后再实现。

## Risks / Trade-offs

- **字段迁移风险** → 使用兼容迁移，历史缺失字段安全兜底，不强制回填。
- **metadata 方案查询性能风险** → 优先独立字段并建立索引；如选择 metadata，必须避免无界模糊扫描。
- **追踪写入失败影响主流程** → Task Trace 写入失败不得吞掉主业务错误，必须记录最小 request log 或安全错误摘要。
- **上传链路多层配置漂移** → 继承 `admin-media-upload-chain` 横切 AC，Docker `:3000` 边界文件验收必须覆盖。
- **API/Orval 漂移** → 新增或调整日志详情 / 任务追踪字段时，同步 OpenAPI、Orval、文档和测试。

## Migration Plan

1. 确认当前 Task Trace 存储结构，选择独立字段或结构化 metadata 方案。
2. 如采用独立字段，新增 SQLite / MySQL 兼容 schema、索引和 Repository 读写。
3. 更新 Task Trace 创建逻辑，从后端请求上下文写入 `parent_request_id`。
4. 更新上传与任务型接口 span 写入逻辑，确保有请求上下文的 span 写入当前 `request_id`。
5. 更新日志详情 API / Schema / OpenAPI / Orval / Web 展示。
6. 补充后端、前端和 Docker Web 上传边界验收。

## Open Questions

- 当前实现中的 Task Trace 表结构是否已存在独立 `task_traces` 表；若未存在，是否沿用组合方案还是新增摘要表。
- 一个主请求触发多个 Task Trace 时，日志详情 UI 使用列表、折叠分组还是摘要卡片，需要在实现阶段按现有组件约束确定。
