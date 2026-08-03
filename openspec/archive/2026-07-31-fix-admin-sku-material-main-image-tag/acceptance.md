---
change_id: fix-admin-sku-material-main-image-tag
status: applied
source_bug: BUG-0097-admin-sku-material-main-image-tag-redundant
created_at: 2026-07-31 15:16:00
updated_at: 2026-07-31 15:40:28
---

# Acceptance

## 验收清单

- [ ] 素材列只显示图片数量与视频数量，不显示「主图已设」「缺主图」或其他素材状态标签。
- [ ] 素材列仍正确显示图片数量与视频数量。
- [ ] 管理端 SKU 列表不展示素材完整度条件筛选，列表请求不提交 `material_completeness`。
- [ ] 缺图、缺视频或素材不完整状态仍可通过图片/视频数量识别。
- [ ] 移除所有素材状态标签后，列表行高、列宽、状态列和操作列不出现遮挡或布局抖动。
- [ ] SKU 新增、编辑、图片主图兜底、上下架、删除等操作行为不受影响。
