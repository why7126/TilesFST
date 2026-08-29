---
bug_id: BUG-0145-admin-log-detail-field-overlap
title: 管理端日志详情长字段名和值重叠
severity: medium
status: done
owner:
discovered_at: 2026-08-26 23:53:45
environment: local
related_requirement:
related_change: fix-admin-log-detail-field-overlap
updated_at: 2026-08-27 08:16:35
created_at: 2026-08-27 00:01:34
---

# 现象

管理端日志审计页面打开日志详情抽屉后，部分长字段名会侵入右侧值列，形成字段名和值的视觉重叠。

当前已观察到的典型字段包括：

- `parent_behavior_event_id`
- `client_request_id`
- `behavior_trace_id`
- `task_trace_id`

这些字段本身承担请求链路、行为链路和 Task Trace 排障定位用途；一旦展示重叠，用户需要复制或肉眼识别链路 ID 时容易误读。

# 复现步骤

1. 打开管理端日志审计页面。
2. 选择一条包含 `parent_behavior_event_id`、`client_request_id`、`behavior_trace_id` 等长字段的请求日志。
3. 点击日志行查看详情，打开右侧「日志详情」抽屉。
4. 查看「基础信息」或 Request Snapshot 中的字段列表。
5. 观察长字段名是否覆盖、贴近或侵入右侧值列。

# 期望 vs 实际

期望：

- 日志详情字段名和值应分列清晰，字段名不会覆盖值。
- 长 snake_case 字段名在抽屉宽度有限时应通过换行、省略、调整列宽或堆叠布局保持可读。
- request_id、behavior_trace_id、task_trace_id 等排障字段应能完整识别，且不被字段名遮挡。
- 移动端或窄宽度抽屉下应保持合理的单列或换行展示，不出现遮挡。

实际：

- 日志详情抽屉中长字段名左列空间不足。
- `parent_behavior_event_id` 等字段名会向右溢出，侵入字段值展示区域。
- 字段名和值发生重叠后，链路 ID 的可读性下降，影响日志排障效率。

# 影响范围

- Web 管理端日志审计页面。
- 日志详情抽屉中的基础信息、请求信息和 Request Snapshot 字段列表。
- 请求日志、行为链路 ID、Task Trace 相关字段阅读体验。
- 管理员、开发者或运维人员基于日志详情定位异常链路的效率。

本缺陷不改变后端日志采集结果，不影响 API 响应结构、数据库表结构、小程序端、对象存储或 Orval 生成类型。

# 严重等级说明

严重等级为 `medium`。

该问题不阻断日志列表查询、详情打开或业务操作，但会直接影响日志详情的关键排障字段阅读。由于 `request_id`、`behavior_trace_id`、`parent_behavior_event_id` 和 `task_trace_id` 是串联请求日志、行为事件和任务链路的重要标识，展示重叠会降低异常定位效率，并增加人工误读风险。

# 初步定位

前置只读探索已定位到以下实现线索：

- `src/web/src/pages/admin/LogAuditPage.tsx` 中 `DetailSection` 和 `SnapshotRows` 使用 `detail-row` 渲染字段名和值。
- `src/web/src/features/admin/styles/log-audit.css` 中 `.detail-row` 使用固定两列布局，普通详情行为 `128px minmax(0, 1fr)`，Snapshot 行为 `112px minmax(0, 1fr)`。
- 字段名与字段说明图标使用 `.field-help-label` 组合展示，但长 snake_case 字段缺少足够的收缩、换行或截断保护。

这些线索说明问题更可能属于管理端详情抽屉字段布局样式缺陷，而不是数据采集或接口返回异常。
openspec_changes:
  - change_id: fix-admin-log-detail-field-overlap
    type: update
    status: archived
