## Context

REQ-0074 是 `REQ-0069-upload-observability-trace-logs` 的覆盖范围扩展。当前正式规格 `product-usage-logging` 已包含 Task Trace 模型、日志审计筛选、详情抽屉和 OpenAPI / Orval 同步要求；`object-storage` 已把图片、视频、文件上传列为首批 Task Trace 场景。

缺口在于：上传之外的保存 SKU、批量操作、导入导出、媒体处理、异步任务和复杂查询等任务型接口仍没有统一接入标准。REQ-0074 要求这些任务可以生成或继承 `task_trace_id`、写入 span、关联 request log / audit log / 后台任务，并在管理端反馈中提供可复制追踪标识。

## Goals / Non-Goals

**Goals:**

- 定义任务型接口判定标准与首批接入清单输出方式。
- 扩展 Task Trace helper 或等价服务封装，支持同步、异步和批量任务。
- 约束关键 span、失败 span、部分成功、超时和慢节点记录。
- 让管理端复杂任务反馈可以展示 / 复制 `task_trace_id`，并跳转日志审计查看时间线。
- 明确 API、DB、OpenAPI、Orval、docs、测试和 smoke evidence 的同步边界。

**Non-Goals:**

- 不建设完整 APM 平台、链路拓扑大屏、采样策略控制台或外部日志系统接入。
- 不保存完整请求体 / 响应体、Authorization、Cookie、密钥、真实客户数据或内部绝对路径。
- 不借本 Change 新增导入导出业务能力、视频转码增强或无关业务重构。
- 不要求为所有历史接口一次性回填 Task Trace。

## Decisions

### D1. Change 类型与 capability

采用 `update` 类型，修改既有 `product-usage-logging` capability，不新增顶层 capability。

原因：正式规格中已经存在 `### Requirement: 任务链路追踪`，REQ-0074 是从上传样例扩展覆盖范围，而不是引入独立子系统。`object-storage` 的上传 Task Trace 规格保持不变，后续实现可复用其上传边界要求。

### D2. 首批接口清单先文档化，再实现

实现阶段必须先输出首批候选接口清单，至少评估：

- 保存 SKU / 商品资料；
- 批量上下架、批量删除、批量排序；
- 导入 / 导出；
- 媒体处理 / 后处理；
- 异步任务 / 状态查询；
- 复杂查询 / 聚合统计。

每项必须标注任务类型、优先级、关键步骤、预期 span、是否异步、是否批量、是否涉及对象存储或外部依赖。未纳入首批的接口也要记录原因和后续排期，避免“只做一两个接口但无覆盖口径”的灰区。

### D3. Task Trace helper 作为接入边界

业务代码不应在每个 service 中重复拼装 span 字典。实现应提供 Task Trace helper 或等价服务封装，至少支持：

- 生成或确认可信 `task_trace_id`；
- 绑定当前请求上下文和 `request_id`；
- 开始 / 结束 / 失败 span；
- 异步任务上下文序列化与继承；
- 批量任务的汇总 span 与失败分类摘要；
- span 写入失败时的可观测性降级。

具体形态可在 apply 阶段选择上下文管理器、装饰器或显式 begin/end API，但路由层不得直接拼 SQL 或直接持久化 span。

### D4. 数据模型延续 REQ-0069 的组合优先策略

优先延续 REQ-0069 的组合方案：日志表保存 `task_trace_id`、`task_type`、任务摘要等查询字段，独立 task trace / span 结构保存时间线明细。若实现阶段选择轻量方案，也必须证明：

- `task_trace_id`、`task_type`、`created_at` 或等价字段可索引查询；
- 日志详情时间线不依赖无界 metadata 模糊扫描；
- SQLite demo 与 MySQL production schema 兼容；
- 数据访问经过 Repository / Service 层。

### D5. UI strategy

采用 Design System / 现有管理端组件扩展策略，不进行 CSS Port。

Conflict Resolution：

```text
HTML > PNG > *-context.md > acceptance.md > ui-design.md > openspec/specs
```

- REQ 原型 HTML 与 context 确认了复杂任务反馈的信息层级：状态、摘要、`task_trace_id`、复制入口、日志审计入口和节点摘要。
- 原型 HTML 使用裸色值仅作为需求阶段静态视觉参考；实现必须使用 Design System semantic token 和现有 shadcn / shared UI 组件，禁止照搬裸 Hex。
- `acceptance.md` 要求无 Task Trace 时保持原交互，因此实现必须为 `no_trace` 分支保留旧行为。
- 由于本 REQ 未命中固定 `admin-list/admin-form/admin-modal/media-upload` 横切标签，本 Change 不写 AC-XCUT；若 apply 实际改动日志审计列表、上传控件或弹窗，必须补读对应 best-practices 并在执行输出中说明。

## Risks / Trade-offs

- [Risk] 首批接口范围过大，导致 apply 难以闭环。→ Mitigation: tasks 要求先落首批清单和优先级，可将未纳入项记录为后续排期，但不得省略清单。
- [Risk] span 写入失败影响主业务。→ Mitigation: helper 必须有降级策略；追踪失败不能掩盖主业务错误。
- [Risk] 异步任务上下文丢失。→ Mitigation: async dispatch 必须显式传递 `task_trace_id`，worker start / failed / finished 写入 span。
- [Risk] metadata 泄露敏感信息。→ Mitigation: 统一脱敏、截断、字段黑名单和安全 JSON 化，前端传入的追踪字段不得用于权限判断。
- [Risk] API / DB / Orval 漂移。→ Mitigation: tasks 固化 OpenAPI export、Orval 生成、SQLite/MySQL schema、docs 和测试同步。
- [Risk] smoke evidence 后置导致 archive 才发现环境问题。→ Mitigation: 涉及生产 DB、对象存储、上传或异步边界时，apply 中段前置 smoke evidence stub 或明确 N/A。

## Migration Plan

1. 梳理首批任务型接口清单与候选排期。
2. 实现或扩展 Task Trace helper / service / repository。
3. 按优先级接入首批同步、异步和批量任务 span。
4. 同步 API schema、OpenAPI、Orval、SQLite/MySQL schema、docs 和测试。
5. 更新管理端复杂任务反馈和日志审计跳转 / 复制体验。
6. 运行后端、前端和必要 smoke 验证。

Rollback：保留已有 request log / audit log / usage event；若新 span 写入异常，可临时关闭任务型接口 span 写入，保留基础业务响应与 request_id 日志，不删除已新增兼容字段。

## Open Questions

- 首批实现是否一次覆盖六类候选，还是按风险优先级选择 2-3 类先落地并记录后续排期？
- 是否需要新增显式任务状态查询接口，还是完全复用日志审计详情查看？
- 异步任务框架是否已有统一入口可承载 `task_trace_id` 继承，还是需要轻量封装？

