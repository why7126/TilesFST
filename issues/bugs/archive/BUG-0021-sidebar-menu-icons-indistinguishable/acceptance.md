---
bug_id: BUG-0021-sidebar-menu-icons-indistinguishable
status: pending_review
created_at: 2026-06-27 21:40:26
updated_at: 2026-06-28 12:05:00
related_requirement: REQ-0011-admin-sidebar-expand-collapse
note: fix-sidebar-menu-icons-indistinguishable apply 完成；Vitest + build 通过
---

# 回归验收标准

> 修复本缺陷 MUST 使 collapsed 态下各菜单图标语义可区分，且 MUST NOT 回归 REQ-0011 折叠/展开、localStorage 持久化、active 路由高亮、≤1023px 响应式与 a11y。

## AC-001 每个菜单项 MUST 配置独立语义图标

**Given** 管理员已登录 Web 管理端（`> 1023px`）  
**When** 检查 `admin-nav.ts` 与各 nav 渲染结果  
**Then** 以下菜单 MUST 各自拥有可区分的图标（Lucide outline 或 DS 等价 SVG）：

| id | label | 建议 icon（可等价替换） |
|---|---|---|
| `home` | 首页 | `LayoutDashboard` |
| `sku` | 瓷砖 SKU | `Package` |
| `brand` | 瓷砖品牌 | `Building2` |
| `category` | 瓷砖类目 | `FolderTree` |
| `banner` | Banner 管理 | `Image` |
| `users` | 用户管理 | `Users` |
| `settings` | 系统设置 | `Settings` |

**And** 任意两菜单的 SVG path / icon 组件 MUST NOT 相同

- [x] AC-001

## AC-002 collapsed 态 MUST 可仅凭图标识别菜单

**Given** 侧栏处于 `data-sidebar-state="collapsed"`  
**When** 用户查看 nav 区域（`.nav-label` 已隐藏）  
**Then** 7 个菜单图标 MUST 在形状上彼此可区分  
**And** 用户点击任一图标 MUST 正确导航至对应路由（或 placeholder 行为不变）

- [x] AC-002

## AC-003 expanded 态 MUST 图标与文案并存且无布局回归

**Given** 侧栏处于 `data-sidebar-state="expanded"`  
**When** 查看各 nav-item  
**Then** 图标 + 文案 MUST 并排显示，间距与 active/hover 样式与现网一致  
**And** `TILESFST` brand-head、chevron、用户菜单 MUST 无布局回归

- [x] AC-003

## AC-004 样式 MUST 使用 semantic token，禁止裸 Hex

**Given** 修复完成  
**When** 检查 `AdminSidebar.tsx` 与 `admin-home.css`  
**Then** 图标颜色 MUST 继承 nav-item 的 `currentColor`（muted / active gold）  
**And** TSX/CSS MUST NOT 新增裸 Hex  
**And** `.nav-icon` CSS 伪元素方块样式 MUST 移除或替换为 SVG 容器样式

- [x] AC-004

## AC-005 角色过滤 MUST 保持

**Given** 以 `employee` 角色登录  
**When** 查看侧栏（expanded 或 collapsed）  
**Then** 「用户管理」菜单 MUST 不可见  
**And** 其余可见菜单图标仍 MUST 可区分

- [x] AC-005

## AC-006 a11y MUST 保持

**Given** collapsed 或 expanded 态  
**When** 检查 nav 按钮  
**Then** 每个按钮 MUST 保留 `aria-label={item.label}`  
**And** 装饰性图标 MUST `aria-hidden="true"`  
**And** chevron MUST 保留正确 `aria-expanded` 与 `aria-label`

- [x] AC-006

## AC-007 REQ-0011 折叠能力 MUST 无回归

**Given** 修复完成  
**When** 执行 REQ-0011 核心交互  
**Then** chevron 切换、264px ↔ 72px 宽度过渡、localStorage（`admin-sidebar-collapsed`）持久化 MUST 正常  
**And** collapsed 态 active 项 MUST 仍带 `.nav-item.active` 与 accent 指示  
**And** ≤1023px MUST 无折叠 chevron 回归（沿用现有 @media）

- [x] AC-007

## AC-008 修复范围 MUST 为纯前端 UI

**Given** 缺陷修复已合并  
**When** 检查变更范围  
**Then** MUST NOT 变更 API、SQLite schema、Orval 生成物、Docker 部署  
**And** MUST NOT 修改店主端 `Sidebar` 筛选栏

- [x] AC-008

## AC-009 测试 MUST 覆盖图标差异

**Given** 进入 `fix-sidebar-menu-icons-indistinguishable`（或等价 fix-* Change）  
**When** 完成 `/opsx-apply`  
**Then** Vitest MUST 断言 collapsed 态下至少 2 个不同 nav id 渲染不同 icon（或 `data-nav-id` + 不同 SVG）  
**And** 现有 `AdminSidebar.collapse.test.tsx` 用例 MUST 仍通过  
**And** `cd src/web && pnpm test` 与 `pnpm build` MUST 通过

- [x] AC-009（AdminSidebar.* 测试 + `vite build` 通过）

## AC-010 视觉验收（SHOULD）

**Given** 修复完成  
**When** 1280×1024 桌面端 expanded / collapsed 并排查看  
**Then** 各菜单图标语义与 label 一致、16px 量级与 nav-item 对齐  
**And** Change `trace.md` SHOULD 记录 collapsed 态 icon-only 验收结论

- [x] AC-010（见 change trace.md；Vitest SVG 差异覆盖 collapsed 识别）
