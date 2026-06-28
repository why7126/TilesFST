## Why

[BUG-0039-banner-list-display-position-column](issues/bugs/archive/BUG-0039-banner-list-display-position-column/) 与 [BUG-0040-banner-modal-width-too-narrow](issues/bugs/archive/BUG-0040-banner-modal-width-too-narrow/) 已评审通过，同属 REQ-0016 Banner 管理页 `fix-banner-admin-ui` 之后的 UX 优化：

1. **BUG-0039**：列表第一列将 Banner 标题与展示位置（`position`）叠放，扫读差；需独立「展示位置」列（与 `banner-management-list.png` 第一列结构 delta）。
2. **BUG-0040**：Banner 弹窗 640px 窄于 SKU 弹窗 880px，复杂表单体验不一致；产品已确认对齐 SKU 880px（与现行 spec / modal PNG 640px **BREAKING** delta）。

两 BUG 共享 `BannerManagementPage` / `banner-management.css`，合并于本 `fix-*` change。

## What Changes

- **BUG-0039**：第一列仅缩略图 + 标题；新增「展示位置」列；`colSpan` 9；MODIFIED 列表列结构（相对 list PNG）。
- **BUG-0040**：`.banner-modal-card` 宽度 640px → **880px**（对齐 `.sku-modal-card`）；保留 `max-width: 100%`、BUG-0033 滚动与 textarea 验收；MODIFIED `web-client` Banner 弹窗宽度；modal PNG 640px 验收改为与 SKU 弹窗并排。
- 补充 `BannerManagementPage` / `BannerFormModal` Vitest；各 BUG acceptance 独立勾选；change `trace.md` 记录验收。

## Capabilities

### New Capabilities

（无。）

### Modified Capabilities

- `web-client`：MODIFIED「管理端 Banner 管理页」— 展示位置独立列；第一列仅标题。
- `web-client`：MODIFIED「Banner 新增编辑弹窗」— 宽度 880px（与 SKU 弹窗一致）。
- `web-client`：MODIFIED「Banner 管理 PNG 视觉验收 Gate」— 列表第一列 delta；弹窗验收对齐 SKU 宽度。

## Impact

| 影响面 | 说明 |
|---|---|
| Web 管理端 | `BannerManagementPage.tsx`、`banner-management.css`；可选 `BannerFormModal.test.tsx` |
| 后端 / API / Orval | 无 |
| 数据库 | 无 |
| 父需求 | REQ-0016-banner-management |
| 关联 BUG | BUG-0039、BUG-0040 |
| 前置 Change | `add-banner-management`、`fix-banner-admin-ui` |

## Rollback Plan

1. 回滚 `BannerManagementPage.tsx`、`banner-management.css` 及测试至 fix 前版本。
2. 运行 `cd src/web && pnpm vitest run Banner && pnpm build`。
3. 若已 archive，从 `openspec/specs/web-client/spec.md` 恢复 MODIFIED requirement 前版本。
4. 重新标记 BUG-0039、BUG-0040 为未修复。
