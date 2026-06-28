## 1. 前端 — 用户管理 confirm（BUG-0016 AC-001～AC-004）

- [x] 1.1 `UserManagementPage.tsx`：冻结/解冻点击打开 confirm modal，不直接调 `updateUserStatus`
- [x] 1.2 新增 `statusConfirmTarget` state；标题/正文/按钮对齐 design D4
- [x] 1.3 删除操作改用 `deleteTarget` modal，移除 `window.confirm`
- [x] 1.4 确认后调用 API；Toast + `loadUsers()`；取消/遮罩/× 不请求

## 2. 前端 — SKU 上下架 confirm（BUG-0016 AC-005～AC-007）

- [x] 2.1 `TileSkuManagementPage.tsx`：上架/下架/恢复点击打开 confirm modal，不直接调 API
- [x] 2.2 新增 `statusConfirmTarget` + `statusConfirmAction`（或等价），与 `deleteTarget` 分离
- [x] 2.3 文案对齐 design D4；确认后 Toast + `loadSkus()`

## 3. 测试

- [x] 3.1 更新 `UserManagementPage.test.tsx`：冻结/解冻/删除须先出 dialog；确认前 mock 未调用；取消后不调用
- [x] 3.2 更新 `TileSkuManagementPage.test.tsx`：上下架/恢复同上
- [x] 3.3 运行 `cd src/web && npx vitest run src/pages/admin/UserManagementPage.test.tsx src/pages/admin/TileSkuManagementPage.test.tsx`
- [x] 3.4 回归 `BrandManagementPage.test.tsx`、`TileCategoryManagementPage.test.tsx` 启停/删除用例
- [x] 3.5 运行 `cd src/web && npm run build`

## 4. 冒烟与追溯

- [ ] 4.1 本地/Docker：`/admin/users` 与 `/admin/tile-skus` 手工 confirm 流程（待 `/opsx-archive` 前人工冒烟）
- [x] 4.2 填写 `openspec/changes/fix-admin-list-status-action-confirm/trace.md` checklist（≥8 项）
- [x] 4.3 更新 `issues/bugs/archive/BUG-0016-admin-list-status-action-confirm-missing/trace.md`（`openspec_changes.status: applied`）
- [x] 4.4 更新 `iterations/archive/sprint-002/acceptance-report.md` BUG-0016 验收状态
- [x] 4.5 完成后 `/opsx-archive fix-admin-list-status-action-confirm`

## 5. 知识沉淀（可选）

- [ ] 5.1 若修复过程有通用经验，可更新 `docs/knowledge-base/incidents/`（本缺陷为 UI 交互缺口，通常可跳过）
