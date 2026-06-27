---
bug_id: BUG-0017-user-reset-password-confirm-ui-inconsistency
review_id: REV-BUG-0017-001
status: approved
reviewed_at: 2026-06-27 13:31:00
reviewer: ai-agent
decision: approve
severity: medium
hotfix_required: false
---

# 缺陷评审

## 1. 评审结论

`BUG-0017-user-reset-password-confirm-ui-inconsistency` 评审通过，状态变更为 `approved`。

该缺陷应进入修复流程，后续可执行：

```text
/bug-opsx BUG-0017-user-reset-password-confirm-ui-inconsistency
```

建议修复 Change：

```text
fix-user-reset-password-confirm-ui
```

## 2. 评审清单

| 检查项 | 结论 | 说明 |
|---|---|---|
| 可复现或根因充分 | 通过 | `handleResetPassword` 内 `window.confirm` 可 100% 稳定复现；`root-cause.md` 已定位直接原因与初版遗留 + BUG-0016 scope 排除；与类目启停 Golden Reference 对比清晰。 |
| 严重等级合理 | 通过 | 确认 Dialog UX 不统一，功能可用且有原生二次确认门槛；无安全/数据风险；`medium` 与同类 confirm 统一缺陷一致。 |
| 回归验收明确 | 通过 | `acceptance.md` AC-001～AC-010 覆盖 DS modal、禁止 `window.confirm`、取消无副作用、Golden Reference、结果弹窗不回归、同页/品牌/类目不回归、Vitest 门禁、已删除用户边界。 |
| 是否需 hotfix 路径 | 不需要 | 纯前端 confirm 形态；workaround 为阅读原生 confirm 文案；走常规 `fix-*` Change 即可。 |

## 3. 批准理由

1. 缺陷包完整：capture → bug → root-cause → workaround → acceptance 齐全；`/bug-explore` 已区分重置前 confirm 与 `ResetPasswordDialog` 结果弹窗 scope。
2. 根因清晰：`add-user-management` 遗留 `window.confirm`；同页冻结/删除已 modal 化，重置密码路径独立遗留；有 `TileCategoryManagementPage` / 同页 `statusConfirmTarget` 可复用模式。
3. 修复成本低：单页 state + inline modal；无需 API、DB、Orval 变更；`ResetPasswordDialog` 逻辑保持不变。
4. 与 BUG-0016 职责边界已在 OpenSpec 与 acceptance 中写明，可同 Sprint 编排但 fix change MUST 独立。

## 4. 后续要求

1. `/bug-opsx` 创建 `fix-user-reset-password-confirm-ui`，delta 扩展 `web-client`（或 `user-management`）重置密码确认 requirement，明确 MUST NOT 使用 `window.confirm`。
2. `UserManagementPage`：新增 `resetPasswordConfirmTarget`；确认后再调 `resetUserPassword`。
3. 更新 vitest：确认前 mock MUST NOT 调用；`window.confirm` spy 断言未调用；取消后不调用；确认后调用并触发结果弹窗。
4. 修复时 MUST NOT 回归同页冻结/删除 modal、品牌/类目启停 confirm 及既有 vitest。
5. MUST NOT 修改 `ResetPasswordDialog` 业务逻辑（除非最小接线）。
