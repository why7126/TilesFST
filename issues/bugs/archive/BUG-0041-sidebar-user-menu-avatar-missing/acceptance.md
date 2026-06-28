---
bug_id: BUG-0041-sidebar-user-menu-avatar-missing
status: pending_review
created_at: 2026-06-28 18:05:06
updated_at: 2026-06-28 18:05:06
related_requirement: REQ-0014-profile-page
related_bug: BUG-0019-user-modal-avatar-upload-display
note: 修复 MUST 为纯前端；复用 GET /profile/me avatar_url；不扩展 auth UserProfile
---

# 回归验收标准

> 修复本缺陷 MUST 使侧栏 `AdminUserMenu` 在有 `avatar_url` 时展示头像图片，无 URL 或加载失败时回退 initials；MUST NOT 回归侧栏菜单、collapsed 布局、密码修改弹窗、Profile 头像上传或 semantic token 规范。

## AC-001 有 avatar_url 时侧栏 MUST 显示头像图片

**Given** 已登录 `admin` 或 `employee`，且 `GET /api/v1/profile/me` 返回非空 `avatar_url`  
**When** 在 desktop 视口（>1023px）任意管理页观察侧栏底部 `AdminUserMenu`  
**Then** `.avatar` 区域 MUST 渲染 `<img src={avatar_url}>`  
**And** 图片 MUST 可见且填充 34×34px 容器（`object-fit: cover`）

- [x] AC-001

## AC-002 无 avatar_url 时 MUST 回退 initials

**Given** 已登录账号 `avatar_url` 为空或 null  
**When** 观察侧栏 `.avatar`  
**Then** MUST 显示 `getUserInitials(display_name, username)` 文本占位  
**And** MUST 保持 `--admin-gold-bg` / `--admin-gold` semantic 样式

- [x] AC-002

## AC-003 图片加载失败 MUST fallback

**Given** 侧栏传入无效或不可访问的 `avatar_url`  
**When** `<img>` 触发 `onError`  
**Then** MUST 回退显示 initials（对齐 `UserManagementPage` img + fallback 模式）  
**And** MUST NOT 出现破损图片图标占满侧栏

- [x] AC-003

## AC-004 Profile 上传后侧栏 MUST 即时更新

**Given** 用户在 `/admin/profile` 成功上传并保存新头像  
**When** 导航至其他管理页（如 `/admin/dashboard`）**不**硬刷新浏览器  
**Then** 侧栏 `.avatar` MUST 展示新头像图片  
**And** MUST NOT 仍显示旧 initials 或旧图（若曾修复过）

- [x] AC-004

## AC-005 collapsed 侧栏 MUST 保留 avatar 图片

**Given** 账号有 `avatar_url`，侧栏处于 `data-sidebar-state="collapsed"`  
**When** 观察 `.user-trigger` 内 `.avatar`  
**Then** MUST 仍显示头像图片（34px 居中）  
**And** `.user-name`、`.user-email`、chevron MUST 仍按 REQ-0011 规则隐藏

- [x] AC-005

## AC-006 侧栏菜单行为 MUST 无回归

**Given** 修复完成  
**When** 点击用户触发区并选择「个人资料」「密码修改」「退出登录」  
**Then** MUST 分别导航至 `/admin/profile`、打开 `ChangePasswordModal`、执行 logout  
**And** Profile 路由下「个人资料」项 MUST 保持 `active` 态

- [x] AC-006

## AC-007 修复范围 MUST 为纯前端

**Given** 缺陷修复已合并  
**When** 检查变更范围  
**Then** MUST NOT 变更 profile/auth API、SQLite schema、Orval 生成物、Docker 部署  
**And** MUST NOT 扩展 login/`/auth/me` `UserProfile` 字段  
**And** 店主端 / 小程序 MUST NOT 受影响

- [x] AC-007

## AC-008 样式 MUST 使用 semantic token

**Given** 修复涉及 `admin-home.css` 或组件 className  
**When** 审查 diff  
**Then** MUST NOT 新增裸 Hex / rgba design token 硬编码  
**And** avatar 边框/背景 MUST 复用 `--admin-avatar-border`、`--admin-gold-bg` 等既有变量

- [x] AC-008

## AC-009 单元测试 MUST 通过

**Given** `fix-sidebar-user-menu-avatar` apply 完成  
**When** 运行 `cd src/web && pnpm vitest run src/features/admin/components/AdminUserMenu.test.tsx`  
**Then** 全部用例 MUST pass（含 avatar 渲染与 fallback 新增用例）  
**And** `pnpm build` MUST pass

- [x] AC-009

## AC-010 tablet 窄屏 MUST 保持既有行为

**Given** 视口 ≤1023px  
**When** 访问管理端  
**Then** `.sidebar-user` MUST 仍为 `display: none`（REQ-0011 回归）  
**And** 本 BUG 修复 MUST NOT 改变 tablet 布局

- [x] AC-010

## AC-011 与 Profile / 用户列表 MUST 视觉一致

**Given** 同一账号在 Profile 页、用户列表、侧栏均有 avatar 入口  
**When** 并排对比三处头像  
**Then** 侧栏 avatar MUST 与 Profile 页使用相同 `avatar_url` 源  
**And** 尺寸/圆角 MUST 符合 admin shell 34px 规范

- [x] AC-011
