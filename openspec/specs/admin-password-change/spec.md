# admin-password-change Specification

## Purpose
TBD - created by archiving change add-admin-password-change. Update Purpose after archive.
## Requirements
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

Web 客户端 MUST 提供 `ChangePasswordModal`（520px 居中），含原密码、新密码、确认新密码三字段；每字段 MUST 支持显隐切换，且显隐切换按钮 MUST 始终相对该字段输入框垂直居中（不受字段下方错误提示影响）；MUST 展示新密码规则提示列表。弹窗 MUST 由 `AdminLayout` 挂载；侧栏 `AdminUserMenu`「密码修改」MUST 打开该弹窗，MUST NOT 使用 placeholder toast。校验失败与 API 错误 MUST 按字段挂载：与新密码相关的错误 MUST 显示在「新密码」字段下方；与原密码验证失败相关的错误 MUST 显示在「原密码」字段下方；确认新密码不一致 MUST 显示在「确认新密码」字段下方。各字段错误区域 MUST 含 `role="alert"`，且对应输入框 MUST 应用错误样式类。

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

#### Scenario: openChangePasswordModal 复用

- **WHEN** `REQ-0014` profile 页或未来入口调用 `openChangePasswordModal`
- **THEN** MUST 打开同一弹窗实例
- **AND** MUST NOT 重复实现改密表单

#### Scenario: 新密码客户端校验错误字段位置

- **WHEN** 用户提交时新密码不符合 8–32 位、缺少字母或数字、或与新密码规则不符
- **THEN** MUST 在「新密码」字段下方展示对应错误文案（如「新密码不符合安全策略」）
- **AND** MUST NOT 在「原密码」字段下方展示该文案

#### Scenario: 新密码与原密码相同错误字段位置

- **WHEN** 用户提交时新密码与原密码相同
- **THEN** MUST 在「新密码」字段下方展示「新密码不能与原密码相同」（或等价文案）
- **AND** MUST NOT 在「原密码」字段下方展示该文案

#### Scenario: 服务端弱密码错误字段位置

- **WHEN** API 返回 HTTP 400 且错误码 `40022`（新密码过于常见）
- **THEN** MUST 在「新密码」字段下方展示「新密码过于常见，请更换」（或 API message）
- **AND** MUST NOT 在「原密码」字段下方展示该文案

#### Scenario: 原密码错误字段位置

- **WHEN** API 返回 HTTP 400 且错误码 `40020`（原密码不正确）
- **THEN** MUST 在「原密码」字段下方展示「原密码不正确」（或 API message）
- **AND** MUST NOT 在「新密码」字段下方展示该错误

#### Scenario: 确认新密码不一致字段位置

- **WHEN** 用户提交时「确认新密码」与「新密码」不一致
- **THEN** MUST 在「确认新密码」字段下方展示「两次输入的新密码不一致」
- **AND** MUST NOT 调用改密 API

#### Scenario: 显隐切换按钮不受错误提示影响

- **WHEN** 任一密码字段下方展示错误提示（`role="alert"`）
- **THEN** 该字段「显示/隐藏」切换按钮 MUST 仍相对该字段输入框垂直居中
- **AND** MUST 与同弹窗无错误字段的切换按钮垂直对齐一致
- **AND** 点击切换 MUST 仍可正常切换 input 的 password/text 类型

### Requirement: 管理端修改密码 PNG 视觉验收 Gate

改密弹窗视觉 MUST 通过 PNG golden reference 验收 gate。

#### Scenario: Modal PNG 并排验收

- **WHEN** 团队在 1440×1024 并排对比弹窗与 `password-change-modal.png`
- **THEN** checklist（520px、遮罩、三字段、规则区、footer 按钮、Sidebar 背景）MUST pass
- **AND** 结果 MUST 记录在 change `trace.md`

