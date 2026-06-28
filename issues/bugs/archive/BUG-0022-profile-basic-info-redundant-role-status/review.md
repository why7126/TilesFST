---
bug_id: BUG-0022-profile-basic-info-redundant-role-status
review_id: REV-BUG-0022-001
status: approved
reviewed_at: 2026-06-28 12:56:26
reviewer: ai-agent
decision: approve
severity: low
hotfix_required: false
---

# 缺陷评审

## 1. 评审结论

`BUG-0022-profile-basic-info-redundant-role-status` 评审通过，状态变更为 `approved`。

该缺陷应进入修复流程，后续可执行：

```text
/bug-opsx BUG-0022-profile-basic-info-redundant-role-status
```

建议修复 Change（可与 BUG-0023 合并）：

```text
fix-profile-page-ux-refine
```

## 2. 评审清单

| 检查项 | 结论 | 说明 |
|---|---|---|
| 可复现或根因充分 | 通过 | 100% 稳定复现（修复前表单与账号安全卡片双区展示）；`root-cause.md` 已定位 REQ-0014 / 原型 spec 双区要求与 UX 反馈冲突。 |
| 严重等级合理 | 通过 | `low` 合理；只读信息重复，不阻断 PATCH、权限或数据。 |
| 回归验收明确 | 通过 | `acceptance.md` AC-001～AC-009 覆盖表单去重、AC-022 保留、PATCH/校验无回归、REQ/OpenSpec MODIFIED、vitest/build。 |
| 是否需 hotfix 路径 | 不需要 | 非阻断、非安全、非数据；常规 `fix-*` Change 即可，纯前端 + 文档 delta。 |

## 3. 批准理由

1. 用户 UX 反馈已采纳：角色/状态仅在「账号安全」卡片展示，REQ-0014 **AC-011 MODIFIED** 与 prototype/OpenSpec 已对齐方向。
2. 根因与修复面集中：移除 `ProfilePage.tsx` 表单内 `profile-role` / `profile-status`；不涉及 API/DB/Orval/Docker。
3. 与 BUG-0023（重复保存按钮）同页，建议合并为 `fix-profile-page-ux-refine` 一次交付。
4. workaround 已说明可忽略重复只读字段继续编辑，但不满足信息架构收敛目标。

## 4. 修复门禁

| 项目 | 结论 |
|---|---|
| 是否允许 `/bug-opsx` | 是 |
| 是否允许进入 Sprint | 是 |
| 建议 Change ID | `fix-profile-page-ux-refine` |
| Change 类型 | `fix-*` |

## 5. 修复范围建议

1. 删除 `profile-form-grid` 内「所属角色」「账号状态」只读 field（若工作区尚未合并则 apply 时执行）。
2. 保留账号安全卡片 info-list 与 AC-022 展示。
3. 确认 REQ-0014 acceptance、prototype HTML、OpenSpec `admin-profile-page` Scenario 已 MODIFIED。
4. `ProfilePage.test.tsx` 现有用例 MUST 仍 pass；可选补充断言表单无 role/status label。
5. MUST NOT 变更 profile API、店主端或 BUG-0023 scope 外的双保存按钮（除非同 change 一并修复）。

## 6. 后续动作

1. 执行 `/bug-opsx BUG-0022-profile-basic-info-redundant-role-status`（或与 BUG-0023 合并 opsx）。
2. 纳入 Sprint 后 `/opsx-apply` → acceptance 勾选 → `/opsx-archive`。
3. 1440×1024 与更新后 `profile-page.html` 并排验收表单字段顺序。
