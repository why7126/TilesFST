---
bug_id: BUG-0013-product-version-ui-inconsistency
title: 产品版本号 UI 与原型及 Design System 不一致
severity: medium
status: draft
owner: product
discovered_at: 2026-06-27 10:54:19
environment: local|docker
related_requirement: REQ-0010-product-version-display
related_change: add-product-version-display
---

# 缺陷说明

REQ-0010「产品版本号展示」已在管理端侧边栏顶部实现 `TILESFST` + 版本号并排布局，但版本 badge 的视觉呈现与 REQ-0010 原型、Golden Reference 及 Design System 徽章规范不一致。

具体表现：

1. 版本号未呈现预期的 muted 版本 pill 形态（弱化文字色、细边框、浅背景、2px 工业圆角），视觉上更接近偏亮的主文字色 sans-serif 文案。
2. 与金色 serif 品牌名 `TILESFST` 并排时，字体与颜色层级混乱，版本区域抢主品牌视觉或缺乏次级信息弱化感。
3. 未满足 REQ-0010 验收 AC-006（布局参照 Golden Reference）、AC-013（semantic token 小号圆角 badge）、AC-015（与原型 HTML 并排验收）。

店主端若共用 `ProductVersionBadge`，存在相同视觉偏差风险。

# 复现步骤

1. 以 admin 用户登录 Web 管理端（local 或 Docker 均可）。
2. 进入任意 `/admin/*` 页面（如 `/admin/tile-skus`）。
3. 观察左侧侧边栏顶部 `TILESFST` 右侧的版本号（如 `v0.0.1`）样式。
4. 并排对照：
   - `issues/requirements/archive/REQ-0010-product-version-display/prototype/web/product-version-sidebar-admin.html`
   - `issues/requirements/archive/REQ-0010-product-version-display/prototype/web/images/sidebar-version-reference.png`
   - `issues/bugs/archive/BUG-0013-product-version-ui-inconsistency/screenshots/admin-sidebar-version-actual.png`
5. 可选：访问店主端带侧栏页面，检查 `Sidebar` 顶部 brand-head 版本 pill 是否同样偏差。

# 期望结果

- 产品名右侧同一行展示小号版本 pill，垂直居中对齐，布局语义对齐 Golden Reference（SoulKing 参考图）。
- 版本 pill 规格：高度约 18px、`padding: 2px 7px`、`rounded-industrial`（2px）、`border-border-chip` 或 `border-border-default`、浅背景（如 `bg-surface/30`）、文字 10px、`text-muted`/`text-subtle`。
- TSX/CSS MUST 使用 semantic token，无裸 Hex；符合 `rules/ui-design.md` §8 徽章与状态标签规范。
- 管理端与店主端共用同一 `ProductVersionBadge` 组件时，两端视觉一致。

# 实际结果

- 版本号呈现为偏亮的主文字色 sans-serif 文案，pill 边框、背景与弱化层级未对齐原型 `.version-pill` 及 Design System 徽章规范。
- 与 `TILESFST` 品牌名并排时视觉层级不符合 REQ-0010 与整体工业石材暗色旗舰风设计方案。
- REQ-0010 功能已实现（版本常量与展示位置正确），但视觉验收未达标。

# 影响范围

| 范围 | 影响 |
|---|---|
| Web 管理端 / AdminSidebar brand-head | 版本 pill 视觉与原型不一致 |
| Web 店主端 / Sidebar brand-head（若共用组件） | 可能存在相同 pill 样式偏差 |
| REQ-0010 验收 | AC-006、AC-013、AC-015 未通过 |
| Design System 验收 | 徽章组件视觉一致性不达标 |
| 关联需求 | REQ-0010-product-version-display |
| 关联 Change | `add-product-version-display`（已实现，需 fix-* 补丁） |

# 严重等级说明

严重程度为 `medium`。

理由：

- 不阻断登录、导航或版本号文案展示等核心功能；版本常量与展示位置已正确实现。
- 不影响 API、数据库或权限边界。
- 但属于可见 UI 缺陷，直接影响 REQ-0010 原型验收与 Design System 徽章规范一致性；需在 `fix-product-version-ui-inconsistency` 中闭环。

# 代码线索

| 线索 | 路径 |
|---|---|
| 版本 badge 组件 | `src/web/src/shared/ui/product-version-badge.tsx` |
| 管理端 brand-head | `src/web/src/features/admin/components/AdminSidebar.tsx` |
| 店主端 brand-head | `src/web/src/shared/ui/sidebar.tsx` |
| 产品版本常量 | `src/shared/product-version.ts`（或等价模块） |
| 管理端原型 | `issues/requirements/archive/REQ-0010-product-version-display/prototype/web/product-version-sidebar-admin.html` |
| 店主端原型 | `issues/requirements/archive/REQ-0010-product-version-display/prototype/web/product-version-sidebar-catalog.html` |
| Golden Reference | `issues/requirements/archive/REQ-0010-product-version-display/prototype/web/images/sidebar-version-reference.png` |
| 验收标准 | `issues/requirements/archive/REQ-0010-product-version-display/acceptance.md` |
| UI 规范 | `rules/ui-design.md` §8 |
