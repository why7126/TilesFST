---
created_at: 2026-06-27 12:02:52
updated_at: 2026-06-27 12:02:52
title: fix-tile-sku-modal-subtitle-inconsistency 追溯
purpose: BUG-0010 SKU 弹窗副标题 UI 对齐
content: 共享 modal-desc；SKU/品牌弹窗头部自适应
owner: product
status: applied
bug_id: BUG-0010-tile-sku-modal-subtitle-inconsistency
related_requirement: REQ-0006-tile-sku-management
sprint: sprint-002
---

# Change 追溯

## 验收 checklist

| AC | 描述 | 结果 |
|---|---|---|
| AC-001 | 使用 modal-desc | pass |
| AC-002 | Typography 与品牌一致 | pass |
| AC-003 | 头部自适应 | pass |
| AC-004 | AC-023 语义保留 | pass |
| AC-005 | 不回退 BUG-0011/0012 | pass |
| AC-006 | Vitest 覆盖 | pass |

## 变更文件

- `src/web/src/features/admin/styles/user-management.css`
- `src/web/src/features/admin/styles/tile-sku-management.css`
- `src/web/src/features/admin/styles/brand-management.css`
- `src/web/src/features/admin/components/TileSkuFormModal.tsx`
- `src/web/src/features/admin/components/BrandFormModal.tsx`
- `src/web/src/features/admin/components/TileSkuFormModal.test.tsx`

## 变更记录

| 日期 | 动作 | 说明 |
|---|---|---|
| 2026-06-27 12:02:52 | `/bug-opsx` + 代码并入 | 创建 change；副标题对齐已实现 |
