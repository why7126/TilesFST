## ADDED Requirements

### Requirement: 管理端修改密码 API

系统 MUST 提供 `POST /api/v1/admin/profile/password`，允许当前已认证 `admin` 或 `employee` 修改**本人**密码。请求 MUST 包含 `old_password` 与 `new_password`。成功响应 MUST 为统一 `ApiResponse`，`data.success` 为 true。

#### Scenario: 改密成功

- **WHEN** 用户提交正确的原密码与符合策略的新密码
- **THEN** 系统返回 HTTP 200
- **AND** MUST 更新 `password_hash`（bcrypt）
- **AND** MUST 递增 `users.token_version`
- **AND** MUST 记录成功 attempt

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

### Requirement: 用户 token_version 与 JWT tv claim

系统 MUST 在 `users` 表维护 `token_version`（INTEGER NOT NULL DEFAULT 0）。登录签发 JWT MUST 含 claim `tv` 等于签发时用户的 `token_version`。受保护 API 校验 JWT 时 MUST 验证 `tv` 与数据库 `token_version` 一致，否则 MUST 返回 HTTP 401。

#### Scenario: 登录 JWT 含 tv

- **WHEN** 用户登录成功
- **THEN** access_token payload MUST 含 `tv` 等于当前 `token_version`

#### Scenario: 改密后旧 token 失效

- **WHEN** 用户改密成功且 `token_version` 已递增
- **THEN** 改密前签发的 JWT 访问受保护 API MUST 返回 HTTP 401

#### Scenario: 未改密用户 token 仍有效

- **WHEN** 用户未改密且 token 未过期
- **THEN** `tv` 匹配时 MUST 允许访问

### Requirement: 管理端修改密码弹窗

Web 客户端 MUST 提供 `ChangePasswordModal`（520px 居中），含原密码、新密码、确认新密码三字段；每字段 MUST 支持显隐切换；MUST 展示新密码规则提示列表。弹窗 MUST 由 `AdminLayout` 挂载；侧栏 `AdminUserMenu`「密码修改」MUST 打开该弹窗，MUST NOT 使用 placeholder toast。

#### Scenario: 菜单打开弹窗

- **WHEN** 用户点击侧栏用户菜单「密码修改」
- **THEN** MUST 打开居中弹窗，无路由跳转
- **AND** MUST 默认聚焦原密码
- **AND** 页面主体 MUST NOT 滚动

#### Scenario: 关闭与脏确认

- **WHEN** 用户点击 ×、取消或 Esc，且表单有输入
- **THEN** MUST 二次确认「当前填写内容尚未保存，确认关闭吗？」

#### Scenario: 提交成功

- **WHEN** API 返回成功
- **THEN** MUST Toast「密码修改成功，请使用新密码重新登录。」
- **AND** MUST 调用 logout 并跳转 `/admin/login`

#### Scenario: openChangePasswordModal 复用

- **WHEN** `REQ-0014` profile 页或未来入口调用 `openChangePasswordModal`
- **THEN** MUST 打开同一弹窗实例
- **AND** MUST NOT 重复实现改密表单

### Requirement: 管理端修改密码 PNG 视觉验收 Gate

改密弹窗视觉 MUST 通过 PNG golden reference 验收 gate。

#### Scenario: Modal PNG 并排验收

- **WHEN** 团队在 1440×1024 并排对比弹窗与 `password-change-modal.png`
- **THEN** checklist（520px、遮罩、三字段、规则区、footer 按钮、Sidebar 背景）MUST pass
- **AND** 结果 MUST 记录在 change `trace.md`
