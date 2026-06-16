## Why

REQ-0003-login-remember-autofill 要求管理端登录页（`/admin/login`）补齐两项体验能力：

1. 勾选「记住登录状态」且登录成功后，下次进入页面自动填充上次成功的用户名与密码。
2. 密码输入框支持显示/隐藏切换。

现网已实现 `remember_me` JWT 长/短有效期（`localStorage` / `sessionStorage`），但 **未** 保存表单凭证；密码框为固定 `type="password"`。`openspec/specs/web-client` 在 `fix-login-css-port` 归档时曾 **禁止** 密码显隐（对齐当时 HTML 原型）；本需求以 REQ-0003 产品决策 **恢复** 显隐，并 **扩展**「记住登录状态」语义。

## What Changes

- 新增 `login-credentials.ts`：`localStorage` 读写 `stonex_login_credentials`（username、password、remember）。
- `LoginForm`：mount 时自动填充；登录成功按勾选保存/清除凭证；密码显隐按钮（`.password-wrap` + `.password-toggle`）。
- `auth-store` 登出：清除凭证（与清除 token 并列）。
- `login-page.css`：密码框右侧图标样式；延续 CSS Port，无裸 Hex。
- 单元测试：`login-credentials.test.ts`、`LoginForm` 显隐与自动填充。
- **不** 变更后端 API、数据库、Orval、MinIO。

## Capabilities

### New Capabilities

（无新 capability 目录；行为归入 `web-client` delta。）

### Modified Capabilities

- `web-client`：MODIFIED「管理端登录页」「登录态保持」「退出登录」「可访问性」— 密码显隐、记住凭证自动填充、登出清凭证。

## Impact

| 影响面 | 说明 |
|---|---|
| 后端 | 无 |
| 前端 Web 管理端 | `LoginForm`、`auth-store`、`login-page.css`、新 `login-credentials.ts` |
| 数据库 | 无 |
| API / Orval | 无 |
| Design System | 无新组件；登录 CSS Port 局部扩展 |
| 测试 | vitest auth 模块 |
| Docker | 可选 `npm run build`；无 compose 变更 |
| 安全 | 密码明文仅存客户端；登出 MUST 清除 |

## 风险

- 共享设备明文密码残留：依赖 FR-003 登出清除与产品接受风险。
- 与 archived spec「禁止显隐」冲突：delta spec MODIFIED 消化。
