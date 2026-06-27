---
bug_id: BUG-0009-tile-sku-list-ui-inconsistency
review_id: REV-BUG-0009-001
status: approved
reviewed_at: 2026-06-27 10:20:38
reviewer: ai-agent
decision: approve
severity: medium
hotfix_required: false
---

# 缺陷评审

## 1. 评审结论

`BUG-0009-tile-sku-list-ui-inconsistency` 评审通过，状态变更为 `approved`。

该缺陷应进入修复流程，后续可执行：

```text
/bug-opsx BUG-0009-tile-sku-list-ui-inconsistency
```

建议修复 Change：

```text
fix-tile-sku-list-ui-inconsistency
```

## 2. 评审清单

| 检查项 | 结论 | 说明 |
|---|---|---|
| 可复现或根因充分 | 通过 | `bug.md` 给出明确复现路径；`root-cause.md` 已定位 `TileSkuManagementPage.tsx` 分页 DOM（`page-left` / `brand-pagination-right`）及 `table-head` 多余标题行，并关联用户管理页参考实现与 BUG-0002 同类修复。 |
| 严重等级合理 | 通过 | `medium` 合理；分页与布局不一致可见但不阻断 SKU 查询、分页、CRUD；不影响 API/DB/权限。 |
| 回归验收明确 | 通过 | `acceptance.md` AC-001～AC-009 覆盖分页结构对齐、移除 table-head、功能不回退、原型并排、DS 约束与 REQ-0006 AC-051 对齐。 |
| 是否需 hotfix 路径 | 不需要 | 非阻断、非安全、非数据损坏问题；可通过常规 `fix-*` Change 在 Sprint 内修复。 |

## 3. 批准理由

1. 与 BUG-0002 同类 UI 一致性缺陷，品牌页已修复但 SKU 页未同步对齐，根因与修复路径清晰。
2. 实现缺口明确：复用废弃 brand 分页结构 + 卡片内臆造标题行，偏离 REQ-0006 原型 context 与 AC-051。
3. 修复面集中（`TileSkuManagementPage.tsx` DOM 调整 + Vitest），不涉及 API/DB 变更。
4. 有可靠 workaround（功能可用），但 AC-051 / AC-054 验收暂不过，需正式修复。

## 4. 修复门禁

| 项目 | 结论 |
|---|---|
| 是否允许 `/bug-opsx` | 是 |
| 是否允许进入 Sprint | 是 |
| 建议 Change ID | `fix-tile-sku-list-ui-inconsistency` |
| Change 类型 | `fix-*` |

## 5. 修复范围建议

1. 分页 DOM 对齐 `UserManagementPage.tsx`（`page-summary` + `page-right` + `page-buttons` + `page-size-wrap`）。
2. 移除 `table-card` 内 `table-head` / `table-title` / `table-note` 区块。
3. 保持 SKU 筛选、分页、CRUD 功能不回退。
4. 参考 `BrandManagementPage.test.tsx` 补充分页 DOM 结构测试。

## 6. 后续动作

1. 执行 `/bug-opsx BUG-0009-tile-sku-list-ui-inconsistency` 创建 `fix-tile-sku-list-ui-inconsistency`。
2. 建议与 BUG-0010、BUG-0012 等同批纳入 Sprint（优先级低于已修复的 BUG-0011）。
3. 修复完成后与用户管理页分页并排验收，再 `/opsx-archive`。
