---
bug_id: BUG-0041-sidebar-user-menu-avatar-missing
title: 侧边栏底部用户菜单未显示用户头像
severity: medium
status: approved
owner: product
discovered_at: 2026-06-28 17:46:25
environment: local|docker
related_requirement: REQ-0014-profile-page
related_change: null
related_bug: BUG-0019-user-modal-avatar-upload-display
---

# 缺陷说明

Web 管理端侧边栏底部用户菜单（`AdminUserMenu`）在用户已上传头像后，触发区仍仅显示首字母占位（如 `AU`），**不展示头像图片**，与个人资料页、用户管理列表等已支持 `avatar_url` 回显的页面不一致。

> **Scope 说明**：本 BUG 聚焦 **侧栏 `AdminUserMenu` 头像图片展示与数据 plumbing**；含 Profile 页上传后侧栏即时刷新。平板/窄屏（≤1023px）侧栏用户区隐藏（by design）不在范围；**不**扩展 auth `/me` 或 login `UserProfile` schema。

# 复现步骤

1. 以 `admin` 或 `employee` 登录 Web 管理端（`http://localhost:3000` 或 `http://localhost:5173`）。
2. 进入「个人资料」（`/admin/profile`），上传 JPG/PNG/WebP 头像并保存（或确保账号在 `GET /api/v1/profile/me` 中已有非空 `avatar_url`）。
3. 观察 Profile 页身份条：头像图片正常显示。
4. 导航至任意其他管理页（如 `/admin/dashboard`），观察侧边栏底部用户菜单触发区（34px avatar 位 + 用户名 + 邮箱 + chevron）。
5. （可选）侧栏收起（`data-sidebar-state="collapsed"`），观察 avatar 位是否仍无图片。

# 期望结果

- 当 `GET /api/v1/profile/me` 返回非空 `avatar_url` 时，侧栏 `AdminUserMenu` **MUST** 在 `.avatar` 区域渲染头像 `<img>`。
- 无 `avatar_url` 或图片加载失败时 **MUST** 回退为首字母占位，行为对齐 `UserManagementPage`（img + fallback）。
- 个人资料页上传/更换头像成功后，返回其他页面时侧栏 **SHOULD** 即时展示新头像（无需整页硬刷新）。
- expanded / collapsed 侧栏状态下 avatar 位 **MUST** 保持 34×34px、圆角与 Design System token 一致。
- **MUST NOT** 引入裸 Hex；样式复用或扩展 `admin-home.css` semantic 规则。

# 实际结果

- 侧栏 `.avatar` **始终**渲染 `getUserInitials()` 文本，无 `<img>` 分支（`AdminUserMenu.tsx` L101）。
- `AdminLayout` 虽调用 `fetchProfileMe()`，但仅提取 `email` 传给侧栏，**未传递 `avatar_url`**。
- auth 会话 `UserProfile`（login / `/auth/me`）不含 `avatar_url` 字段，侧栏当前数据源无法直接获得头像 URL。
- Profile 页上传头像后，侧栏在会话内不自动更新（Layout 仅在 `user` 引用变化时 refetch profile）。

# 影响范围

| 范围 | 影响 |
|---|---|
| Web 管理端侧栏 `AdminUserMenu` | 头像图片缺失，仅 initials；UX 与 Profile/用户列表不一致 |
| `admin` / `employee` | 均受影响 |
| desktop expanded / collapsed | 受影响（collapsed 仍保留 34px avatar 位） |
| ≤1023px 视口 | 侧栏用户区 `display: none`，**不在本 BUG 范围** |
| 后端 / API / 数据库 | **无变更**（复用现有 `GET /profile/me`） |
| Orval | **无**（不推荐扩展 auth `UserProfile`） |
| 店主端 / 小程序 | 无 |

**与 REQ / 已归档能力关系**

| 项 | 说明 |
|---|---|
| REQ-0011 | 侧栏壳层与 collapsed 布局；原型曾为 initials 占位（`AU`） |
| REQ-0014 | 个人资料头像上传已交付；侧栏未同步 avatar 展示能力 |
| BUG-0019 | 用户弹窗/列表 avatar 回显已修复；可参考 img + fallback 模式 |
| BUG-0021 | 同侧栏域、独立问题（菜单 icon）；可同 Sprint、不同 Change |

# 严重等级说明

严重程度为 `medium`。

理由：

- **不阻塞登录或导航**：用户菜单、个人资料入口、密码修改、退出均可用。
- **100% 稳定复现**：凡有 `avatar_url` 的账号，侧栏均不显示图片。
- **UX / 一致性缺陷**：REQ-0014 上线后用户合理预期侧栏同步展示本人头像。
- **修复面可控**：前端 `AdminLayout` + `AdminUserMenu` + CSS + vitest；无需 API/DB 变更。

# 代码线索

| 线索 | 路径 |
|---|---|
| 侧栏 avatar 仅 initials | `src/web/src/features/admin/components/AdminUserMenu.tsx` |
| profile 数据未传 avatar | `src/web/src/pages/admin/AdminLayout.tsx` |
| 参考 img + fallback | `src/web/src/pages/admin/UserManagementPage.tsx` |
| Profile 头像展示 | `src/web/src/pages/admin/ProfilePage.tsx` |
| 侧栏样式 | `src/web/src/features/admin/styles/admin-home.css` |
| 列表 avatar 样式参考 | `src/web/src/features/admin/styles/user-management.css` |
| 单元测试 | `src/web/src/features/admin/components/AdminUserMenu.test.tsx` |
| Profile API | `src/web/src/features/admin/api/profile-api.ts` |
| 建议 Change | `fix-sidebar-user-menu-avatar` |

# 分类结论

| 判断 | 结论 |
|---|---|
| 需求 vs 缺陷 | 缺陷（REQ-0014 交付后的 UX 一致性缺口，非新能力 REQ） |
| 根因类型 | frontend-ui + 数据 plumbing（渲染未实现 + Layout 未传 avatar_url） |
| 是否回归 | 否（侧栏自 REQ-0011 起即为 initials，从未实现真实头像） |
| 是否存储/API 问题 | 否（profile/me 已返回 avatar_url） |
| 建议修复 Change | `fix-sidebar-user-menu-avatar` |
