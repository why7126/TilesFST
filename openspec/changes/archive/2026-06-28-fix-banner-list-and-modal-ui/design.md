## Context

- **BUG**: BUG-0039（medium）、BUG-0040（medium）
- **Related REQ**: `REQ-0016-banner-management`
- **Parent Changes**: `add-banner-management`、`fix-banner-admin-ui`
- **Target files**: `BannerManagementPage.tsx`、`banner-management.css`；`BannerFormModal` 仅 CSS 宽度（组件类名不变）

### 原型 / 验收优先级（MUST）

```text
1. issues/bugs/review/BUG-0039、BUG-0040/acceptance.md
2. TileSkuFormModal + .sku-modal-card（880px 弹窗基准 — BUG-0040）
3. issues/requirements/archive/REQ-0016-banner-management/prototype/web/banner-management-list.html（列表列结构历史参考）
4. openspec/specs/web-client/spec.md（MODIFIED 后为准）
5. rules/ui-design.md
```

## Bug Analysis Report

| ID | 摘要 | 根因类型 |
|---|---|---|
| 0039 | 第一列 banner-main + banner-sub 叠放 | design / frontend-ui（原型 port） |
| 0040 | banner-modal-card 640px vs sku 880px | design / frontend-ui（REQ-0016 640px spec） |

## Goals / Non-Goals

**Goals:**

- 列表独立「展示位置」列；第一列仅标题（0039）。
- Banner 弹窗 880px，与 SKU 弹窗一致（0040）。
- BUG-0033 滚动、textarea、footer 无回归。
- Vitest 覆盖列结构与弹窗宽度。
- delta spec MODIFIED 消化 list PNG 第一列与 modal 640px 要求。

**Non-Goals:**

- Banner 后端 / API / 权限。
- 店主 Web / 小程序展示端。
- 抽取共享 admin 大弹窗 token（可选后续 REQ）。

## Decisions

### D1：两 BUG 合并单一 fix change

- **理由**：同属 Banner 管理 UI；单 PR 交付。

### D2：展示位置列（0039）

- 表头新增「展示位置」；`positionLabel(banner.position)` 纯文本或弱样式（非 badge，与展示端区分）。
- 第一列删除 `banner-sub`；可选删除未用 `.banner-sub` CSS。
- `colSpan` 8 → 9。

### D3：弹窗 880px（0040）

- `.banner-modal-card { width: 880px }`；保留 `max-height: 92vh`、flex scroll（0033）。
- 可选对齐 `.sku-modal-card` 的 `border`、`box-shadow`、`modal-head` padding（非必须，以实现验收为准）。
- **不**改 `BannerFormModal.tsx` 结构除非测试需要。

### D4：验收基准切换

- 列表：acceptance 优先于 `banner-management-list.png` 第一列。
- 弹窗：与 SKU 弹窗并排宽度；不以 640px modal PNG 为 pass gate。

## Risks / Trade-offs

| 风险 | 缓解 |
|---|---|
| 列表 PNG 第一列不一致 | delta MODIFIED + trace 记录 |
| 880px 与 modal HTML 冲突 | delta MODIFIED + review 已确认 |
| BUG-0033 回归 | AC-003 显式回归滚动/textarea |

## Test Plan

- Vitest：`BannerManagementPage` — 表头「展示位置」、第一列无 `.banner-sub`。
- Vitest/CSS：`banner-modal-card` 880px（或 computed style 断言）。
- 手工：Banner vs SKU 弹窗并排；四套 jump_type 滚动到底。
- `cd src/web && pnpm vitest run Banner && pnpm build`
