---
bug_id: BUG-0040-banner-modal-width-too-narrow
review_id: REV-BUG-0040-001
status: approved
reviewed_at: 2026-06-28 17:44:19
reviewer: ai-agent
decision: approve
severity: medium
hotfix_required: false
---

# 缺陷评审

## 1. 评审结论

`BUG-0040-banner-modal-width-too-narrow` 评审通过，状态变更为 `approved`。

**产品决策确认：** 接受 Banner 弹窗由 640px 调整为 **880px**（与瓷砖 SKU 弹窗一致），偏离 REQ-0016 modal HTML/PNG（640px）及现行 `web-client` spec；须在 `/bug-opsx` 以 MODIFIED delta 更新规范。

该缺陷应进入修复流程，后续可执行：

```text
/bug-opsx BUG-0040-banner-modal-width-too-narrow
```

建议修复 Change：

```text
fix-banner-modal-width
```

（可与 BUG-0039 合并为 `fix-banner-list-and-modal-ui`。）

## 2. 评审清单

| 检查项 | 结论 | 说明 |
|---|---|---|
| 可复现或根因充分 | 通过 | 100% 稳定复现；`root-cause.md` 已对比 `.banner-modal-card` 640px vs `.sku-modal-card` 880px，并说明与 spec/原型的冲突及 delta 路径。 |
| 严重等级合理 | 通过 | `medium` 合理；不阻断保存（BUG-0033 已修滚动），主要为横向空间与跨页弹窗一致性。 |
| 回归验收明确 | 通过 | `acceptance.md` AC-001～AC-010 覆盖 880px、SKU 并排、BUG-0033 无回归、OpenSpec delta、验收基准切换。 |
| 是否需 hotfix 路径 | 不需要 | 非阻断；主要为 CSS + spec delta，无 API/DB 变更。 |

## 3. 批准理由

1. 管理端「复杂表单」弹窗应对齐 SKU 880px 档位，运营体验一致。
2. 实现成本低：`.banner-modal-card { width: 880px }` 及可选 head/footer 对齐。
3. BUG-0033 回归要求在 acceptance AC-003 已明确。
4. 640px → 880px 的 spec 变更路径在 root-cause 与 AC-009 已写清，评审确认采纳。

## 4. 修复门禁

| 项目 | 结论 |
|---|---|
| 是否允许 `/bug-opsx` | 是 |
| 是否允许进入 Sprint | 是 |
| 建议 Change ID | `fix-banner-modal-width` |
| Change 类型 | `fix-*` |

## 5. 修复范围建议

1. `.banner-modal-card` 宽度改为 880px，保留 `max-width: 100%`。
2. 可选对齐 `.sku-modal-card` 边框、阴影、head padding。
3. 回归 BUG-0033：modal-body 滚动、textarea 整行、footer 可达。
4. `/bug-opsx` **MUST** MODIFIED `web-client` Banner 弹窗宽度（640 → 880）。
5. 验收以 SKU 弹窗并排为准，不以 640px modal PNG 为 pass 条件。

## 6. 后续动作

1. 执行 `/bug-opsx BUG-0040-banner-modal-width-too-narrow`（建议与 BUG-0039 合并 change）。
2. `/opsx-apply` → 按 AC-001～AC-003 与 SKU 弹窗并排验收 → `/opsx-archive`。
