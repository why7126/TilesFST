---
created_at: 2026-08-27 00:00:00
updated_at: 2026-08-27 00:00:00
---

# 测试计划

## 前端回归

- 运行日志审计页面相关 Vitest / Testing Library 测试，覆盖详情抽屉渲染、字段说明 tooltip 和 Request Snapshot 展示。
- 若现有测试未覆盖长字段名，新增最小 fixture：`parent_behavior_event_id`、`client_request_id`、`behavior_trace_id`、`task_trace_id` 与长 ID 值同时出现。
- 检查字段说明按钮保留 `aria-label` 或等价可访问名称。

## 视觉验收

- 使用 Playwright 或等价浏览器工具打开 `/admin/logs`，选择包含长链路字段的日志详情。
- 记录桌面视口截图，确认基础信息与 Request Snapshot 中字段名和值不重叠。
- 记录窄宽度或移动端视口截图，确认抽屉可滚动、可关闭、无横向失控滚动。

## 治理校验

- 运行 `python scripts/validate-openspec-language.py`。
- 运行 `openspec validate fix-admin-log-detail-field-overlap --strict`。
- 运行 Design System 或样式校验，确认未新增裸 Hex。

## N/A 校验

- API：N/A，本次不修改请求、响应、错误码或 OpenAPI。
- DB：N/A，本次不修改 SQLite/MySQL schema、迁移、索引或日志采集字段。
- Orval：N/A，本次不修改接口契约。
- Docker Compose：N/A，本次不修改部署、端口、环境变量或容器配置。

