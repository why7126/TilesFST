## MODIFIED Requirements

### Requirement: 密码安全存储

系统 MUST 使用 bcrypt 算法哈希存储用户密码，数据库中 MUST NOT 存在明文密码。用户设置新密码或管理员重置/创建用户密码时，系统 MUST 按 **effective** 安全策略（`system_settings` merge 代码/env 默认值）校验：最小长度、大写/小写/数字/特殊字符复杂度（若对应开关启用）。校验失败 MUST 返回 400 及统一业务错误码，并 SHOULD 提供可被客户端展示的具体失败项。具体失败项 MUST NOT 包含明文密码。

#### Scenario: 密码哈希验证

- **WHEN** 系统创建或验证用户密码
- **THEN** 系统 MUST 使用 passlib bcrypt 进行哈希与校验
- **AND** 日志与 API 响应 MUST NOT 包含明文密码

#### Scenario: 密码不符合 effective 策略

- **GIVEN** effective 最小长度为 12 且要求数字
- **WHEN** 用户或管理员提交不含数字的 10 位密码
- **THEN** MUST 返回 400 及密码策略错误码
- **AND** MUST 提供可识别的失败项，至少能表达长度不足与缺少数字
- **AND** MUST NOT 更新 password_hash

