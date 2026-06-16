## Why

REQ-0004 要求 TILESFST 管理端在登录成功后提供专业工作台首页。当前 `/admin/dashboard` 仅为占位文案，且 `AdminLayout` 仍采用顶栏 + 外露退出按钮布局，与 V5 原型（固定 Sidebar、底部用户菜单、三模块工作台）严重不符。登录页已通过 CSS Port 建立暗色旗舰风基线，管理端首页 MUST 在同一视觉语言下补齐，否则运营人员无法形成连贯的管理端体验。

## What Changes

- 重构 `AdminLayout`：264px 固定 Sidebar（100vh）+ 右侧独立滚动内容区，交互参考 ChatGPT.com 固定侧栏模式。
- 新增管理端导航 Shell：品牌 **TILESFST**、OPERATIONS / SYSTEM 分组、底部用户菜单与下拉框（个人资料、密码修改、退出登录）。
- 实现 `DashboardPage` 三模块：数据概览（4 指标卡）、快捷操作（4 宫格，仅新建类入口）、最近更新（表格）；本期使用 mock 数据。
- 移除顶栏外露「退出登录」按钮；退出收纳至用户菜单下拉框（**BREAKING** 相对当前 AdminLayout UI，auth 行为不变）。
- 新增 admin-home 专用 CSS Port（自 `admin-home.html`），颜色引用 `globals.css` `--color-*` token。
- Sidebar 非首页链接、快捷操作、个人资料/密码修改本期为占位，不实现子模块业务页。
- 不新增 Dashboard 统计或审计 API；复用 `GET /api/v1/auth/me` 与 `POST /api/v1/auth/logout`。

## Capabilities

### New Capabilities

- `admin-dashboard`：管理端工作台 Shell（Sidebar 布局、用户菜单、Dashboard 三模块、mock 数据、PNG 视觉验收 gate）。

### Modified Capabilities

- `web-client`：退出登录入口从管理端顶栏迁移至 Sidebar 用户菜单下拉框；新增管理端首页路由内容要求（与 `admin-dashboard` 协同，delta 仅修改既有「退出登录」requirement）。

## Impact

| 影响面 | 说明 |
|---|---|
| 前端 Web 管理端 | `AdminLayout.tsx`、`DashboardPage.tsx`；新增 `features/admin/` 或 `shared/` 管理 Shell 组件与 `admin-home.css` |
| 后端 | 无变更 |
| 数据库 | 无变更 |
| API / Orval | 无新接口；不触发 Orval |
| Design System | 新增管理端 Shell 复合组件；`/design-system` 可选预览 |
| 测试 | 前端布局、用户菜单、logout  smoke 测试 |
| Docker | 仅 Web 镜像重建 |
| 需求追踪 | `issues/requirements/REQ-0004-admin-home/` |
