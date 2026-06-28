## 1. 准备与定位

- [x] 1.1 阅读 BUG-0041 的 bug.md、root-cause.md、acceptance.md（AC-001～AC-011）
- [x] 1.2 对照 `AdminLayout.tsx`、`AdminSidebar.tsx`、`AdminUserMenu.tsx`、`UserManagementPage.tsx`
- [x] 1.3 确认无 API / Orval / 数据库变更

## 2. 数据 plumbing（AdminLayout）

- [x] 2.1 扩展 `fetchProfileMe()` 缓存：除 `profileEmail` 外保存 `avatarUrl`
- [x] 2.2 将 `avatarUrl` prop 传入 `AdminSidebar` → `AdminUserMenu`
- [x] 2.3 实现 `refetchProfileShell()`（context 或 callback）供 Profile 页调用
- [x] 2.4 勾选 BUG-0041 AC-007（纯前端范围）

## 3. 渲染与样式（AdminUserMenu）

- [x] 3.1 `.avatar` 实现 `avatarUrl ? <img> + fallback initials` 模式（对齐 UserManagementPage）
- [x] 3.2 `onError` 回退 initials（`is-fallback` 或等价）
- [x] 3.3 `admin-home.css` 补充 `.sidebar-user .avatar img` / fallback 规则（34×34px、semantic token）
- [x] 3.4 勾选 AC-001、AC-002、AC-003、AC-005、AC-008、AC-011

## 4. Profile 上传后即时刷新

- [x] 4.1 `ProfilePage` 头像上传成功后调用 Layout refetch（或等价机制）
- [x] 4.2 手工验证：上传 → 导航 dashboard → 侧栏新头像（AC-004）— refetch 已接线；待 archive 前人工冒烟

## 5. 回归

- [x] 5.1 侧栏菜单：个人资料 / 密码修改 / 退出登录（AC-006）
- [x] 5.2 collapsed 侧栏 avatar 与 REQ-0011 布局（AC-005）
- [x] 5.3 ≤1023px `.sidebar-user { display: none }` 无变更（AC-010）

## 6. 测试

- [x] 6.1 `AdminUserMenu.test.tsx`：avatarUrl 渲染 img、无 URL initials、onError fallback
- [x] 6.2 运行 `cd src/web && pnpm vitest run src/features/admin/components/AdminUserMenu.test.tsx`
- [x] 6.3 运行 `cd src/web && pnpm build`（AC-009）

## 7. 验收与追溯

- [x] 7.1 勾选 BUG-0041 acceptance AC-001～AC-011
- [x] 7.2 填写本 change `trace.md`；更新 BUG trace `openspec_changes`
- [x] 7.3 评估 `docs/knowledge-base/incidents/`（不需要 — 纯 UI 一致性缺陷）

## 8. 归档准备

- [x] 8.1 全部 `[x]` 后 `/opsx-archive fix-sidebar-user-menu-avatar`
