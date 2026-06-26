## 1. 前端 — 启停确认（O-01）

- [x] 1.1 `BrandManagementPage.tsx`：启停点击打开确认弹窗，不直接调 API
- [x] 1.2 复用删除 modal 结构；标题/正文/按钮对齐 `brand-status-confirm-context.md`
- [x] 1.3 独立 `statusConfirmTarget` / `statusConfirmAction` state，与 `deleteTarget` 分离
- [x] 1.4 确认后调用 `enableBrand` / `disableBrand`；Toast + `loadBrands()`

## 2. 测试

- [x] 2.1 更新 `BrandManagementPage.test.tsx`：启停须先出确认弹窗；确认前 mock API 未被调用
- [x] 2.2 vitest：确认启用/停用后 mock API 被调用；取消/关闭后 API 未被调用
- [x] 2.3 运行 `cd src/web && npx vitest run src/pages/admin/BrandManagementPage.test.tsx`
- [x] 2.4 运行 `cd src/web && npm run build`

## 3. 冒烟与视觉

- [x] 3.1 本地/Docker：`/admin/brands` 200；手工启停确认流程（vitest + build 通过；Docker 可选手工）
- [x] 3.2 填写 `openspec/changes/fix-brand-status-confirm/trace.md` checklist（≥8 项）
- [ ] 3.3 （可选）导出启停确认 PNG

## 4. 追溯与归档

- [x] 4.1 更新 `issues/requirements/REQ-0008-brand-status-confirm/trace.md`（`openspec_changes.status: applied`）
- [x] 4.2 更新 `iterations/sprint-002/acceptance-report.md` REQ-0008 验收状态
- [x] 4.3 完成后 `/opsx-archive fix-brand-status-confirm`
