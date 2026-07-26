## Why

REQ-0005 要求 TILESFST 管理后台提供完整的用户生命周期管理能力（创建、编辑、冻结、软删除、重置密码），且仅**后台管理员**（`role=admin`）可见并操作。当前仅有认证 API（login/me/logout），无用户 CRUD、`users` 表缺少头像与软删除状态，Sidebar「用户管理」无路由。本迭代（sprint-002）在 `add-admin-home` Admin Shell 基座就绪后 MUST 补齐用户管理能力，否则无法运营账号与权限。

## What Changes

- 扩展 `users` 表：`avatar_object_key`、`status` 增加 `deleted`；`display_name`（昵称）允许为空。
- 新增 Admin Users REST API：`GET/POST /api/v1/admin/users`、`GET/PATCH /api/v1/admin/users/{id}`、重置密码、状态变更；仅 `admin` 可调用。
- 用户名校验：4–32 位、格式规则与保留字；创建后不可修改；创建/重置返回一次性明文密码。
- 业务规则：冻结（`disabled`）禁止登录；软删除仅允许从未登录用户；已删除用户禁止登录。
- 前端 `/admin/users`：列表、筛选、分页、统计指标卡；添加/编辑弹窗；重置密码/冻结/删除交互。
- CSS Port 自 `user-management-list.html` / `user-management-modal.html`；复用 `AdminLayout` + `admin-home.css` Shell。
- Sidebar：`admin` 可见「用户管理」并导航至 `/admin/users`；`employee` 隐藏菜单且访问路由展示无权限。
- 头像上传走后端授权（扩展现有 `/api/v1/admin/uploads` 或等价接口），MinIO 存储。
- OpenAPI 更新 + Orval 重新生成；补充后端集成测试与前端组件测试。
- PNG 视觉验收 gate（list + modal，1280×1024）。

## Capabilities

### New Capabilities

- `user-management`：管理端用户管理 API、数据模型扩展、列表/弹窗页面、权限边界、PNG 验收 gate。

### Modified Capabilities

- `auth`：用户数据模型（`deleted` 状态、头像、可空昵称）；登录拒绝已删除用户；新增「管理端用户管理 API 访问控制」requirement。
- `web-client`：角色权限前端拦截（`/admin/users` 仅 admin；employee 隐藏 SYSTEM 用户管理菜单）。

## Impact

| 影响面 | 说明 |
|---|---|
| 后端 | 新 `admin/users` 路由、service、repository；schema 迁移；密码生成 |
| 前端 Web 管理端 | `UserManagementPage`、port CSS、Orval 客户端、路由、Sidebar 条件渲染 |
| 数据库 | `users` 表 ALTER；更新 `schema.sql` 与 `docs/04-database-design.md` |
| API / Orval | **MUST** 重新生成 |
| MinIO | 头像 object_key；单桶前缀策略 |
| Design System | `/design-system` 可选用户管理预览区块 |
| 测试 | pytest 集成测试 + vitest 组件测试 |
| Docker | backend + web 镜像重建 |
| 迭代 | sprint-002；依赖 `add-admin-home` Admin Shell |
