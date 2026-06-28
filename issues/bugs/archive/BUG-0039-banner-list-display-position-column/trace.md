---
created_at: 2026-06-28 17:28:15
title: 缺陷追踪
purpose: BUG-0039 Banner 列表展示位置未独立成列
content: 记录第一列 Banner 标题与展示位置挤在同一列
owner: product
status: done
lifecycle_stage: archive
readiness: ready
note: fix-banner-list-and-modal-ui applied；待 opsx-archive
updated_at: 2026-06-28 19:40:42
---

# 缺陷追踪

## 1. 基本信息

```yaml
bug_id: BUG-0039-banner-list-display-position-column
bug_name: banner-list-display-position-column
severity: medium
status: done
iteration: sprint-003
related_requirement: REQ-0016-banner-management
related_bug: BUG-0040-banner-modal-width-too-narrow
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

**Readiness:** Ready — REV-BUG-0039-001 通过；可 `/bug-opsx`

## 4. 变更记录

| 时间 | 事件 | 说明 |
|---|---|---|
| 2026-06-28 18:02:30 | `/opsx-apply` | fix-banner-list-and-modal-ui 实现完成；待 archive |
| 2026-06-28 18:02:00 | `/sprint-propose` | 纳入 sprint-003 正式 Scope |
| 2026-06-28 17:46:46 | `/bug-opsx` | 创建 change `fix-banner-list-and-modal-ui`（合并 BUG-0039、BUG-0040） |
| 2026-06-28 17:44:19 | `/bug-review --approve` | REV-BUG-0039-001；plan → review；status → approved |
| 2026-06-28 17:43:07 | `/bug-complete` | 补齐 root-cause、workaround、acceptance；status → pending_review |
| 2026-06-28 17:34:12 | `/bug-generate` | 生成 bug.md；status → draft |
| 2026-06-28 17:28:15 | `/bug-capture` | 记录 Banner 列表第一列标题与展示位置混排 |
