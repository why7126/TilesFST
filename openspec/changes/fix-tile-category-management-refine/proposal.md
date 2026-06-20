## Why

`add-tile-category-management`（REQ-0005）与 `fix-tile-category-enable-action`（BUG-0001）已落地 `/admin/tile-categories`，但产品对 **启停误操作防护、检索/列表区标题层级、分页与管理端一致性** 提出四项 UI/交互优化（REQ-0007-tile-category-management-refine）。当前实现：启停点击即调 API；检索/列表区保留 v1 HTML 的 `section-head`；分页仍为「当前显示 x-y / N 条」+ `cat-pager`，与用户管理 v2 不一致。本 change 为 **fix-*** 专项，在不动 API、弹窗字段、删除规则与 BUG-0001 启停可见性前提下对齐 v2 context。

## What Changes

- **启停二次确认（O-01）**：点击「启用」「停用」弹出确认框（复用删除 modal 结构）；确认后调用 enable/disable；取消不请求。
- **检索区（O-02）**：删除「类目检索」`section-head` 及副标题；`filter-card` 直接展示。
- **列表区（O-03）**：删除「类目列表」外层 `section-head` 及副标题；**保留** `cat-table-toolbar`（树上下文 + 共 N 条记录 + 调整排序）。
- **分页区（O-04）**：对齐 `UserManagementPage` v2 — 左「共 {total} 个类目」；右页码 +「每页显示」；移除「当前显示 x-y / N 条」；选项「10 条」非「10 条/页」。
- **样式**：`tile-category-management.css` 增量 + 复用 `.pagination` 结构（或等价）。
- **测试**：vitest 启停确认、分页文案、section 标题缺失；build 通过。

## Capabilities

### New Capabilities

（无）

### Modified Capabilities

- `web-client`：MODIFIED「管理端瓷砖类目管理页」（启停确认、去 section 标题、分页 v2）。

## Impact

| 影响面 | 说明 |
|---|---|
| 后端 | 无变更 |
| 前端 Web 管理端 | `TileCategoryManagementPage.tsx`、`tile-category-management.css` |
| API / Orval | 无 |
| 数据库 | 无 |
| Design System | 无新 Token；延续 CSS Port |
| 测试 | vitest 页面测试更新/新增 |
| Docker | web 镜像重建 |
| 依赖 | `add-tile-category-management` 已 archive；`fix-tile-category-enable-action` 已 archive |
