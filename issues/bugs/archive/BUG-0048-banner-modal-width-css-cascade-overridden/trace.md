---
created_at: 2026-06-28 18:10:30
title: 缺陷追踪
purpose: BUG-0048 Banner 弹窗 880px 被 modal-card 层叠覆盖
content: BUG-0040 follow-up；CSS 特异性/顺序导致 880px 未生效
owner: product
status: done
lifecycle_stage: archive
readiness: ready
note: follow-up of BUG-0040；explore 已定位层叠根因
updated_at: 2026-06-28 19:40:42
---

# 缺陷追踪

## 1. 基本信息

```yaml
bug_id: BUG-0048-banner-modal-width-css-cascade-overridden
bug_name: banner-modal-width-css-cascade-overridden
severity: medium
status: done
iteration: sprint-003
related_requirement: REQ-0016-banner-management
related_bug: BUG-0040-banner-modal-width-too-narrow
related_change: fix-banner-list-and-modal-ui
suggested_fix_change: fix-banner-modal-width-css-cascade
target_clients:
  web_admin: 是
environment: local|docker
lifecycle:
  captured: 2026-06-28 18:10:30
  generated: 2026-06-28 18:37:24
  completed: 2026-06-28 18:42:00
  reviewed: 2026-06-28 18:44:30
openspec_changes:
  - change_id: fix-banner-modal-width-css-cascade
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

## 3. 初步分类

| 判断 | 结论 |
|---|---|
| 需求 vs 缺陷 | 缺陷（BUG-0040 修复未闭环） |
| 根因类型 | code / frontend-css（双类名 + 全局 modal-card 重复定义） |
| 修复面 | `BannerFormModal.tsx`、可选 `banner-management.css` 特异性；Vitest 层叠断言 |
| 是否回归 | 是（相对 BUG-0040 验收意图） |

## 4. 变更记录

| 时间 | 事件 | 说明 |
|---|---|---|
| 2026-06-28 18:10:30 | `/bug-capture` | BUG-0040 follow-up；记录 880px CSS 层叠被 520px 覆盖 |
| 2026-06-28 18:37:24 | `/bug-generate` | 生成 bug.md；status → draft |
| 2026-06-28 18:42:00 | `/bug-complete` | 补齐 root-cause、workaround、acceptance；status → pending_review |
| 2026-06-28 18:44:30 | `/bug-review --approve` | 评审通过；status → approved |
| 2026-06-28 18:46:00 | `/bug-opsx` | 创建 fix-banner-modal-width-css-cascade |
| 2026-06-28 18:53:52 | `/opsx-apply` | 移除 modal-card 双类名；Vitest CSS 栈断言；build pass |
