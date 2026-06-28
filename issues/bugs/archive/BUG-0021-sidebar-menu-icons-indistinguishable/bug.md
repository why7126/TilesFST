---
bug_id: BUG-0021-sidebar-menu-icons-indistinguishable
title: 侧边栏收起后各菜单图标相同无法区分
severity: medium
status: draft
owner: product
discovered_at: 2026-06-27 21:33:13
environment: local|docker
related_requirement: REQ-0011-admin-sidebar-expand-collapse
related_change: null
related_bug: null
---

# 缺陷说明

Web 管理端 `AdminSidebar` 各导航菜单项前方图标视觉完全一致（CSS 绘制的通用 `.nav-icon` 占位方块）。侧边栏 **展开** 时可依赖文字标签区分菜单；**收起**（`data-sidebar-state="collapsed"`，72px 图标列）后文案被隐藏，用户无法仅凭图标识别首页、瓷砖 SKU、品牌、类目、Banner、用户管理、系统设置等功能模块，降低导航效率并易误点。

> **Scope 说明**：本 BUG 聚焦 **各菜单项差异化语义图标**；不包含侧边栏折叠/展开交互本身（已由 REQ-0011 / `add-admin-sidebar-collapse` 交付）、Chevron 控件、localStorage 持久化或 ≤1023px 响应式布局。

# 复现步骤

1. 以 admin 登录 Web 管理端（`http://localhost:3000` 或 `http://localhost:5173`）。
2. 进入任意管理页（如 `/admin/dashboard`）。
3. 点击侧边栏头部 chevron，使侧栏进入 **collapsed** 状态（`data-sidebar-state="collapsed"`）。
4. 观察 OPERATIONS / SYSTEM 分组下各菜单项前方图标：首页、瓷砖 SKU、瓷砖品牌、瓷砖类目、Banner 管理、用户管理、系统设置。
5. （对照）展开侧栏后各菜单文字标签不同，但图标仍相同。

# 期望结果

- 每个 `AdminNavItem` **MUST** 配置语义明确且彼此可区分的图标（建议 Lucide outline，与项目现有 DS 用法一致）。
- **collapsed** 态下用户 **MUST** 可仅凭图标形状识别目标菜单并正确切换路由。
- **expanded** 态下图标与文案并存，样式与 admin semantic token 一致，无裸 Hex。
- 非 admin 角色隐藏「用户管理」时，其余可见菜单图标仍须可区分。
- 各 nav 按钮保留 `aria-label={label}`；图标 `aria-hidden="true"`。

# 实际结果

- 所有菜单项渲染相同的 `<span className="nav-icon" aria-hidden="true" />`（`AdminSidebar.tsx`）。
- `admin-nav.ts` 的 `AdminNavItem` 无 `icon` 字段；`admin-home.css` 用边框 + 伪元素绘制通用方块，无 per-item 差异。
- collapsed 态隐藏 `.nav-label` 后，7 个（或非 admin 时 6 个）菜单图标视觉无差别。

# 影响范围

| 范围 | 影响 |
|---|---|
| Web 管理端 / 桌面端（> 1023px） | collapsed 侧栏导航可用性下降，依赖 hover/记忆/试错 |
| Web 管理端 / expanded 侧栏 | 图标同质但不阻塞（有文字标签） |
| REQ-0011 验收体验 | AC-014 要求保留 nav 图标，但未要求差异化；折叠能力落地后暴露 UX 缺口 |
| 后端 / API / 数据库 / Orval | 无 |
| 店主端 / 小程序 | 无 |
| ≤1023px 响应式 | 无（折叠 chevron 隐藏，顶栏双列 nav 仍显示文案） |

**与 REQ-0011 / 已归档 Change 关系**

| 项 | 说明 |
|---|---|
| REQ-0011 | 引入 collapsed icon-only 布局，使「图标不可区分」问题显性化 |
| `add-admin-sidebar-collapse` | 已归档；交付折叠态，原型 HTML 亦使用相同 `.nav-icon` 占位 |
| 本 BUG | 补全折叠场景下缺失的 per-menu 语义图标，非折叠功能回归 |

# 严重等级说明

严重程度为 `medium`。

理由：

- **不阻塞核心功能**：路由仍可切换；`aria-label` 对屏幕阅读器仍有效。
- **影响日常效率**：习惯 collapsed 侧栏的用户无法快速识别菜单，增加误点与认知负担。
- **100% 稳定复现**：纯前端实现，与账号/数据无关。
- **修复面小**：预计仅改 `admin-nav.ts`、`AdminSidebar.tsx`、`admin-home.css` 及 vitest；无 API/DB 变更。

# 代码线索

| 线索 | 路径 |
|---|---|
| 侧栏渲染 | `src/web/src/features/admin/components/AdminSidebar.tsx`（L83 统一 `nav-icon`） |
| 菜单配置 | `src/web/src/features/admin/data/admin-nav.ts`（7 项，无 icon） |
| 图标样式 | `src/web/src/features/admin/styles/admin-home.css`（`.nav-icon` CSS 方块） |
| 折叠态裁剪 | `admin-home.css` `[data-sidebar-state='collapsed'] .nav-label { display: none }` |
| 折叠逻辑 | `src/web/src/pages/admin/AdminLayout.tsx`、`admin-sidebar-preference.ts` |
| 图标库 | 项目已用 `lucide-react`（如 `SearchBar`、`Pagination`） |
| 现有测试 | `AdminSidebar.collapse.test.tsx`（未断言图标差异） |
| 关联需求 | `issues/requirements/archive/REQ-0011-admin-sidebar-expand-collapse/` |
| 建议 Change | `fix-sidebar-menu-icons-indistinguishable` |

# 分类结论

| 判断 | 结论 |
|---|---|
| 需求 vs 缺陷 | 缺陷（REQ-0011 折叠交付后的 UX 缺口，非新功能 REQ） |
| 根因类型 | 前端 UI / 导航配置不完整（占位图标未替换为语义 icon） |
| 是否回归 | 否（图标始终相同；折叠能力使问题可见） |
| 建议修复 Change | `fix-sidebar-menu-icons-indistinguishable` |
