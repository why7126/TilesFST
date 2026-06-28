---
bug_id: BUG-0024-change-password-error-wrong-field
review_id: REV-BUG-0024-001
status: approved
reviewed_at: 2026-06-28 12:56:52
reviewer: ai-agent
decision: approve
severity: medium
hotfix_required: false
---

# 缺陷评审

## 1. 评审结论

`BUG-0024-change-password-error-wrong-field` 评审通过，状态变更为 `approved`。

该缺陷应进入修复流程，后续可执行：

```text
/bug-opsx BUG-0024-change-password-error-wrong-field
```

建议修复 Change（可与 BUG-0025、BUG-0026 合并编排）：

```text
fix-change-password-modal-errors
```

## 2. 评审清单

| 检查项 | 结论 | 说明 |
|---|---|---|
| 可复现或根因充分 | 通过 | 100% 稳定复现；`root-cause.md` 已定位单一 `error` 误绑原密码字段、后端错误码可字段化但前端未分流；截图与代码路径一致。 |
| 严重等级合理 | 通过 | `medium` 合理；错误文案误导用户修改错误字段，但功能不阻断、非安全漏洞。 |
| 回归验收明确 | 通过 | `acceptance.md` AC-001～AC-010 覆盖客户端/服务端新密码错误、原密码错误、确认不一致无回归、Vitest 与视觉验收。 |
| 是否需 hotfix 路径 | 不需要 | 非阻断、非安全、非数据问题；常规 `fix-*` Change 即可，预计改动 `ChangePasswordModal.tsx` + 测试。 |

## 3. 批准理由

1. 根因明确：前端状态设计问题，非 API/后端策略缺陷；修复面集中。
2. 后端已提供细分错误码（40020–40023、42901），前端按码分流即可闭环。
3. 与 BUG-0025（按钮错位）、BUG-0026（取消二次确认）同属修改密码弹窗，可合并为单一 fix change 减少重复 touch。
4. workaround 已说明可按文案语义规避，但不消除误导性 UX。

## 4. 修复门禁

| 项目 | 结论 |
|---|---|
| 是否允许 `/bug-opsx` | 是 |
| 是否允许进入 Sprint | 是 |
| 建议 Change ID | `fix-change-password-modal-errors` |
| Change 类型 | `fix-*` |

## 5. 修复范围建议

1. 拆分 `oldPasswordError` / `newPasswordError`；客户端新密码校验写入 `newPasswordError`。
2. API catch 按 `error_code` 分流：40020 → 原密码；40021/40022/40023 → 新密码。
3. 更新 `ChangePasswordModal.test.tsx` 断言错误字段位置。
4. MUST NOT 变更 API 契约、密码策略、成功改密登出流程。
5. 可选：同 change 一并修复 BUG-0025、BUG-0026（tasks 分列 scope）。

## 6. 后续动作

1. 执行 `/bug-opsx BUG-0024-change-password-error-wrong-field` 创建 OpenSpec change。
2. 可纳入 Sprint（`related_requirement: REQ-0014-profile-page`）。
3. 修复完成后 `/opsx-apply` → 按 AC-010 视觉验收 → `/opsx-archive`。
