## MODIFIED Requirements

### Requirement: 密码安全存储

系统 MUST 使用 bcrypt 算法哈希存储用户密码，数据库中 MUST NOT 存在明文密码。用户设置新密码或管理员重置/创建用户密码时，系统 MUST 使用统一基础密码策略校验：长度 5-32 位，至少包含 1 个 ASCII 英文字符（`A-Z` / `a-z`），至少包含 1 个 ASCII 数字（`0-9`）。符号等其他字符 MAY 与英文/数字共同出现；非 ASCII 字母或数字 MUST NOT 被计入英文字符或数字满足项，除非后续规范明确扩展字符集。

校验失败 MUST 返回 400 及统一业务错误码，并 SHOULD 提供可被客户端展示的具体失败项。失败项至少 MUST 能区分 `min_length`、`max_length`、`missing_letter`、`missing_digit`。具体失败项 MUST NOT 包含明文密码。

#### Scenario: 密码哈希验证

- **WHEN** 系统创建或验证用户密码
- **THEN** 系统 MUST 使用 passlib bcrypt 进行哈希与校验
- **AND** 日志与 API 响应 MUST NOT 包含明文密码

#### Scenario: 密码长度不足

- **WHEN** 用户或管理员提交少于 5 位的新密码
- **THEN** MUST 返回 400 及密码策略错误码
- **AND** MUST 提供可识别的 `min_length` 失败项
- **AND** MUST NOT 更新 `password_hash`

#### Scenario: 密码长度超限

- **WHEN** 用户或管理员提交超过 32 位的新密码
- **THEN** MUST 返回 400 及密码策略错误码
- **AND** MUST 提供可识别的 `max_length` 失败项
- **AND** MUST NOT 更新 `password_hash`

#### Scenario: 密码缺少英文字符

- **WHEN** 用户或管理员提交长度合规但不含 ASCII 英文字符的新密码
- **THEN** MUST 返回 400 及密码策略错误码
- **AND** MUST 提供可识别的 `missing_letter` 失败项
- **AND** MUST NOT 更新 `password_hash`

#### Scenario: 密码缺少数字

- **WHEN** 用户或管理员提交长度合规但不含 ASCII 数字的新密码
- **THEN** MUST 返回 400 及密码策略错误码
- **AND** MUST 提供可识别的 `missing_digit` 失败项
- **AND** MUST NOT 更新 `password_hash`

#### Scenario: 密码满足基础策略

- **WHEN** 用户或管理员提交 5-32 位且同时包含 ASCII 英文字符和 ASCII 数字的新密码
- **THEN** 基础密码策略校验 MUST 通过
- **AND** 后续业务规则 MAY 继续校验弱密码、新旧密码相同、受保护账号或限流
