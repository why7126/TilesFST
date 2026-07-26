## 1. 数据库与后端基础

- [x] 1.1 Migration：`users.token_version`；`password_change_attempts` 表
- [x] 1.2 更新 ORM、`schema.sql`
- [x] 1.3 弱密码表 + `validate_password()` 扩展
- [x] 1.4 改密限流查询（15min fail / 24h success）

## 2. Auth JWT tv

- [x] 2.1 `create_access_token` 写入 `tv` claim
- [x] 2.2 `get_current_user` 校验 `tv == token_version`
- [x] 2.3 更新现有 auth pytest

## 3. Change Password API

- [x] 3.1 Pydantic `ChangePasswordRequest` / `ChangePasswordData`
- [x] 3.2 `POST /api/v1/admin/profile/password` + service
- [x] 3.3 错误码 40020–40023、42901；登记 error-codes.md
- [x] 3.4 OpenAPI + router 注册

## 4. 后端测试

- [x] 4.1 pytest：成功、原密码错、弱密码、限流、旧 JWT 401
- [x] 4.2 `uv run pytest tests/ -k password`

## 5. 前端

- [x] 5.1 Orval regenerate
- [x] 5.2 `password-change-modal.css` port
- [x] 5.3 `ChangePasswordModal` + context
- [x] 5.4 `AdminLayout` 挂载；`AdminUserMenu.onChangePassword`
- [x] 5.5 Toast + logout 成功流

## 6. 前端测试

- [x] 6.1 vitest：打开、校验、脏关闭、成功 logout
- [x] 6.2 `pnpm vitest run` 相关用例

## 7. 与 REQ-0014 联调

- [x] 7.1 导出 `openChangePasswordModal` 供 ProfilePage（0014 apply 时接入）
- [x] 7.2 协调 AdminUserMenu 与 `add-admin-profile-page` 不冲突

## 8. PNG 验收

- [ ] 8.1 1440×1024 并排 `password-change-modal.png`（需浏览器手动并排验收）
- [x] 8.2 填写 change `trace.md` checklist

## 9. 文档

- [x] 9.1 `docs/03-api-index.md`、`docs/04-database-design.md`
- [x] 9.2 REQ-0015 trace 更新

## 10. 归档

- [x] 10.1 `/opsx-archive add-admin-password-change`
