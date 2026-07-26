---
requirement_id: REQ-0075-audit-log-task-trace-linking
title: 审计操作日志任务链路展示原型说明
status: pending_review
owner: product
created_at: 2026-07-26 13:02:25
updated_at: 2026-07-26 13:02:25
---

# 原型说明

## 1. 原型范围

本原型用于说明管理端日志审计页在 `audit` 类型日志中展示 Task Trace 信息的交互策略。它不是前端实现，不引入新页面；后续实现应复用现有 `/admin/logs` 页面、列表模板和详情抽屉。

## 2. 入口与布局

- 页面：管理端 `SYSTEM / 日志审计`。
- 列表：在现有时间、类型、事件 / 摘要、操作者、客户端、状态、耗时、request_id 等信息基础上，补充任务摘要。
- 筛选：优先将现有关键字提示扩展为“路径 / request_id / task_trace_id”；若信息密度不足，可新增独立 `task_trace_id` 筛选。
- 详情抽屉：在基础信息、请求信息、操作者 / 客户端、操作上下文之后新增 `Task Trace` 分组。

## 3. 关键状态

| 状态 | 展示策略 |
|---|---|
| 有 `task_trace_id` | 列表展示任务标识短码；详情展示 `task_trace_id`、`task_type`、任务状态、关键节点摘要和复制操作。 |
| 无 `task_trace_id` | 列表任务列展示 `—` 或不显示任务摘要；详情不渲染空时间线错误。 |
| Task Trace 已过期或未找到 | 详情保留审计基础信息，并在 Task Trace 分组展示安全兜底提示。 |
| 查询失败 | 使用 fixed toast 或等价固定反馈，不推动布局。 |

## 4. UI 约束

- 使用 Design System semantic token 和现有管理端列表页结构。
- 复制 `task_trace_id` / `request_id` 使用图标按钮或图标+文字按钮。
- 详情抽屉任务分组应优先展示可排障字段：任务类型、状态、耗时、关键节点、关联 request_id、错误码。
- 分页、指标卡、toast、confirm 约束见 `acceptance.md` 的横切 AC。

## 5. Golden Reference

- HTML 草图：`prototype/web/audit-log-task-trace.html`
- PNG Golden Reference：待后续设计确认后导出。
