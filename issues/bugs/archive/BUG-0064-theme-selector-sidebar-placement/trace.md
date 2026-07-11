---
created_at: 2026-07-11 19:29:34
title: 缺陷追踪
purpose: BUG-0064 界面主题选择器位置未放在侧边栏用户头像上方
content: 记录管理端主题选择器位置与期望侧边栏布局不一致的问题
owner: product
status: done
lifecycle_stage: archive
updated_at: 2026-07-11 20:05:04
---

# 缺陷追踪

## 1. 基本信息

```yaml
bug_id: BUG-0064-theme-selector-sidebar-placement
bug_name: theme-selector-sidebar-placement
severity: medium
status: done
related_requirement: REQ-0020-theme-comfort-refine
related_bug:
target_clients:
  web_admin: 是
environment: local|docker
lifecycle_stage: review
lifecycle:
  captured: 2026-07-11 19:29:34
  draft: 2026-07-11 19:31:56
  enriching: 2026-07-11 19:34:59
  pending_review: 2026-07-11 19:34:59
  approved: 2026-07-11 19:38:21
iteration: sprint-006
suggested_fix_change: fix-theme-selector-sidebar-placement
openspec_changes:
  - change_id: fix-theme-selector-sidebar-placement
    type: fix
    status: archived
```

## 2. Readiness

| 文档 | 状态 |
|---|---|
| capture.md | done |
| bug.md | done |
| root-cause.md | done |
| workaround.md | done |
| acceptance.md | done |
| review.md | done |

**Readiness:** Approved — 可 `/bug-opsx`

## 3. 变更记录

| 时间 | 事件 | 说明 |
|---|---|---|
| 2026-07-11 19:29:34 | `/capture` | 记录界面主题选择器应移动到侧边栏用户头像上方 |
| 2026-07-11 19:31:56 | `/bug-generate` | 生成 bug.md；trace → draft |
| 2026-07-11 19:34:59 | `/bug-complete` | 补齐 root-cause、workaround、acceptance；trace → pending_review |
| 2026-07-11 19:38:21 | `/bug-review --approve` | 评审通过；status → approved |
| 2026-07-11 19:41:11 | `/bug-opsx` | 创建 OpenSpec change `fix-theme-selector-sidebar-placement` |
