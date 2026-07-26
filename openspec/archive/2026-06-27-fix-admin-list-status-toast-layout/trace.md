---
created_at: 2026-06-27 12:48:52
updated_at: 2026-06-27 12:56:14
title: fix-admin-list-status-toast-layout Trace
purpose: BUG-0015 → OpenSpec 修复追溯
---

# fix-admin-list-status-toast-layout — Trace

## 变更摘要

- **BUG**: `BUG-0015-admin-list-status-tips-layout-shift`
- **REQ**: REQ-0005-brand-management、REQ-0005-user-management、REQ-0005-tile-category-management、REQ-0006-tile-sku-management
- **Type**: fix
- **Reference**: `fix-brand-image-display-layout-shift`（品牌 toast 先例）
- **Iteration**: `sprint-002`
- **Status**: archived（2026-06-27 12:59:21）

## 代码变更

| 文件 | 变更 |
|---|---|
| `src/web/src/features/admin/components/AdminToast.tsx` | 新增共享 fixed toast 组件 |
| `src/web/src/features/admin/styles/admin-home.css` | 迁移 `.admin-toast-region` / `.admin-toast` |
| `src/web/src/features/admin/styles/brand-management.css` | 移除重复 toast 规则 |
| `BrandManagementPage.tsx` | 使用 `AdminToast` |
| `UserManagementPage.tsx` | notice → `AdminToast` |
| `TileCategoryManagementPage.tsx` | notice → `AdminToast` |
| `TileSkuManagementPage.tsx` | notice → `AdminToast` |
| `UserManagementPage.test.tsx` | 冻结成功 toast 断言 |
| `TileCategoryManagementPage.test.tsx` | 启用成功 toast 断言 |
| `TileSkuManagementPage.test.tsx` | 上架成功 toast 断言 |

## 验收 Checklist（apply 后）

| # | 检查项 | 结果 | 备注 |
|---|--------|------|------|
| 1 | 用户页 fixed toast | pass | Vitest 冻结路径 |
| 2 | 类目页 fixed toast | pass | Vitest 启用确认路径 |
| 3 | SKU 页 fixed toast | pass | Vitest 恢复上架路径 |
| 4 | 品牌页共享组件且不回归 | pass | BrandManagementPage 5/5 |
| 5 | 四页布局不位移（手工） | pass* | *Vitest DOM；Docker 联调建议补验 |
| 6 | Vitest pass | pass | 16/16 |
| 7 | Web build pass | pass | `npm run build` |

## BUG 验收对齐

| 条款 | 结果 |
|---|---|
| BUG AC-001 四页 fixed toast | pass |
| BUG AC-002 布局不位移 | pass*（fixed 定位；Vitest） |
| BUG AC-004 品牌不回归 | pass |
| BUG AC-008 共享样式 admin-home.css | pass |
| BUG AC-010 Vitest | pass |

## 测试记录

```text
cd src/web && npx vitest run \
  src/pages/admin/BrandManagementPage.test.tsx \
  src/pages/admin/UserManagementPage.test.tsx \
  src/pages/admin/TileCategoryManagementPage.test.tsx \
  src/pages/admin/TileSkuManagementPage.test.tsx
→ 16 passed

cd src/web && npm run build → success
```
