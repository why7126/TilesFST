---
change_id: fix-admin-category-tree-count
status: proposed
source_bug: BUG-0095-admin-category-tree-count-shows-product-count
created_at: 2026-07-31 15:13:20
updated_at: 2026-07-31 15:13:20
---

# Acceptance

## 验收清单

- [ ] 管理端一级类目右侧数字显示直接子类目数量，不显示商品数量。
- [ ] 管理端叶子类目右侧数字显示 `0`，即使该类目下存在商品也不显示商品数量。
- [ ] “全部类目”入口右侧数字显示顶层类目数量，不显示商品总数。
- [ ] 展开/折叠类目树和点击节点刷新右侧列表行为不回归。
- [ ] `sku_count` 既有商品/SKU 数量语义不变，删除规则和商品统计不受影响。
- [ ] 若补齐 API 契约，OpenAPI、Orval、接口文档和后端接口测试同步完成。
