## ADDED Requirements

### Requirement: 管理端修改密码弹窗组件

Web 客户端 MUST 在 `AdminLayout` 层挂载 `ChangePasswordModal`，并通过 context 或等价机制暴露 `openChangePasswordModal` / `closeChangePasswordModal`。`AdminUserMenu` MUST 通过 `onChangePassword` 回调打开弹窗。弹窗视觉 MUST CSS Port 自 `password-change-modal.html`，宽度 520px，使用 semantic token。

#### Scenario: Layout 托管 modal

- **WHEN** 任意 `/admin/*` 页渲染
- **THEN** `ChangePasswordModal` MUST 可在全局打开
- **AND** MUST NOT 依赖独立路由

#### Scenario: 前端校验与 Orval

- **WHEN** 用户提交改密
- **THEN** MUST 使用 Orval 生成的客户端调用 `POST /api/v1/admin/profile/password`
- **AND** 前端校验失败 MUST NOT 发起请求

#### Scenario: 密码不入持久化存储

- **WHEN** 改密流程完成或失败
- **THEN** MUST NOT 将明文密码写入 localStorage 或 URL
