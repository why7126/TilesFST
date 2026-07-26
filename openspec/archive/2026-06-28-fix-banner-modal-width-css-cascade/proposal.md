## Why

[BUG-0048-banner-modal-width-css-cascade-overridden](issues/bugs/archive/BUG-0048-banner-modal-width-css-cascade-overridden/) 已评审通过（REV-BUG-0048-001）。`fix-banner-list-and-modal-ui` 已将 `.banner-modal-card` 源 CSS 改为 880px，但 Banner 弹窗 **运行时 Computed width 仍约 520px** — `BannerFormModal` 同时挂载 `modal-card` 与 `banner-modal-card`，全站 CSS bundle 中 `.admin-shell .modal-card { width: 520px }` 层叠覆盖了 880px。BUG-0040 验收意图未闭环。

## What Changes

- `BannerFormModal.tsx`：移除外层冗余 `modal-card` 类，对齐 `TileSkuFormModal` 仅使用 `banner-modal-card` 模式。
- 可选：`banner-management.css` 组合选择器特异性加固（若仍保留双类名则 MUST 保证 880px 生效）。
- `BannerFormModal.test.tsx`：import 完整 admin CSS 冲突栈（`user-management.css`、`system-settings.css`、`banner-management.css`），断言运行时宽度/层叠，**不得**仅 regex 源 CSS 文件。
- MODIFIED `web-client`「Banner 新增编辑弹窗」— 明确运行时 Computed 880px 与禁止 `modal-card` 层叠冲突。
- MODIFIED「Banner 管理 PNG 视觉验收 Gate」— 弹窗验收 MUST 含 DevTools Computed width 检查。
- 勾选 BUG-0048 acceptance AC-001～AC-010；与 `fix-banner-list-and-modal-ui` 一并闭环后 archive。

## Capabilities

### New Capabilities

（无。）

### Modified Capabilities

- `web-client`：MODIFIED「Banner 新增编辑弹窗」— 运行时 Computed 880px；MUST NOT 双类名触发 `.modal-card` 520px 覆盖。
- `web-client`：MODIFIED「Banner 管理 PNG 视觉验收 Gate」— 并排验收 MUST 含 Computed width 与 Styles 面板层叠检查。

## Impact

| 影响面 | 说明 |
|---|---|
| Web 管理端 | `BannerFormModal.tsx`；可选 `banner-management.css`；`BannerFormModal.test.tsx` |
| 后端 / API / Orval | 无 |
| 数据库 | 无 |
| 父需求 | REQ-0016-banner-management |
| 关联 BUG | BUG-0048（本 change）；BUG-0040（父项）；BUG-0033（滚动回归） |
| 前置 Change | `fix-banner-list-and-modal-ui`（880px 源 CSS，待与本 change 一并 archive） |

## Rollback Plan

1. 回滚 `BannerFormModal.tsx`、测试及可选 CSS 至 fix 前版本。
2. 运行 `cd src/web && pnpm vitest run BannerFormModal && pnpm build`。
3. 若已 archive，从 `openspec/specs/web-client/spec.md` 恢复 MODIFIED requirement 前版本。
4. 重新标记 BUG-0048 为未修复；`fix-banner-list-and-modal-ui` 保持未 archive 直至层叠修复验收。
