## 1. 准备与定位

- [x] 1.1 阅读 BUG-0039、BUG-0040 的 bug.md、root-cause.md、acceptance.md
- [x] 1.2 对照 `BannerManagementPage.tsx`、`banner-management.css`、`TileSkuFormModal` / `.sku-modal-card`
- [x] 1.3 确认无 API / Orval 变更

## 2. 前端修复（BUG-0039 — 列表展示位置列）

- [x] 2.1 表头新增「展示位置」；第一列移除 `banner-sub` / `positionLabel` 叠放
- [x] 2.2 新增 `<td>` 展示 `positionLabel(banner.position)`
- [x] 2.3 加载/空态 `colSpan` 调整为 9
- [x] 2.4 可选：移除未用 `.banner-sub` CSS
- [x] 2.5 勾选 BUG-0039 AC-001～AC-008

## 3. 前端修复（BUG-0040 — 弹窗 880px）

- [x] 3.1 `.banner-modal-card { width: 880px }`；保留 `max-width: 100%`、`max-height: 92vh`、flex scroll（0033）
- [x] 3.2 可选：对齐 `.sku-modal-card` border/shadow/head padding
- [x] 3.3 回归 BUG-0033：矮视口滚动、textarea 整行、footer 可达
- [x] 3.4 与 SKU 弹窗并排宽度验收
- [x] 3.5 勾选 BUG-0040 AC-001～AC-010

## 4. 测试

- [x] 4.1 SHOULD：`BannerManagementPage.test.tsx` — 表头「展示位置」、第一列无 `.banner-sub`
- [x] 4.2 SHOULD：`BannerFormModal.test.tsx` 或 CSS 断言 — `.banner-modal-card` 880px
- [x] 4.3 运行 `cd src/web && pnpm vitest run Banner && pnpm build`

## 5. 验收与追溯

- [x] 5.1 列表：第一列仅标题 + 展示位置列人工确认
- [x] 5.2 弹窗：Banner vs SKU 880px 并排；四套 jump_type 滚动冒烟
- [x] 5.3 勾选 BUG-0039、BUG-0040 acceptance
- [x] 5.4 填写本 change `trace.md`；更新 BUG trace `openspec_changes`
- [x] 5.5 评估 `docs/knowledge-base/incidents/`（通常不需要）

## 6. 归档准备

- [x] 6.1 全部 `[x]` 后 `/opsx-archive fix-banner-list-and-modal-ui`（**BUG-0048 apply 完成，可 archive**）
