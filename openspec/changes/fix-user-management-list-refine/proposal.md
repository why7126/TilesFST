## Why

`add-user-management`（REQ-0005）已落地 `/admin/users` 列表页，但产品对筛选区、表格信息层级与用户列展示提出六项 UI/交互优化（REQ-0005-user-management-list-refine）。当前实现仍保留「搜索」按钮、6 列筛选网格、`section-head` / `table-toolbar`、用户列邮箱回退与旧分页文案，且后端 `keyword` 仍匹配 email/phone，与 v2 原型及实际搜索能力不一致。本 change 为 **fix-*** 专项，在不动弹窗、行操作与权限模型的前提下对齐列表页 v2 原型。

## What Changes

- **筛选区（O-01、O-02）**：删除「搜索」按钮；网格由 6 列减为 5 列（关键词、角色、状态、登录情况、重置）；placeholder 改为「搜索用户名/昵称」；关键词回车/防抖（~300ms）或筛选项变更自动查询；重置清空全部条件并 page=1。
- **表格区（O-03、O-04）**：删除「用户列表」标题行（`section-head`）与 `table-toolbar`（含「当前显示 x-y / N」「仅后台管理员可编辑用户」）。
- **用户列（O-05）**：用户名与昵称固定两行纵向展示（`.user-meta`）；空昵称显示「未设置昵称」；**MUST NOT** 以邮箱作为副标题。
- **分页区（O-06）**：左侧「共 {total} 个用户」；右侧页码按钮 +「每页显示」条数选择；移除「1-10 / N」「每页」（孤立词）等旧文案。
- **后端 keyword 范围收窄**：`GET /api/v1/admin/users?keyword=` 仅模糊匹配 `username`、`display_name`；移除 email/phone LIKE 条件。
- **原型与验收**：列表 HTML/PNG Golden Reference 切换至 `REQ-0005-user-management-list-refine/prototype/web/` v2；modal 原型不变。
- **测试**：补充/更新 pytest keyword 范围用例；更新 vitest 列表交互与布局断言。

## Capabilities

### New Capabilities

（无）

### Modified Capabilities

- `user-management`：MODIFIED「管理端用户列表与筛选 API」（keyword 范围）；「管理端用户管理页面」（筛选交互、列表布局、用户列、分页）；「管理端用户管理 PNG 视觉验收 Gate」（v2 checklist 与 PNG 路径）。

## Impact

| 影响面 | 说明 |
|---|---|
| 后端 | `user_repository.py` keyword WHERE 子句；`test_admin_users.py` |
| 前端 Web 管理端 | `UserManagementPage.tsx`、`user-management.css`；防抖查询逻辑 |
| API / Orval | 无新端点；OpenAPI 描述可同步 keyword 范围说明（可选） |
| 数据库 | 无 schema 变更 |
| Design System | 无新 Token；延续 CSS Port |
| 测试 | pytest keyword 集成测试；vitest 列表页组件/交互测试 |
| Docker | web 镜像重建（样式与页面逻辑） |
| 迭代 | sprint-002；依赖 `add-user-management` 基线 |
| 归档顺序 | 建议 `add-user-management` 先 archive，再 archive 本 change；或同批 archive 时 delta MODIFIED 标题须与 `user-management` capability 一致 |
