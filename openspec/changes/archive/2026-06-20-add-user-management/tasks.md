## 1. 数据库与后端基础

- [x] 1.1 更新 `schema.sql`：`avatar_object_key`、`status` 含 `deleted`、`display_name` 可空
- [x] 1.2 更新 `app/models/user.py` ORM 与 CheckConstraint
- [x] 1.3 实现用户名校验（4–32 位、保留字、连续特殊符号）与随机密码生成工具
- [x] 1.4 扩展 `UserRepository`：分页列表、筛选、summary、CRUD、status 变更
- [x] 1.5 实现 `UserAdminService` 业务规则（删除仅限从未登录等）

## 2. Admin Users API

- [x] 2.1 新增 `require_system_admin` 依赖（仅 `admin`）
- [x] 2.2 实现 `GET/POST /api/v1/admin/users` 与 Pydantic schemas
- [x] 2.3 实现 `GET/PATCH /api/v1/admin/users/{id}`
- [x] 2.4 实现 `POST .../reset-password` 与 `PATCH .../status`
- [x] 2.5 注册路由、错误码；更新 OpenAPI
- [x] 2.6 扩展 auth login：拒绝 `deleted` 状态用户（非 `active` 统一拒绝）
- [x] 2.7 扩展头像上传（`/api/v1/admin/uploads` avatars 前缀 + admin 鉴权；MinIO 桩）

## 3. 后端测试

- [x] 3.1 pytest：admin CRUD、employee 403、用户名冲突、删除规则、冻结后登录失败
- [x] 3.2 运行 `cd src/backend && uv run pytest tests/ -k user`

## 4. 前端 API 与路由

- [x] 4.1 运行 `./scripts/generate-openapi-client.sh`（Orval）
- [x] 4.2 `admin-nav.ts` 添加 `path: '/admin/users'`；Sidebar 按 role 过滤 SYSTEM 项
- [x] 4.3 注册 `/admin/users` 路由与 `ProtectedRoute requireAdmin`
- [x] 4.4 实现 `features/admin/api/users-api.ts`

## 5. CSS Port 与页面

- [x] 5.1 创建 `features/admin/styles/user-management.css`
- [x] 5.2 实现 `UserManagementPage`：hero、筛选、指标卡、表格、分页
- [x] 5.3 实现 `UserFormModal`（字段顺序：用户名、头像、昵称、角色）
- [x] 5.4 实现重置密码确认 + 一次性密码弹窗（复制按钮）
- [x] 5.5 实现行操作：冻结/解冻、删除禁用逻辑、Toast 反馈
- [x] 5.6 角色/状态中文 badge 映射

## 6. Design System 预览（可选）

- [ ] 6.1 `/design-system` 增加用户管理列表/弹窗预览片段（可选，未纳入本期）

## 7. 前端测试

- [x] 7.1 vitest：employee 无菜单、admin 可见、弹窗字段顺序
- [x] 7.2 运行 `cd src/web && npx vitest run src/features/admin src/pages/admin`

## 8. 构建与部署

- [x] 8.1 `cd src/web && npm run build`
- [x] 8.2 `./scripts/docker-up.sh` 验证 `/admin/users`（admin 登录）

## 9. 视觉验收（PNG Golden Reference Gate）

- [x] 9.1 1280×1024 并排 `/admin/users` 与 `user-management-list.png`
- [x] 9.2 打开添加用户弹窗并排 `user-management-modal.png`
- [x] 9.3 填写 `openspec/changes/add-user-management/trace.md` checklist（实现完成，待人工 PNG sign-off）

## 10. 文档与追溯

- [x] 10.1 更新 `docs/04-database-design.md`、`docs/03-api-index.md`
- [x] 10.2 更新 `issues/requirements/REQ-0005-user-management/trace.md`（status: applied）
- [x] 10.3 更新 `iterations/sprint-002/acceptance-report.md`（实现完成，待验收勾选）

## 11. 归档准备

- [x] 11.1 本文件全部 `[x]` 后执行 `/opsx-archive add-user-management`
