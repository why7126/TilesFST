## Why

REQ-0015 要求将 `REQ-0004-admin-home` 侧栏用户菜单「密码修改」从占位 toast 落地为完整 self-service 改密能力。当前登录用户无法自主修改密码，只能依赖管理员在用户管理页「重置密码」。本 change 交付 520px 居中弹窗、`POST /api/v1/admin/profile/password`、弱密码校验、改密限流与 `token_version` 全端 JWT 失效，并与 `REQ-0014-profile-page` 共享 `ChangePasswordModal`。

## What Changes

- `AdminUserMenu`「密码修改」→ `openChangePasswordModal()`（替换 `onPlaceholder`）
- 新增 `ChangePasswordModal`（520px）：原密码 / 新密码 / 确认新密码；显隐切换；脏关闭二次确认
- `AdminLayout` 托管 modal 状态；暴露 `openChangePasswordModal` 供 REQ-0014 profile 页复用
- 后端 `POST /api/v1/admin/profile/password`；`users.token_version` migration
- JWT 新增 `tv` claim；`get_current_user` 校验 token_version
- 弱密码表；15min 失败 / 24h 成功改密限流；attempt 记录表
- 改密成功 Toast + logout + 跳转登录页
- OpenAPI / Orval；pytest + vitest；PNG 并排验收

## Capabilities

### New Capabilities

- `admin-password-change`：改密弹窗 UI、改密 API、token_version、限流与弱密码、PNG 验收 gate

### Modified Capabilities

- `auth`：用户数据模型 `token_version`；登录 JWT `tv` claim；当前用户校验 token_version；改密后旧 JWT 401
- `admin-dashboard`：用户菜单「密码修改」打开弹窗（非 placeholder）
- `web-client`：`ChangePasswordModal`；`AdminLayout` password modal context

## Impact

| 影响面 | 说明 |
|---|---|
| 后端 | `admin/profile` 路由组（password）；migration；validation；rate limit |
| 前端 | ChangePasswordModal CSS Port；AdminLayout/AdminUserMenu |
| 数据库 | `users.token_version`；`password_change_attempts`（或等价表） |
| API / Orval | **MUST** 重生成 |
| 安全 | 全端 token 失效；密码不入日志 |
| 关联 | REQ-0014 共用 modal；与 `add-admin-profile-page` 同 Sprint 联调菜单 |
| 测试 | pytest + vitest + PNG gate |
