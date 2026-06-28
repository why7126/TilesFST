---
created_at: 2026-06-28 16:04:18
title: 缺陷追踪
purpose: BUG-0030 Banner 列表页 UI 与用户管理页不一致
content: 记录分页、多余标题与当前显示统计行
owner: product
status: done
lifecycle_stage: archive
readiness: ready
note: merged fix-banner-admin-ui; /bug-opsx 2026-06-28 16:20:00
updated_at: 2026-06-28 19:40:42
---

# 缺陷追踪

## 1. 基本信息

```yaml
bug_id: BUG-0030-banner-list-ui-inconsistency
bug_name: banner-list-ui-inconsistency
severity: medium
status: done
iteration: sprint-003
related_change: fix-banner-admin-ui
related_requirement: REQ-0016-banner-management
related_bug:
suggested_fix_change: fix-banner-admin-ui
target_clients:
  web_admin: 是
environment: local|docker
lifecycle:
  captured: 2026-06-28 16:04:18
  generated: 2026-06-28 16:15:00
  completed: 2026-06-28 16:16:51
  reviewed: 2026-06-28 16:18:11
  approved: 2026-06-28 16:18:11
openspec_changes:
  - change_id: fix-banner-admin-ui
    type: fix
    status: archived
  opsx: 2026-06-28 16:20:00```

## 2. Readiness

| 文档 | 状态 |
|---|---|
| capture.md | done |
| bug.md | done |
| root-cause.md | done |
| workaround.md | done |
| acceptance.md | done |
| review.md | done |

**Readiness:** Ready — merged `fix-banner-admin-ui`

## 3. 分类结论

| 判断 | 结论 |
|---|---|
| 需求 vs 缺陷 | 缺陷（BUG） |
| 根因类型 | design / frontend-ui（原型 port 未对齐用户管理分页基准） |
| 修复面 | Web 管理端 Banner 列表页 section-head / table-toolbar / 分页 DOM |
| 建议 Change | `fix-banner-admin-ui`（建议与 BUG-0031–0036 合并） |

## 4. 变更记录

| 时间 | 事件 | 说明 |
|---|---|---|
| 2026-06-28 17:05:08 | `/sprint-propose` | 纳入 sprint-003 正式 Scope |
| 2026-06-28 16:20:00 | `/bug-opsx` | 创建 change `fix-banner-admin-ui`（合并 BUG-0030～0036） |
| 2026-06-28 16:18:11 | `/bug-review --approve` | REV-BUG-0030-001 通过；plan → review；status → approved |
| 2026-06-28 16:16:51 | `/bug-complete` | 补齐 root-cause、workaround、acceptance；status → pending_review |
| 2026-06-28 16:15:00 | `/bug-generate` | 生成 bug.md；status → draft |
| 2026-06-28 16:04:18 | `/bug-capture` | 记录 Banner 列表页分页与多余标题行 |
