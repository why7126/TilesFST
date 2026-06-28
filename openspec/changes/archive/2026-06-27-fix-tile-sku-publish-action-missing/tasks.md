## 1. 前端修复

- [x] 1.1 修改 `TileSkuManagementPage.tsx`：非 `PUBLISHED` 行（含 `DISABLED`）展示 publish 操作；`DISABLED` 文案「恢复」，其余「上架」；与 delete 独立渲染
- [x] 1.2 确认 `handlePublish` / `publishTileSku` 在 `DISABLED` 行可正常触发并刷新列表

## 2. 测试

- [x] 2.1 扩展 `TileSkuManagementPage.test.tsx`：mock `DISABLED` 行含「恢复」；mock `PUBLISHED` 行含「下架」
- [x] 2.2 运行 `cd src/web && npx vitest run src/pages/admin/TileSkuManagementPage.test.tsx`
- [x] 2.3 运行 `cd src/web && npm run build`

## 3. 冒烟与验收

- [x] 3.1 Docker 或本地：`/admin/tile-skus` 200；手工确认 BUG AC-001（下架后行有「恢复」）与 AC-004（恢复后变已上架）
- [x] 3.2 填写 `openspec/changes/fix-tile-sku-publish-action-missing/trace.md` checklist

## 4. 追溯与归档

- [x] 4.1 更新 `issues/bugs/archive/BUG-0014-tile-sku-publish-action-missing/trace.md`（`status: done`；`openspec_changes.status: applied`）
- [ ] 4.2 （可选）`docs/knowledge-base/incidents/` 沉淀「DISABLED 行勿排除 publish 按钮」
- [x] 4.3 完成后 `/opsx-archive fix-tile-sku-publish-action-missing`
