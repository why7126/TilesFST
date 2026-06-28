---
change_id: fix-sidebar-user-menu-avatar
type: fix
bug_id: BUG-0041-sidebar-user-menu-avatar-missing
related_requirement: REQ-0014-profile-page
status: archived
created_at: 2026-06-28 18:37:10
updated_at: 2026-06-28 18:49:06
---

# Change Trace — fix-sidebar-user-menu-avatar

## 关联

| 项 | 值 |
|---|---|
| BUG | BUG-0041-sidebar-user-menu-avatar-missing |
| REQ | REQ-0014-profile-page |
| 严重度 | medium |
| 修复面 | Web 管理端纯前端 |

## 实现摘要

| 文件 | 变更 |
|---|---|
| `AdminLayout.tsx` | `loadProfileShell` 缓存 email + avatar_url；Outlet 暴露 `refetchProfileShell` |
| `AdminSidebar.tsx` | 传递 `profileAvatarUrl` |
| `AdminUserMenu.tsx` | img + initials fallback；`onError` → `is-fallback` |
| `admin-home.css` | avatar img / fallback 样式 |
| `ProfilePage.tsx` | 上传成功后 `refetchProfileShell()` |
| `AdminUserMenu.test.tsx` | avatar 渲染与 error fallback 用例 |

## 测试

- `vitest` AdminUserMenu 6/6、AdminLayout 3/3
- `vite build` pass

## 变更记录

| 时间 | 事件 | 说明 |
|---|---|---|
| 2026-06-28 18:46:00 | `/opsx-apply` | 实现侧栏 avatar 展示与 Profile 上传刷新 |
| 2026-06-28 18:37:10 | `/bug-opsx` | 创建 change；status proposed |
