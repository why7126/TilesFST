# 管理端修改密码规范

## Purpose
定义管理端本人修改密码 API、token_version 与 JWT tv claim、修改密码弹窗交互和 PNG 视觉验收要求，确保改密后旧 token 失效且受保护账号不可误改密。
## Requirements
### Requirement: 管理端修改密码 API

系统 MUST 提供 `POST /api/v1/admin/profile/password`，允许当前已认证 `admin` 或 `employee` 修改**本人**密码。请求 MUST 包含 `old_password` 与 `new_password`。成功响应 MUST 为统一 `ApiResponse`，`data.success` 为 true。当当前用户 username 等于 `settings.admin_username` / `ADMIN_USERNAME` 时，系统 MUST 按默认策略拒绝管理端本人改密，返回 HTTP 403 与已登记的受保护账号错误码，且 MUST NOT 校验通过后更新 `password_hash`，MUST NOT 递增 `users.token_version`。

当新密码不满足 effective 密码策略时，系统 MUST 返回可被前端识别的具体失败项，至少覆盖最小长度、最大长度、大写字母、小写字母、数字、特殊字符、弱密码和与原密码相同。错误响应 MUST 继续遵循统一 `{ code, message, data }` envelope；若 `data` 携带策略失败详情，MUST NOT 包含明文密码。

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

- **GIVEN** effective 密码策略要求最小长度、最大长度、大小写、数字或特殊字符
- **WHEN** 新密码未满足一项或多项 effective 策略
- **THEN** 系统 MUST 返回 HTTP 400 与策略错误码 `40021`（或登记等价码）
- **AND** 错误响应 MUST 包含可被前端识别的具体失败项
- **AND** 失败项 MUST 能区分 `min_length`、`max_length`、`missing_uppercase`、`missing_lowercase`、`missing_digit`、`missing_special`
- **AND** MUST NOT 更新 `password_hash`
- **AND** MUST NOT 递增 `users.token_version`

#### Scenario: 弱密码拒绝

- **WHEN** 新密码命中弱密码表
- **THEN** 系统 MUST 返回 HTTP 400，错误码 `40022`
- **AND** 错误响应 MUST 允许前端展示“密码过于常见，请更换”或等价文案

#### Scenario: 新密码与原密码相同

- **WHEN** 新密码与原密码相同
- **THEN** 系统 MUST 返回 HTTP 400，错误码 `40023`
- **AND** 错误响应 MUST 允许前端展示“新密码不能与原密码相同”或等价文案

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

Web 客户端 MUST 提供 `ChangePasswordModal`（520px 居中），含原密码、新密码、确认新密码三字段；每字段 MUST 支持显隐切换，且显隐切换按钮 MUST 始终相对该字段输入框垂直居中（不受字段下方错误提示影响）。弹窗 MUST 由 `AdminLayout` 挂载；侧栏 `AdminUserMenu`「密码修改」MUST 打开该弹窗，MUST NOT 使用 placeholder toast。

弹窗 MUST 展示与当前 effective 密码策略一致的规则提示，至少覆盖长度、大小写、数字、特殊字符和不能与原密码相同。校验失败与 API 错误 MUST 按字段或规则区清晰展示：与新密码相关的错误 MUST 显示在「新密码」字段下方或新密码规则区；与原密码验证失败相关的错误 MUST 显示在「原密码」字段下方；确认新密码不一致 MUST 显示在「确认新密码」字段下方。各字段错误区域 MUST 含 `role="alert"` 或等价可访问错误语义，且对应输入框 MUST 应用错误样式类。当 API 返回受保护账号不可改密错误时，弹窗 MUST 展示接口 message，MUST NOT 显示通用不明错误。

#### Scenario: 新密码规则提示与 effective 策略一致

- **GIVEN** 当前 effective 密码策略要求最小长度 12、大小写、数字和特殊字符
- **WHEN** 用户打开修改密码弹窗
- **THEN** 弹窗 MUST 展示与该策略一致的规则提示
- **AND** MUST NOT 仅展示旧规则“8-32 位、至少包含字母和数字”

#### Scenario: 策略失败展示具体原因

- **WHEN** 用户提交缺少特殊字符或缺少大写字母的新密码
- **THEN** 弹窗 MUST 展示具体失败原因
- **AND** MUST NOT 仅展示“新密码不符合安全策略”
- **AND** 错误 MUST 归属到新密码字段或新密码规则区

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

### Requirement: 管理端修改密码 PNG 视觉验收 Gate

改密弹窗视觉 MUST 通过 PNG golden reference 验收 gate。

#### Scenario: Modal PNG 并排验收

- **WHEN** 团队在 1440×1024 并排对比弹窗与 `password-change-modal.png`
- **THEN** checklist（520px、遮罩、三字段、规则区、footer 按钮、Sidebar 背景）MUST pass
- **AND** 结果 MUST 记录在 change `trace.md`
