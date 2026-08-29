---
bug_id: BUG-0145-admin-log-detail-field-overlap
acceptance_status: passed
created_at: 2026-08-27 00:06:57
updated_at: 2026-08-28 16:21:48
---

# 验收目标

修复 Web 管理端日志详情抽屉中长字段名和值重叠的问题，确保链路排障字段在桌面和窄宽度场景下均清晰可读。

# 回归验收项

## AC-001 基础信息长字段名和值不重叠

给定一条包含 `parent_behavior_event_id`、`client_request_id`、`behavior_trace_id` 的请求日志，当打开日志详情抽屉时：

- 字段名不得侵入字段值展示区域。
- 字段值不得被字段名或字段说明图标遮挡。
- 字段名和值之间应保留可辨识间距或采用合理换行/堆叠布局。

## AC-002 Request Snapshot 长字段保持可读

给定 Request Snapshot 中包含 `behavior_trace_id`、`parent_behavior_event_id` 等长字段，当展开日志详情时：

- Snapshot 区域字段名和值不应重叠。
- 长字段名可通过换行、省略或响应式列宽保持布局稳定。
- 长 ID 值仍应可完整查看或复制，不因修复被裁切到不可读。

## AC-003 窄宽度和移动端布局不遮挡

给定浏览器宽度缩小或移动端视口，当打开日志详情抽屉时：

- 字段名和值应切换为合理单列或换行展示。
- `parent_behavior_event_id` 等最长字段不应覆盖下一行或右侧值。
- 抽屉主体滚动不应出现横向不可控溢出。

## AC-004 字段说明交互保留

给定字段名旁存在说明图标，当用户悬浮或键盘聚焦说明图标时：

- tooltip 仍可展示字段说明。
- 图标不会挤压字段值导致新的重叠。
- 键盘聚焦状态和 `aria-label` 不应丢失。

## AC-005 影响边界保持在 Web 管理端

修复完成后应确认：

- 不改变后端 API、数据库、日志采集字段、OpenAPI 或 Orval 生成物。
- 不影响小程序端和对象存储。
- 不新增裸 Hex 样式，继续使用管理端现有 semantic token 或 CSS 变量。

## AC-006 回归测试与视觉证据

修复完成后应补充或提供以下验证：

- 至少一个前端测试或组件级断言覆盖日志详情中长字段名和值同时存在的场景。
- 至少一张桌面视口截图或等价 Playwright 截图，证明 `parent_behavior_event_id` 不再和值重叠。
- 如涉及响应式样式，补充窄宽度或移动端截图/测试。

# 验收结果回填

```yaml
acceptance_status: not_started
accepted_at: null
accepted_by: null
source_change: null
source_sprint: null
evidence: []
failed_items: []
source_event: bug.complete
notes: 由 Workflow Sync 根据 Change/Sprint 状态回填。
```

## 验收结果回填

```yaml
acceptance_status: passed
accepted_at: 2026-08-27 08:16:35
accepted_by: workflow-sync
source_change: fix-admin-log-detail-field-overlap
source_sprint: sprint-026
evidence: []
failed_items: []
source_event: sprint.archive
notes: 由 Workflow Sync 根据 Change/Sprint 状态回填。
```

