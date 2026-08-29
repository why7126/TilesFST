---
requirement_id: REQ-0124-log-audit-behavior-trace-model
title: 日志审计补齐行为链路与任务链路采集模型 - 验收标准
acceptance_status: passed
owner: product
source: requirement.md
created_at: 2026-08-25 22:31:11
updated_at: 2026-08-28 16:21:48
---

# 验收标准

## 功能 AC

- [ ] AC-001 `usage_events` 增加并持久化 `behavior_trace_id` 与 `behavior_event_id`，字段语义和中文注释与 PRD 数据结构一致。
- [ ] AC-002 界面触发的一次用户行为必须生成同一个 `behavior_trace_id`；同一次行为触发多个 API 请求时，这些请求在 `request_logs.behavior_trace_id` 上可关联。
- [ ] AC-003 `behavior_event_id` 标识 `usage_events` 中单条行为事件；`request_logs.parent_behavior_event_id` 可以回指触发该请求的具体行为事件。
- [ ] AC-004 前端请求统一封装在页面访问、按钮点击、搜索筛选、详情查看、表单提交、上传、发布、删除等界面行为触发请求中透传 `behavior_trace_id` / `behavior_event_id`。
- [ ] AC-005 `request_logs` 增加并持久化 `behavior_trace_id` 与 `parent_behavior_event_id`；直接 API 调用场景允许两者为空。
- [ ] AC-006 `request_logs.request_id` 继续由后端生成并作为服务端可信单次 HTTP 请求 ID，不依赖前端传入值。
- [ ] AC-007 任务类请求继续通过 `task_traces.parent_request_id` 关联 `request_logs.request_id`，直接 API 调用和界面触发两种入口都能进入任务链路。
- [ ] AC-008 `task_trace_spans` 继续作为任务流程节点事实源；管理端中文展示使用“流程节点”，底层结构可继续使用 span 命名。
- [ ] AC-009 日志审计查询支持 `behavior_trace_id`、`request_id`、`task_trace_id` 三种入口，且与既有时间、用户、状态、路径等筛选条件协同工作。
- [ ] AC-010 日志审计详情可以联动展示“行为事件 -> API 请求 -> 任务链路 -> 流程节点”；直接 API 调用展示“API 请求 -> 任务链路 -> 流程节点”。
- [ ] AC-011 历史日志、无前端上下文的请求、外部系统调用和后台脚本调用缺少行为链路时，页面和接口必须兼容展示，不得因空 `behavior_trace_id` 报错。
- [ ] AC-012 采集 payload、请求摘要、响应摘要、错误摘要和 span metadata 必须脱敏，不保存或展示 Authorization、Cookie、Token、真实密钥、完整请求体、完整响应体、本机绝对路径或未授权对象存储 key。
- [ ] AC-013 SQLite / MySQL schema、迁移和数据库设计文档同步新增字段、中文注释、可空约束、索引建议和兼容策略。
- [ ] AC-014 若接口响应、查询参数或管理端 API schema 变化，必须同步 OpenAPI、Orval、API 文档和前后端测试；若仅内部采集不影响对外 schema，需在实现记录中说明不需要 Orval。
- [ ] AC-015 自动化测试至少覆盖界面触发一行为多请求、直接 API 调用无行为链路、任务请求关联 `parent_request_id`、按三类链路 ID 查询、敏感信息脱敏和旧日志兼容。

## 横切 AC（knowledge-base）

> 来源：`docs/knowledge-base/best-practices/admin-list-page-consistency.md`、`docs/knowledge-base/retrospectives/sprint-022-retrospective.md`

- [ ] AC-XCUT-001 日志审计列表必须复用管理端列表页基准或等价 shared shell，分页 DOM 保持 `page-summary` + `page-right`，展示后端真实 total、页码和每页条数。
- [ ] AC-XCUT-002 链路 ID、路径、错误摘要等长字段必须使用 nowrap、固定宽度截断、tooltip/title 或等价可访问策略，不能撑宽整表或挤压操作列。
- [ ] AC-XCUT-003 筛选区新增或修改 Select、Dropdown、Popover、Combobox、date picker、可搜索下拉或等价控件时，必须命中 `admin-filter-dropdown` gate，复用共享筛选控件或说明等价 wrapper 理由。
- [ ] AC-XCUT-004 操作成功 / 失败反馈使用 fixed toast，不得用文档流 notice 推挤日志审计列表、详情区或分页。
- [ ] AC-XCUT-005 本需求不新增危险状态变更；若后续实现加入删除、重放、批量处理、导出敏感明细等操作，必须使用 DS confirm modal，禁止 `window.confirm` / `window.alert`。

## 验收结果回填

```yaml
acceptance_status: passed
accepted_at: 2026-08-27 23:11:52
accepted_by: workflow-sync
source_change: add-log-audit-behavior-trace-model
source_sprint: sprint-026
evidence: []
failed_items: []
source_event: sprint.archive
notes: 由 Workflow Sync 根据 Change/Sprint 状态回填。
```

