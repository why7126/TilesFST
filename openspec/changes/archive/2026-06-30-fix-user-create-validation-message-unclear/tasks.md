---
change_id: fix-user-create-validation-message-unclear
title: 创建用户校验失败提示明确化 - 任务
created_at: 2026-06-30 18:35:35
updated_at: 2026-06-30 18:52:07
source_bug: BUG-0050-user-create-validation-message-unclear
status: applied
---

# Tasks

## 1. 后端修复

- [x] 1.1 梳理 `UserCreateRequest.username` 与 `validate_username()` 的校验顺序，确定局部收敛或统一 422 转换策略。
- [x] 1.2 修复 `POST /api/v1/admin/users` 中 `username="abc"` 返回默认 FastAPI `detail` 的问题。
- [x] 1.3 确保用户名长度、首字符、连续特殊符号、保留字等错误返回明确中文 `message`。
- [x] 1.4 保持重复用户名 HTTP 409 / `USER_USERNAME_TAKEN` 不回归。
- [x] 1.5 若新增或调整错误码，同步 `src/backend/app/core/error_codes.py` 与 `docs/standards/error-codes.md`。

## 2. 前端修复

- [x] 2.1 检查 `/admin/users` 添加用户弹窗错误提取逻辑，确保优先展示 API `message`。
- [x] 2.2 在弹窗内或等价错误提示区域展示包含「用户名」和具体原因的文案。
- [x] 2.3 修复后确认错误提示不会破坏 modal 宽度、字段间距、按钮区或头像上传区域。
- [x] 2.4 保持创建成功 Toast、一次性密码弹窗、列表刷新行为不回归。

## 3. 测试

- [x] 3.1 补充 pytest：`username="abc"` 返回统一 envelope，且 message 指明用户名长度。
- [x] 3.2 补充 pytest：至少一个业务层用户名格式错误路径返回明确 message。
- [x] 3.3 补充 pytest：重复用户名和合法创建成功路径不回归。
- [x] 3.4 若实现全局 `RequestValidationError` 处理，补充一个非用户管理接口请求体验回归测试。
- [x] 3.5 补充 Vitest / Testing Library：创建用户失败时展示后端 `message`。
- [x] 3.6 补充或更新前端测试：修正用户名后可重新提交成功，错误状态清除。

## 4. API / 文档 / 生成物

- [x] 4.1 判断 OpenAPI 错误响应或 schema 是否变化；如变化，执行 `./scripts/generate-openapi-client.sh`。
- [x] 4.2 如错误码或 API 行为说明变化，同步 `docs/03-api-index.md` 与 `docs/standards/error-codes.md`。
- [x] 4.3 运行 `openspec validate fix-user-create-validation-message-unclear --strict`。
- [x] 4.4 回归 `REQ-0005-user-management` 用户创建验收路径。

## 5. 知识沉淀

- [x] 5.1 修复完成后评估是否沉淀 `docs/knowledge-base/incidents/`：表单 Schema 校验与业务校验文案不一致的处理经验。

## Apply Notes

- 采用局部收敛策略：移除 `UserCreateRequest.username` 的 Pydantic 长度约束，让 `validate_username()` 统一返回业务错误 envelope；未引入全局 `RequestValidationError` 转换，因此 3.4 无需新增跨接口回归。
- 未新增错误码；同步补齐既有运行时代码 `40010`、`40011`、`40012`、`40410`、`40910` 的文档说明。
- 前端复用现有 modal 结构与错误区，仅调整创建失败业务错误的可访问提示；未变更 admin modal 宽度、class 或设计 token。
- 已评估知识沉淀：本次处理模式已记录在本 change 的 design / tasks / trace 中，暂不新增 incident 长期文档。
