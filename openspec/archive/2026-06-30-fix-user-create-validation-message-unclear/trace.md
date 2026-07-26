---
change_id: fix-user-create-validation-message-unclear
status: applied
source_bug: BUG-0050-user-create-validation-message-unclear
created_at: 2026-06-30 18:35:35
updated_at: 2026-06-30 18:52:07
---

# Change Trace

## 来源

- BUG: `issues/bugs/archive/BUG-0050-user-create-validation-message-unclear/`
- 关联需求: `REQ-0005-user-management`
- Sprint: `sprint-004`

## 状态

| 时间 | 动作 | 说明 |
|---|---|---|
| 2026-06-30 18:35:35 | `/bug-opsx` | 创建 OpenSpec fix change，状态 proposed |
| 2026-06-30 18:52:07 | `/opsx-apply` | 已实现后端用户名业务校验收敛、前端错误展示、OpenAPI 客户端生成物与文档同步 |

## 追溯矩阵

| BUG AC | OpenSpec Artifact | 说明 |
|---|---|---|
| AC-001 | `specs/user-management/spec.md`、`specs/api-governance/spec.md` | 用户名长度不足返回统一 envelope 与明确 message |
| AC-002 | `specs/web-client/spec.md` | 添加用户弹窗展示具体错误 |
| AC-003 | `specs/user-management/spec.md` | 其他用户名格式错误仍明确 |
| AC-004 | `specs/user-management/spec.md` | 重复用户名 409 不回退 |
| AC-005 | `specs/user-management/spec.md`、`specs/web-client/spec.md` | 合法创建与一次性密码弹窗不回归 |
| AC-006 | `tasks.md` | 后端与前端回归测试 |

## Apply Verification

| 检查项 | 结果 | 说明 |
|---|---|---|
| Backend pytest | PASS | `uv run pytest src/backend/tests/test_admin_users.py`，12 passed |
| Frontend Vitest | PASS | `node_modules/.bin/vitest run src/features/admin/components/UserFormModal.test.tsx`，6 passed |
| OpenAPI / Orval | PASS | 已执行 `./scripts/generate-openapi-client.sh` 并更新 Web OpenAPI 生成物 |
| OpenSpec strict validate | PASS | `openspec validate fix-user-create-validation-message-unclear --strict` |
| API standard validate | KNOWN-DEBT | `python scripts/validate-api-standard.py` 仍因既有多处路由缺少显式 `tags=` 未通过；本 change 未扩大修复范围 |
