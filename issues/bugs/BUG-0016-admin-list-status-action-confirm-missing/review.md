---
bug_id: BUG-0016-admin-list-status-action-confirm-missing
review_id: REV-BUG-0016-001
status: approved
reviewed_at: 2026-06-27 13:15:21
reviewer: ai-agent
decision: approve
severity: medium
hotfix_required: false
---

# 缺陷评审

## 1. 评审结论

`BUG-0016-admin-list-status-action-confirm-missing` 评审通过，状态变更为 `approved`。

该缺陷应进入修复流程，后续可执行：

```text
/bug-opsx BUG-0016-admin-list-status-action-confirm-missing
```

建议修复 Change：

```text
fix-admin-list-status-action-confirm
```

## 2. 评审清单

| 检查项 | 结论 | 说明 |
|---|---|---|
| 可复现或根因充分 | 通过 | 用户冻结/解冻、SKU 上下架/恢复可 100% 稳定复现（点击即 API）；`root-cause.md` 已定位 handler 直调与 `window.confirm` 混用；vitest 固化无确认行为。品牌启停已证伪出 scope，文档已收窄。 |
| 严重等级合理 | 通过 | 存在误触冻结/上下架风险，但操作可逆、无数据损坏；与 REQ-0008 交互缺口同类，`medium` 合理。 |
| 回归验收明确 | 通过 | `acceptance.md` AC-001～AC-015 覆盖用户 freeze/unfreeze/delete modal、SKU publish/unpublish confirm、Golden Reference 对齐、品牌/类目不回归、Vitest 门禁、BUG-0017 边界。 |
| 是否需 hotfix 路径 | 不需要 | 纯前端交互；workaround 为操作习惯规避；走常规 `fix-*` Change 即可。 |

## 3. 批准理由

1. 缺陷包完整：capture → bug → root-cause → workaround → acceptance 齐全；`/bug-explore` 已修正 capture 中品牌范围过时问题。
2. 根因清晰：按页专项交付（REQ-0007/0008）未横向推广至用户/SKU；有 `BrandManagementPage` / `TileCategoryManagementPage` 可复用 modal 模式。
3. 修复成本低：默认纯前端 state + modal JSX；无需 API、DB、Orval 变更。
4. 与 BUG-0015（toast 布局）、BUG-0017（重置密码 confirm UI）职责独立，可同 Sprint 编排但不阻塞本 fix 独立交付。

## 4. 后续要求

1. `/bug-opsx` 创建 `fix-admin-list-status-action-confirm`，delta 扩展 `web-client` 用户冻结/解冻与 SKU 上下架确认 requirement（参考已归档品牌/类目条目）。
2. `UserManagementPage`：冻结/解冻 + 删除 modal 化（移除 `window.confirm`）；`TileSkuManagementPage`：上下架/恢复 confirm。
3. 更新 vitest：确认前 mock MUST NOT 调用；取消后不调用；确认后调用。
4. 修复时 MUST NOT 回归品牌/类目/SKU 删除既有 confirm 及 `BrandManagementPage.test.tsx` 启停用例。
5. 重置密码 confirm UI 统一 **不纳入** 本 change（→ BUG-0017）。
