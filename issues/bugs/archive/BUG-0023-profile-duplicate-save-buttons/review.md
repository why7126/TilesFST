---
bug_id: BUG-0023-profile-duplicate-save-buttons
review_id: REV-BUG-0023-001
status: approved
reviewed_at: 2026-06-28 12:55:00
reviewer: ai-agent
decision: approve
severity: low
hotfix_required: false
---

# 缺陷评审

## 1. 评审结论

`BUG-0023-profile-duplicate-save-buttons` 评审通过，状态变更为 `approved`。

该缺陷应进入修复流程，后续可执行：

```text
/bug-opsx BUG-0023-profile-duplicate-save-buttons
```

建议修复 Change（可与 BUG-0022 合并）：

```text
fix-profile-page-ux-refine
```

## 2. 评审清单

| 检查项 | 结论 | 说明 |
|---|---|---|
| 可复现或根因充分 | 通过 | 100% 稳定复现；`root-cause.md` 已定位页头 + 表单底双按钮、`ProfilePage.tsx` 两处 `handleSave()` 绑定及 REQ-0014 原型/AC-017 允许双 CTA 的根因。 |
| 严重等级合理 | 通过 | `low` 合理；保存功能正常，仅 UX 冗余，不阻断业务。 |
| 回归验收明确 | 通过 | `acceptance.md` AC-001～AC-011 覆盖单入口、表单 actions 区、保存/重置/disabled、REQ-0014 无回归、vitest 与 AC-017 delta。 |
| 是否需 hotfix 路径 | 不需要 | 非阻断、非安全、非数据问题；常规 `fix-*` Change 即可，预计改动 `ProfilePage.tsx` + 测试 + spec delta。 |

## 3. 批准理由

1. REQ-0014 / `add-admin-profile-page` 已交付，本 BUG 为交付后 UX polish，与「已实现需求 + fix-* 补丁」模式一致。
2. 根因与修复面集中：移除页头重复按钮，保留表单底 CTA 与 save-tip 同区；不涉及 API/DB/Orval/Docker。
3. 与 BUG-0022（同页冗余字段）同属个人资料页 UX  refine，建议合并为单一 change 减少重复 touch。
4. workaround 已说明可任选按钮保存，但不消除重复 CTA 的认知负担。

## 4. 修复门禁

| 项目 | 结论 |
|---|---|
| 是否允许 `/bug-opsx` | 是 |
| 是否允许进入 Sprint | 是 |
| 建议 Change ID | `fix-profile-page-ux-refine` |
| Change 类型 | `fix-*` |

## 5. 修复范围建议

1. 移除 `profile-page-head` 内「保存修改」按钮，保留 `profile-form-actions` 区按钮。
2. 更新 `ProfilePage.test.tsx`：`getAllByRole` → `getByRole('button', { name: '保存修改' })`。
3. fix change delta spec **MODIFIED** REQ-0014 AC-017（单 CTA）。
4. 页头眉标/标题/说明 MUST 保留，布局无回归。
5. 可选：与 BUG-0022 一并移除表单内「所属角色」「账号状态」只读字段。
6. MUST NOT 变更 PATCH 逻辑、inline save-tip、头像上传或账号安全卡片行为。

## 6. 后续动作

1. 执行 `/bug-opsx BUG-0023-profile-duplicate-save-buttons` 创建 `fix-profile-page-ux-refine`（或与 BUG-0022 合并 opsx）。
2. 可纳入 Sprint（`related_requirement: REQ-0014-profile-page`）。
3. 修复完成后 `/opsx-apply` → 1440×1024 单 CTA 验收 → `/opsx-archive`。
