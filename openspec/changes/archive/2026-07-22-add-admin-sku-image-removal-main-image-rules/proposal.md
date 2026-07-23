## Why

管理端 SKU 编辑弹窗已支持商品图片添加与设为主图，但缺少移除任意图片、主图自动前置、移除当前主图后的兜底规则。运营维护错误图片或替换主图时无法形成闭环，保存后的图片顺序和主图状态也容易与展示预期不一致。

## What Changes

- SKU 编辑弹窗商品图片支持移除任意图片，包括当前主图。
- 设置主图后，该图片在弹窗展示和保存 payload 中均移动到第一位。
- 移除非主图时保留当前主图；移除当前主图时按“移除前后一张优先，否则剩余第一张”自动兜底新主图。
- 移除全部图片后允许草稿保持缺图片/缺主图状态，并沿用既有素材完整度规则。
- 明确本 change 不新增上传接口、不调整 MinIO 物理删除策略；图片移除仅解除 SKU 与图片关联。
- 补充前端组件测试、必要的后端回归测试，以及 admin-modal/media-upload 横切验收。

## Capabilities

### New Capabilities

无。

### Modified Capabilities

- `tile-sku-management`: 补充 SKU 编辑弹窗商品图片移除、主图前置、主图兜底和保存回填一致性要求。

## Impact

- **Web 管理端:** 影响 `TileSkuFormModal` 的图片网格、设主图、移除和 payload 构建逻辑。
- **后端 API:** 默认沿用现有 `PUT /api/v1/admin/tile-skus/{id}` images 全量提交语义；不新增接口。
- **数据库:** 默认不新增字段，继续使用 `tile_images.is_main` 与 `sort_order`。
- **对象存储:** 不物理删除 MinIO 对象；仅更新 SKU 与图片关联。
- **测试:** 需要补充 Vitest/Testing Library 组件测试；必要时补充后端主图唯一性和顺序回填测试。
- **Orval:** 默认不需要；若实现改变 images 请求/响应 contract，必须同步 OpenAPI 与 Orval。
