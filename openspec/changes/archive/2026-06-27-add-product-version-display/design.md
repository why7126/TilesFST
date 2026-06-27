## Context

- **现状**：管理端 `AdminSidebar` 顶部 `.logo` 仅 `TILESFST`；店主端 `Sidebar`（`src/web/src/shared/ui/sidebar.tsx`）无品牌头；无 `PRODUCT_VERSION` 常量。
- **依赖**：`REQ-0004-admin-home` Admin Shell；店主端 `LandingPage` / `ListPage` + `CatalogBody`。
- **原型来源**（优先级，design.md 声明）：
  1. `issues/requirements/REQ-0010-product-version-display/prototype/web/product-version-sidebar-admin.html`
  2. `issues/requirements/REQ-0010-product-version-display/prototype/web/product-version-sidebar-catalog.html`
  3. `issues/requirements/REQ-0010-product-version-display/prototype/web/images/sidebar-version-reference.png`（Golden Reference — 布局参照）
  4. `issues/requirements/REQ-0010-product-version-display/prototype/web/product-version-display-context.md`
  5. `issues/requirements/REQ-0010-product-version-display/acceptance.md`
  6. `rules/ui-design.md` §8 徽章
  7. `openspec/specs/admin-dashboard/spec.md`、`openspec/specs/web-client/spec.md`

## Conflict Resolution

| 检查项 | admin-home.html / PNG | SoulKing 参考 PNG | acceptance / REQ-0010 | openspec/specs | 决议 |
|--------|----------------------|-------------------|----------------------|----------------|------|
| Sidebar 顶部 | 仅 TILESFST `.logo` | 产品名 + v0.0.6 pill | **必须有** pill | 仅 TILESFST 文案 | **MODIFIED** `管理端 Sidebar 品牌与导航` |
| 店主端侧栏 | 无 brand-head | 同布局语义 | 侧栏内 brand-head | 无要求 | **ADDED** `web-client` 产品版本展示 |
| 版本来源 | — | — | 人工 `src/shared/` | — | **ADDED** 禁止 package.json/API version |
| 登录页/页脚 | — | — | Out of Scope | — | 无变更 |

## Goals / Non-Goals

**Goals:**

- 单一 `PRODUCT_VERSION` 常量；管理端 + 店主端展示一致。
- 产品名右侧小号 pill；10–11px muted；semantic token；读屏可感知。
- Vitest 通过 import 常量断言；`pnpm test` + `pnpm build` 通过。

**Non-Goals:**

- 登录页、页脚、关于页、小程序版本。
- API / `/health` 版本、CI 自动递增、Git 注入。
- 侧边栏折叠 chevron（参考图右侧，后续迭代）。
- 实现 PNG Golden 导出（apply 阶段条件项，非阻塞 archive）。

## Decisions

### D1：实现策略 — Tailwind DS + 共享组件（非 CSS Port 全页）

- **决策**：新增 `ProductVersionBadge`（`src/web/src/shared/ui/` 或 `shared/business/`）+ `src/shared/product-version.ts`；管理端 brand-head 扩展 `.logo` 区域为 flex 行；店主端 `Sidebar` 增加可选 `brandHead` prop 或内置头部 slot。
- **理由**：变更面小（2 处挂载 + 1 常量）；复用 DS semantic class（`text-muted`、`border-border-chip`、`rounded-industrial`）；不必 port 整页 HTML。
- **备选**：纯 CSS Port 改 `admin-home.css` only — 无法覆盖店主端；弃用。

### D2：版本常量位置

```typescript
// src/shared/product-version.ts
export const PRODUCT_VERSION = 'v0.0.1';
```

- Web 通过 `@shared/` 或现有 alias 引用。
- 发版时人工更新；MUST NOT 读 `import.meta.env` 构建号作为产品版本。

### D3：店主端品牌名

- 默认展示 Design System 店主端品牌 **STONEX**（与 `SiteNav` 一致）；MAY 通过 `Sidebar` prop 覆盖。
- 版本 pill 规格与管理端相同组件。

### D4：可访问性

- brand-head 容器或 badge：`aria-label="产品版本 v0.0.1"`（动态拼接常量值）。
- pill 内保留可见 `v0.0.1` 文本。

## Risks / Trade-offs

| 风险 | 缓解 |
|------|------|
| 发版忘记改常量 | acceptance AC-003 + release checklist |
| 与 npm 0.1.0 混淆 | spec 禁止；代码 review |
| 窄屏 brand-head 换行 | flex-wrap；pill 紧跟产品名语义组 |

## Migration Plan

- 无数据迁移；部署后即可见新版本常量。
- 回滚：revert 前端 commit 即可。

## Open Questions

- 无（REQ-0010 已 approved，探索项已闭合）。
