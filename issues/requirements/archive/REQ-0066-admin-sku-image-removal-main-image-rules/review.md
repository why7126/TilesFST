---
review_id: REV-REQ-0066-001
date: 2026-07-22
participants:
  - product
result: approved
created_at: 2026-07-22 09:24:44
updated_at: 2026-07-22 09:24:44
---

# REQ-0066 需求评审

## 评审结论

通过。

本需求作为 `REQ-0006-tile-sku-management` 的 refinement，范围清晰聚焦在管理端 SKU 编辑弹窗的商品图片移除、主图前置和移除主图后的兜底主图规则；Out of Scope 已明确不做拖拽排序、批量删除、上传接口变更、对象存储物理删除、小程序/店主端展示调整。

验收标准覆盖图片移除入口、移除非主图、设置主图并前置、移除当前主图、移除全部图片、保存 payload 与回填一致性；UI 类原型策略已提供 `prototype/web/` HTML 与 context；已按 knowledge-base 写入 `admin-modal`、`media-upload` 横切 AC。

## 评审检查清单

- [x] 范围清晰，Out of Scope 明确。
- [x] 验收标准可测试。
- [x] 优先级与依赖合理。
- [x] UI 类原型或实现策略已决。
- [x] 无与现有 REQ 重复未说明；本需求作为 `REQ-0006-tile-sku-management` 的 refinement 独立推进。

## 条件通过项

- [ ] 后续 `/req-opsx` 的 design.md 必须引用 `knowledge_base_refs`，并保留 `admin-modal`、`media-upload` 横切验收。
- [ ] 实现阶段默认不调整图片上传接口、大小限制、MinIO 前缀或对象存储物理删除策略；若发生 contract 变化，必须同步 OpenAPI、Orval、docs 和测试。
- [ ] 图片移除仅解除 SKU 与图片的关联；不得在未补充媒体治理设计前物理删除可能被复用的对象文件。
- [ ] 前端组件测试必须覆盖移除非主图、设主图前置、移除主图兜底和移除全部图片。

## 后续动作

1. `/req-opsx REQ-0066-admin-sku-image-removal-main-image-rules`
2. `/sprint-propose` 纳入迭代后再开发
