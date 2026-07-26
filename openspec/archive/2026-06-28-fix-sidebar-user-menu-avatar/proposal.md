## Why

[BUG-0041-sidebar-user-menu-avatar-missing](issues/bugs/archive/BUG-0041-sidebar-user-menu-avatar-missing/) 已评审通过（REV-BUG-0041-001）。REQ-0014 交付个人资料头像上传后，Profile 页与用户列表已支持 `avatar_url` 回显，但侧栏 `AdminUserMenu` 仍固定渲染首字母占位，造成全局 shell UX 不一致。

根因：渲染层未实现 `<img>` + fallback；`AdminLayout` 预取 `profile/me` 时仅传递 `email`，丢弃 `avatar_url`；Profile 上传后无侧栏刷新机制。

## What Changes

- `AdminLayout`：扩展 `fetchProfileMe()` 缓存，向 `AdminSidebar` / `AdminUserMenu` 传递 `avatarUrl`（与 `profileEmail` 同源）。
- `AdminUserMenu`：有 `avatarUrl` 时渲染头像 `<img>`；无 URL 或 `onError` 时回退 initials（对齐 `UserManagementPage`）。
- `admin-home.css`：补充 `.sidebar-user .avatar img` 样式（34×34px、`object-fit: cover`、semantic token）。
- Profile 页上传头像成功后触发 Layout refetch 或等价机制，侧栏即时更新。
- `AdminUserMenu.test.tsx`：avatar 渲染、fallback、菜单行为回归。
- MODIFIED `admin-dashboard`「管理端 Sidebar 用户菜单」与 `web-client`「管理端个人资料路由」delta spec。

## Capabilities

### New Capabilities

（无。）

### Modified Capabilities

- `admin-dashboard`：MODIFIED「管理端 Sidebar 用户菜单」— 有 `avatar_url` 时展示头像图片，否则 initials fallback。
- `web-client`：MODIFIED「管理端个人资料路由」— AdminLayout 传递侧栏 avatar；Profile 上传后侧栏刷新。

## Impact

| 影响面 | 说明 |
|---|---|
| Web 管理端 | `AdminLayout.tsx`、`AdminSidebar.tsx`、`AdminUserMenu.tsx`、`admin-home.css`；可选 `ProfilePage.tsx`（refetch hook） |
| 后端 / API / Orval | 无（复用 `GET /profile/me`） |
| 数据库 | 无 |
| 父需求 | REQ-0014-profile-page |
| 关联 BUG | BUG-0041；参考 BUG-0019 avatar 模式 |

## Rollback Plan

1. 回滚 `AdminLayout`、`AdminSidebar`、`AdminUserMenu`、`admin-home.css` 及测试至 fix 前版本。
2. 运行 `cd src/web && pnpm vitest run AdminUserMenu && pnpm build`。
3. 若已 archive，从 `openspec/specs/admin-dashboard/spec.md` 与 `web-client/spec.md` 恢复 MODIFIED requirement 前版本。
4. 重新标记 BUG-0041 为未修复。
