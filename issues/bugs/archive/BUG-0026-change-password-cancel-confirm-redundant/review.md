---
bug_id: BUG-0026-change-password-cancel-confirm-redundant
review_id: REV-BUG-0026-001
status: approved
reviewed_at: 2026-06-28 13:13:16
reviewer: ai-agent
decision: approve
severity: low
hotfix_required: false
---

# 缺陷评审

## 1. 评审结论

`BUG-0026-change-password-cancel-confirm-redundant` 评审通过，状态变更为 `approved`。

该缺陷应进入修复流程，后续可执行：

```text
/bug-opsx BUG-0026-change-password-cancel-confirm-redundant
```

建议与 BUG-0024、BUG-0025 合并编排于同一 Change：

```text
fix-change-password-modal-errors
```

## 2. 评审清单

| 检查项 | 结论 | 说明 |
|---|---|---|
| 可复现或根因充分 | 通过 | 100% 稳定复现；`root-cause.md` 已定位 `isDirty` + `window.confirm` 于统一 `requestClose`；截图与代码路径一致。 |
| 严重等级合理 | 通过 | `low` 合理；仅增加一次点击、不阻断改密，但与管理端其它表单弹窗 UX 不一致。 |
| 回归验收明确 | 通过 | `acceptance.md` AC-001～AC-011 覆盖取消/×/Esc/遮罩、空表单、reopen reset、提交无回归、Vitest、OpenSpec delta。 |
| 是否需 hotfix 路径 | 不需要 | 非阻断、非安全、非数据问题；常规 `fix-*` Change 即可，预计改动 `ChangePasswordModal.tsx` + 测试 + spec delta。 |

## 3. 批准理由

1. 根因明确：`requestClose` 脏关闭 guard 为 REQ-0015 原规格交付，但与 Brand/User/TileSku 弹窗「直接关闭」模式冲突；改密无草稿持久化，二次 confirm 无实质保护价值。
2. 修复面小：删除 `isDirty`/`window.confirm` 即可；`acceptance.md` AC-009 已要求 OpenSpec **MODIFIED** 脏关闭 Scenario，规格冲突可在 fix change 内闭环。
3. 与 BUG-0024（错误字段）、BUG-0025（按钮错位）同属 `ChangePasswordModal`，合并为 `fix-change-password-modal-errors` 可减少重复 touch。
4. workaround 已说明可点「确定」规避，但不消除 UX 不一致与原生对话框问题。

## 4. 修复门禁

| 项目 | 结论 |
|---|---|
| 是否允许 `/bug-opsx` | 是 |
| 是否允许进入 Sprint | 是 |
| 建议 Change ID | `fix-change-password-modal-errors`（与 BUG-0024/0025 共用） |
| Change 类型 | `fix-*` |

## 5. 修复范围建议

1. `requestClose` 直接 `onClose()`，移除 `isDirty` 与 `window.confirm`。
2. 更新 `ChangePasswordModal.test.tsx`：dirty 关闭 MUST NOT 调用 `window.confirm`。
3. OpenSpec delta **MODIFIED** `admin-password-change`「关闭与脏确认」Scenario；同步 REQ-0015 AC-007、AC-040。
4. MUST NOT 变更 API 契约、密码策略、成功改密登出流程。
5. 可选：同 change 一并修复 BUG-0024、BUG-0025（tasks 分列 scope）。

## 6. 后续动作

1. 若 BUG-0024 已创建 `fix-change-password-modal-errors`，本 BUG 可追加 scope 至同一 change；否则执行 `/bug-opsx BUG-0026-change-password-cancel-confirm-redundant`。
2. 可纳入 Sprint（`related_requirement: REQ-0014-profile-page`）。
3. 修复完成后 `/opsx-apply` → 按 AC-011 视觉验收 → `/opsx-archive`。
