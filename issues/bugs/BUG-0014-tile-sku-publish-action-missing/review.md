---
bug_id: BUG-0014-tile-sku-publish-action-missing
review_id: REV-BUG-0014-001
status: approved
reviewed_at: 2026-06-27 12:19:51
reviewer: ai-agent
decision: approve
severity: high
hotfix_required: false
---

# 缺陷评审

## 1. 评审结论

`BUG-0014-tile-sku-publish-action-missing` 评审通过，状态变更为 `approved`。

该缺陷应进入修复流程，后续可执行：

```text
/bug-opsx BUG-0014-tile-sku-publish-action-missing
```

建议修复 Change：

```text
fix-tile-sku-publish-action-missing
```

## 2. 评审清单

| 检查项 | 结论 | 说明 |
|---|---|---|
| 可复现或根因充分 | 通过 | `bug.md` 给出稳定复现路径（下架后观察操作列）；`root-cause.md` 已定位 `TileSkuManagementPage.tsx` L349–365 对 `DISABLED` 显式渲染 `null`，后端 publish API 可用。 |
| 严重等级合理 | 通过 | 下架后无法从 UI 恢复上架，阻断 SKU 上下架运营闭环；与 REQ-0006 FR-007 直接冲突，`high` 合理。 |
| 回归验收明确 | 通过 | `acceptance.md` AC-001～AC-011 覆盖 DISABLED/PUBLISHED/DRAFT 各状态操作列、Toast/错误、Vitest、冒烟及 OpenSpec 流程。 |
| 是否需 hotfix 路径 | 不需要 | 影响管理端核心流程但可通过 API 临时规避；本地/Docker 环境，走常规 `fix-*` Change 即可。 |

## 3. 批准理由

1. 实现缺口明确：非 `PUBLISHED` 分支错误排除 `DISABLED`，与 REQ-0006 AC-018、AC-037 及 `business-flow.md` §6 矛盾。
2. 与 BUG-0001 同类对称问题，已有 `fix-tile-category-enable-action` 可参考，修复面集中（前端条件渲染 + 单测）。
3. 后端 `publish_sku` 已就绪，无需 API/DB/Orval 变更。
4. workaround 仅 API 应急，正常运营路径不可用，应优先修复。

## 4. 后续要求

1. `/bug-opsx` 创建 `fix-tile-sku-publish-action-missing`，对齐 REQ-0006 AC-018、AC-037 与 BUG acceptance。
2. `DISABLED` 行文案优先「恢复」，其余非上架态保持「上架」；publish 与 delete 独立渲染（参照 BUG-0001 修复后类目页）。
3. 补充 `TileSkuManagementPage` Vitest：mock `DISABLED` 行 MUST 含恢复/上架按钮。
4. 建议纳入当前 Sprint（与 REQ-0006 / `add-tile-sku-management` 同批），优先级高于 medium 级 UI 一致性缺陷。
