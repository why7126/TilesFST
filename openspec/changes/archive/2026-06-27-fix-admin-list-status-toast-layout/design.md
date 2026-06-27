## Context

[BUG-0015-admin-list-status-tips-layout-shift](issues/bugs/BUG-0015-admin-list-status-tips-layout-shift/) 关联四份 REQ 与 archived change `fix-brand-image-display-layout-shift`（品牌 toast 先例）。当前代码线索：

| 页面 | 文件 | 当前模式 |
|---|---|---|
| 瓷砖品牌 | `BrandManagementPage.tsx` | `.admin-toast-region` + `.admin-toast`（fixed，`brand-management.css`） |
| 用户管理 | `UserManagementPage.tsx` | `.admin-notice` 文档流 |
| 瓷砖类目 | `TileCategoryManagementPage.tsx` | `.admin-notice` 文档流 |
| 瓷砖 SKU | `TileSkuManagementPage.tsx` | `.admin-notice` 文档流 |

共性：`notice` state + `useEffect` 3200ms 定时清除。`.admin-notice`（`admin-home.css`）无 fixed/overlay。

## Decisions

### D1：共享 toast 样式位置

`.admin-toast-region` / `.admin-toast` MUST 迁移至 `src/web/src/features/admin/styles/admin-home.css`（或等价管理端全局样式），使四页均通过 `admin-home.css` / 既有页面 CSS import 链加载。

`brand-management.css` 中同名规则 MUST 移除，避免重复定义。

### D2：组件抽取策略

**推荐**：抽取轻量 `AdminToast`（`src/web/src/shared/ui/AdminToast.tsx` 或 `features/admin/components/AdminToast.tsx`），props：`message: string | null`，内部渲染 fixed region + 3200ms 清除由父组件保留或封装。

**最小方案**：四页复制与品牌页相同的 JSX 结构，共用 CSS class；apply 阶段二选一，以 tasks 为准。

无论哪种，列表页 MUST NOT 在 `page-hero` 前使用 `<p className="admin-notice">` 承载自动消失反馈。

### D3：保留 `.admin-notice` 的合法用途

以下 MAY 继续使用 `.admin-notice` 或 inline 错误：

- 表单弹窗内静态/字段错误（如 `BrandFormModal`、`TileSkuFormModal` body 内错误）
- `AdminLayout.tsx` 侧栏「功能建设中」占位（非本 change scope）

### D4：行为参数

- 自动消失：**3200ms**（与现网四页一致）
- 位置：`position: fixed; top: 24px; right: 24px; z-index: 60`（与品牌页现网一致）
- a11y：`aria-live="polite"`，`role="status"`；region 可用 `aria-atomic="true"`

### D5：品牌页回归

`BrandManagementPage.test.tsx` 现有断言 MUST 保持通过：

- 启用后存在 `.admin-toast-region`
- 不存在列表顶文档流 `.admin-notice`

品牌 Logo 展示、上传进度（BUG-0003/0004/0007）MUST NOT 在本 change 中回归。

### D6：API / Orval

纯前端 CSS/DOM 变更；MUST NOT 变更 API、SQLite、Orval。

## Test Strategy

| 层级 | 验证 |
|---|---|
| Vitest | 品牌：保留启用 toast 断言；用户/类目/SKU：mock 成功操作后 `.admin-toast-region` 存在、无文档流 `.admin-notice` |
| 手工 | 四页各执行一次状态变更或 CRUD；Tips 出现/消失时 hero/表格纵向位置不变 |
| 构建 | `cd src/web && npm run build` |

## Risks

| 风险 | 缓解 |
|---|---|
| fixed toast 遮挡右上角内容 | 与品牌页现网一致；z-index 60，pointer-events: none |
| 重复 import 导致样式丢失 | 确保 admin-home.css 在 AdminLayout 或各页 import 链中 |
| 品牌页回归 | 保留 BrandManagementPage.test.tsx；手工验证 Logo |

## Open Questions

| 问题 | 决策 |
|---|---|
| 是否必须抽 AdminToast 组件 | apply 时优先组件化以减少四页重复；若时间紧可仅共享 CSS + 复制 JSX |
| 是否更新 incidents 知识库 | 可选；本缺陷为 UI 模式问题，非生产事故 |
