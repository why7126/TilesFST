---
change_id: update-password-validation-policy
status: applied
change_type: update
created_at: 2026-07-20 19:59:14
updated_at: 2026-07-21 23:01:00
source_requirement: REQ-0063-password-validation-policy-simplification
source_requirement_path: issues/requirements/archive/REQ-0063-password-validation-policy-simplification/
iteration: sprint-010
related_specs:
  - auth
  - admin-password-change
  - user-management
knowledge_base_refs:
  - docs/knowledge-base/best-practices/admin-form-page-consistency.md
  - docs/knowledge-base/best-practices/admin-modal-width-css-cascade.md
  - docs/knowledge-base/retrospectives/sprint-008-retrospective.md
cross_cutting_tags:
  - admin-form
  - admin-modal
---

# Change Trace

## 来源

- REQ：`REQ-0063-password-validation-policy-simplification`
- 评审：`REV-REQ-0063-001`
- 预期 Change：`update-password-validation-policy`

## Requirement Readiness Report

| 项 | 结论 |
|---|---|
| REQ status | approved |
| Readiness | Ready |
| 五件套 | capture / requirement / user-stories / business-flow / acceptance / trace / review 齐全 |
| Prototype | `prototype/web/password-policy-hints.html` + `context.md` |
| Knowledge-base gate | Pass |

## Impact

```yaml
impact:
  backend: true
  web: true
  miniapp: false
  admin: true
  database: false
  storage: false
  api: true
capabilities:
  new: []
  modified:
    - auth
    - admin-password-change
    - user-management
```

## Conflict Report

| 来源 | 内容 | 决议 |
|---|---|---|
| REQ prototype HTML/context | 密码提示为 5-32 位、英文、数字，修改密码弹窗保持 520px | 采用 |
| acceptance.md | 要求清除旧文案，多入口一致 | 采用 |
| `admin-password-change` spec | 仍提到 effective 策略、大小写和特殊字符 | 通过 MODIFIED delta 覆盖 |
| `auth` spec | 仍提到 system_settings 复杂度开关 | 通过 MODIFIED delta 覆盖 |
| `user-management` spec | 重置密码按 effective 策略生成 | 通过 MODIFIED delta 覆盖 |

优先级：HTML > context.md > acceptance.md > ui-design.md > openspec/specs。

## UI Checklist

- [x] 修改密码弹窗仍为 520px computed width。
- [x] 新密码字段附近展示 5-32 位、英文字符、数字提示。
- [x] 不展示“至少 8 位”、大小写、特殊字符旧提示。
- [x] 字段级错误不只依赖全局 Toast。
- [x] 矮视口下弹窗 body scroll 和 footer 可访问。

## 实现 Evidence

| 项 | 结论 |
|---|---|
| 后端统一策略 | `src/backend/app/core/password_validation.py` 固定为 5-32 位、ASCII 英文字符、ASCII 数字；失败项为 `min_length`、`max_length`、`missing_letter`、`missing_digit` |
| 随机密码 | `src/backend/app/core/user_validation.py` 生成结果复用统一基础策略，覆盖创建用户 `initial_password` 与重置密码 `password` |
| 既有安全能力 | 弱密码、新旧密码相同、限流、受保护账号、bcrypt hash、`token_version` 失效路径保留，并由既有/新增测试覆盖 |
| API / docs | `POST /api/v1/admin/profile/password` 路径与错误码不变；策略详情示例同步 `docs/03-api-index.md` 与 `docs/standards/error-codes.md` |
| Orval | 未运行；本次未新增/修改 OpenAPI schema 类型，错误响应 `data` 仍为统一 envelope 的运行时详情 |
| DB / Docker | 不涉及数据库结构、迁移、容器配置或对象存储 |
| Web 管理端 | `ChangePasswordModal` 展示 5-32 位、英文字符、数字提示；字段级错误仍在对应字段/规则区；未使用原生 confirm |
| 横切检查 | `admin-form` / `admin-modal` refs 已读；弹窗使用单一 `password-modal` 类，不挂载 `modal-card`；CSS 保持 520px 与矮视口 body scroll |

## 测试摘要

| 命令 | 结果 |
|---|---|
| `uv run pytest src/backend/tests/test_password_change.py src/backend/tests/test_admin_users.py` | 35 passed |
| `uv run pytest src/backend/tests/test_system_settings.py` | 12 passed |
| `pnpm --dir src/web exec vitest run src/features/admin/components/ChangePasswordModal.test.tsx` | 13 passed |
| `pnpm --dir src/web exec vitest run src/pages/admin/SystemSettingsPage.test.tsx` | 7 passed |

备注：曾运行 `pnpm --dir src/web test -- ChangePasswordModal.test.tsx`，该命令匹配范围过宽并跑到无关 `DesignSystemPage.test.tsx`，该无关用例 5000ms 超时；随后已用精确 Vitest 路径完成目标测试。

## 变更记录

| 时间 | 命令 | 说明 |
|---|---|---|
| 2026-07-20 19:59:14 | `/req-opsx REQ-0063` | 创建 OpenSpec Change 并生成 proposal/design/specs/tasks/trace |
| 2026-07-20 22:30:24 | `/sprint-propose sprint-010` | 纳入 sprint-010 正式范围 |
| 2026-07-21 23:01:00 | `/opsx-apply update-password-validation-policy` | 完成密码策略实现、API/文档同步与后端/前端测试 |
