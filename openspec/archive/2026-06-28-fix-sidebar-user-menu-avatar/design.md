## Context

- **BUG**: BUG-0041（medium）
- **Related REQ**: `REQ-0014-profile-page`、`REQ-0011-admin-sidebar-expand-collapse`
- **Reference BUG**: BUG-0019（用户列表/弹窗 avatar 回显模式）
- **Target files**: `AdminLayout.tsx`、`AdminSidebar.tsx`、`AdminUserMenu.tsx`、`admin-home.css`；可选 `ProfilePage.tsx` + Layout context

### 原型 / 验收优先级（MUST）

```text
1. issues/bugs/archive/BUG-0041-sidebar-user-menu-avatar-missing/acceptance.md（AC-001～AC-011）
2. UserManagementPage.tsx（img + avatar-fallback 参考实现）
3. ProfilePage.tsx（avatar_url 数据源）
4. openspec/specs/admin-dashboard/spec.md（MODIFIED 后为准）
5. rules/ui-design.md
```

## Bug Analysis Report

| 维度 | 结论 |
|---|---|
| 现象 | 侧栏用户菜单始终 initials，不显示头像图片 |
| 直接原因 | `AdminUserMenu` 无 img 分支；`AdminLayout` 未传 `avatar_url` |
| 根本原因 | REQ-0011 initials 占位交付；REQ-0014 未同步侧栏 |
| 严重度 | medium |
| 修复面 | 纯前端 |

## Goals / Non-Goals

**Goals:**

- 有 `avatar_url` 时侧栏展示头像图片；无 URL / 加载失败回退 initials。
- Profile 上传后侧栏即时更新（AC-004）。
- expanded / collapsed 态 avatar 正常；菜单行为无回归。
- Vitest 覆盖 avatar 与 fallback。
- delta spec MODIFIED 消化「头像缩写」语义扩展。

**Non-Goals:**

- 扩展 auth `UserProfile` / login `/me` schema。
- 修改 ≤1023px 隐藏 `sidebar-user` 行为。
- 后端 / API / Orval / Docker 变更。
- 店主端 / 小程序。

## Decisions

### D1：复用 `GET /profile/me` 而非扩展 auth schema

- **理由**：Layout 已调用 `fetchProfileMe()`；`ProfileMe.avatar_url` 可用；避免 Orval/API 回归。

### D2：`avatarUrl` 独立 prop 传入 `AdminUserMenu`

- **理由**：auth `UserProfile` 无 avatar 字段；与现有 `profileEmail` plumbing 一致。

### D3：img + fallback 对齐 `UserManagementPage`

- **结构**：`.avatar` 内 `<img>` + `.avatar-fallback` initials；`onError` 添加 `is-fallback` class。
- **样式**：在 `admin-home.css` 扩展，参考 `user-management.css` 的 img 规则。

### D4：Profile 上传后刷新策略

- **首选**：Layout 暴露 `refetchProfileShell()` via context；Profile 上传成功后调用。
- **备选**：路由离开 `/admin/profile` 时 Layout refetch（弱于 AC-004，仅作 fallback）。

### D5：delta spec 位置

- `admin-dashboard` MODIFIED「管理端 Sidebar 用户菜单」— avatar 图片 + fallback。
- `web-client` MODIFIED「管理端个人资料路由」— Layout 传递 avatar、上传后刷新。

## Risks / Trade-offs

| 风险 | 缓解 |
|---|---|
| REQ-0011 原型 initials `AU` 与真实头像 delta | delta MODIFIED + acceptance 为准 |
| Profile refetch 增加请求 | 仅 avatar 变更时触发；复用已有 profile fetch |
| collapsed 态 img 裁剪 | CSS `object-fit: cover` + 既有 34px 容器 |

## Test Plan

- Vitest：`AdminUserMenu.test.tsx` — 有 `avatarUrl` 渲染 img；无 URL 显示 initials；img error fallback。
- Vitest（可选）：`AdminLayout.test.tsx` — profile fetch 传递 avatarUrl。
- 手工：Profile 上传 → 导航 dashboard → 侧栏新头像；collapsed 态；无效 URL fallback。
- `cd src/web && pnpm vitest run AdminUserMenu && pnpm build`
