---
change_id: update-admin-superuser-protection
title: 管理端超级管理员账号保护任务清单
created_at: 2026-06-30 18:26:13
updated_at: 2026-06-30 21:57:06
source_requirement: REQ-0019-admin-superuser-protection
status: applied
---

# Tasks

## 1. 后端保护与 API 契约

- [x] 1.1 增加统一受保护账号判定 helper / service，读取 `settings.admin_username`，默认 `admin`，并处理 `strip()` / 大小写归一化。
- [x] 1.2 用户列表与详情 schema 增加 `is_protected`、`protected_reason`，列表和详情接口统一填充字段。
- [x] 1.3 `PATCH /api/v1/admin/users/{id}` 对受保护账号返回 403，且不修改 `display_name`、`role`、`avatar_object_key`。
- [x] 1.4 `POST /api/v1/admin/users/{id}/reset-password` 对受保护账号返回 403，且不生成新密码、不更新 `password_hash`。
- [x] 1.5 `PATCH /api/v1/admin/users/{id}/status` 对受保护账号任意状态变更返回 403，且不修改 `status`。
- [x] 1.6 `POST /api/v1/admin/profile/password` 对当前受保护账号返回 403，且不更新 `password_hash`、不递增 `token_version`。
- [x] 1.7 登记受保护账号错误码（建议 `30060`），同步 `src/backend/app/core/error_codes.py`、异常映射与 `docs/standards/error-codes.md`。
- [x] 1.8 保留 `.env` 级 `ADMIN_RESET_PASSWORD_ON_STARTUP` / `ADMIN_INITIAL_PASSWORD` 运维恢复能力，不改变 seed 语义。

## 2. OpenAPI / Orval / 文档

- [x] 2.1 确认 FastAPI OpenAPI 暴露 `is_protected` 与 `protected_reason` 字段。
- [x] 2.2 执行 `./scripts/generate-openapi-client.sh`，提交 Orval 生成的 `src/web/src/shared/api/generated.ts`。
- [x] 2.3 更新 `docs/03-api-index.md` 管理端用户接口说明，记录新增字段与受保护账号错误分支。
- [x] 2.4 如 API governance 校验脚本覆盖错误码登记，执行并修复漂移。

## 3. Web 管理端

- [x] 3.1 `/admin/users` 前端类型改用 Orval 生成字段，禁止 `username === 'admin'` 或 role 推导保护状态。
- [x] 3.2 受保护账号行「编辑」「重置密码」「冻结/解冻」「删除」按钮保留但置灰，并展示 `protected_reason`。
- [x] 3.3 禁用操作不得打开 confirm modal、不得调用 API。
- [x] 3.4 普通用户编辑、重置密码、冻结/解冻、删除 confirm、toast 和列表刷新不回归。
- [x] 3.5 改密弹窗对受保护账号错误展示接口返回 message，不显示通用未知错误。
- [x] 3.6 保持 `/admin/users` 分页 DOM：左侧 `page-summary`，右侧 `page-right` 页码与每页条数。
- [x] 3.7 不引入 `window.confirm`，不使用文档流 notice 推挤页面；样式复用 `user-management.css` / semantic token，不新增裸 Hex。

## 4. 测试

- [x] 4.1 pytest 覆盖用户列表返回受保护标识与普通 admin 不受保护。
- [x] 4.2 pytest 覆盖编辑受保护账号返回 403 且字段不变。
- [x] 4.3 pytest 覆盖重置受保护账号密码返回 403 且 `password_hash` 不变。
- [x] 4.4 pytest 覆盖状态变更受保护账号返回 403 且 `status` 不变。
- [x] 4.5 pytest 覆盖受保护账号本人改密返回 403，`password_hash` 与 `token_version` 不变。
- [x] 4.6 Vitest / Testing Library 覆盖受保护账号行操作按钮置灰、禁用原因与普通用户操作不回归。
- [x] 4.7 运行相关后端测试、前端测试、API governance 校验和 OpenSpec validate。

## 5. 验收与追踪

- [x] 5.1 更新 change `trace.md`：记录 pytest、Vitest、Orval、OpenSpec validate 和 UI 横切 checklist。
- [x] 5.2 更新 `issues/requirements/archive/REQ-0019-admin-superuser-protection/trace.md` 的 `openspec_changes` 状态。
- [x] 5.3 更新 `iterations/change/sprint-004/acceptance-report.md` 中 REQ-0019 AC 勾选状态。
- [x] 5.4 实现完成后执行 `/opsx-archive update-admin-superuser-protection`。
