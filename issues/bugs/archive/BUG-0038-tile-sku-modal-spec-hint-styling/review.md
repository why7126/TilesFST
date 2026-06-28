---
bug_id: BUG-0038-tile-sku-modal-spec-hint-styling
review_id: REV-BUG-0038-001
status: approved
reviewed_at: 2026-06-28 17:08:07
reviewer: ai-agent
decision: approve
severity: low
hotfix_required: false
---

# 缺陷评审

## 1. 评审结论

`BUG-0038-tile-sku-modal-spec-hint-styling` 评审通过，状态变更为 `approved`。

该缺陷应进入修复流程，后续可执行：

```text
/bug-opsx BUG-0038-tile-sku-modal-spec-hint-styling
```

建议修复 Change：

```text
fix-tile-sku-modal-spec-hint-styling
```

## 2. 评审清单

| 检查项 | 结论 | 说明 |
|---|---|---|
| 可复现或根因充分 | 通过 | 编辑 `spec_id` 为 NULL 的 SKU 可稳定复现；`root-cause.md` 已确认 `form-hint` 无 CSS 定义，全项目仅一处引用，与 `form-help` 对比清晰。 |
| 严重等级合理 | 通过 | `low` 合理；纯视觉层级问题，提示语义正确，不阻断保存/上架。 |
| 回归验收明确 | 通过 | `acceptance.md` AC-001～AC-006 覆盖类名、Typography、显隐逻辑、非触发场景、同弹窗回归与 Vitest。 |
| 是否需 hotfix 路径 | 不需要 | 非阻断、非安全、非数据问题；单行类名修复，常规 `fix-*` Change 即可。 |

## 3. 批准理由

1. 根因与 BUG-0010 同构：CSS Port 误用未定义类名，应复用既有 `form-help` 共享样式。
2. 修复面极小：`TileSkuFormModal.tsx` 单行 `form-hint` → `form-help`，无 API/DB 变更。
3. 行为已满足 `web-client/spec.md` SKU 无 `spec_id` 提示 Scenario，修复仅补齐 Design System 视觉层级。
4. `TileSkuManagementPage` 已 import `user-management.css`，无需新增 CSS 文件。

## 4. 修复门禁

| 项目 | 结论 |
|---|---|
| 是否允许 `/bug-opsx` | 是 |
| 是否允许进入 Sprint | 是 |
| 建议 Change ID | `fix-tile-sku-modal-spec-hint-styling` |
| Change 类型 | `fix-*` |

## 5. 修复范围建议

1. `TileSkuFormModal.tsx`：提示元素改用 `form-help`。
2. `TileSkuFormModal.test.tsx`：补充 `spec_id: null` 编辑模式断言。
3. MUST NOT 新增 `.form-hint` CSS 或裸 Hex。
4. MUST NOT 变更提示文案或显隐条件逻辑。

## 6. 后续动作

1. 执行 `/bug-opsx BUG-0038-tile-sku-modal-spec-hint-styling` 创建 OpenSpec change。
2. 修复完成后 `/opsx-apply` → 按 AC-001/AC-002 与截图并排验收 → `/opsx-archive`。
