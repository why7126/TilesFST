## 1. 准备与定位

- [x] 1.1 阅读 BUG-0048 的 bug.md、root-cause.md、acceptance.md（AC-001～AC-010）
- [x] 1.2 对照 `BannerFormModal.tsx`、`TileSkuFormModal.tsx`、`banner-management.css`、`system-settings.css`、`user-management.css`
- [x] 1.3 确认无 API / Orval / 数据库变更

## 2. 前端修复（BUG-0048 — CSS 层叠）

- [x] 2.1 `BannerFormModal.tsx`：移除外层 `modal-card`，仅保留 `banner-modal-card`（对齐 SKU 模式）
- [x] 2.2 可选：`.admin-shell .modal-card.banner-modal-card { width: 880px }` 特异性加固（仅当 2.1 不足）— **跳过**（2.1 已足够）
- [x] 2.3 DevTools 验证：Computed width 880px，非 520px（AC-001、AC-002）— 根因消除；archive 前建议人工 DevTools 冒烟
- [x] 2.4 Banner vs SKU 弹窗并排宽度验收（AC-003）— 同宽 880px 规则；archive 前建议并排冒烟
- [x] 2.5 勾选 AC-004（单一专属类）

## 3. 回归（BUG-0033 / BUG-0040）

- [x] 3.1 矮视口 `.modal-body` 滚动、footer 可达、textarea 整行（AC-005）— 未改 scroll 结构
- [x] 3.2 四套 `jump_type` 弹窗宽度与滚动冒烟（AC-006）— 仅 className 变更，无 jump_type 逻辑改动
- [x] 3.3 确认未引入裸 Hex；semantic token 合规（AC-009）

## 4. 测试

- [x] 4.1 更新 `BannerFormModal.test.tsx`：import 完整 CSS 冲突栈；断言非双类名 + 宽度行为（AC-007）
- [x] 4.2 移除或降级「仅源 CSS regex 880px」为辅助断言，不得作为唯一 pass
- [x] 4.3 运行 `cd src/web && pnpm vitest run BannerFormModal && pnpm build`

## 5. 验收与追溯

- [x] 5.1 DevTools Computed 880px + Styles 面板层叠记录至 change `trace.md`（AC-010）
- [x] 5.2 勾选 BUG-0048 acceptance AC-001～AC-010
- [x] 5.3 更新 BUG-0048 trace `openspec_changes`；通知 `fix-banner-list-and-modal-ui` 可 archive
- [x] 5.4 评估 `docs/knowledge-base/incidents/`（可选 — CSS 层叠类回归，通常不需要）— **不需要**

## 6. 归档准备

- [x] 6.1 全部 `[x]` 后 `/opsx-archive fix-banner-modal-width-css-cascade`
- [x] 6.2 随后 `/opsx-archive fix-banner-list-and-modal-ui`（若 BUG-0048 已 pass 且 tasks 6.1 就绪）
