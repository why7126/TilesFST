---
created_at: 2026-06-28 16:04:18
title: 缺陷追踪
purpose: BUG-0031 Banner 弹窗图片模块多余首行文案
content: 记录自定义上传/SKU主图首行说明文案应移除
owner: product
status: done
lifecycle_stage: archive
readiness: ready
note: REV-BUG-0031-002 复审通过；合并 fix-banner-admin-ui
updated_at: 2026-06-28 19:40:42
---

# 缺陷追踪

## 1. 基本信息

```yaml
bug_id: BUG-0031-banner-modal-image-section-label
bug_name: banner-modal-image-section-label
severity: low
status: done
iteration: sprint-003
related_requirement: REQ-0016-banner-management
related_change: fix-banner-admin-ui
related_bug: BUG-0032-banner-modal-upload-button-label
suggested_fix_change: fix-banner-admin-ui
target_clients:
  web_admin: 是
environment: local|docker
lifecycle:
  captured: 2026-06-28 16:04:18
  generated: 2026-06-28 16:45:00
  completed: 2026-06-28 16:46:00
  reviewed: 2026-06-28 16:25:05
  approved: 2026-06-28 16:25:05
openspec_changes:
  - change_id: fix-banner-admin-ui
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

**Readiness:** Ready — 可 `/opsx-apply fix-banner-admin-ui` 或纳入 Sprint

## 3. 变更记录

| 时间 | 事件 | 说明 |
|---|---|---|
| 2026-06-28 17:05:08 | `/sprint-propose` | 纳入 sprint-003 正式 Scope |
| 2026-06-28 16:25:05 | `/bug-review --approve` | REV-BUG-0031-002 复审通过 |
| 2026-06-28 16:46:00 | `/bug-complete` | 刷新 root-cause / workaround / acceptance |
| 2026-06-28 16:45:00 | `/bug-generate` | 刷新 bug.md |
| 2026-06-28 16:20:00 | `/bug-opsx` | 创建 change `fix-banner-admin-ui` |
| 2026-06-28 16:20:00 | `/bug-review --approve` | REV-BUG-0031-001（已被 002 取代） |
| 2026-06-28 16:04:18 | `/bug-capture` | 记录 Banner 图片模块首行文案冗余 |
