## Context

- **BUG**: `BUG-0021-sidebar-menu-icons-indistinguishable`
- **Severity**: medium
- **Root cause type**: design / frontend-ui
- **Related REQ**: `REQ-0011-admin-sidebar-expand-collapse`（已 archive）
- **Parent change**: `add-admin-sidebar-collapse`（已 archive）
- **Target**: `admin-nav.ts`、`AdminSidebar.tsx`、`admin-home.css`、vitest

### 原型优先级（MUST）

```text
1. issues/bugs/archive/BUG-0021-sidebar-menu-icons-indistinguishable/acceptance.md
2. issues/requirements/archive/REQ-0011-admin-sidebar-expand-collapse/prototype/web/admin-sidebar-collapsed.html
3. issues/requirements/archive/REQ-0011-admin-sidebar-expand-collapse/prototype/web/admin-sidebar-expanded.html
4. rules/ui-design.md（semantic token、禁止裸 Hex）
5. src/web 现有 lucide-react 用法（SearchBar、Pagination 等）
```

## Bug Analysis Report

### 现象

管理端 `AdminSidebar` 全部 nav 项使用相同 `<span className="nav-icon" />` + CSS 方块。collapsed 态隐藏 `.nav-label` 后，7 个菜单图标视觉无差别。

### 复现路径

1. admin 登录 Web 管理端（>1023px）。
2. 进入 `/admin/dashboard`。
3. 点击 chevron → `data-sidebar-state="collapsed"`。
4. 观察 nav 区各图标形状完全一致。

### 影响

- 不阻断路由与 `aria-label` 读屏。
- collapsed 态导航效率下降，易误点。
- 无 API/DB/权限影响。

## Root Cause（摘要）

| ID | 结论 |
|---|---|
| RC-001 | `AdminSidebar` 未读取 per-item icon，统一空 span |
| RC-002 | `AdminNavItem` 无 `icon` 字段 |
| RC-003 | `.nav-icon` 为 CSS 伪元素方块，非语义 SVG |
| RC-004 | REQ-0011 原型/AC 仅要求保留 icon 占位，未要求差异化 |

## Goals / Non-Goals

**Goals:**

- 7 个菜单各自 Lucide 语义 icon，collapsed 态可区分。
- expanded 态 icon + 文案并排，active/hover 无回归。
- semantic token / currentColor；无裸 Hex。
- Vitest 图标差异 + collapse 用例通过。

**Non-Goals:**

- 修改 REQ-0011 折叠宽度、localStorage、chevron、≤1023px 响应式。
- 店主端 `Sidebar` 筛选栏。
- API / DB / Orval / Docker compose。

## Decisions

### D1：图标库 — lucide-react

- **决策**：`AdminNavItem.icon: LucideIcon`；与项目现有 DS 用法一致。
- **映射**（可等价替换，MUST 保持 id 间可区分）：

| id | label | icon |
|---|---|---|
| home | 首页 | LayoutDashboard |
| sku | 瓷砖 SKU | Package |
| brand | 瓷砖品牌 | Building2 |
| category | 瓷砖类目 | FolderTree |
| banner | Banner 管理 | Image |
| users | 用户管理 | Users |
| settings | 系统设置 | Settings |

### D2：样式 — SVG 容器取代 CSS 方块

- **决策**：`.nav-icon` 设为 `display: inline-flex; width/height: 16px; flex-shrink: 0; color: inherit`；删除 border + `::after` 伪元素规则。
- **理由**：图标颜色随 `.nav-item` / `.nav-item.active` 的 currentColor 变化（muted / brand gold）。

### D3：a11y

- 保留 `aria-label={item.label}` on button；icon `aria-hidden="true"`。
- chevron `aria-expanded` 不变。

### D4：测试策略

- 扩展 `AdminSidebar.collapse.test.tsx` 或新增 `AdminSidebar.icons.test.tsx`：渲染 collapsed，断言至少 2 个 nav id 对应不同 `data-lucide` 或 SVG path。
- 现有 collapse / user-mgmt 用例 MUST pass。
- `cd src/web && pnpm test && pnpm build`。

### D5：与 sprint-003 其他 Change 协调

- 可与 `add-admin-profile-page` 并行（同 touch AdminSidebar 时 merge 顺序注意）。
- 建议在 profile 菜单入口改动前或同一 PR 内完成 icon 映射，避免冲突。

## Risks / Trade-offs

| 风险 | 缓解 |
|------|------|
| AdminSidebar 与 REQ-0014 菜单改动冲突 | sprint-003 内协调 PR 顺序；icon 映射独立于 profile 路由 |
| Lucide bundle 略增 | 仅 7 个 tree-shakeable icon |
| employee 角色隐藏 users 后仍须可区分其余项 | 沿用现有 filter 逻辑 |

## Migration Plan

- 无数据迁移；前端 deploy 即生效。
- 回滚见 proposal Rollback Plan。

## Open Questions

- 无（BUG-0021 approved，acceptance 已明确）。
