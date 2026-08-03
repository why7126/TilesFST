---
change_id: fix-admin-sku-list-publish-sort-order
source_bug: BUG-0090-admin-sku-list-publish-sort-order
status: proposed
created_at: 2026-07-30 23:28:00
updated_at: 2026-07-30 23:28:00
---

# 验收计划

## 必验项

- 已发布 SKU 默认按 `published_at DESC` 展示。
- 未发布 SKU 默认按 `created_at DESC` 展示。
- 已发布与未发布混排时已发布分组优先，分组内排序符合业务时间。
- `published_at` 为空、主排序时间相同、跨页分页时顺序稳定。
- 搜索、品牌筛选、类目筛选、状态筛选、素材完整度筛选后继续遵循同一排序契约。
- SKU 新增、编辑、上架、下架、删除行为不因排序修复回归。

## 测试建议

- 后端：补充或更新 `src/backend/tests/test_admin_tile_skus.py` 或等价测试。
- 前端：补充或更新 `src/web/src/pages/admin/TileSkuManagementPage.test.tsx`。
- 校验：运行相关 pytest、Vitest、`openspec validate fix-admin-sku-list-publish-sort-order --strict` 和目录结构校验。

## 非目标

- 不要求新增排序控件。
- 不要求迁移历史 `published_at` 为空的数据。
- 不要求变更 API 请求/响应字段；若实现阶段选择变更，必须另行同步契约与生成物。
