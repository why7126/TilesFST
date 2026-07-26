## Context

- **BUG**: `BUG-0022-profile-basic-info-redundant-role-status`
- **Severity**: low
- **Root cause type**: design / frontend-ui（信息架构）
- **Related REQ**: `REQ-0014-profile-page`（已 archive）
- **Parent change**: `add-admin-profile-page`（已 archive）
- **Target**: `ProfilePage.tsx`、REQ-0014 文档、OpenSpec delta

### 原型优先级（MUST）

```text
1. issues/bugs/archive/BUG-0022-profile-basic-info-redundant-role-status/acceptance.md
2. issues/requirements/archive/REQ-0014-profile-page/acceptance.md AC-011（MODIFIED）
3. issues/requirements/archive/REQ-0014-profile-page/prototype/web/profile-page.html（已移除表单内 role/status）
4. issues/requirements/archive/REQ-0014-profile-page/prototype/web/profile-page-context.md §5
5. rules/ui-design.md（semantic token、禁止裸 Hex）
```

## Bug Analysis Report

### 现象

`/admin/profile`「基础资料」表单内「所属角色」「账号状态」与「账号安全」卡片重复展示。

### 复现路径

1. `admin` 或 `employee` 登录 Web 管理端。
2. 访问 `/admin/profile`。
3. 观察表单 grid 与账号安全卡片。

### 影响

- 不阻断 PATCH、校验、权限。
- 表单冗长、信息重复。
- 无 API/DB 影响。

## Root Cause（摘要）

| ID | 结论 |
|---|---|
| RC-001 | `ProfilePage.tsx` 表单 grid 渲染 `profile-role` / `profile-status` |
| RC-002 | REQ-0014 原 AC-011 要求表单内含角色/状态只读字段 |
| RC-003 | 原型 HTML 双区并列；`add-admin-profile-page` 忠实 port |
| RC-004 | 账号安全卡片（AC-022）已承担结构化展示职责 |

## Goals / Non-Goals

**Goals:**

- 表单 grid 仅含：用户名（只读）、昵称、邮箱、手机、备注。
- 账号安全卡片保留角色/状态 badge。
- PATCH、重置、校验、save-tip、头像、timeline 无回归。
- REQ-0014 / OpenSpec delta 与实现对齐。

**Non-Goals:**

- 移除 identity-strip 角色 meta / mini-badge 或 card-head「账号正常」badge。
- BUG-0023 双「保存修改」按钮（`fix-profile-duplicate-save-buttons`）。
- API / DB / Orval / Docker。

## Decisions

### D1：删除表单内 role/status field

- **决策**：移除 `profile-form-grid` 内两个 `field readonly` 块（`profile-role`、`profile-status`）。
- **理由**：与 UX 定稿、MODIFIED AC-011 一致；账号安全卡片为唯一结构化展示区。
- **备选**：保留表单字段、隐藏账号安全卡片 — 拒绝（违背 UX 定稿）。

### D2：文档同步

- **决策**：apply 时确认 `REQ-0014` acceptance、requirement、prototype HTML/context 已 MODIFIED；若工作区已先行更新则 verify only。
- **理由**：避免 spec / 原型 / 实现三方漂移。

### D3：测试策略

- 现有 `ProfilePage.test.tsx` 未断言 role/status label；移除字段后 MUST 仍 pass。
- 可选：补充 `queryByLabelText('所属角色')` 为 null 断言。
- `cd src/web && pnpm vitest run src/pages/admin/ProfilePage`

### D4：Spec delta

- MODIFIED `admin-profile-page` → Scenario「表单字段与只读规则」：MUST NOT 表单内展示角色/状态。

## Risks / Trade-offs

| 风险 | 缓解 |
|------|------|
| 原型 PNG 仍含表单内 role/status | acceptance 以 BUG-0022 UX 定稿与更新后 HTML 为准；trace 记录并排结论 |
| 与 BUG-0023 分 change | 两 change 可同 Sprint 并行 apply；touch 同一文件时 merge 顺序：先 0022 字段、再 0023 按钮 |
| 工作区可能已有先行修复 | apply 以 diff 为准；tasks 含 verify 步骤 |

## Migration Plan

- 无数据迁移；前端 deploy 即生效。
- 回滚见 proposal Rollback Plan。

## Open Questions

- 无（BUG-0022 approved，acceptance 已明确）。
