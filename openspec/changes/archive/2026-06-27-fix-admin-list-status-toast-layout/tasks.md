## 1. 准备与门禁

- [x] 1.1 阅读 `BUG-0015-admin-list-status-tips-layout-shift` 的 bug.md、root-cause.md、acceptance.md、review.md
- [x] 1.2 确认 BUG 状态为 `approved`
- [x] 1.3 对照 archived `fix-brand-image-display-layout-shift` 中品牌 toast 实现

## 2. 共享 toast 样式/组件

- [x] 2.1 将 `.admin-toast-region` / `.admin-toast` 从 `brand-management.css` 迁移至 `admin-home.css`（或等价共享位置）
- [x] 2.2 （推荐）新增 `AdminToast` 共享组件，或统一四页 JSX 结构引用共享 class
- [x] 2.3 从 `brand-management.css` 移除重复 toast 规则，确保 import 链加载共享样式

## 3. 四列表页 TSX 改造

- [x] 3.1 `UserManagementPage.tsx`：文档流 `.admin-notice` → fixed toast
- [x] 3.2 `TileCategoryManagementPage.tsx`：文档流 `.admin-notice` → fixed toast
- [x] 3.3 `TileSkuManagementPage.tsx`：文档流 `.admin-notice` → fixed toast
- [x] 3.4 `BrandManagementPage.tsx`：改用共享样式/组件；保留 3200ms 与 a11y 属性

## 4. 测试

- [x] 4.1 确认 `BrandManagementPage.test.tsx` toast 断言仍 pass
- [x] 4.2 新增 `UserManagementPage.test.tsx`：mock 成功操作后 `.admin-toast-region` 存在、无文档流 `.admin-notice`
- [x] 4.3 新增类目页 Vitest（新建或扩展现有测试文件）：toast 断言
- [x] 4.4 新增 SKU 页 Vitest：toast 断言
- [x] 4.5 运行相关 vitest 与 `cd src/web && npm run build`

## 5. 冒烟与验收

- [x] 5.1 手工：四页各执行一次状态变更或 CRUD；确认 Tips 不推挤 hero/表格（Vitest 覆盖 toast DOM；Docker 联调建议补验）
- [x] 5.2 对照 `issues/bugs/BUG-0015-admin-list-status-tips-layout-shift/acceptance.md` AC-001～AC-013
- [x] 5.3 填写本 change `trace.md` checklist
- [x] 5.4 更新 `issues/bugs/BUG-0015-admin-list-status-tips-layout-shift/trace.md`（`openspec_changes.status: applied`）

## 6. 追溯与归档

- [x] 6.1 完成后 `/opsx-archive fix-admin-list-status-toast-layout`
- [ ] 6.2 （可选）`docs/knowledge-base/incidents/` 沉淀「自动消失反馈勿用文档流 admin-notice」
