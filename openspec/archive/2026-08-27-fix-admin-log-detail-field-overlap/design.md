---
created_at: 2026-08-27 00:00:00
updated_at: 2026-08-27 00:00:00
---

# 设计说明

## 根因结论

BUG-0145 的根因状态为 `confirmed`。管理端日志详情抽屉的字段行使用固定两列 grid 布局，左侧字段名列宽不足以容纳 `parent_behavior_event_id` 等长 snake_case 字段名及字段说明图标；字段名缺少换行、截断或收缩保护，导致内容向右溢出并覆盖值列。

证据入口：

- 用户提供的日志详情截图：`parent_behavior_event_id` 与右侧 `be:...` 值发生重叠。
- `src/web/src/pages/admin/LogAuditPage.tsx`：`DetailSection` 与 `SnapshotRows` 均使用 `.detail-row` 渲染字段名和值。
- `src/web/src/features/admin/styles/log-audit.css`：普通详情行固定为 `128px minmax(0, 1fr)`，Snapshot 行固定为 `112px minmax(0, 1fr)`，值列具备换行保护但字段名列缺少同等保护。

## 修复方案

- 调整日志详情字段行布局，使左侧字段名和右侧值列在有限宽度内保持明确边界。
- 对 `.field-help-label` 或等价字段说明组合增加收缩、换行、截断、tooltip/title 或等价可访问策略。
- 对 Request Snapshot 行使用同等布局保护，避免只修基础信息而遗漏 Snapshot。
- 在窄宽度视口下切换为单列或等价响应式布局，避免抽屉内容横向失控滚动。
- 保持字段值的长 ID 可读或可复制，不因字段名修复被裁切到不可识别。

## 设计约束

- 必须复用管理端现有结构和 Design System 语义 token，不新增裸 Hex 样式。
- 必须保留字段说明图标的 hover 与 focus tooltip 能力，不能用隐藏图标的方式规避重叠。
- 不修改 API schema、数据库 schema、日志采集字段、行为事件或 Task Trace 语义。
- 不手改 Orval generated 文件。

## 测试策略

- 使用前端测试或组件级测试覆盖包含 `parent_behavior_event_id`、`client_request_id`、`behavior_trace_id`、`task_trace_id` 的日志详情数据。
- 使用 Playwright 或等价浏览器截图覆盖桌面抽屉和窄宽度视口。
- 断言字段说明按钮仍具备可访问名称或可聚焦交互。
- 运行 Design System 或前端样式相关校验，确认没有新增裸 Hex。

## 风险与取舍

- 若只扩大左列宽度，短字段会浪费空间且窄屏仍可能重叠；优先采用响应式和溢出策略。
- 若只对值列换行，字段名仍可能覆盖值列；字段名列和字段说明组合必须共同受控。
- 若采用纯省略而无完整值入口，长字段名可读性会下降；应通过 title、tooltip、换行或等价方式保留完整语义。

