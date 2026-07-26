---
requirement_id: REQ-0069-upload-observability-trace-logs
prototype_id: REQ-0069-task-trace-log-detail
title: 日志审计 Task Trace 详情抽屉原型说明
status: draft
created_at: 2026-07-25 11:45:49
updated_at: 2026-07-25 11:45:49
---

# 原型说明

## 目标

展示管理端日志审计详情抽屉如何承载 Task Trace 时间线。该原型用于后续 `/req-opsx` design 与 UI 验收对齐，不代表最终 React 实现。

## 页面结构

- 左侧：日志审计列表片段，包含任务追踪筛选输入、摘要指标、表格和分页区域。
- 右侧：日志详情抽屉，包含基础信息、任务摘要、任务时间线、关联请求和 metadata JSON。
- 时间线节点强调：节点名称、耗时、状态、关联 `request_id`，慢节点以 warning 状态标识。

## 关键验收点

- 列表筛选保留 `task_trace_id` 查询入口。
- 详情抽屉在 1440x1024 下不遮挡主要信息。
- `task_trace_id` 和 `request_id` 均有复制操作入口。
- 普通日志没有 `task_trace_id` 时，任务时间线分组应隐藏或显示 N/A。
- 样式后续实现必须使用 Design System semantic token，禁止裸 Hex。

## PNG 状态

PNG Golden Reference 待后续设计确认后导出；当前 HTML/context 作为需求阶段原型策略。
