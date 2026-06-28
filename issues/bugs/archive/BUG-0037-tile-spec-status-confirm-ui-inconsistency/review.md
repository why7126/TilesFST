---
bug_id: BUG-0037-tile-spec-status-confirm-ui-inconsistency
review_id: REV-BUG-0037-001
status: approved
reviewed_at: 2026-06-28 16:16:41
reviewer: ai-agent
decision: approve
severity: medium
hotfix_required: false
---

# 缺陷评审

## 1. 评审结论

`BUG-0037-tile-spec-status-confirm-ui-inconsistency` 评审通过，状态变更为 `approved`。

该缺陷应进入修复流程，后续可执行：

```text
/bug-opsx BUG-0037-tile-spec-status-confirm-ui-inconsistency
```

建议修复 Change：

```text
fix-tile-spec-status-confirm-ui
```

## 2. 评审清单

| 检查项 | 结论 | 说明 |
|---|---|---|
| 可复现或根因充分 | 通过 | 100% 稳定复现；`root-cause.md` 已定位简化 confirm 内联模板、无效 `confirm-card`、与类目/品牌页 DOM/文案差异；源码对比一致。 |
| 严重等级合理 | 通过 | `medium` 合理；confirm UI/UE 不一致不阻断启停/删除功能，但 REQ-0009 AC-013/AC-018 未满足。 |
| 回归验收明确 | 通过 | `acceptance.md` AC-001～AC-011 覆盖启停/删除 confirm 结构、文案、取消无副作用、Vitest 门禁、REQ-0009 对齐及非回归项。 |
| 是否需 hotfix 路径 | 不需要 | 非阻断、非安全、非数据问题；常规 `fix-*` Change，参照 BUG-0017 修复模式即可。 |

## 3. 批准理由

1. 根因与 BUG-0017 同构：新页 confirm 未对齐已交付 DS modal Golden Reference（类目/品牌页），修复路径清晰。
2. 修复面集中：`TileSpecManagementPage.tsx` 启停/删除 confirm JSX + Vitest，无 API/DB 变更。
3. REQ-0009 AC-013/AC-018 实现缺口明确，修复后可补齐 confirm 对齐验收。
4. workaround 已说明功能可继续运营，但不消除管理端 Confirm Dialog 一致性债务。

## 4. 修复门禁

| 项目 | 结论 |
|---|---|
| 是否允许 `/bug-opsx` | 是 |
| 是否允许进入 Sprint | 是 |
| 建议 Change ID | `fix-tile-spec-status-confirm-ui` |
| Change 类型 | `fix-*` |

## 5. 修复范围建议

1. 启停/删除 confirm markup 对齐 `TileCategoryManagementPage`（含 `modal-close`、`page-desc`、语义化主按钮）。
2. 停用正文补「停用后前台将不再展示该规格。」；删除主按钮改为「删除规格」，移除 `danger` class。
3. 移除无效 `confirm-card` class；补 `aria-labelledby`。
4. 补充 `TileSpecManagementPage.test.tsx` 停用 confirm 门禁用例（参照类目页测试）。
5. MUST NOT 回改已 archived `fix-tile-spec-admin-ui`；MUST NOT 变更 API、schema 或启停/删除业务逻辑。

## 6. 后续动作

1. 执行 `/bug-opsx BUG-0037-tile-spec-status-confirm-ui-inconsistency` 创建 OpenSpec change。
2. 可与 BUG-0027/28/29 同 Sprint 编排，fix change 职责 MUST 独立。
3. 修复完成后 `/opsx-apply` → 按 AC-001/AC-005 与类目页并排验收 → `/opsx-archive`。
