---
created_at: 2026-06-27 21:33:13
title: 缺陷追踪
purpose: BUG-0021 侧边栏菜单图标无法区分
content: 记录管理端侧边栏收起后各菜单图标相同导致无法识别
owner: product
status: done
lifecycle_stage: archive
note: fix-sidebar-menu-icons-indistinguishable archived；Sprint-003 closed
iteration: sprint-003
readiness: ready
updated_at: 2026-06-28 19:41:09
---

# 缺陷追踪

## 1. 基本信息

```yaml
bug_id: BUG-0021-sidebar-menu-icons-indistinguishable
bug_name: sidebar-menu-icons-indistinguishable
severity: medium
status: done
iteration: sprint-003
related_requirement: REQ-0011-admin-sidebar-expand-collapse
related_bug: null
related_change: fix-sidebar-menu-icons-indistinguishable
suggested_fix_change: fix-sidebar-menu-icons-indistinguishable
target_clients:
  web_admin: 是
environment: local|docker
lifecycle:
  captured: 2026-06-27 21:33:13
  generated: 2026-06-27 21:37:11
  completed: 2026-06-27 21:40:26
  reviewed: 2026-06-27 21:42:20
  approved: 2026-06-27 21:42:20
  archived: 2026-06-28 19:39:54
openspec_changes:
  - change_id: fix-sidebar-menu-icons-indistinguishable
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

**Readiness:** Ready

## 3. 初步分类

| 判断 | 结论 |
|---|---|
| 需求 vs 缺陷 | 缺陷（REQ-0011 折叠交付后的 UX 缺口） |
| 根因类型 | design / frontend-ui（占位 icon 未升级为 per-menu 语义 SVG） |
| 修复面 | `admin-nav.ts`、`AdminSidebar.tsx`、`admin-home.css`、vitest |

## 4. 关联文档

| 文档 | 路径 |
|---|---|
| capture | `capture.md` |
| bug | `bug.md` |
| root-cause | `root-cause.md` |
| workaround | `workaround.md` |
| acceptance | `acceptance.md` |
| 父需求 | `issues/requirements/archive/REQ-0011-admin-sidebar-expand-collapse/` |
| UI 规范 | `rules/ui-design.md` |
| collapsed 原型 | `issues/requirements/archive/REQ-0011-admin-sidebar-expand-collapse/prototype/web/admin-sidebar-collapsed.html` |
| 侧栏组件 | `src/web/src/features/admin/components/AdminSidebar.tsx` |
| 导航配置 | `src/web/src/features/admin/data/admin-nav.ts` |

## 5. 变更记录

| 时间 | 事件 | 说明 |
|---|---|---|
| 2026-06-27 21:33:13 | `/capture` | 记录侧边栏菜单图标无法区分 |
| 2026-06-27 21:37:11 | `/bug-generate` | 生成 bug.md；status → draft |
| 2026-06-27 21:40:26 | `/bug-complete` | 补齐 root-cause、workaround、acceptance；Readiness → Ready |
| 2026-06-28 12:10:00 | `/opsx-archive` | change archived；admin-dashboard + web-client spec 已合并 |
| 2026-06-28 12:05:00 | `/sprint-apply` | Lucide 语义图标 + vitest；openspec status → applied |
| 2026-06-28 10:40:00 | `/bug-opsx` | 创建 fix-sidebar-menu-icons-indistinguishable；status proposed |
| 2026-06-28 10:35:00 | `/sprint-propose` | 纳入 sprint-003；status → in_sprint |
| 2026-06-27 21:42:20 | `/bug-review --approve` | REV-BUG-0021-001 评审通过 |
