---
bug_id: BUG-0059-user-password-copy-not-working
status: done
lifecycle_stage: archive
severity: high
created_at: 2026-07-05 20:30:59
updated_at: 2026-07-06 16:06:34
---

# 缺陷追踪

## 基本信息

```yaml
bug_id: BUG-0059-user-password-copy-not-working
bug_name: user-password-copy-not-working
severity: high
status: done
owner: product
source: 反馈
iteration: sprint-005
related_requirement: REQ-0005-user-management
related_bug: null
related_change: fix-user-password-copy-not-working
suggested_fix_change: fix-user-password-copy-not-working
target_clients:
  web_admin: 是
environment: local|docker
openspec_changes:
  - change_id: fix-user-password-copy-not-working
    type: fix
    status: archived
lifecycle:
  captured: 2026-07-05 20:30:59
  draft: 2026-07-06 14:54:16
  enriching: 2026-07-06 14:56:29
  pending_review: 2026-07-06 14:56:29
  approved: 2026-07-06 15:17:18
  in_sprint: 2026-07-06 15:23:04
  applied: 2026-07-06 15:40:09
  done: 2026-07-06 16:06:34
readiness: Ready
readiness_notes: 已完成 /opsx-archive；缺陷修复闭环，已归档。
documents:
  - capture.md
  - bug.md
  - root-cause.md
  - workaround.md
  - acceptance.md
  - review.md
  - logs/README.md
  - screenshots/README.md
```

## 变更记录

| 日期 | 动作 | 说明 |
|---|---|---|
| 2026-07-06 16:06:34 | lifecycle-stage-migrate | review → archive（/opsx-archive fix-user-password-copy-not-working） |
| 2026-07-05 20:30:59 | `/capture` | 记录创建用户与重置密码两个一次性密码弹窗中复制密码功能均未生效 |
| 2026-07-06 14:54:16 | `/bug-generate` | 生成 `bug.md`，状态进入 draft |
| 2026-07-06 14:56:29 | `/bug-complete` | 补齐 root-cause、workaround、acceptance 与附件目录占位，状态进入 pending_review |
| 2026-07-06 15:17:18 | `/bug-review --approve` | 评审通过，允许进入 `/bug-opsx` 与 Sprint 正式规划 |
| 2026-07-06 15:18:07 | lifecycle-stage-migrate | plan → review（/bug-review --approve） |
| 2026-07-06 15:23:04 | `/sprint-propose` | 纳入 sprint-005，状态进入 in_sprint；Change 待 `/bug-opsx` 创建 |
| 2026-07-06 15:40:09 | `/opsx-apply` | 完成复制成功/失败/fallback 修复，相关 Vitest 通过；Change 状态进入 applied |
| 2026-07-06 15:33:45 | `/bug-opsx` | 创建 `fix-user-password-copy-not-working`，状态 proposed |
| 2026-07-06 16:06:23 | workflow-sync | 状态同步为 done（Change archived） |
