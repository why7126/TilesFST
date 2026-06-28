---
bug_id: BUG-0041-sidebar-user-menu-avatar-missing
status: pending_review
created_at: 2026-06-28 18:05:06
updated_at: 2026-06-28 18:05:06
root_cause_type: code
---

# 根因分析

## 1. 直接原因

### 1.1 `AdminUserMenu` 未实现头像图片渲染

`AdminUserMenu.tsx` 在 `.avatar` 容器内**固定**渲染 `getUserInitials()` 文本，无 `avatar_url` 条件分支，无 `<img>` 元素：

```tsx
<span className="avatar">{initials}</span>
```

对比 `UserManagementPage.tsx` 与 `ProfilePage.tsx` 已实现 `avatar_url ? <img /> : initials/fallback` 模式。

### 1.2 `AdminLayout` 未向侧栏传递 `avatar_url`

`AdminLayout.tsx` 在 `useEffect` 中调用 `fetchProfileMe()`，但**仅**将 `profile.email` 写入 `profileEmail` 状态并传给 `AdminSidebar` → `AdminUserMenu`；`avatar_url` 被丢弃。

侧栏组件 props 当前为 `user`（auth `UserProfile`）、`profileEmail`，**无** `avatarUrl` 或等价字段。

### 1.3 auth 会话 `UserProfile` 不含头像 URL

login / `GET /auth/me` 返回的 `UserProfile` schema 仅含 `id、username、display_name、role、status`，**无** `avatar_url` / `avatar_object_key`。侧栏若只依赖 `useAuth().user`，无法获得可访问头像 URL。

### 1.4 Profile 上传后无侧栏刷新机制

`ProfilePage` 上传头像成功后仅更新本页 `profile` 状态，**未**通知 `AdminLayout` refetch。Layout 的 profile effect 依赖 `[user]`，同会话内更换头像后侧栏保持旧 initials，直至整页刷新。

## 2. 根本原因

### 2.1 REQ-0011 侧栏原型以 initials 占位交付

`REQ-0011-admin-sidebar-expand-collapse` 原型（`admin-sidebar-expanded.html` / `collapsed.html`）侧栏 `.avatar` 为静态文本 `AU`。`add-admin-sidebar-collapse` 按原型 CSS Port，`AdminUserMenu` 从未接入真实头像能力。

### 2.2 REQ-0014 头像能力未向下游 shell 同步

REQ-0014 交付个人资料页头像上传与 `GET /profile/me` 的 `avatar_url` 字段，验收聚焦 Profile 页身份条（AC-010/018），**未**要求侧栏 `AdminUserMenu` 同步展示。BUG-0019 修复用户弹窗/列表回显时，侧栏被遗漏。

### 2.3 Layout 层 profile 预取 scope 过窄

`AdminLayout` 引入 `fetchProfileMe()` 主要为侧栏展示真实邮箱（替代 `username@tilesfst.com` 占位），实现时只抽取 `email` 字段，未将同一响应中的 `avatar_url` 一并 plumbing 至侧栏。

## 3. 触发条件

满足以下条件时 **100% 稳定复现**：

1. 以 `admin` 或 `employee` 登录 Web 管理端（desktop 视口 >1023px，侧栏用户区可见）。
2. 账号在 `GET /api/v1/profile/me` 中 `avatar_url` 非空（Profile 页可正常显示头像图片）。
3. 观察任意管理页侧栏底部 `AdminUserMenu` 触发区。

与 MinIO、上传链路、角色类型无关；**后端与 Profile 页均正常**，缺陷纯在前端侧栏渲染与数据传递。

## 4. 分类结论

| 维度 | 结论 |
|---|---|
| 缺陷分类 | code / frontend-ui（渲染 + 数据 plumbing） |
| 是否接口缺陷 | 否（`profile/me` 已返回 `avatar_url`） |
| 是否数据库缺陷 | 否 |
| 是否存储/MinIO 缺陷 | 否 |
| 是否回归 | 否（侧栏从未实现真实头像） |
| 主要修复面 | `AdminLayout.tsx`、`AdminUserMenu.tsx`、`admin-home.css`、vitest |
| 关联需求 | REQ-0014（头像能力）、REQ-0011（侧栏壳层） |
| 建议 Change | `fix-sidebar-user-menu-avatar` |

## 5. 后续修复建议

1. `AdminLayout`：扩展 profile 预取，缓存 `avatarUrl`（与 `profileEmail` 同源 `fetchProfileMe()`），传入 `AdminSidebar` / `AdminUserMenu`。
2. `AdminUserMenu`：有 `avatarUrl` 时渲染 `<img>` + `avatar-fallback` initials；`onError` 回退（对齐 `UserManagementPage`）。
3. `admin-home.css`：为 `.sidebar-user .avatar img` 补充 `object-fit: cover` 等规则（可参考 `user-management.css`，保持 34×34px token）。
4. **即时刷新**：Profile 上传成功后通过 Layout context / callback / 路由 effect 触发 Layout refetch profile，或共享轻量 profile cache。
5. **不**扩展 auth `UserProfile` schema（避免 Orval/API 回归）；**不**改 tablet 隐藏 `sidebar-user` 行为。
6. `AdminUserMenu.test.tsx`：补充 `avatarUrl` 渲染、img error fallback、无 avatar 时 initials 用例。
