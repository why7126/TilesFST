## MODIFIED Requirements

### Requirement: 管理端重置密码 API

系统 MUST 提供 `POST /api/v1/admin/users/{id}/reset-password`，仅 `admin` 可调用。系统 MUST 生成满足 **effective** 密码策略的随机密码（长度与复杂度按 `system_settings` security 分组 merge 默认值）并在响应中一次性返回明文；后续 GET 接口 MUST NOT 再返回该密码。

#### Scenario: 重置密码成功

- **WHEN** `admin` 对存在且非 `deleted` 的用户调用重置密码
- **THEN** 系统返回 HTTP 200，`data.password` 为一次性明文
- **AND** 用户 password_hash MUST 已更新
- **AND** 生成密码 MUST 满足 effective 最小长度与复杂度开关
