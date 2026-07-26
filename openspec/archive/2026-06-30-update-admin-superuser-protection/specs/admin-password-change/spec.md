---
change_id: update-admin-superuser-protection
capability: admin-password-change
created_at: 2026-06-30 18:26:13
updated_at: 2026-06-30 18:26:13
---

## MODIFIED Requirements

### Requirement: 管理端修改密码 API

系统 MUST 提供 `POST /api/v1/admin/profile/password`，允许当前已认证 `admin` 或 `employee` 修改**本人**密码。请求 MUST 包含 `old_password` 与 `new_password`。成功响应 MUST 为统一 `ApiResponse`，`data.success` 为 true。当当前用户 username 等于 `settings.admin_username` / `ADMIN_USERNAME` 时，系统 MUST 按默认策略拒绝管理端本人改密，返回 HTTP 403 与已登记的受保护账号错误码，且 MUST NOT 校验通过后更新 `password_hash`，MUST NOT 递增 `users.token_version`。

#### Scenario: 改密成功

- **WHEN** 用户提交正确的原密码与符合策略的新密码
- **THEN** 系统返回 HTTP 200
- **AND** MUST 更新 `password_hash`（bcrypt）
- **AND** MUST 递增 `users.token_version`
- **AND** MUST 记录成功 attempt

#### Scenario: 受保护账号本人改密被拒绝

- **GIVEN** 当前登录用户 username 等于 `ADMIN_USERNAME`
- **WHEN** 该用户请求 `POST /api/v1/admin/profile/password`
- **THEN** 系统 MUST 返回 HTTP 403
- **AND** 错误响应 `code` MUST 为已登记的受保护账号错误码
- **AND** `password_hash` MUST 保持不变
- **AND** `token_version` MUST 不递增
- **AND** 前端可展示接口返回的 message

#### Scenario: 原密码错误

- **WHEN** `old_password` 与当前 hash 不匹配
- **THEN** 系统 MUST 返回 HTTP 400，错误码 `40020`（或登记等价码）
- **AND** MUST 记录失败 attempt

#### Scenario: 新密码策略不符

- **WHEN** 新密码长度不在 8–32、缺少字母或数字、或与原密码相同
- **THEN** 系统 MUST 返回 HTTP 400，错误码 `40021` 或 `40023`

#### Scenario: 弱密码拒绝

- **WHEN** 新密码命中弱密码表
- **THEN** 系统 MUST 返回 HTTP 400，错误码 `40022`

#### Scenario: 改密频率限制

- **WHEN** 15 分钟内原密码错误 ≥ 5 次，或 24 小时内成功改密 ≥ 3 次
- **THEN** 系统 MUST 返回 HTTP 429，错误码 `42901`

#### Scenario: 店主被拒绝

- **WHEN** `store_owner` 调用改密 API
- **THEN** 系统 MUST 返回 HTTP 403

#### Scenario: 未登录

- **WHEN** 无有效 Bearer token
- **THEN** 系统 MUST 返回 HTTP 401

### Requirement: 管理端修改密码弹窗

Web 客户端 MUST 提供 `ChangePasswordModal`（520px 居中），含原密码、新密码、确认新密码三字段；每字段 MUST 支持显隐切换，且显隐切换按钮 MUST 始终相对该字段输入框垂直居中（不受字段下方错误提示影响）；MUST 展示新密码规则提示列表。弹窗 MUST 由 `AdminLayout` 挂载；侧栏 `AdminUserMenu`「密码修改」MUST 打开该弹窗，MUST NOT 使用 placeholder toast。校验失败与 API 错误 MUST 按字段挂载：与新密码相关的错误 MUST 显示在「新密码」字段下方；与原密码验证失败相关的错误 MUST 显示在「原密码」字段下方；确认新密码不一致 MUST 显示在「确认新密码」字段下方。各字段错误区域 MUST 含 `role="alert"`，且对应输入框 MUST 应用错误样式类。当 API 返回受保护账号不可改密错误时，弹窗 MUST 展示接口 message，MUST NOT 显示通用不明错误。

#### Scenario: 受保护账号改密错误展示

- **GIVEN** 当前登录用户为受保护账号
- **WHEN** 用户提交修改密码表单且 API 返回受保护账号错误
- **THEN** 弹窗 MUST 展示接口返回 message
- **AND** MUST NOT 显示“未知错误”或技术堆栈
- **AND** MUST NOT 调用 logout

#### Scenario: 菜单打开弹窗

- **WHEN** 用户点击侧栏用户菜单「密码修改」
- **THEN** MUST 打开居中弹窗，无路由跳转
- **AND** MUST 默认聚焦原密码
- **AND** 页面主体 MUST NOT 滚动

#### Scenario: 关闭弹窗无二次确认

- **WHEN** 用户点击 ×、取消、Esc 或遮罩关闭弹窗
- **THEN** MUST 直接关闭弹窗
- **AND** MUST NOT 弹出浏览器原生二次确认对话框（无论表单是否有输入）
- **AND** 再次打开时 MUST 重置表单字段为空

#### Scenario: 提交成功

- **WHEN** API 返回成功
- **THEN** MUST Toast「密码修改成功，请使用新密码重新登录。」
- **AND** MUST 调用 logout 并跳转 `/admin/login`
