---
requirement_id: REQ-0076-observability-dashboard
title: 日志审计与链路观测仪表 - 验收标准
status: pending_review
owner: product
created_at: 2026-07-26 13:02:41
updated_at: 2026-07-26 13:02:41
knowledge_base_refs:
  - docs/knowledge-base/best-practices/admin-list-page-consistency.md
  - docs/knowledge-base/retrospectives/sprint-010-retrospective.md
cross_cutting_tags:
  - admin-list
---

# 验收标准

## 功能 AC

- [ ] AC-001 管理端 MUST 提供日志审计与链路观测入口，入口位于管理端权限边界内。
- [ ] AC-002 仅系统管理员或具备日志审计权限的角色可访问观测仪表；无权限用户直链访问 MUST 返回 403 或管理端无权限页。
- [ ] AC-003 页面 MUST 展示请求日志、行为事件、审计操作和 Task Trace 的统一摘要。
- [ ] AC-004 摘要指标 MUST 至少包含总日志量、API 错误数 / 错误率、慢请求数、任务成功率、慢任务数和审计操作数。
- [ ] AC-005 所有摘要、分布、排行和明细入口 MUST 与当前筛选条件保持同一统计口径。
- [ ] AC-006 仪表 MUST 支持按时间范围、日志类型、客户端、任务类型、接口路径、状态 / 结果筛选。
- [ ] AC-007 默认时间范围、可选范围和时区口径 MUST 在 OpenSpec design 中明确。
- [ ] AC-008 Task Trace 指标 MUST 展示任务状态分布、任务成功率、失败任务数量和任务耗时分布或等价分桶。
- [ ] AC-009 慢任务排行 MUST 展示任务类型、耗时、状态、触发来源和 `task_trace_id`。
- [ ] AC-010 最慢 span 排行 MUST 展示 span 名称、任务类型、耗时、结果和关联 `task_trace_id`。
- [ ] AC-011 慢任务、失败任务和最慢 span MUST 可跳转到对应 Task Trace 时间线或日志详情。
- [ ] AC-012 请求观测 MUST 支持按接口路径、方法、状态码统计请求量、错误量和错误率。
- [ ] AC-013 慢请求排行 MUST 展示路径、方法、状态码、耗时、客户端和 `request_id`。
- [ ] AC-014 失败原因分布 MUST 优先使用错误码、异常摘要或业务失败原因，不展示完整敏感 payload。
- [ ] AC-015 错误接口、慢请求和失败原因项 MUST 可跳转到相关日志详情。
- [ ] AC-016 页面 MUST 支持复制 `request_id` 和 `task_trace_id`，成功或失败反馈不得造成布局位移。
- [ ] AC-017 用户输入 `request_id` 后，系统 MUST 能查询同请求链路的请求日志、行为事件、审计操作和关联 Task Trace。
- [ ] AC-018 用户输入 `task_trace_id` 后，系统 MUST 能查询任务主记录、span 时间线和关联 `request_id` 日志。
- [ ] AC-019 追踪 ID 未命中时，页面 MUST 展示清晰空态，不误报系统错误。
- [ ] AC-020 客户端分布 SHOULD 覆盖 `web_admin`、`web_catalog`、`miniapp`、`backend` 和未识别客户端。
- [ ] AC-021 行为事件分布 SHOULD 展示事件类型、模块、结果和失败原因。
- [ ] AC-022 后端聚合查询 MUST 支持 SQLite demo 与生产 MySQL，且避免无条件全表扫描后在应用内聚合。
- [ ] AC-023 聚合查询 MUST 返回结构化摘要、分布、排行和跳转所需 ID。
- [ ] AC-024 空数据时聚合接口 MUST 返回零值摘要和空集合，前端 MUST 展示可理解空态。
- [ ] AC-025 聚合接口失败时前端 MUST 展示加载失败状态和重试入口，不影响基础日志列表能力。
- [ ] AC-026 指标聚合、日志详情和追踪结果 MUST 不展示 Authorization、Cookie、Token、密码、真实密钥、数据库 DSN、`.env` 内容、真实客户数据或内部绝对路径。
- [ ] AC-027 若新增或调整管理端观测 API，MUST 同步 OpenAPI、Orval、`docs/03-api-index.md`、错误码文档和后端/前端测试。
- [ ] AC-028 UI MUST 使用管理端 Design System semantic token 和既有管理端列表 / 筛选 / 表格 / 详情模式，禁止裸 Hex。
- [ ] AC-029 原型策略 MUST 至少提供链路观测仪表 HTML/context；PNG Golden Reference 可在后续设计确认后导出。
- [ ] AC-030 OpenSpec design MUST 明确采用“扩展现有日志 summary”还是“新增观测聚合接口”，并说明分位值、慢任务阈值和错误率口径。

## 横切 AC（knowledge-base）

> 来源：`docs/knowledge-base/best-practices/admin-list-page-consistency.md` — 预防 Sprint 002/003 管理端列表页一致性复发类缺陷。

- [ ] AC-XCUT-001 观测仪表中的日志 / 任务明细分页 DOM MUST 对齐用户管理基准：左侧 `.page-summary`，右侧 `.page-right` 页码 + 每页条数。
- [ ] AC-XCUT-002 摘要指标卡 MUST 使用 `.metric-label` / `.metric-value` / `.metric-desc` 结构，不得只复用外层卡片后用裸 `strong` / `span` 承载数值和说明。
- [ ] AC-XCUT-003 查询、刷新、复制 `request_id` / `task_trace_id`、打开详情、加载失败等反馈 MUST 使用 fixed toast 或等价固定层，不得造成页面头部、筛选区、图表区或表格纵向位移。
- [ ] AC-XCUT-004 N/A — 本需求首期仅查询、追踪和查看观测数据，不包含启停、删除、重置、清理等危险状态变更；若后续新增清理、删除、导出等危险操作，MUST 使用 DS confirm modal。
- [ ] AC-XCUT-005 页面实现 MUST 不调用 `window.confirm`；本期无确认操作时以静态检查或代码 review 说明 N/A。
- [ ] AC-XCUT-006 1440x1024 与移动端管理端视口 MUST 纳入页面级 smoke 或截图验收，覆盖摘要指标、筛选、排行、表格、详情入口和空态；Sprint 010 复盘指出管理端 UI 细节需共享 smoke matrix 预防复发。

