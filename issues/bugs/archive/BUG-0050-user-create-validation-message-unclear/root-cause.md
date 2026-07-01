---
bug_id: BUG-0050-user-create-validation-message-unclear
title: 创建用户校验失败未明确提示具体问题点 - 根因分析
severity: medium
status: pending_review
owner: product
created_at: 2026-06-30 18:11:55
updated_at: 2026-06-30 18:11:55
related_requirement: REQ-0005-user-management
---

# 根因分析

## 直接原因

`POST /api/v1/admin/users` 创建用户时，`UserCreateRequest.username` 在 Pydantic Schema 中声明了 `min_length=4` 与 `max_length=32`。当用户名为 `abc` 这类长度不足的输入时，请求在 FastAPI/Pydantic 参数校验阶段被提前拦截，业务服务层 `UserAdminService.create_user()` 没有机会执行。

因此，业务层中 `validate_username()` 已定义的中文错误文案「用户名长度须为 4–32 位」不会返回给前端。

## 根本原因

用户创建的同一条用户名规则分散在两层校验中：

| 层级 | 现状 | 结果 |
|---|---|---|
| Schema 层 | `username: str = Field(min_length=4, max_length=32)` | 长度不足时 FastAPI 返回默认 422 `detail` |
| Service 层 | `validate_username()` 返回中文业务错误 | 仅在通过 Schema 长度校验后才执行 |

同时，后端当前只对 `AppError` 做统一错误响应处理，未将 FastAPI 的请求体校验错误统一转换为项目约定的 `{ code, message, data }` 结构。

前端 `getErrorMessage()` 主要读取 `response.data.message`；当后端返回默认 422 `detail` 时，前端无法提取中文业务文案，最终显示兜底错误。

## 触发条件

满足以下条件即可触发：

1. 调用 `POST /api/v1/admin/users`。
2. 请求体包含长度小于 4 位或大于 32 位的 `username`。
3. 前端依赖统一响应中的 `message` 展示错误提示。

典型输入：

```json
{
  "username": "abc",
  "role": "store_owner"
}
```

## 分类

| 分类 | 判断 |
|---|---|
| code | 是，Schema 校验与业务校验顺序导致错误结构不一致 |
| design | 是，字段级错误提示策略未在 API 与前端之间统一 |
| db | 否，不涉及数据库结构或数据写入 |
| security | 否，不涉及鉴权绕过或敏感信息泄露 |
| ui | 是，管理端表单错误提示不明确 |

## 关联实现点

- 后端 Schema：`src/backend/app/schemas/user_admin.py`
- 后端业务校验：`src/backend/app/core/user_validation.py`
- 后端业务服务：`src/backend/app/services/user_admin_service.py`
- 后端统一异常：`src/backend/app/main.py`
- 前端错误提取：`src/web/src/features/auth/api/auth-api.ts`

## 修复方向建议

后续修复 Change 中建议优先保证两点：

1. 用户名长度不足时，后端返回项目统一错误结构，并包含中文 `message`。
2. 管理端创建用户弹窗能展示具体字段与原因，至少覆盖用户名长度、格式、连续特殊符号、保留字、重复用户名等路径。

可选实现策略：

- 将用户名长度校验统一收敛到 `validate_username()`，避免 Schema 层提前返回默认 422。
- 或增加全局 `RequestValidationError` 处理，将 Pydantic 校验错误转换为统一响应结构。
- 前端可补充提交前校验作为体验增强，但不应替代后端统一错误响应。
