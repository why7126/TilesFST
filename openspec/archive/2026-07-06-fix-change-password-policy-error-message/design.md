---
created_at: 2026-07-07 00:04:42
updated_at: 2026-07-07 00:04:42
---

# Design: 修改密码安全策略错误提示修复

## 背景

管理端修改密码能力来自 REQ-0015 / `add-admin-password-change`。当前已生效规范要求 `POST /api/v1/admin/profile/password` 支持本人改密、token_version 失效旧 token、弱密码拒绝和策略失败错误码。

随着系统设置引入 effective 安全策略，后端实际策略已经包含最小长度、大小写、数字和特殊字符开关；但修改密码弹窗仍展示固定旧规则，且后端对多类策略失败仅返回泛化 `40021` / “新密码不符合安全策略”。

## Root Cause

- `validate_password_policy()` 将长度、大写、小写、数字、特殊字符失败统一返回 `"policy"`。
- `PasswordPolicyError` 默认 message 只有“新密码不符合安全策略”，没有失败项列表。
- `ChangePasswordModal` 前端规则写死为 `8-32 位 + 字母数字 + 不同于原密码`，没有读取 effective 策略，也无法根据服务端策略失败项展示具体建议。
- 测试只覆盖错误码或泛化文案，未要求用户可见具体失败原因。

## Fix Strategy

### 后端策略失败详情

后端校验应返回可解释失败项，建议使用稳定枚举：

```text
min_length
max_length
missing_uppercase
missing_lowercase
missing_digit
missing_special
same_as_old
weak
```

实现可选择：

- 保持错误码 `40021`，在错误响应 `data` 中返回 `violations` / `failed_rules`。
- 或在 `message` 中拼接面向用户的具体原因，同时保持机器可读字段。

无论采用哪种方式，统一响应 envelope `{ code, message, data }` MUST 保持；成功响应 `{ success: true }` MUST 不变。

### 前端规则展示

修改密码弹窗应展示当前 effective 密码策略。可选实现路径：

1. 复用已有系统设置 effective settings API（如可用且权限允许）。
2. 后端增加/暴露只读的当前密码策略摘要（若新增 API，需另行纳入 spec/docs/Orval）。
3. 在提交后使用服务端返回的失败项更新规则状态和错误文案。

本 Change 的最低验收是：用户在失败后能够看到具体失败项；更优路径是提交前规则列表也与 effective 策略一致。

### 错误提示归属

- 原密码错误仍显示在原密码字段下方。
- 新密码策略、弱密码、同原密码错误显示在新密码字段或新密码规则区。
- 确认新密码不一致仍显示在确认字段下方。
- 受保护账号不可改密、限流等错误继续展示可理解 message，不能误归为策略失败。

### API / Orval / Docs 同步

如果错误响应 `data` 从 `null` 变为结构化详情，必须：

- 更新 OpenAPI schema。
- 运行 `./scripts/generate-openapi-client.sh`。
- 同步 `docs/03-api-index.md` 修改密码错误响应说明。
- 按需同步错误码/治理文档和前端类型使用。

### 安全边界

- 不放宽密码策略。
- 不绕过后端校验。
- 不在 API 响应、日志、埋点、URL 或本地存储中写入明文密码。
- 不改变受保护管理员账号不可本人改密的策略。

## Compatibility

- Database：无 schema 变更。
- Miniapp / public Web：无影响。
- Object storage / Docker：无影响。
- API：可能增强错误响应详情；若实施该路径需同步 OpenAPI/Orval。
- Web Admin：修改 `ChangePasswordModal` 及相关测试。

## Validation

- 后端测试覆盖每类策略失败项、弱密码、同原密码、原密码错误、限流和受保护账号。
- 前端测试覆盖动态/具体规则提示、API 错误映射和成功改密无回归。
- 若 API schema 变化，运行 OpenAPI 导出与 Orval 生成。
- 运行 OpenSpec validate 和目录结构校验。

