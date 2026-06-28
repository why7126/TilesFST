---
created_at: 2026-06-28 12:47:55
title: 缺陷追踪
purpose: BUG-0024 修改密码弹窗错误提示字段错位
content: 记录新密码校验错误显示在原密码字段下方
owner: product
status: done
lifecycle_stage: archive
readiness: ready
updated_at: 2026-06-28 19:40:42
---

# 缺陷追踪

## 1. 基本信息

```yaml
bug_id: BUG-0024-change-password-error-wrong-field
bug_name: change-password-error-wrong-field
severity: medium
status: done
iteration: sprint-003
related_requirement: REQ-0014-profile-page
related_bug: BUG-0025-change-password-toggle-button-misalignment
related_change: fix-change-password-modal-errors
suggested_fix_change: fix-change-password-modal-errors
target_clients:
  web_admin: 是
environment: local|docker
openspec_changes:
  - change_id: fix-change-password-modal-errors
    type: fix
    status: archived
lifecycle:
  captured: 2026-06-28 12:47:55
  generated: 2026-06-28 12:53:34
  completed: 2026-06-28 12:55:16
  reviewed: 2026-06-28 12:56:52
  approved: 2026-06-28 12:56:52
  opsx: 2026-06-28 12:58:01```

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

## 3. 变更记录

| 时间 | 事件 | 说明 |
|---|---|---|
| 2026-06-28 13:00:49 | `/sprint-propose` | 纳入 sprint-003 |
| 2026-06-28 12:58:01 | `/bug-opsx` | 创建 OpenSpec change `fix-change-password-modal-errors` |
| 2026-06-28 12:56:52 | `/bug-review --approve` | REV-BUG-0024-001 通过；status → approved；plan → review |
| 2026-06-28 12:55:16 | `/bug-complete` | 补齐 root-cause、workaround、acceptance；status → pending_review |
| 2026-06-28 12:53:34 | `/bug-generate` | 生成 bug.md；status → draft |
| 2026-06-28 12:47:55 | `/bug-capture` | 记录修改密码弹窗新密码错误提示显示在原密码字段下方 |
