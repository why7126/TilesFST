---
created_at: 2026-06-28 17:46:25
title: 缺陷追踪
purpose: BUG-0041 侧边栏用户菜单未显示头像
content: 记录管理端侧栏底部 AdminUserMenu 未展示用户头像
owner: product
status: done
lifecycle_stage: archive
readiness: ready
updated_at: 2026-06-28 19:40:42
---

# 缺陷追踪

## 1. 基本信息

```yaml
bug_id: BUG-0041-sidebar-user-menu-avatar-missing
bug_name: sidebar-user-menu-avatar-missing
severity: medium
status: done
iteration: null
related_requirement: REQ-0014-profile-page
related_bug: BUG-0019-user-modal-avatar-upload-display
related_change: fix-sidebar-user-menu-avatar
suggested_fix_change: fix-sidebar-user-menu-avatar
target_clients:
  web_admin: 是
environment: local|docker
lifecycle:
  captured: 2026-06-28 17:46:25
  generated: 2026-06-28 18:02:20
  completed: 2026-06-28 18:05:06
  reviewed: 2026-06-28 18:35:30
  approved: 2026-06-28 18:35:30
openspec_changes:
  - change_id: fix-sidebar-user-menu-avatar
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

**Readiness:** Ready — REV-BUG-0041-001 评审通过；可 `/bug-opsx`

## 3. 初步分类

| 判断 | 结论 |
|---|---|
| 需求 vs 缺陷 | 缺陷（REQ-0014 交付后侧栏 UX 一致性缺口） |
| 根因类型 | code / frontend-ui（渲染未实现 + Layout 未传 avatar_url） |
| 修复面 | `AdminLayout.tsx`、`AdminUserMenu.tsx`、`admin-home.css`、vitest |
| 是否回归 | 否 |

## 4. 关联文档

| 文档 | 路径 |
|---|---|
| capture | `capture.md` |
| bug | `bug.md` |
| root-cause | `root-cause.md` |
| workaround | `workaround.md` |
| acceptance | `acceptance.md` |
| 父需求 | `issues/requirements/archive/REQ-0014-profile-page/` |
| 参考 BUG | `issues/bugs/archive/BUG-0019-user-modal-avatar-upload-display/` |
| 侧栏组件 | `src/web/src/features/admin/components/AdminUserMenu.tsx` |
| Layout | `src/web/src/pages/admin/AdminLayout.tsx` |
| 列表 avatar 参考 | `src/web/src/pages/admin/UserManagementPage.tsx` |

## 5. 变更记录

| 时间 | 事件 | 说明 |
|---|---|---|
| 2026-06-28 18:37:10 | `/bug-opsx` | 创建 fix-sidebar-user-menu-avatar；openspec status → proposed |
| 2026-06-28 18:35:30 | `/bug-review --approve` | REV-BUG-0041-001；plan → review；status → approved |
| 2026-06-28 18:05:06 | `/bug-complete` | 补齐 root-cause、workaround、acceptance；Readiness → Ready |
| 2026-06-28 18:02:20 | `/bug-generate` | 生成 bug.md；status → draft |
| 2026-06-28 17:46:25 | `/bug-capture` | 记录侧栏底部用户菜单未显示用户头像 |
