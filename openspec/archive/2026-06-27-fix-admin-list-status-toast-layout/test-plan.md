---
purpose: fix-admin-list-status-toast-layout 测试计划
bug_id: BUG-0015-admin-list-status-tips-layout-shift
created_at: 2026-06-27 12:48:52
updated_at: 2026-06-27 12:48:52
---

# 测试计划

## 单元 / 组件（Vitest）

| 页面 | 文件 | 用例 |
|---|---|---|
| 瓷砖品牌 | `BrandManagementPage.test.tsx` | 保留：启用后 `.admin-toast-region` 存在、无 `.admin-notice` |
| 用户管理 | `UserManagementPage.test.tsx` | 新增：mock 冻结/成功路径 toast 断言 |
| 瓷砖类目 | `TileCategoryManagementPage.test.tsx`（或新建） | 新增：mock 启停成功 toast 断言 |
| 瓷砖 SKU | `TileSkuManagementPage.test.tsx` | 新增：mock 上下架成功 toast 断言 |

## 手工冒烟

1. 登录 admin，依次访问四列表页。
2. 每页执行至少一次会触发 Tips 的操作。
3. 目视或 DevTools 记录 `page-hero` 的 `getBoundingClientRect().top` 在 Tips 出现前后不变。

## 回归

- 品牌 Logo 列表展示与弹窗回显
- 四页 CRUD、筛选、分页、权限
- BUG-0003 AC-004/AC-005 品牌 Tips 子集

## 构建

```bash
cd src/web && npx vitest run src/pages/admin/BrandManagementPage.test.tsx src/pages/admin/UserManagementPage.test.tsx
cd src/web && npm run build
```
