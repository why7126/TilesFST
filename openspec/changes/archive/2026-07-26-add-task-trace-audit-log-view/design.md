## Context

REQ-0069 是 `REQ-0024-product-usage-logging` 的平台治理扩展。当前系统已有 `request_logs`、`usage_events`、`audit_logs` 和管理端 `/admin/logs` 查询入口，但缺少“一次业务任务”的跨节点追踪模型。

本 Change 以 `task_trace_id` 为中心串联用户动作、前端节点、API 请求、后端服务、对象存储、数据库、后处理和最终响应。上传是首批落地场景，但设计必须保持通用，后续可扩展导入、导出、发布、同步等任务。

## Goals

- 为可追踪业务任务生成或确认 `task_trace_id`。
- 记录 task span，支持时间线展示和耗时拆解。
- 支持管理端日志审计按 `task_trace_id` 查询。
- 在日志详情抽屉展示任务时间线。
- 覆盖图片、视频、文件上传首批场景，解决 BUG-0085 耗时分析。
- 保持安全脱敏、权限边界、SQLite/MySQL schema 兼容和 OpenAPI/Orval 同步。

## Non-Goals

- 不建设完整 APM 平台、链路拓扑大屏或外部日志系统接入。
- 不保存完整请求体、响应体、Authorization、Cookie、密钥或真实客户数据。
- 不新增视频转码、压缩、多清晰度或封面生成能力；只记录已有后处理节点或 N/A。
- 不要求历史日志回填 `task_trace_id`。

## Decisions

### D1. UI strategy

采用 Design System / AdminListPage 扩展策略，而不是 CSS Port。

原因：

- 日志审计页面已经是管理端列表/详情模式，REQ-0069 只扩展筛选字段、列表字段和详情抽屉分组。
- 原型 `issues/requirements/archive/REQ-0069-upload-observability-trace-logs/prototype/web/task-trace-log-detail.html` 是需求阶段视觉参考，不作为最终 CSS 源码 port。
- 实现应复用 `AdminListPage`、现有日志审计组件、Fixed Toast、分页和详情抽屉模式。

### D2. Data model

实现阶段必须在以下方案中二选一或组合，并在 apply 输出中说明最终选择：

| 方案 | 优点 | 风险 |
|---|---|---|
| 扩展日志表 | 查询入口简单，迁移成本低 | task span 明细可能挤入 metadata，索引和时间线查询较弱 |
| 新增 `task_traces` / `task_trace_spans` | 模型清晰，支持时间线和慢节点统计 | 需要新增 schema、Repository、同步 SQLite/MySQL |
| 组合方案 | 日志表保存摘要，span 表保存明细 | 实现复杂度较高，但最符合长期演进 |

推荐组合方案：日志列表项保存 `task_trace_id`、`task_type` 等摘要字段，独立 span 表保存节点时间线。若实现阶段选择轻量扩展日志表，必须证明可索引查询和详情时间线不会依赖无界 metadata 模糊扫描。

### D3. task_trace_id and request_id

`request_id` 表示一次 HTTP 请求，`task_trace_id` 表示一次业务任务。一个 `task_trace_id` 可以关联多个 `request_id`。

- 后端应作为 `task_trace_id` 的可信生成方。
- 前端可在任务开始前请求或携带候选值，但后端必须校验格式并可覆盖。
- 上传任务的响应应返回或可让前端获得最终 `task_trace_id`，用于前端完成/失败事件关联。
- `task_trace_id` 不得包含用户原始文件名、手机号、密钥、业务敏感信息或可枚举自增序列。

### D4. Upload span coverage

上传首批场景必须覆盖：

```text
frontend_select_file
frontend_upload_start
frontend_upload_body_done
api_receive
validate_file
storage_put_object
db_create_media
post_process (N/A allowed)
api_response
frontend_done | frontend_failed
```

`BUG-0085` 的关键验收是统计 `frontend_upload_body_done` 到 `api_response` 之间耗时，并能定位最慢节点。

### D5. Log audit detail timeline

日志详情抽屉新增 Task Trace 分组：

- 任务摘要：`task_trace_id`、`task_type`、状态、总耗时、资源类型/ID。
- 时间线：节点名称、耗时、状态、错误码、关联 `request_id`、摘要。
- 复制：支持复制 `task_trace_id` 和 `request_id`，使用 fixed toast 或等价固定反馈。
- 普通日志无 `task_trace_id` 时隐藏时间线或显示 N/A，不能破坏现有详情。

## Conflict Resolution

优先级按 REQ-0069 约定：

```text
HTML > context.md > acceptance.md > rules/ui-design.md > archived specs
```

- HTML/context 确认了右侧详情抽屉中的 Task Trace 时间线布局；实现可根据现有组件体系调整 DOM，但必须保留任务摘要和节点时间线分组。
- acceptance 要求 PNG Golden Reference 可后续导出；当前不存在 PNG，不阻断 Change 创建。
- HTML 原型使用裸 CSS 变量和色值仅作为需求阶段静态原型；实现代码必须使用 Design System semantic token，禁止新增裸 Hex。
- 日志审计既有 spec 以 `request_id` 为核心；本 Change 通过 delta spec 扩展为 `request_id + task_trace_id`，不移除既有 request_id 能力。

## Knowledge-base refs

后续 design / tasks / acceptance 必须引用并落实：

- `docs/knowledge-base/best-practices/admin-list-page-consistency.md`
- `docs/knowledge-base/best-practices/admin-media-upload-chain.md`
- `docs/knowledge-base/retrospectives/sprint-010-retrospective.md`

横切要求：

- 日志审计分页 DOM、指标卡 DOM、fixed toast、无 `window.confirm`。
- 上传状态机 `idle -> uploading -> done / failed`，同会话即时回显，Docker `:3000` 上传边界验证。
- 上传有效限制来源必须同步前端提示、后端校验、系统设置、Nginx / 代理和对象存储策略。

## API impact

可能修改：

- `GET /api/v1/admin/logs`
  - 查询参数新增 `task_trace_id` 或将 `path_or_request_id` 扩展为路径 / request_id / task_trace_id。
  - 列表项新增 `task_trace_id`、`task_type`、`task_status`、`task_duration_ms`。
- `GET /api/v1/admin/logs/{id}`
  - 详情新增 `task_trace` 或 `task_spans` 分组。
- 上传 API
  - 响应或 metadata 可新增 `task_trace_id`，用于前端后续事件关联。

所有 API 变更必须同步 OpenAPI、Orval、`docs/03-api-index.md` 和测试。

## Database impact

可能新增或修改：

- `task_traces`
- `task_trace_spans`
- 或扩展 `request_logs`、`usage_events`、`audit_logs`

必须满足：

- SQLite demo 与 MySQL production schema 兼容。
- `task_trace_id`、`task_type`、`created_at` 或等价字段有索引。
- Repository / Service 层访问，路由层不得直接拼 SQL。
- 日志保留周期与 `audit.retention_days` 或新配置一致。

## Security

- 管理端查询仅系统管理员可用。
- metadata 统一脱敏、截断和安全 JSON 化。
- 不保存 Authorization、Cookie、AccessKey、SecretKey、数据库 DSN、`.env` 内容、真实客户数据、内部绝对路径或完整敏感请求体。
- 前端传入的 `task_trace_id`、`task_type`、`resource_id` 不得作为权限判断依据。

## Testing strategy

- 后端 pytest：任务 trace repository/service、日志列表筛选、详情时间线、上传 span、权限、脱敏、错误码、SQLite/MySQL schema。
- 前端 Vitest：日志审计筛选、任务时间线详情、复制 fixed toast、无 task trace 普通日志、上传状态机。
- OpenAPI/Orval：生成并确认新增字段类型。
- Docker smoke：经 `http://localhost:3000` 上传小文件和超限文件，覆盖图片、视频、文件边界或明确 N/A。
