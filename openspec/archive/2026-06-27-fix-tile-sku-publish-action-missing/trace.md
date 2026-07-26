---
created_at: 2026-06-27 12:21:11
updated_at: 2026-06-27 12:29:15
title: fix-tile-sku-publish-action-missing Trace
purpose: BUG-0014 → OpenSpec 修复追溯
---

# fix-tile-sku-publish-action-missing — Trace

## 变更摘要

- **BUG**: `BUG-0014-tile-sku-publish-action-missing`
- **REQ**: `REQ-0006-tile-sku-management`
- **Type**: fix
- **Depends**: `add-tile-sku-management`
- **Iteration**: `sprint-002`
- **Status**: archived（2026-06-27 12:29:15）

## 代码变更

| 文件 | 变更 |
|---|---|
| `src/web/src/pages/admin/TileSkuManagementPage.tsx` | 非 PUBLISHED 行展示 publish；DISABLED 文案「恢复」 |
| `src/web/src/pages/admin/TileSkuManagementPage.test.tsx` | 新增 DISABLED「恢复」、PUBLISHED「下架」、publish 点击 Vitest |

## 列表操作列验收 Checklist

| # | 检查项 | 结果 | 备注 |
|---|--------|------|------|
| 1 | DISABLED 行含「恢复」 | pass | Vitest `shows restore action for disabled SKU rows` |
| 2 | PUBLISHED 行含「下架」 | pass | Vitest `shows unpublish action for published SKU rows` |
| 3 | DRAFT 行含「上架」 | pass | 既有 listPayload DRAFT 用例仍通过 |
| 4 | 点击恢复后调用 publishTileSku | pass | Vitest `calls publishTileSku when restore is clicked` |
| 5 | publish 与 delete 独立渲染 | pass | DISABLED 行同时含恢复+删除 |
| 6 | 筛选/分页/弹窗无回归 | pass | 分页 Vitest 4/4 pass；build pass |

## REQ-0006 / BUG 验收对齐

| 条款 | 结果 |
|---|---|
| AC-018 操作列 | pass（Vitest + 代码审查） |
| AC-037 上下架/恢复 | pass（DISABLED→「恢复」） |
| FR-007 | pass |
| BUG AC-001～AC-004 | pass（自动化覆盖核心路径） |

## 测试记录

```text
cd src/web && npx vitest run src/pages/admin/TileSkuManagementPage.test.tsx  → 4 passed
cd src/web && npm run build  → success
```
