---
bug_id: BUG-0145-admin-log-detail-field-overlap
status: done
created_at: 2026-08-26 23:53:45
updated_at: 2026-08-27 08:16:40
severity_hint: medium
environment: local
related_requirement:
related_bug:
lifecycle_stage: plan
---

# 现象

管理端日志详情抽屉中，长字段名和值发生视觉重叠。`parent_behavior_event_id`、`client_request_id`、`behavior_trace_id` 等字段名会侵入右侧值列，导致日志排障时难以准确阅读链路 ID。

# 复现步骤

1. 打开管理端日志审计页面。
2. 选择一条包含 `parent_behavior_event_id`、`client_request_id`、`behavior_trace_id` 等长字段的请求日志。
3. 点击查看日志详情，打开右侧详情抽屉。
4. 查看「基础信息」或 Request Snapshot 等字段列表中的长字段名和值展示。

# 期望 vs 实际

- 期望：字段名和值分列清晰展示，长字段名不会覆盖或侵入值列；长 ID 可以完整阅读、换行或以可理解方式展示。
- 实际：长字段名在详情抽屉左列宽度不足时溢出，与右侧值重叠，影响 request_id、behavior_trace_id 和相关链路字段的排障阅读。

# 影响范围

- Web 管理端日志审计页面的日志详情抽屉。
- 请求日志、行为链路 ID、Task Trace 相关字段阅读体验。
- 不影响后端 API、数据库、小程序、对象存储或 Orval 生成物。

# 初步线索

- 只读探索已定位到 `src/web/src/pages/admin/LogAuditPage.tsx` 的 `DetailSection` 和 `SnapshotRows` 使用 `detail-row` 渲染字段名和值。
- `src/web/src/features/admin/styles/log-audit.css` 中 `.detail-row` 使用固定两列布局，普通详情行为 `128px minmax(0, 1fr)`，Snapshot 行为 `112px minmax(0, 1fr)`。
- 字段名与字段说明图标使用 `.field-help-label` 组合展示，但长 snake_case 字段没有充分的收缩、换行或截断保护。

# 建议验收或复现要点

- [ ] 打开包含 `parent_behavior_event_id` 的日志详情，字段名和值不再重叠。
- [ ] `client_request_id`、`behavior_trace_id`、`task_trace_id` 等长字段在基础信息和 Request Snapshot 中均可读。
- [ ] 移动端或窄宽度抽屉下字段名和值改为合理堆叠或换行，不出现遮挡。
- [ ] 修复仅影响 Web 管理端样式，不改变 API、数据库、日志采集数据或 Orval 类型。

# 附件

- 用户提供截图：日志详情抽屉中 `parent_behavior_event_id` 字段名和值发生重叠。
