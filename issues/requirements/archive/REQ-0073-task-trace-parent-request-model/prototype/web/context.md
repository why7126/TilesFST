---
requirement_id: REQ-0073-task-trace-parent-request-model
title: Task Trace 主请求与子请求关联模型 - Web 原型策略
status: approved
owner: product
created_at: 2026-07-26 13:03:43
updated_at: 2026-07-26 17:18:10
---

# Web 原型策略

本需求不新增独立页面，复用 `REQ-0069-upload-observability-trace-logs` 的管理端日志审计详情与上传控件原型方向，仅补充字段展示策略。

## 1. 日志详情补充

- 日志列表追踪列按 `request_id`、`client_request_id`、`task_trace_id` 顺序展示，表头保持单行，`Task Trace` 表头文案统一为 `task_trace_id`。
- 日志详情抽屉的「操作者」展示用户账号，不展示用户名称；列表与详情保持一致。
- 日志详情抽屉字段标签旁展示说明图标，鼠标 hover 或键盘 focus 时显示字段含义；tooltip 使用 fixed 浮层，不能被右侧抽屉边界裁切。
- Task Trace 分组展示 `task_trace_id`、`parent_request_id`、任务状态、任务类型和耗时。
- span 列表展示 `span_name`、状态、耗时、`request_id`、错误码和摘要。
- `parent_request_id`、`task_trace_id`、span `request_id` 均应支持复制；复制反馈使用 fixed toast 或等价固定层，不能造成布局位移。
- 历史数据缺少字段时展示“未记录”或隐藏关联入口，不展示误导性跳转。

## 2. 上传控件补充

- 上传状态仍保持 `idle → uploading → done / failed`。
- 上传开始后保留当前 `task_trace_id`；失败时在控件内展示错误，并保留可复制排障编号。
- 同会话上传成功后即时回显缩略图、文件卡片或媒体结果。

## 3. PNG / HTML

- 本 REQ 当前不要求新增独立 HTML 原型；后续 `/req-opsx` 若决定改动日志详情布局，再以 `REQ-0069` 原型为基线补充 HTML / PNG Golden Reference。
