---
bug_id: BUG-0013-product-version-ui-inconsistency
status: captured
created_at: 2026-06-27 10:54:19
updated_at: 2026-06-27 10:54:19
severity_hint: medium
environment: local|docker
related_requirement: REQ-0010-product-version-display
related_bug:
---

# 现象

管理端侧边栏顶部产品版本号（如 `v0.0.1`）的视觉样式与 REQ-0010 原型及 Design System 不一致：未呈现预期的 muted 版本 pill（边框、圆角、弱化文字色），与 `TILESFST` 品牌名并排时字体/颜色层级混乱，破坏侧边栏 brand-head 统一视觉。

# 复现步骤

1. 以 admin 登录管理端（本地或 Docker）。
2. 进入任意 `/admin/*` 页面（如 `/admin/tile-skus`）。
3. 观察左侧侧边栏顶部 `TILESFST` 右侧的版本号展示。
4. 并排对照：
   - `issues/requirements/archive/REQ-0010-product-version-display/prototype/web/product-version-sidebar-admin.html`
   - `issues/requirements/archive/REQ-0010-product-version-display/prototype/web/images/sidebar-version-reference.png`
   - `issues/requirements/archive/REQ-0010-product-version-display/acceptance.md`（AC-006、AC-013、AC-015）

# 期望 vs 实际

| | 说明 |
|---|---|
| **期望** | 产品名右侧同一行展示小号版本 pill：高度约 18px、`rounded-industrial`（2px）、`border-border-chip`/`border-border-default`、弱化文字色（`text-muted`/`text-subtle`）、10px 字号；布局与原型 `.version-pill` 及 Golden Reference 一致；使用 semantic token，无裸 Hex。 |
| **实际** | 版本号呈现为偏亮的主文字色 sans-serif 文案，pill 边框/背景/弱化层级未对齐原型与 `rules/ui-design.md` §8 徽章规范；与金色 serif 品牌名并排时视觉层级不符合整体设计。 |

# 影响范围

- Web 管理端：`AdminSidebar` brand-head 区域（`ProductVersionBadge`）。
- 可能连带：店主端 `Sidebar` 顶部同一组件（若共用 `ProductVersionBadge`）。
- 关联需求：REQ-0010-product-version-display。
- 关联 Change：`add-product-version-display`（已实现但视觉未达标）。

# 初步分类（待 /bug-generate 确认）

| 判断 | 结论 |
|---|---|
| 缺陷类型 | UI 视觉一致性缺陷 |
| 严重程度建议 | medium |
| 可能修复面 | `ProductVersionBadge` / brand-head 样式对齐原型与 semantic token |
| 设计约束 | `prototype/web/product-version-sidebar-admin.html`、`rules/ui-design.md` §8 |

# 附件

- `screenshots/admin-sidebar-version-actual.png`（用户提供的实际截图）
- 原型：`issues/requirements/archive/REQ-0010-product-version-display/prototype/web/product-version-sidebar-admin.html`
- Golden Reference：`issues/requirements/archive/REQ-0010-product-version-display/prototype/web/images/sidebar-version-reference.png`
