## Why

当前密码策略在规范中仍以 effective 安全策略表达，涉及最小长度、大小写、数字、特殊字符等复杂度开关；管理端提示也可能继续展示旧规则。`REQ-0063` 已评审通过，要求将基础密码校验简化为 5-32 位、包含英文字符、包含数字，并保证后端、管理端提示、API message 与测试一致。

## What Changes

- 将系统“设置新密码”的基础校验规则统一为 5-32 位、至少 1 个 ASCII 英文字符、至少 1 个 ASCII 数字。
- 修改修改本人密码、创建用户初始密码、管理员重置密码等入口的规范，要求复用统一密码校验/生成策略。
- 修改管理端修改密码弹窗规则提示：不得再展示大小写/特殊字符或“至少 8 位”等旧规则。
- 保留既有安全边界：bcrypt 哈希、原密码校验、新旧密码不得相同、弱密码表、限流、token_version 失效、受保护账号限制。
- 后续实现必须同步后端校验、前端提示、API 错误 message、测试；如 OpenAPI/Orval 受影响，必须同步生成与验证。

## Capabilities

### New Capabilities

无。

### Modified Capabilities

- `auth`: 修改密码安全存储中的统一新密码基础策略。
- `admin-password-change`: 修改本人密码 API 与弹窗的密码策略失败项和规则提示。
- `user-management`: 修改创建用户初始密码与重置密码生成策略，确保生成密码满足新规则。

## Impact

- **backend:** 统一密码校验函数、随机密码生成、修改密码 API、用户创建/重置密码 API。
- **web/admin:** 修改密码弹窗、用户创建/重置密码的一次性密码提示与相关测试。
- **api:** 策略错误 message / data 失败项可能调整；若 OpenAPI schema 或错误码文档受影响需同步。
- **database:** 不新增表字段，不改变 `users.password_hash` / `token_version` 结构。
- **storage/media/miniapp:** 不涉及。
- **tests:** 后端 pytest、前端 Vitest/Testing Library、必要的 API 集成测试。
