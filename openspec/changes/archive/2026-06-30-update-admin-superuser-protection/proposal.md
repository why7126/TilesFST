---
change_id: update-admin-superuser-protection
title: 管理端超级管理员账号保护
created_at: 2026-06-30 18:26:13
updated_at: 2026-06-30 18:26:13
source_requirement: REQ-0019-admin-superuser-protection
status: proposed
---

## Why

管理端现有用户管理和个人改密能力可以影响所有 `admin` 角色用户。项目依赖 `.env` 中的 `ADMIN_USERNAME` 作为保底管理员账号；如果该账号被编辑、重置密码、冻结、删除或通过管理端改掉密码，系统可能失去运维恢复入口。

REQ-0019 已评审通过并纳入 sprint-004，需要在不新增 `super_admin` / `root` 角色的前提下，把 `ADMIN_USERNAME` 对应账号升级为受保护系统账号。

## What Changes

- 后端新增统一受保护账号判定：以 `settings.admin_username` / `ADMIN_USERNAME` 为唯一事实源，默认回退 `admin`。
- 用户列表和详情 API 返回 `is_protected`、`protected_reason`，供前端控制操作态。
- 用户编辑、重置密码、冻结、解冻、软删除接口对受保护账号返回 403，且不得修改数据库字段。
- 管理端本人修改密码接口默认拒绝受保护账号本人改密，不更新 `password_hash`，不递增 `token_version`。
- 用户管理列表保留受保护账号行操作按钮但置灰，不隐藏操作，不硬编码 `admin`。
- 新增或登记稳定错误码，保持统一响应结构，并同步 OpenAPI / Orval。
- 补充 pytest 与 Vitest / Testing Library 覆盖受保护账号保护和普通用户不回归。

## Capabilities

### New Capabilities

无。该需求是既有用户管理、改密、API 治理、Web 客户端与测试能力的策略扩展。

### Modified Capabilities

- `user-management`: 用户列表/详情响应扩展受保护字段；编辑、重置密码、状态变更必须拒绝受保护账号；列表行操作禁用态必须消费后端字段。
- `admin-password-change`: 当前用户为受保护账号时，管理端本人修改密码接口必须拒绝且不改变密码或 token_version。
- `api-governance`: 新增或复用稳定错误码，错误响应保持 `{ code, message, data }`，OpenAPI / Orval 必须同步新增字段。
- `web-client`: 用户管理列表对受保护账号行操作置灰，保留 DS confirm / fixed toast 横切规则，不引入 `window.confirm` 或文档流 notice。
- `testing`: 本 change 实现必须补齐后端集成测试和前端组件测试。

## Impact

| 影响面 | 说明 |
|---|---|
| 后端 | `Settings`、用户查询 schema、用户管理 service/router、admin profile password service/router、错误码 |
| API | `GET /api/v1/admin/users`、`GET /api/v1/admin/users/{id}` 响应字段新增；用户维护与改密接口新增 403 错误分支 |
| 数据库 | 不新增表或字段；保护既有 `users` 记录不被管理端破坏性更新 |
| Web 管理端 | `/admin/users` 行操作禁用态和提示；改密弹窗展示接口 message |
| Web 展示端 / 小程序 | 不涉及 |
| Orval | API 契约变化后必须重新生成 `src/web/src/shared/api/generated.ts` |
| 文档 | `docs/standards/error-codes.md`、`docs/03-api-index.md`、change trace 与验收记录 |
| 测试 | pytest 覆盖保护拦截；Vitest / Testing Library 覆盖置灰和普通用户不回归 |
