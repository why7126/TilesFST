## 1. 前端修复

- [x] 1.1 修改 `TileCategoryManagementPage.tsx`：操作列对齐 `BrandManagementPage`（启停按钮与删除独立；停用行始终展示「启用」）
- [x] 1.2 确认 `handleToggleStatus` / `enableCategory` 在停用+SKU=0 场景可正常触发

## 2. 测试

- [x] 2.1 新增 `TileCategoryManagementPage.test.tsx`（或等价）：停用+SKU=0 行含「启用」「删除」；启用行含「停用」且无「删除」
- [x] 2.2 运行 `cd src/web && npx vitest run src/pages/admin/TileCategoryManagementPage.test.tsx`
- [x] 2.3 运行 `cd src/web && npm run build`

## 3. 冒烟与验收

- [x] 3.1 Docker 或本地：`/admin/tile-categories` 200；手工确认 BUG AC-002（停用+SKU=0 行有「启用」）
- [x] 3.2 填写 `openspec/changes/fix-tile-category-enable-action/trace.md` checklist

## 4. 追溯与归档

- [x] 4.1 更新 `issues/bugs/BUG-0001-tile-category-enable-missing/trace.md`（`status: done`；`openspec_changes.status: applied`）
- [ ] 4.2 （可选）`docs/knowledge-base/incidents/` 沉淀「canDelete 勿绑定启停展示」
- [x] 4.3 完成后 `/opsx-archive fix-tile-category-enable-action`
