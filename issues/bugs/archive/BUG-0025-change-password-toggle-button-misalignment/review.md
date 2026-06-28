---
bug_id: BUG-0025-change-password-toggle-button-misalignment
review_id: REV-BUG-0025-001
status: approved
reviewed_at: 2026-06-28 12:58:00
reviewer: ai-agent
decision: approve
severity: medium
hotfix_required: false
---

# 缺陷评审

## 1. 评审结论

`BUG-0025-change-password-toggle-button-misalignment` 评审通过，状态变更为 `approved`。

该缺陷应进入修复流程，后续可执行：

```text
/bug-opsx BUG-0025-change-password-toggle-button-misalignment
```

建议修复 Change（可与 BUG-0024、BUG-0026 合并编排）：

```text
fix-change-password-modal-errors
```

## 2. 评审清单

| 检查项 | 结论 | 说明 |
|---|---|---|
| 可复现或根因充分 | 通过 | 100% 稳定复现；`root-cause.md` 已定位 `toggle-pass` 的 `bottom: 8px` 相对含 `error-text` 的 `.password-field` 定位；截图与 DOM/CSS 分析一致。 |
| 严重等级合理 | 通过 | `medium` 合理；视觉/UX 问题、功能不阻断、非安全漏洞。 |
| 回归验收明确 | 通过 | `acceptance.md` AC-001～AC-010 覆盖三字段有/无 error 时 toggle 居中、功能无回归、DOM 结构、视觉并排验收。 |
| 是否需 hotfix 路径 | 不需要 | 非阻断、非安全；常规 `fix-*` Change，预计改动 DOM 包装层 + CSS。 |

## 3. 批准理由

1. 根因明确：CSS 定位参照容器错误，非 API/后端问题；修复面集中。
2. 修复方案清晰：input + toggle 独立 `position: relative` 包装层，`error-text` 不参与定位。
3. 与 BUG-0024（错误字段映射）、BUG-0026（取消 confirm）同属修改密码弹窗，可合并为单一 fix change。
4. 修复 BUG-0024 后错位仍会出现在「有错误的字段」，本缺陷 MUST 独立验收。

## 4. 修复门禁

| 项目 | 结论 |
|---|---|
| 是否允许 `/bug-opsx` | 是 |
| 是否允许进入 Sprint | 是 |
| 建议 Change ID | `fix-change-password-modal-errors` |
| Change 类型 | `fix-*` |

## 5. 修复范围建议

1. 为 `PasswordField` 增加 `.password-input-wrap`（或等价）包裹 input + `toggle-pass`。
2. 将 `.toggle-pass` 绝对定位规则绑定至 wrap，而非 `.password-field`。
3. `error-text` 置于 wrap 外，确保动态 error 不撑高 toggle 定位参照。
4. 更新/补充 `ChangePasswordModal.test.tsx` DOM 结构或行为断言。
5. MUST NOT 变更 API、密码策略、成功改密登出流程。
6. 可选：同 change 一并修复 BUG-0024、BUG-0026（tasks 分列 scope）。

## 6. 后续动作

1. 执行 `/bug-opsx BUG-0025-change-password-toggle-button-misalignment` 创建 OpenSpec change（或与 BUG-0024 共用 change）。
2. 可纳入 Sprint（`related_requirement: REQ-0014-profile-page`）。
3. 修复完成后 `/opsx-apply` → 按 AC-010 与截图并排视觉验收 → `/opsx-archive`。
