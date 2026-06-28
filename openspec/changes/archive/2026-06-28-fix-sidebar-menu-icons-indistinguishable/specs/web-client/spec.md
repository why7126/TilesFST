## ADDED Requirements

### Requirement: 管理端 Sidebar 菜单语义图标修复

Web 客户端 MUST 修复管理端 Sidebar 各菜单图标无法区分的缺陷（BUG-0021）：`AdminNavItem` MUST 配置 per-item Lucide（或 DS 等价）语义 icon；`AdminSidebar` MUST 渲染 SVG icon 而非纯 CSS 占位方块。**collapsed** 态下用户 MUST 可仅凭图标识别目标菜单；**expanded** 态 MUST 图标与文案并存且无布局回归。修复 MUST NOT 变更 REQ-0011 折叠/展开、localStorage（`admin-sidebar-collapsed`）、chevron、active 路由高亮、≤1023px 响应式或店主端 `Sidebar`。修复 MUST NOT 变更 API、SQLite、Orval 或 Docker 部署。

#### Scenario: nav 配置含 icon 字段

- **WHEN** 开发者查看 `admin-nav.ts`
- **THEN** 每个 `AdminNavItem` MUST 含 `icon` 属性（LucideIcon 或等价）
- **AND** home/sku/brand/category/banner/users/settings MUST 映射至可区分的 icon

#### Scenario: AdminSidebar 渲染 Lucide icon

- **WHEN** 用户查看任意 `/admin/*` 页面 Sidebar
- **THEN** 各 nav 按钮 MUST 渲染对应 Lucide SVG（约 16px，`strokeWidth` 约 1.5）
- **AND** 装饰性 icon MUST `aria-hidden="true"`
- **AND** nav 按钮 MUST 保留 `aria-label={item.label}`

#### Scenario: collapsed 态 Vitest 覆盖

- **WHEN** 运行 vitest 覆盖 AdminSidebar icon 修复
- **THEN** MUST 断言 collapsed（或等价）渲染下至少 2 个不同 nav id 对应不同 icon
- **AND** 现有 `AdminSidebar.collapse.test.tsx` 用例 MUST 仍通过

#### Scenario: REQ-0011 折叠能力无回归

- **WHEN** 用户切换 chevron 或刷新页面
- **THEN** 264px ↔ 72px 过渡、localStorage 持久化、`data-sidebar-state` MUST 正常
- **AND** ≤1023px MUST 无折叠 chevron 回归

#### Scenario: 纯前端修复范围

- **WHEN** 本 change 合并
- **THEN** MUST NOT 修改后端路由、数据库 migration 或 Orval 生成物
- **AND** `cd src/web && pnpm test` 与 `pnpm build` MUST 通过
