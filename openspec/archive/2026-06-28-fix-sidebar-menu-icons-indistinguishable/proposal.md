## Why

[BUG-0021-sidebar-menu-icons-indistinguishable](issues/bugs/archive/BUG-0021-sidebar-menu-icons-indistinguishable/) 已评审通过并纳入 sprint-003。REQ-0011 交付 collapsed 72px icon-only 侧栏后，各菜单项仍渲染相同 CSS `.nav-icon` 占位方块，收起态无法凭图标识别首页、SKU、品牌等功能。根据项目规则，已交付能力上的 UX 缺口 MUST 使用新的 `fix-*` change 修复。

## What Changes

- `AdminNavItem` 增加 `icon` 字段（Lucide `LucideIcon`），为 7 个菜单 id 配置语义图标（LayoutDashboard、Package、Building2、FolderTree、Image、Users、Settings）。
- `AdminSidebar` 渲染 `<item.icon className="nav-icon" size={16} strokeWidth={1.5} aria-hidden />`，移除 CSS 伪元素通用方块。
- `admin-home.css`：`.nav-icon` 改为 SVG 容器样式（尺寸、currentColor、flex 对齐）；移除 border/::after 占位规则。
- Vitest：断言各 nav id 渲染不同 icon；`AdminSidebar.collapse.test.tsx` 无回归。
- collapsed / expanded 1280×1024 人工验收；记录于 change `trace.md`。
- **不** 变更后端 API、SQLite、Orval、Docker、店主端 `Sidebar`、REQ-0011 折叠/localStorage/chevron 逻辑。

## Capabilities

### New Capabilities

（无新 capability 目录；修复归入 `admin-dashboard` 与 `web-client` delta。）

### Modified Capabilities

- `admin-dashboard`：MODIFIED「管理端 Sidebar 品牌与导航」— 各菜单 MUST 配置可区分的语义图标。
- `web-client`：ADDED「管理端 Sidebar 菜单语义图标修复」— collapsed 态 icon-only 可识别；REQ-0011 无回归。

## Impact

| 影响面 | 说明 |
|---|---|
| Web 管理端 | `admin-nav.ts`、`AdminSidebar.tsx`、`admin-home.css` |
| 店主端 | 无 |
| 后端 / API / DB / Orval | 无 |
| 父需求 | REQ-0011（折叠已 archive；本 fix 补 collapsed UX） |
| Sprint | sprint-003 |
| 测试 | vitest AdminSidebar；1280×1024 collapsed 并排验收 |

## Rollback Plan

若 Lucide 图标引入导致侧栏布局或构建异常，可回滚本 change 的前端改动：

1. 恢复 `admin-nav.ts`、`AdminSidebar.tsx`、`admin-home.css` 至 fix 前版本。
2. 移除新增 Vitest 图标差异断言。
3. 运行 `cd src/web && pnpm test && pnpm build` 确认通过。

回滚不涉及 API、数据库或部署配置。
