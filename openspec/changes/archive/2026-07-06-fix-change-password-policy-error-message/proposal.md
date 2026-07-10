---
created_at: 2026-07-07 00:04:42
updated_at: 2026-07-07 00:04:42
---

# Change: fix-change-password-policy-error-message

## Why

BUG-0061 记录了管理端修改密码时，新密码不满足安全策略只提示“新密码不符合安全策略”的问题。当前后端已经支持 effective 密码策略（最小长度、大小写、数字、特殊字符），但策略失败原因被折叠为同一个 `policy` 结果；前端 `ChangePasswordModal` 仍展示静态旧规则，用户无法知道具体应补足哪一项。

该问题不构成权限绕过，但会显著增加管理端用户修改密码的试错成本，并在安全策略配置更严格时放大误导风险。

## What Changes

- 后端密码策略校验返回可解释的失败项，覆盖长度、大写、小写、数字、特殊字符、弱密码、同原密码等场景。
- 修改密码 API 的策略失败错误响应必须支持前端识别具体失败原因；若响应结构变化，必须同步 OpenAPI、Orval、`docs/03-api-index.md` 和错误码/治理文档。
- Web 管理端修改密码弹窗展示与当前 effective 密码策略一致的规则提示，并在提交失败时展示具体失败项与可操作建议。
- 保持原密码错误、弱密码、与原密码相同、限流、受保护账号不可改密等既有错误语义无回归。
- 补充后端和前端回归测试，覆盖各策略失败项、动态策略展示和既有路径。

## Capabilities

- Modified: `admin-password-change`
- Modified: `auth`
- Modified: `web-client`
- Modified: `testing`

## Impact

- 影响 API：`POST /api/v1/admin/profile/password` 的错误表达可能增强；不得改变成功响应结构。
- 影响 Web：`ChangePasswordModal` 的规则展示、错误提示和测试。
- 影响 Orval：若 OpenAPI schema 因错误响应详情变化而变化，必须重新生成 Orval 客户端。
- 影响 docs：若 API 错误响应结构变化，必须同步 `docs/03-api-index.md`、`docs/standards/api-governance.md` 或错误码文档。
- 不影响数据库 schema、MinIO、Docker Compose、小程序或店主 Web。
- 不得记录、回显或持久化明文密码。

## Rollback Plan

- 若前端规则展示或错误映射导致误导，可回退 `ChangePasswordModal` 相关实现与测试，恢复原错误展示路径。
- 若 API 错误响应详情导致客户端兼容问题，可保留原 `code/message/data` envelope，回退新增详情字段，并同步回退 OpenAPI、Orval 与接口文档。
- 回滚后必须运行修改密码后端测试、前端 `ChangePasswordModal` 测试和 OpenAPI/Orval 校验（若涉及契约）。

