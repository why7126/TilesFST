## 1. 数据库与后端基础

- [x] 1.1 Migration：`users.remark` TEXT NULL；创建 `profile_activity_logs` 表与索引
- [x] 1.2 更新 `schema.sql`、`app/models/user.py`（remark + ProfileActivityLog ORM）
- [x] 1.3 实现 `ProfileActivityRepository`（insert、list_by_user limit 20）
- [x] 1.4 实现 `ProfileService`（get_me、patch_me、校验、audit 写入）

## 2. Profile API

- [x] 2.1 新增 Pydantic schemas（ProfileMe、ProfilePatch、ActivityItem）
- [x] 2.2 实现 `GET/PATCH /api/v1/profile/me`、`GET .../activities`
- [x] 2.3 注册 router（`require_admin_access`）；更新 OpenAPI
- [x] 2.4 扩展 `AuthService.login`：登录成功写入 `login` audit
- [x] 2.5 放宽头像 upload：`POST /api/v1/uploads` avatars → `require_admin_access`

## 3. 后端测试

- [x] 3.1 pytest：GET/PATCH profile、validation、employee 200、store_owner 403
- [x] 3.2 pytest：activities 排序/limit、audit 写入（login/profile/avatar）
- [x] 3.3 运行 `cd src/backend && uv run pytest tests/ -k profile`

## 4. 前端 API 与路由

- [x] 4.1 运行 `./scripts/generate-openapi-client.sh`（Orval）
- [x] 4.2 注册 `/admin/profile` 路由（ProtectedRoute，非 requireAdmin）
- [x] 4.3 实现 `features/admin/api/profile-api.ts`

## 5. CSS Port 与页面

- [x] 5.1 创建 `features/admin/styles/profile-page.css`（自 profile-page.html port）
- [x] 5.2 实现 `ProfilePage`：page-head、profile-card、side-stack、timeline
- [x] 5.3 表单校验、重置、inline save-tip；头像 upload 复用 UserFormModal 状态机
- [x] 5.4 更新 `AdminUserMenu`：个人资料 navigate + active；密码修改 modal hook（REQ-0015 stub 或联调）
- [x] 5.5 更新 `getUserEmail` / 侧栏展示真实 email

## 6. 前端测试

- [x] 6.1 vitest：ProfilePage 校验、重置、保存 mock、菜单导航
- [x] 6.2 运行 `cd src/web && pnpm vitest run src/pages/admin/ProfilePage`

## 7. 构建与部署

- [x] 7.1 `cd src/web && pnpm build`
- [x] 7.2 `./scripts/docker-up.sh` 验证 `/admin/profile`（admin + employee 登录）

## 8. 视觉验收（PNG Golden Reference Gate）

- [x] 8.1 1440×1024 并排 `/admin/profile` 与 `profile-page.png`
- [x] 8.2 填写 `openspec/changes/add-admin-profile-page/trace.md` checklist

## 9. 文档与追溯

- [x] 9.1 更新 `docs/04-database-design.md`、`docs/03-api-index.md`
- [x] 9.2 更新 `issues/requirements/archive/REQ-0014-profile-page/trace.md`（openspec_changes、status: in_sprint 若纳入 Sprint）

## 10. 归档准备

- [x] 10.1 本文件全部 `[x]` 后执行 `/opsx-archive add-admin-profile-page`
