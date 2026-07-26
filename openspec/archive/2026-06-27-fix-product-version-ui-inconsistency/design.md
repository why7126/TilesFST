## Context

- **BUG**: `BUG-0013-product-version-ui-inconsistency`
- **Severity**: medium
- **Root cause type**: design / frontend-ui
- **Related REQ**: `REQ-0010-product-version-display`
- **Parent change**: `add-product-version-display`（complete，17/17 tasks；功能已 apply，待 archive）
- **Target**: `ProductVersionBadge`、`Badge`、`admin-home.css` brand-head、店主端 `Sidebar`

### 原型优先级（MUST）

```text
1. issues/requirements/archive/REQ-0010-product-version-display/prototype/web/product-version-sidebar-admin.html
2. issues/requirements/archive/REQ-0010-product-version-display/prototype/web/product-version-sidebar-catalog.html
3. issues/requirements/archive/REQ-0010-product-version-display/prototype/web/images/sidebar-version-reference.png
4. issues/requirements/archive/REQ-0010-product-version-display/prototype/web/product-version-display-context.md
5. issues/bugs/archive/BUG-0013-product-version-ui-inconsistency/acceptance.md
6. rules/ui-design.md §8
7. src/web/src/shared/ui/badge.tsx（DS 黄金参考）
```

## Bug Analysis Report

### 现象

管理端侧边栏 `TILESFST` 右侧版本号视觉未呈现可辨识 muted pill；与原型及 Golden Reference 并排不一致。店主端共用 `ProductVersionBadge`，存在相同风险。

### 复现路径

1. admin 登录，访问 `/admin/tile-skus`（或任意 `/admin/*`）。
2. 观察 brand-head 版本 pill。
3. 并排对照原型 HTML、Golden Reference PNG、`screenshots/admin-sidebar-version-actual.png`。

### 影响

- 不阻断版本文案展示与 `PRODUCT_VERSION` 常量正确性。
- 阻塞 REQ-0010 AC-006、AC-013、AC-015 与 BUG-0013 acceptance。
- 不影响 API、DB、权限、MinIO。

## Root Cause（摘要）

| ID | 结论 |
|---|---|
| RC-001 | `ProductVersionBadge` ad-hoc 实现，未扩展 DS `Badge` neutral variant |
| RC-002 | 样式规格在原型 context 与 ui-design §8 间取中间值，并排验收未执行 |
| RC-003 | 管理端 brand-head 产品名走 CSS port，pill 纯 Tailwind，admin shell 下对比度不足 |
| RC-004 | Vitest 仅断言文案，无 pill class 覆盖 |

## Goals / Non-Goals

**Goals:**

- 版本 pill 在 admin/catalog 双端可辨识（边框 + 浅背景 + muted 文字）。
- 对齐原型 `.version-pill` 语义与 DS §8（padding 2px 7px、font-weight 500、tracking-badge、semantic token）。
- Vitest 样式断言 + 1280×1024 并排验收记录。
- REQ-0010 视觉 AC 与 BUG-0013 acceptance 闭环。

**Non-Goals:**

- 修改 `PRODUCT_VERSION` 来源或发版流程。
- 登录页/页脚/关于页版本展示。
- API / 后端 / OpenAPI 版本。
- 侧边栏折叠 chevron（REQ-0011 范围）。

## Decisions

### D1：重构策略 — 扩展 `Badge` variant，而非继续 ad-hoc span

- **决策**：为 `Badge` 新增 `version` variant（或等价），`ProductVersionBadge` 薄封装该 variant；规格对齐 prototype context §3（高度 ~18px、10px 字号、2px 圆角、`text-muted`、`border-border-chip`、浅背景 token）。
- **理由**：符合 AGENTS.md 组件选用优先级；与 `/design-system` Badge 预览一致。
- **备选**：纯 `admin-home.css` `.version-pill` port — 无法覆盖店主端；作为 **admin 兜底** 保留（D2）。

### D2：管理端 CSS 兜底

- **决策**：在 `admin-home.css` 增加 `.admin-shell .brand-head .version-pill`（或 data-attribute）scoped 规则，确保在 `--admin-text` 继承环境下 pill 边框/背景/文字弱化可见。
- **理由**：RC-003 admin shell 混用策略；Tailwind-only 在渐变侧栏下 pill  affordance 不足。

### D3：原型 vs ui-design §8 冲突决议

| 属性 | 原型 | ui-design §8 | 决议 |
|------|------|--------------|------|
| 圆角 | 2px | 1px badge | **2px**（`rounded-industrial`，对齐 REQ-0010 context + Golden Reference 布局语义） |
| 字号 | 10px | 9px | **10px**（REQ-0010 acceptance AC-013） |
| padding | 2px 7px | 2px 7px | 一致 |
| 字重/字距 | — | 500 / tracking-badge | **采用 DS** |

### D4：测试策略

- Vitest：`ProductVersionBadge` / `AdminSidebar` / `Sidebar` 断言 pill 元素含 `border-border-chip`、`text-muted`（或 variant class）。
- 人工：1280×1024 admin + catalog 原型 HTML + Golden Reference PNG 并排。
- 构建：`cd src/web && pnpm test && pnpm build`。

### D5：Archive 顺序

- **决策**：`add-product-version-display` SHOULD 先于本 fix archive，避免 main spec 缺少版本 requirement 标题。
- **缓解**：本 change delta 使用 ADDED fix requirement，降低 archive 顺序硬依赖。

## Risks / Trade-offs

| 风险 | 缓解 |
|------|------|
| Badge variant 与现有 neutral 混淆 | 独立 `version` variant；Design System 页补充示例 |
| admin CSS 与 Tailwind 重复 | CSS 仅作 admin shell 兜底；店主端仍靠 shared component |
| add 未 archive 导致 spec 合并顺序 | proposal/design 声明 archive 顺序；delta 用 ADDED fix requirement |

## Migration Plan

- 无数据迁移；前端样式 deploy 即生效。
- 回滚：revert 本 change 前端 commit（见 proposal Rollback Plan）。

## Open Questions

- 无（BUG-0013 已 approved，acceptance 已明确）。
