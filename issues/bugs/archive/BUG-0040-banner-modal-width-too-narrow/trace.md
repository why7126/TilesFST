---
created_at: 2026-06-28 17:28:15
title: 缺陷追踪
purpose: BUG-0040 Banner 弹窗宽度偏小
content: 记录 Banner 弹窗宽度未对齐 SKU 弹窗基准
owner: product
status: done
lifecycle_stage: archive
readiness: ready
note: follow-up BUG-0048（880px 层叠未生效）；fix-banner-list-and-modal-ui 待补修 + archive
updated_at: 2026-06-28 19:40:42
---

# 缺陷追踪

## 1. 基本信息

```yaml
bug_id: BUG-0040-banner-modal-width-too-narrow
bug_name: banner-modal-width-too-narrow
severity: medium
status: done
iteration: sprint-003
related_requirement: REQ-0016-banner-management
related_bug: BUG-0039-banner-list-display-position-column
related_change: fix-banner-list-and-modal-ui
suggested_fix_change: fix-banner-list-and-modal-ui
target_clients:
  web_admin: 是
environment: local|docker
lifecycle:
  captured: 2026-06-28 17:28:15
  generated: 2026-06-28 17:34:12
  completed: 2026-06-28 17:43:07
  reviewed: 2026-06-28 17:44:19
  approved: 2026-06-28 17:44:19
  opsx: 2026-06-28 17:46:46
openspec_changes:
  - change_id: fix-banner-list-and-modal-ui
    type: fix
    status: archived```

## 2. Readiness

| 文档 | 状态 |
|---|---|
| capture.md | done |
| bug.md | done |
| root-cause.md | done |
| workaround.md | done |
| acceptance.md | done |
| review.md | done |

**Readiness:** Ready — REV-BUG-0040-001 通过；可 `/bug-opsx`

## 4. 变更记录

| 时间 | 事件 | 说明 |
|---|---|---|
| 2026-06-28 18:10:30 | follow-up | 创建 BUG-0048（modal-card 层叠覆盖 880px） |
| 2026-06-28 18:02:30 | `/opsx-apply` | fix-banner-list-and-modal-ui 实现完成；880px 层叠未生效 |
| 2026-06-28 18:02:00 | `/sprint-propose` | 纳入 sprint-003 正式 Scope |
| 2026-06-28 17:46:46 | `/bug-opsx` | 创建 change `fix-banner-list-and-modal-ui`（合并 BUG-0039、BUG-0040） |
| 2026-06-28 17:44:19 | `/bug-review --approve` | REV-BUG-0040-001；plan → review；880px 策略确认；status → approved |
| 2026-06-28 17:43:07 | `/bug-complete` | 补齐 root-cause、workaround、acceptance；status → pending_review |
| 2026-06-28 17:34:12 | `/bug-generate` | 生成 bug.md；status → draft |
| 2026-06-28 17:28:15 | `/bug-capture` | 记录 Banner 弹窗宽度应参照 SKU 弹窗调整 |
