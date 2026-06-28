---
created_at: 2026-06-28 17:53:48
title: 缺陷追踪
purpose: BUG-0047 系统设置保存提示导致页面位移
content: 记录保存设置成功 tip 推挤下方内容
owner: product
status: done
lifecycle_stage: archive
readiness: ready
iteration: sprint-003
updated_at: 2026-06-28 19:40:42
---

# 缺陷追踪

## 1. 基本信息

```yaml
bug_id: BUG-0047-system-settings-save-tip-layout-shift
bug_name: system-settings-save-tip-layout-shift
severity: medium
status: done
iteration: sprint-003
related_requirement: REQ-0017-system-settings
related_bug: BUG-0015-admin-list-status-tips-layout-shift
related_change: fix-system-settings-save-tip-layout-shift
suggested_fix_change: fix-system-settings-save-tip-layout-shift
target_clients:
  web_admin: 是
environment: local|docker
lifecycle:
  captured: 2026-06-28 17:53:48
  generated: 2026-06-28 18:06:17
  completed: 2026-06-28 18:35:49
  reviewed: 2026-06-28 18:41:44
  approved: 2026-06-28 18:41:44
  opsx: 2026-06-28 18:45:00
openspec_changes:
  - change_id: fix-system-settings-save-tip-layout-shift
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

**Readiness:** Ready

## 4. 变更记录

| 时间 | 事件 | 说明 |
|---|---|---|
| 2026-06-28 17:53:48 | `/capture` | 记录保存成功 tip 导致下方内容 layout shift |
| 2026-06-28 18:06:17 | `/bug-generate` | 生成 bug.md；status → draft |
| 2026-06-28 18:35:49 | `/bug-complete` | 补齐 root-cause、workaround、acceptance；status → pending_review |
| 2026-06-28 18:41:44 | `/bug-review --approve` | REV 通过；plan → review；status → approved |
| 2026-06-28 18:45:00 | `/bug-opsx` | 创建 change `fix-system-settings-save-tip-layout-shift` |
| 2026-06-28 19:09:15 | `/sprint-propose` | 纳入 sprint-003 |
