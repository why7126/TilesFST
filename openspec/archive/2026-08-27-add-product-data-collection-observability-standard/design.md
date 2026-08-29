## 上下文

REQ-0126 来源于 REQ-0124 的项目内日志审计链路模型沉淀。现有系统已经具备 `usage_events`、`request_logs`、`task_traces`、`task_trace_spans` 等事实源，也已有 `docs/standards/task-trace-coverage.md`、`docs/standards/api-governance.md` 和 `openspec/specs/product-usage-logging/spec.md` 作为局部标准。

本 Change 的交付目标不是再次改造采集实现，而是建立跨产品可执行规范，使后续新产品或新模块从设计阶段就明确采集范围、链路字段、Task Trace 接入条件、保留周期和脱敏边界。

## 目标与非目标

目标：

- 建立长期标准文档，覆盖小程序、店主端、App、Web 管理端和后端 API。
- 明确 `usage_events -> request_logs -> task_traces -> task_trace_spans` 四层链路模型。
- 明确界面触发和直接 API 调用两种入口。
- 明确所有业务 API 请求记录 `request_logs`，Task Trace 采用分级覆盖。
- 明确默认保留周期、禁止采集字段、脱敏边界和新产品接入 checklist。
- 明确后续 REQ、BUG、OpenSpec Change 和 Sprint 如何引用该规范。

非目标：

- 不直接新增或修改业务接口、数据库表、前端页面、小程序页面或 App 代码。
- 不强制历史日志批量回填。
- 不接入外部 APM / OpenTelemetry、第三方埋点平台、实时告警、BI 大屏或复杂用户画像。
- 不替代已有 `product-usage-logging` 的项目内实现 spec，也不重写 API 治理规范。

## 设计决策

### D1 新增独立规范能力

采用新增 `product-data-collection-observability-standard` 能力，而不是直接修改 `product-usage-logging`。

原因：

- `product-usage-logging` 更偏项目内采集实现和日志审计查询。
- REQ-0126 是跨产品治理规范，强调后续产品开发阶段的引用和接入门禁。
- 独立能力可避免把实现细节和通用规范混在一个 spec 中。

备选方案：

- 直接修改 `product-usage-logging`：会把跨产品治理口径塞入既有实现能力，后续归档时容易扩大既有行为语义。

### D2 规范正文落入 `docs/standards/`

实现阶段应新增长期标准文档，例如 `docs/standards/product-data-collection-observability.md`，并从相关索引引用。

原因：

- `docs/standards/` 是长期治理细则归属。
- `issues/` 与 `iterations/` 只记录生命周期事实，不适合作为跨产品标准唯一事实源。
- 后续 REQ、BUG、Change 和 Sprint 可以稳定引用该文档。

### D3 保持两类入口并列

规范必须同时覆盖界面触发和直接 API 调用：

```text
界面触发：usage_events.behavior_trace_id -> request_logs.behavior_trace_id -> task_traces.parent_request_id -> task_trace_spans
直接 API：request_logs.request_id -> task_traces.parent_request_id -> task_trace_spans
```

原因：

- 直接 API 调用不应伪造 `usage_events`。
- 排障入口必须允许 `behavior_trace_id` 为空。
- `request_id` 仍是服务端可信的单次 HTTP 请求 ID。

### D4 Task Trace 采用分级覆盖

所有业务 API 必须有 request log，但 Task Trace 只对长耗时、多步骤、批量、异步、导入导出、上传 / 对象存储、第三方依赖、失败需定位节点、高风险写操作或关键业务数据变更强制接入。

原因：

- 对所有写操作强制 Task Trace 会增加实现和存储成本。
- 对高价值任务强制拆流程节点，才能保证异常定位价值。

### D5 后端脱敏作为安全边界

前端脱敏只作为展示优化，后端持久化前脱敏、截断和安全序列化必须作为安全边界。

原因：

- 客户端字段不可信，不能作为权限、身份、租户隔离或安全过滤依据。
- 日志、行为事件和任务 metadata 一旦持久化，敏感信息泄露风险高。

### D6 标准数据结构采用“最小字段 + 产品扩展”

规范必须包含 `usage_events`、`request_logs`、`task_traces`、`task_trace_spans` 的字段级结构，但不锁死每个产品的物理 DDL。

原因：

- 通用规范如果只写链路模型，不写数据结构，后续产品会在字段名、可空规则、生成方、索引和脱敏边界上出现分歧。
- 直接把某个产品的 SQLite / MySQL DDL 固化为跨产品标准，会限制不同产品的分区、归档、枚举和索引实现。
- “最小标准字段 + 产品扩展字段”能保证链路查询和审计口径一致，同时允许产品按规模、存储和合规要求调整物理实现。

备选方案：

- 不纳入数据结构：规范可执行性不足，后续接入仍需重复确认字段。
- 固化完整 DDL：跨产品适配成本高，且容易把本项目实现细节误当成通用标准。

## 影响分析

```yaml
impact:
  backend: indirect
  web: indirect
  miniapp: indirect
  admin: indirect
  database: indirect
  storage: none
  api: indirect
capabilities:
  new:
    - product-data-collection-observability-standard
  modified: []
```

说明：

- `indirect` 表示本 Change 不直接修改代码或契约，但规范将约束后续具体 Change 的实现和验收。
- 若后续具体接入新增接口字段、查询参数、响应字段、DB 字段或索引，必须在对应 Change 中同步 OpenAPI、Orval、数据库文档和测试。

## 冲突与 UI 说明

- 本 REQ 无 `prototype/`，不触发 UI Explore Gate。
- 本 Change 不新增具体 UI 页面。
- 后续日志审计或观测页面引用该规范时，仍需按具体页面类型执行 `admin-list`、长 ID 截断、复制反馈、敏感字段脱敏和后端真实分页等 UI 验收。

## 风险与取舍

- 规范只写文档、不提供 checklist 或引用入口 → 实现阶段必须交付新产品接入 checklist 和后续引用方式。
- “全量点击采集”被误读为纯 UI 噪音全量采集 → 规范必须使用“所有可命名业务行为必须采集，纯 UI 噪音可排除”的口径。
- 保留周期变成静态数字但缺少调整流程 → 规范必须说明变更保留周期需要原因、范围和审批依据。
- 后续产品引用时只做前端脱敏 → 规范必须明确后端脱敏是安全边界。

## 迁移计划

1. 新增长期标准文档和 docs 索引引用。
2. 在标准中列出四层链路模型、入口规则、字段语义、标准数据结构、Task Trace 分级覆盖、保留周期、敏感字段清单和接入 checklist。
3. 更新相关标准文档的交叉引用，例如 Task Trace 覆盖标准、API 治理标准、数据库设计或文档索引。
4. 添加或更新轻量校验脚本 / 文档测试，确保标准文档和索引存在。
5. 不做历史数据迁移；后续产品或模块按独立 REQ / Change 分批接入。

## 开放问题

- App 离线上报、重试、去重和设备标识脱敏策略是否需要在后续独立 REQ 中展开。
- 聚合数据 1 年保留的具体聚合表、粒度和分析口径是否需要后续产品分析需求承接。
