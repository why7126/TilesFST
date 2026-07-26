## Context

- **BUG**: `BUG-0023-profile-duplicate-save-buttons`
- **Severity**: low
- **Root cause type**: design / frontend-ui
- **Related REQ**: `REQ-0014-profile-page`（已 archive）
- **Parent change**: `add-admin-profile-page`（已 archive）
- **Target**: `ProfilePage.tsx`、`ProfilePage.test.tsx`

### 原型优先级（MUST）

```text
1. issues/bugs/archive/BUG-0023-profile-duplicate-save-buttons/acceptance.md
2. issues/requirements/archive/REQ-0014-profile-page/prototype/web/profile-page-context.md §5（表单区「重置 + 保存修改」）
3. issues/requirements/archive/REQ-0014-profile-page/prototype/web/profile-page.html（双按钮为历史原型；本 fix 以 UX 定稿为准）
4. rules/ui-design.md（semantic token、禁止裸 Hex）
```

## Bug Analysis Report

### 现象

`/admin/profile` 页头与表单底部各有一个「保存修改」主按钮，共用 `handleSave()`，视觉与交互重复。

### 复现路径

1. `admin` 或 `employee` 登录 Web 管理端。
2. 访问 `/admin/profile`。
3. 观察页头与表单底各一「保存修改」。

### 影响

- 不阻断保存、PATCH、inline save-tip。
- 重复 CTA 增加认知负担。
- 无 API/DB/权限影响。

## Root Cause（摘要）

| ID | 结论 |
|---|---|
| RC-001 | `ProfilePage.tsx` 页头与表单底各渲染「保存修改」 |
| RC-002 | REQ-0014 FR-003 MAY 页头 CTA + 原型 HTML 双按钮 |
| RC-003 | AC-017 仅要求行为一致，未禁止双入口 |
| RC-004 | save-tip 在表单底，页头 CTA 与成功反馈视觉分离 |

## Goals / Non-Goals

**Goals:**

- 全页仅一处「保存修改」，位于 `profile-form-actions`。
- 页头保留眉标/标题/说明，无重复主按钮。
- 保存、重置、disabled、save-tip 行为无回归。
- Vitest 单按钮断言通过。

**Non-Goals:**

- BUG-0022（移除表单内角色/状态字段）— 可同 Sprint 另 apply 或后续 change。
- API / DB / Orval / Docker。
- 修改密码 modal、头像上传、timeline。

## Decisions

### D1：移除页头按钮，保留表单底按钮

- **决策**：删除 `profile-page-head` 内 `<button>保存修改</button>`；保留 `profile-form-actions` 区按钮。
- **理由**：与「重置」、inline `.save-tip` 同区；符合 `profile-page-context.md` §5 与 BUG-0023 acceptance AC-002。
- **备选**：仅保留页头 — 拒绝（save-tip 远离触发点，UX 更差）。

### D2：页头 layout

- **决策**：页头仅保留标题区（eyebrow + h1 + desc），不添加占位按钮。
- **理由**：`profile-page-head` 为 flex；移除按钮后标题区自然左对齐，无需 dummy spacer。

### D3：测试策略

- `ProfilePage.test.tsx`：`getByRole('button', { name: '保存修改' })` 单入口。
- 保留校验失败、重置、save-tip 用例。
- `cd src/web && pnpm vitest run src/pages/admin/ProfilePage`

### D4：Spec delta

- MODIFIED `admin-profile-page` →「管理端个人资料页面」增加单 CTA 约束与新 Scenario。

## Risks / Trade-offs

| 风险 | 缓解 |
|------|------|
| 原型 PNG 仍含页头按钮 | acceptance 以 BUG-0023 UX 定稿为准；trace 记录单 CTA 验收 |
| 用户习惯页头保存 | 表单底按钮位置更符合 edit-form 模式 |
| 与 BUG-0022 分 change | 本 change scope 仅 0023；0022 可后续 `fix-profile-redundant-role-status` |

## Migration Plan

- 无数据迁移；前端 deploy 即生效。
- 回滚见 proposal Rollback Plan。

## Open Questions

- 无（BUG-0023 approved，acceptance 已明确）。
