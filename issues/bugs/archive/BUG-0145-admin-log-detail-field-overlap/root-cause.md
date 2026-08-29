---
bug_id: BUG-0145-admin-log-detail-field-overlap
root_cause_status: confirmed
root_cause_category: design
created_at: 2026-08-27 00:06:57
updated_at: 2026-08-27 00:06:57
---

# 根因状态

`confirmed`

# 直接原因

管理端日志详情抽屉的字段行使用固定两列 grid 布局，左侧字段名列宽不足以容纳 `parent_behavior_event_id` 等长 snake_case 字段名及字段说明图标。

当字段名长度超过左列宽度时，字段名内容没有被换行、截断或单独收缩保护，导致文本向右溢出并侵入右侧字段值列。

# 根本原因

日志详情字段布局最初按普通中文字段或短英文标签设计，未把日志链路字段的真实长度纳入约束，例如：

- `parent_behavior_event_id`
- `client_request_id`
- `behavior_trace_id`
- `task_trace_id`

这些字段用于排障链路定位，天然较长；详情抽屉又是固定窄宽度区域。当前样式只给右侧值列设置了 `minmax(0, 1fr)` 和换行能力，但没有为左侧字段名列、字段名文本和字段说明图标组合建立同等的响应式溢出策略。

# 触发条件

满足以下条件时容易触发重叠：

1. 打开 Web 管理端日志审计页面的日志详情抽屉。
2. 当前日志详情包含较长字段名，如 `parent_behavior_event_id`。
3. 详情行使用两列布局展示字段名和值。
4. 左侧字段名列宽不足，字段名和说明图标组合无法在列内正常换行或收缩。

# 证据链

| 证据类型 | 证据入口 | 说明 |
|---|---|---|
| 截图证据 | 用户提供的日志详情截图 | 截图中 `parent_behavior_event_id` 字段名与右侧 `be:...` 字段值发生重叠，现象与本 BUG 描述一致。 |
| 代码定位 | `src/web/src/pages/admin/LogAuditPage.tsx:541` | `DetailSection` 将字段名和值渲染为同一个 `.detail-row`，左侧 `dt` 使用 `FieldHelp`，右侧 `dd` 展示值。 |
| 代码定位 | `src/web/src/pages/admin/LogAuditPage.tsx:409` | `SnapshotRows` 同样使用 `.detail-row` 渲染 Request Snapshot 字段，因此基础信息和 Snapshot 区域共享同类布局风险。 |
| 样式定位 | `src/web/src/features/admin/styles/log-audit.css:497` | 普通详情行固定为 `grid-template-columns: 128px minmax(0, 1fr)`，左列宽度不足以容纳长字段名和说明图标。 |
| 样式定位 | `src/web/src/features/admin/styles/log-audit.css:606` | Snapshot 行固定为 `grid-template-columns: 112px minmax(0, 1fr)`，左列更窄，更容易触发长字段名溢出。 |
| 样式定位 | `src/web/src/features/admin/styles/log-audit.css:508` | `.field-help-label` 使用 `inline-flex` 承载字段名和图标，但字段名文本本身没有换行、省略或 `overflow-wrap` 约束。 |
| 样式定位 | `src/web/src/features/admin/styles/log-audit.css:561` | 右侧值列 `dd` 具备 `word-break: break-word`，说明当前换行保护主要作用于值列，而非字段名列。 |

# 影响范围

- Web 管理端日志审计页面。
- 日志详情抽屉的基础信息、请求信息、Request Snapshot 等字段列表。
- `request_id`、`client_request_id`、`behavior_trace_id`、`parent_behavior_event_id`、`task_trace_id` 等排障字段的阅读体验。

本问题不涉及后端日志采集、数据库结构、API 响应、Orval 生成、小程序端或对象存储。

# 验证方式

修复前验证：

1. 打开包含 `parent_behavior_event_id` 的日志详情抽屉。
2. 在基础信息或 Request Snapshot 中观察长字段名和值是否发生视觉重叠。
3. 对照代码样式，确认详情行左列宽度固定且字段名无换行/截断保护。

修复后验证：

1. 同一日志详情中 `parent_behavior_event_id` 字段名和值不再重叠。
2. `client_request_id`、`behavior_trace_id`、`task_trace_id` 等长字段在基础信息和 Request Snapshot 中均可读。
3. 桌面抽屉宽度和移动端窄宽度下，字段名和值通过合理换行、列宽调整或单列布局保持不遮挡。
4. 日志详情字段说明图标仍可聚焦和悬浮展示 tooltip，不因布局调整丢失可访问性。

# 人工补证步骤

当前根因已由截图和代码定位闭环确认。修复实现后，仍建议补充浏览器截图或 Playwright 截图作为验收证据，覆盖桌面抽屉与移动端窄宽度两个视口。
