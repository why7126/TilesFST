## Why

[BUG-0013-product-version-ui-inconsistency](issues/bugs/BUG-0013-product-version-ui-inconsistency/) 已评审通过。`add-product-version-display` 已在管理端与店主端挂载 `ProductVersionBadge`，但版本 pill 视觉未对齐 REQ-0010 原型、Golden Reference 与 Design System §8 徽章规范（AC-006、AC-013、AC-015 未达标）。根据项目规则，已交付能力上的 UI 验收缺口 MUST 使用新的 `fix-*` change 修复。

## What Changes

- 重构 `ProductVersionBadge`：优先扩展 `Badge` 组件 variant，对齐原型 `.version-pill` 与 `rules/ui-design.md` §8（padding、字重、tracking、semantic token）。
- 管理端 `admin-home.css`：为 `.brand-head` 内版本 pill 提供 shell 级样式兜底（确保 admin 渐变侧栏下边框/背景/弱化文字可辨识）。
- 店主端 `Sidebar` brand-head：与管理端共用同一 badge 实现，双端视觉一致。
- Vitest：断言 pill 关键 class（边框、muted 文字等），不仅断言版本文案。
- 1280×1024 并排验收：admin/catalog 原型 HTML + Golden Reference PNG；记录于 change `trace.md`。
- **不** 变更 `PRODUCT_VERSION` 维护策略、API、数据库、Orval、MinIO。

## Capabilities

### New Capabilities

（无新 capability 目录；视觉修复归入 `admin-dashboard` 与 `web-client` delta。）

### Modified Capabilities

- `admin-dashboard`：ADDED 产品版本 pill 视觉一致性修复要求（管理端 brand-head）。
- `web-client`：ADDED 产品版本 pill 视觉一致性修复要求（店主端 brand-head + 跨端 badge 复用）。

## Impact

| 影响面 | 说明 |
|---|---|
| Web 管理端 | `ProductVersionBadge`、`AdminSidebar`、`admin-home.css` brand-head |
| Web 店主端 | `shared/ui/sidebar.tsx` brand-head |
| Design System | 复用/扩展 `Badge`；可选 `/design-system` 预览 |
| REQ-0010 | 闭环 AC-006、AC-013、AC-015 |
| 父 Change | 依赖 `add-product-version-display`（功能已 apply；**建议先 archive 再 archive 本 fix**） |
| API / DB / Orval | 无 |

## Rollback Plan

若 pill 样式调整引起 brand-head 布局异常，可回滚本 change 的前端样式与测试改动：

1. 恢复 `product-version-badge.tsx`（及 `badge.tsx` variant 若有变更）至 fix 前版本。
2. 移除 `admin-home.css` 新增 pill scoped 样式。
3. 移除新增 Vitest 样式断言。

回滚不涉及 API、数据库、对象存储或 `PRODUCT_VERSION` 常量。
