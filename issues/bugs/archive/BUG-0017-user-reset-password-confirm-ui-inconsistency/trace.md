---
created_at: 2026-06-27 12:03:34
title: 缺陷追踪
purpose: BUG-0017 用户重置密码确认弹窗UI不一致
content: 记录重置密码确认框与类目启停确认框样式不对齐
owner: product
status: done
lifecycle_stage: archive
note: /opsx-archive fix-user-reset-password-confirm-ui
iteration: sprint-002
updated_at: 2026-06-27 22:33:15
---

# 缺陷追踪

## 1. 基本信息

```yaml
bug_id: BUG-0017-user-reset-password-confirm-ui-inconsistency
bug_name: user-reset-password-confirm-ui-inconsistency
severity: medium
status: done
iteration: sprint-002
related_requirement: REQ-0005-user-management
related_bug: BUG-0016-admin-list-status-action-confirm-missing
related_change: fix-user-reset-password-confirm-ui
suggested_fix_change: fix-user-reset-password-confirm-ui
target_clients:
  web_admin: 是
environment: local|docker
openspec_changes:
  - change_id: fix-user-reset-password-confirm-ui
    type: fix
    status: archived
    requirement_id: REQ-0005-user-management
    iteration: sprint-002
lifecycle:
  captured: 2026-06-27 12:03:34
  draft: 2026-06-27 13:28:24
  pending_review: 2026-06-27 13:29:34
  approved: 2026-06-27 13:31:00
  in_sprint: 2026-06-27 13:32:00
  applied: 2026-06-27 13:37:39
  done: 2026-06-27 13:40:00```

## 2. Readiness

| 文档 | 状态 |
|---|---|
| capture.md | done |
| bug.md | done |
| root-cause.md | done |
| workaround.md | done |
| acceptance.md | done |
| review.md | done |

**Readiness:** Done

## 3. OpenSpec

| Change | 状态 |
|---|---|
| `fix-user-reset-password-confirm-ui` | archived（2026-06-27） |

## 5. 变更记录

| 日期 | 动作 | 说明 |
|---|---|---|
| 2026-06-27 12:03:34 | `/capture` | 记录用户重置密码确认弹窗与类目启停弹窗 UI 不一致 |
| 2026-06-27 13:28:24 | `/bug-generate` | 生成 bug.md；trace → draft |
| 2026-06-27 13:29:34 | `/bug-complete` | 补齐 root-cause、workaround、acceptance；trace → pending_review |
| 2026-06-27 13:31:00 | `/bug-review` | 评审通过 → approved |
| 2026-06-27 13:32:00 | `/sprint-propose` | 纳入 sprint-002 正式规划 → in_sprint |
| 2026-06-27 13:34:57 | `/bug-opsx` | 创建 `fix-user-reset-password-confirm-ui`（proposed） |
| 2026-06-27 13:37:39 | `/opsx-apply` | 重置密码 confirm modal + Vitest 7/7 + build |
| 2026-06-27 13:40:00 | `/opsx-archive` | archived；`web-client` +1 requirement |

## 6. 后续动作

- 无（已闭环）；可选 Docker 手工冒烟重置密码 confirm
