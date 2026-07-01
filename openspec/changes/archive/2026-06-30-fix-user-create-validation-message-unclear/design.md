---
change_id: fix-user-create-validation-message-unclear
title: 创建用户校验失败提示明确化 - 设计
created_at: 2026-06-30 18:35:35
updated_at: 2026-06-30 18:35:35
source_bug: BUG-0050-user-create-validation-message-unclear
status: proposed
---

# Design

## Bug Analysis Report

| 项 | 内容 |
|---|---|
| 现象 | 创建用户时输入 `abc`，界面未明确提示用户名长度不足 |
| 稳定复现 | 管理员进入 `/admin/users` → 添加用户 → 用户名填 `abc` → 提交 |
| 实际响应 | 后端返回 FastAPI 默认 422 `detail` 列表，前端无法读取 `message` |
| 期望响应 | 后端返回统一 `{ code, message, data }`，`message` 指明用户名长度须为 4-32 位 |
| 影响范围 | 管理端用户创建弹窗、`POST /api/v1/admin/users` 错误响应一致性 |
| 严重等级 | medium |

## Root Cause

用户名规则存在两层校验：

| 层级 | 现状 | 问题 |
|---|---|---|
| Schema | `UserCreateRequest.username` 使用 `min_length=4` / `max_length=32` | 长度错误在业务 service 前被 FastAPI 拦截 |
| Service | `validate_username()` 返回中文业务文案 | Pydantic 拦截后不会执行 |
| 异常处理 | 只统一处理 `AppError` | `RequestValidationError` 仍返回默认 `detail` |
| 前端 | 优先读取 `response.data.message` | 无 `message` 时只能展示兜底文案 |

## Repair Strategy

推荐实现顺序：

1. 后端优先收敛用户名规则：避免 `username="abc"` 在 Schema 层返回默认 422，确保进入统一业务错误路径。
2. 若保留 Pydantic 长度约束，必须增加 `RequestValidationError` 处理，将请求体校验错误转成 `{ code, message, data }`。
3. 用户名错误文案优先复用 `validate_username()` 已定义中文文案，例如「用户名长度须为 4-32 位」。
4. 前端创建用户弹窗继续展示 API `message`，并确保错误提示不会破坏用户弹窗 CSS Port、modal 宽度和字段布局。
5. 重复用户名仍返回 409 与既有错误码；合法创建成功仍展示「用户已创建」和一次性密码弹窗。

## API Contract

- Endpoint: `POST /api/v1/admin/users`
- Invalid username length:
  - HTTP status SHOULD be 400 if进入业务校验路径；若全局 request validation 仍使用 422，则 body MUST 统一为 `{ code, message, data }`。
  - `code` MUST use registered user validation code, preferred `USER_INVALID_USERNAME` when applicable.
  - `message` MUST include field and reason in Chinese.
- Duplicate username:
  - HTTP 409 and `USER_USERNAME_TAKEN` MUST remain unchanged.

## Frontend Design

- Error source priority stays: API `message` > known detail mapping > fallback.
- The add-user modal MAY show the message in form-level alert or field-adjacent error area.
- Visible text MUST help locate the username field.
- Styling MUST reuse existing user-management modal classes and Design System tokens; no bare Hex.

## Test Design

- Backend:
  - `username="abc"` returns unified envelope and Chinese message.
  - `username="1abc"` or equivalent format error returns explicit message.
  - duplicate username still returns conflict.
  - valid user creation still returns `initial_password`.
  - if global `RequestValidationError` handling is changed, add one non-user-management request validation regression.
- Frontend:
  - create user failure displays backend message.
  - correcting username clears error and successful create path still works.
  - modal layout does not regress under visible error text.

## Risk

| 风险 | 缓解 |
|---|---|
| 全局 422 处理影响其他 API | 优先局部收敛用户创建用户名校验；若做全局处理，补通用回归测试 |
| 前端只显示 toast 不便定位字段 | 至少显示包含「用户名」的具体 message；可在弹窗内补充错误区域 |
| 与 REQ-0019 用户管理改动并行 | 保持本 change 聚焦创建校验；不修改受保护账号策略字段 |
