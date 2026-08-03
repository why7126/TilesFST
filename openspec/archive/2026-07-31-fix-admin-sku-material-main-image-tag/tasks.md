## 1. Implementation

- [x] 1.1 调整管理端 SKU 列表素材列渲染，移除「主图已设」「缺主图」等素材状态标签。
- [x] 1.2 保留图片数量与视频数量展示。
- [x] 1.3 确认缺图、缺视频或素材不完整状态仍可通过图片/视频数量识别。
- [x] 1.4 删除管理端 SKU 列表素材完整度条件筛选，列表请求不提交 `material_completeness`。

## 2. Tests

- [x] 2.1 更新 `TileSkuManagementPage` 相关前端测试，验证素材列不显示「主图已设」「缺主图」等素材状态标签。
- [x] 2.2 更新或补充测试，验证素材列仍显示图片数量与视频数量。
- [x] 2.3 更新或补充测试，验证素材完整度筛选控件已移除，列表请求不提交 `material_completeness`。

## 3. Validation

- [x] 3.1 运行相关前端测试。
- [x] 3.2 视检管理端 SKU 列表，确认素材列行高、列宽、状态列和操作列无遮挡或布局抖动。
- [x] 3.3 判断是否需要沉淀到 `docs/knowledge-base/incidents/`；若无跨模块复用价值，在执行输出中说明不适用。

## 验收返修记录

| 时间 | 反馈 | 调整 | 验证 |
|---|---|---|---|
| 2026-07-31 15:36:22 | 删除素材完整度的条件筛选。 | 移除管理端 SKU 列表素材完整度筛选状态、下拉控件与 `material_completeness` 请求参数；同步测试、验收、设计、delta spec、Sprint 验收/发布文案。 | `pnpm --dir src/web test -- TileSkuManagementPage` 通过；`openspec validate fix-admin-sku-material-main-image-tag --strict` 通过；`git diff --check` 通过。 |
| 2026-07-31 15:28:34 | 素材列只显示图片/视频数量，其他标签全部移除。 | 移除缺主图标签，素材列统一只渲染 `image_count` / `video_count` 数量；同步测试、验收、设计、delta spec、Sprint 验收/发布文案。 | `pnpm --dir src/web test -- TileSkuManagementPage` 通过；`openspec validate fix-admin-sku-material-main-image-tag --strict` 通过；`git diff --check` 通过。 |
