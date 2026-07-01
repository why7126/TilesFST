---
change_id: fix-user-create-validation-message-unclear
title: 创建用户校验失败提示明确化
created_at: 2026-06-30 18:35:35
updated_at: 2026-06-30 18:35:35
source_bug: BUG-0050-user-create-validation-message-unclear
status: proposed
---

## Why

BUG-0050 已评审通过并纳入 sprint-004。管理端 `/admin/users` 创建用户时，输入 `abc` 这类长度不足的用户名会被 FastAPI/Pydantic 请求体校验提前拦截，后端返回默认 422 `detail` 列表，前端只能读取不到 `message` 后展示泛化兜底错误。

这破坏了 `REQ-0005-user-management` 已交付的用户名规则反馈体验，也与 API 统一响应结构 `{ code, message, data }` 不一致。

## What Changes

- 修复 `POST /api/v1/admin/users` 用户名长度不足、格式非法、连续特殊符号、保留字等路径的错误响应。
- 保证请求体校验错误不会直接暴露 FastAPI 默认 `detail` 列表给管理端用户。
- 管理端创建用户弹窗展示后端返回的明确中文错误原因，至少覆盖 `username="abc"`。
- 保持重复用户名 409、合法创建成功、一次性初始密码弹窗和用户列表刷新不回归。
- 补充后端与前端回归测试；若实现选择全局 `RequestValidationError` 处理，需要覆盖非用户管理接口的通用请求体验。

## Capabilities

### Modified Capabilities

- `user-management`: 用户创建 API 必须对用户名校验失败返回统一错误结构和明确 message。
- `api-governance`: 请求体校验错误进入统一错误响应 envelope，不直接透传默认 422 `detail`。

### New Capabilities

- `web-client`: 管理端创建用户弹窗错误提示修复，确保用户能定位「用户名」字段与具体原因。

## Rollback Plan

1. 回滚后端用户创建校验与错误处理改动，恢复原 Pydantic / FastAPI 默认行为。
2. 回滚前端创建用户弹窗错误展示改动，恢复原 `getErrorMessage()` 兜底逻辑。
3. 保留新增测试作为回归信号；若需要临时跳过，必须在 issue trace 中记录原因。
4. 回滚不涉及数据库迁移、对象存储或环境变量变更。

## Impact

| 影响面 | 说明 |
|---|---|
| 后端 | `UserCreateRequest`、用户创建 service/router、统一异常处理或错误提取逻辑 |
| API | `POST /api/v1/admin/users` 用户名校验失败响应结构与 message |
| 数据库 | 不新增表、字段或迁移 |
| Web 管理端 | `/admin/users` 添加用户弹窗错误提示 |
| Web 展示端 / 小程序 | 不涉及 |
| Orval | 若 OpenAPI 错误响应或 schema 发生变化，必须重新生成 |
| 文档 | 视错误码策略同步 `docs/standards/error-codes.md` 与 `docs/03-api-index.md` |
| 测试 | pytest 覆盖 422/业务错误结构；Vitest 覆盖弹窗错误展示 |
