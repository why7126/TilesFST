---
change_id: update-password-validation-policy
status: proposed
change_type: update
created_at: 2026-07-20 19:59:14
updated_at: 2026-07-20 22:30:24
source_requirement: REQ-0063-password-validation-policy-simplification
source_requirement_path: issues/requirements/review/REQ-0063-password-validation-policy-simplification/
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

- [ ] 修改密码弹窗仍为 520px computed width。
- [ ] 新密码字段附近展示 5-32 位、英文字符、数字提示。
- [ ] 不展示“至少 8 位”、大小写、特殊字符旧提示。
- [ ] 字段级错误不只依赖全局 Toast。
- [ ] 矮视口下弹窗 body scroll 和 footer 可访问。

## 变更记录

| 时间 | 命令 | 说明 |
|---|---|---|
| 2026-07-20 19:59:14 | `/req-opsx REQ-0063` | 创建 OpenSpec Change 并生成 proposal/design/specs/tasks/trace |
| 2026-07-20 22:30:24 | `/sprint-propose sprint-010` | 纳入 sprint-010 正式范围 |
