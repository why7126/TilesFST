---
change_id: fix-admin-sku-material-main-image-tag
status: applied
source_bug: BUG-0097-admin-sku-material-main-image-tag-redundant
created_at: 2026-07-31 15:16:00
updated_at: 2026-07-31 15:40:28
---

# Test Plan

## Automated

- 运行 `pnpm --dir src/web test -- TileSkuManagementPage` 或项目等价前端测试命令。
- 覆盖已有图片 SKU 不显示「主图已设」或「缺主图」。
- 覆盖素材列图片数量与视频数量展示。
- 覆盖缺主图 SKU 素材列也只显示图片/视频数量。
- 覆盖页面不展示素材完整度筛选控件，列表请求不提交 `material_completeness`。

## Manual

- 打开管理后台「瓷砖 SKU」列表。
- 检查 SKU 素材列只显示图片/视频数量，不再显示主图状态标签。
- 检查筛选区不再显示素材完整度条件筛选。
- 检查无图片或素材不完整 SKU 仍能通过图片/视频数量识别。
- 检查列表行高、列宽、状态列和操作列无遮挡。

## Not Required

- 不需要 API 集成测试。
- 不需要数据库迁移测试。
- 不需要 Orval 生成校验。
- 不需要 Docker Compose 验证。
