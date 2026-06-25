## 1. 前端 — 启停确认（O-01）

- [x] 1.1 `TileCategoryManagementPage.tsx`：启停点击打开确认弹窗，不直接调 API
- [x] 1.2 复用删除 modal 结构；标题/正文/按钮对齐 `tile-category-status-confirm-context.md`
- [x] 1.3 确认后调用 `enableCategory` / `disableCategory`；Toast + `refreshAll()`

## 2. 前端 — 布局精简（O-02、O-03）

- [x] 2.1 移除检索区 `section-head`（「类目检索」+ 副标题）
- [x] 2.2 移除列表区外层 `section-head`（「类目列表」+ 副标题）；保留 `cat-table-toolbar`
- [x] 2.3 调整 `tile-category-management.css` 间距（去标题后无异常留白）

## 3. 前端 — 分页 v2（O-04）

- [x] 3.1 分页 JSX 对齐 `UserManagementPage`（`.pagination` / `.page-summary` / `.page-right`）
- [x] 3.2 左侧「共 {total} 个类目」；右侧页码 +「每页显示」；选项「10 条」「20 条」「50 条」
- [x] 3.3 移除「当前显示 x-y / N 条」及 `cat-pager` 旧结构

## 4. 测试

- [x] 4.1 更新 `TileCategoryManagementPage.test.tsx`：启停须先出确认弹窗；确认后 mock API
- [x] 4.2 vitest：无「类目检索」「类目列表」section 标题；分页含「共 N 个类目」
- [x] 4.3 回归：停用+SKU=0 行「启用」「删除」仍可见（BUG-0001）
- [x] 4.4 运行 `cd src/web && npx vitest run src/pages/admin/TileCategoryManagementPage.test.tsx`
- [x] 4.5 运行 `cd src/web && npm run build`

## 5. 冒烟与视觉

- [x] 5.1 本地/Docker：`/admin/tile-categories` 200；手工启停确认流程
- [x] 5.2 填写 `openspec/changes/fix-tile-category-management-refine/trace.md` checklist（≥12 项）
- [ ] 5.3 （可选）导出 `tile-category-management-list-refine.png`

## 6. 追溯与归档

- [x] 6.1 更新 `issues/requirements/REQ-0007-tile-category-management-refine/trace.md`（`openspec_changes.status: applied`）
- [x] 6.2 完成后 `/opsx-archive fix-tile-category-management-refine`
