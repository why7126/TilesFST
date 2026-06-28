---
bug_id: BUG-0039-banner-list-display-position-column
review_id: REV-BUG-0039-001
status: approved
reviewed_at: 2026-06-28 17:44:19
reviewer: ai-agent
decision: approve
severity: medium
hotfix_required: false
---

# 缺陷评审

## 1. 评审结论

`BUG-0039-banner-list-display-position-column` 评审通过，状态变更为 `approved`。

该缺陷应进入修复流程，后续可执行：

```text
/bug-opsx BUG-0039-banner-list-display-position-column
```

建议修复 Change：

```text
fix-banner-list-display-position-column
```

（可与 BUG-0040 合并为 `fix-banner-list-and-modal-ui`。）

## 2. 评审清单

| 检查项 | 结论 | 说明 |
|---|---|---|
| 可复现或根因充分 | 通过 | 100% 稳定复现；`root-cause.md` 已定位 `BannerManagementPage.tsx` 第一列 `banner-main` + `banner-sub` 叠放及原型 port 来源；`position` 数据与 `positionLabel()` 已就绪。 |
| 严重等级合理 | 通过 | `medium` 合理；为列表信息架构 / 可读性问题，不阻断 CRUD、筛选、分页。 |
| 回归验收明确 | 通过 | `acceptance.md` AC-001～AC-008 覆盖独立列、colSpan、功能无回归、原型 delta 与 Vitest。 |
| 是否需 hotfix 路径 | 不需要 | 非阻断；纯前端 TSX/CSS，无 API/DB 变更。 |

## 3. 批准理由

1. 用户反馈明确：展示位置应与展示端一样独立成列，提升扫读效率。
2. 修复面小：表头 + 列拆分 + `colSpan` 调整，无需后端。
3. 与 `banner-management-list.png` 第一列差异已在 acceptance AC-008 明确 delta 消化路径（同 BUG-0030 模式）。
4. 可与 BUG-0040 合并同一 Banner UI fix change，降低交付碎片。

## 4. 修复门禁

| 项目 | 结论 |
|---|---|
| 是否允许 `/bug-opsx` | 是 |
| 是否允许进入 Sprint | 是 |
| 建议 Change ID | `fix-banner-list-display-position-column` |
| Change 类型 | `fix-*` |

## 5. 修复范围建议

1. 新增「展示位置」表头与数据列；第一列仅缩略图 + 标题。
2. 加载/空态 `colSpan` 调整为 9。
3. 可选移除 `.banner-sub` 样式（若不再使用）。
4. SHOULD 补充 `BannerManagementPage` Vitest。
5. `/bug-opsx` delta spec MODIFIED 列表列结构（相对 list PNG）。

## 6. 后续动作

1. 执行 `/bug-opsx BUG-0039-banner-list-display-position-column`（建议与 BUG-0040 一并 opsx）。
2. `/opsx-apply` → 按 acceptance 验收 → `/opsx-archive`。
