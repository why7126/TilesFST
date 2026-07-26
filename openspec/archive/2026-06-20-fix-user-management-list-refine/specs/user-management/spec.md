## MODIFIED Requirements

### Requirement: 管理端用户列表与筛选 API

系统 MUST 提供 `GET /api/v1/admin/users`，仅 `role=admin` 的用户可调用。接口 MUST 支持分页（默认 `page_size=10`，可选 10/20/50）、关键词模糊搜索（**仅** `username`、`display_name`）、角色筛选、状态筛选（`active`/`disabled`/`deleted`）与登录情况筛选（从未登录、最近 7 天登录、超过 30 天未登录）。`keyword` MUST NOT 对 `email`、`phone` 做模糊匹配。响应 MUST 包含用户列表与 summary（用户总数、当前筛选数、正常用户数、已冻结用户数）。

#### Scenario: 管理员查询用户列表

- **WHEN** `admin` 携带有效 token 请求 `GET /api/v1/admin/users`
- **THEN** 系统返回 HTTP 200，`data` 包含 `items`、`pagination` 与 `summary`
- **AND** 每条用户记录 MUST 包含 id、username、display_name、role、status、avatar_object_key（或 avatar_url）、email、phone、last_login_at、created_at

#### Scenario: 非管理员被拒绝

- **WHEN** `employee` 或 `store_owner` 请求 `GET /api/v1/admin/users`
- **THEN** 系统 MUST 返回 HTTP 403

#### Scenario: 分页默认值

- **WHEN** 请求未指定 `page_size`
- **THEN** 系统 MUST 默认每页 10 条

#### Scenario: keyword 仅匹配用户名与昵称

- **WHEN** `admin` 请求 `GET /api/v1/admin/users?keyword=` 且 keyword 仅存在于某用户的 `email` 或 `phone` 字段
- **THEN** 该用户 MUST NOT 出现在 `items` 中
- **WHEN** keyword 匹配某用户的 `username` 或 `display_name`（模糊）
- **THEN** 该用户 MUST 出现在 `items` 中

### Requirement: 管理端用户管理页面

Web 客户端 MUST 提供 `/admin/users` 页面，视觉 MUST 高保真对齐 **`REQ-0005-user-management-list-refine`** 目录下 v2 `user-management-list.html` / `user-management-list.png` 的 CSS Port 策略。页面 MUST 继承 `AdminLayout`（264px Sidebar、右侧独立滚动、主内容 max-width 1080px）。当前路由为用户管理时 SYSTEM「用户管理」导航 MUST 为 active。

#### Scenario: 管理员访问用户管理页

- **WHEN** `role=admin` 用户访问 `/admin/users`
- **THEN** MUST 展示页面标题「用户管理」、筛选区、4 指标卡、用户表格（**无** `section-head` 标题行与 **无** `table-toolbar`）与分页
- **AND** 样式 MUST 主要来自 port CSS（`user-management.css`）

#### Scenario: 筛选与搜索交互

- **WHEN** 用户在关键词输入框按回车、失焦后防抖（约 300ms）或变更角色/状态/登录情况下拉
- **THEN** 系统 MUST 带 query 重新请求列表并重置到第 1 页
- **AND** 筛选区 MUST NOT 展示「搜索」按钮
- **WHEN** 用户点击「重置」
- **THEN** MUST 清空关键词及全部筛选项并重新加载默认列表（page=1）
- **AND** 关键词 placeholder MUST 为「搜索用户名/昵称」（或与 v2 HTML 完全一致），MUST NOT 提及邮箱或手机号

#### Scenario: 列表字段与分页

- **WHEN** 用户查看表格
- **THEN** MUST 展示用户列（头像 + **两行**：第一行 `username`、第二行 `display_name` 或「未设置昵称」）、角色、状态、最后登录、创建时间、操作列
- **AND** 用户列第二行 MUST NOT 展示邮箱
- **AND** 分页左侧 MUST 展示「共 {total} 个用户」（`total` 与当前筛选 `summary.total` 或 `pagination.total` 一致）
- **AND** 分页右侧 MUST 展示页码控件与「每页显示」条数选择（10/20/50）
- **AND** MUST NOT 展示「1-10 / N」「当前显示」「仅后台管理员可编辑用户」等 v1 文案

### Requirement: 管理端用户管理 PNG 视觉验收 Gate

用户管理**列表页**视觉 MUST 通过 v2 PNG golden reference 验收 gate（`REQ-0005-user-management-list-refine/prototype/web/user-management-list.png`）。弹窗 gate 仍以 `REQ-0005-user-management` modal PNG 为准，本 requirement 不修改弹窗 checklist。

#### Scenario: 列表 PNG 并排验收

- **WHEN** 团队在 1280px 视口并排对比 `/admin/users` 与 v2 `user-management-list.png`
- **THEN** diff checklist（Shell、筛选 **5** 列且无搜索按钮、placeholder「搜索用户名/昵称」、4 指标卡、**无** section-head、**无** table-toolbar、用户列两行、分页左「共 x 个用户」右页码与每页条数、添加按钮品牌金、激活「用户管理」菜单等）MUST 全部 pass
- **AND** 结果 MUST 记录在 change `trace.md`

#### Scenario: 弹窗 PNG 并排验收

- **WHEN** 团队打开添加用户弹窗并对比 `user-management-modal.png`
- **THEN** checklist（520px 宽、单列字段顺序、遮罩、主按钮品牌金等）MUST pass（**回归**，本 change 不修改弹窗实现）
