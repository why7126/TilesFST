---
bug_id: BUG-0048-banner-modal-width-css-cascade-overridden
review_id: REV-BUG-0048-001
status: approved
reviewed_at: 2026-06-28 18:44:30
reviewer: ai-agent
decision: approve
severity: medium
hotfix_required: false
---

# 缺陷评审

## 1. 评审结论

`BUG-0048-banner-modal-width-css-cascade-overridden` 评审通过，状态变更为 `approved`。

**确认：** 本缺陷为 BUG-0040 修复未闭环的 **CSS 层叠回归**；880px 策略已在 BUG-0040 确立，此处仅须使运行时 Computed width 真正生效，**无需**重新 debate 640→880 或重复 OpenSpec 策略 delta。

该缺陷应进入修复流程，后续可执行：

```text
/bug-opsx BUG-0048-banner-modal-width-css-cascade-overridden
```

建议修复 Change：

```text
fix-banner-modal-width-css-cascade
```

（可并入 `fix-banner-list-and-modal-ui` 补修后再 archive。）

## 2. 评审清单

| 检查项 | 结论 | 说明 |
|---|---|---|
| 可复现或根因充分 | 通过 | 100% 稳定复现；`root-cause.md` 已定位双类名 + bundle 层叠，DevTools Computed ≈ 520px 与 SKU 880px 对比清晰。 |
| 严重等级合理 | 通过 | `medium` 合理；不阻断保存，但 BUG-0040 验收意图未达成，属明确回归。 |
| 回归验收明确 | 通过 | `acceptance.md` AC-001～AC-010 覆盖 Computed 880px、层叠规则、SKU 并排、Vitest 层叠断言、BUG-0033 无回归。 |
| 是否需 hotfix 路径 | 不需要 | 非 P0 阻断；纯前端 CSS/类名 + 测试，无 API/DB 变更。 |

## 3. 批准理由

1. 根因明确：`modal-card` 与 `banner-modal-card` 双类名导致 `.admin-shell .modal-card { 520px }` 覆盖 880px。
2. 修复面小：移除冗余 `modal-card`（对齐 SKU `sku-modal-card` 模式）即可闭环。
3. 测试 gap 已在 acceptance AC-007 写清，可防止同类回归。
4. `fix-banner-list-and-modal-ui` 在 BUG-0048 修复前 **SHOULD NOT archive**。

## 4. 修复门禁

| 项目 | 结论 |
|---|---|
| 是否允许 `/bug-opsx` | 是 |
| 是否允许进入 Sprint | 是 |
| 建议 Change ID | `fix-banner-modal-width-css-cascade` |
| Change 类型 | `fix-*` |

## 5. 修复范围建议

1. `BannerFormModal.tsx`：移除 `modal-card`，仅保留 `banner-modal-card`。
2. 可选：`.admin-shell .modal-card.banner-modal-card` 特异性加固。
3. Vitest：import 完整冲突 CSS 栈，断言 Computed / 层叠行为。
4. 回归 BUG-0033 与 BUG-0040 AC；DevTools Computed 880px 为 pass 条件。
5. **不**变更 OpenSpec 640→880 策略（已由 BUG-0040 delta 完成）。

## 6. 后续动作

1. 执行 `/bug-opsx BUG-0048-banner-modal-width-css-cascade-overridden`。
2. `/opsx-apply` → 按 AC-001～AC-003 DevTools 验收 → 与 BUG-0040 一并闭环 `fix-banner-list-and-modal-ui` archive。
