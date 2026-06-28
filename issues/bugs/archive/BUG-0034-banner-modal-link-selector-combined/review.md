---
bug_id: BUG-0034-banner-modal-link-selector-combined
review_id: REV-BUG-0034-001
status: approved
reviewed_at: 2026-06-28 16:18:39
reviewer: ai-agent
decision: approve
severity: medium
hotfix_required: false
---

# 缺陷评审

## 1. 评审结论

`BUG-0034-banner-modal-link-selector-combined` 评审通过，状态变更为 `approved`。

该缺陷应进入修复流程，后续可执行：

```text
/bug-opsx BUG-0034-banner-modal-link-selector-combined
```

建议修复 Change：

```text
fix-banner-modal-ui
```

（可与 BUG-0030–0036 合并为单一 fix change。）

## 2. 评审清单

| 检查项 | 结论 | 说明 |
|---|---|---|
| 可复现或根因充分 | 通过 | 100% 稳定复现；`root-cause.md` 已定位 `BannerFormModal.tsx` 中 `input` + `<select>` 双控件、`Enter` 触发搜索与编辑回显缺失；与代码及 prototype 对比一致。 |
| 严重等级合理 | 通过 | `medium` 合理；为 UX / 原型 fidelity 问题，不阻断 Banner 保存与 keyword API。 |
| 回归验收明确 | 通过 | `acceptance.md` AC-001～AC-012 覆盖单控件、debounce 搜索、编辑回显、SKU 主图联动、纯前端范围、原型并排与 Vitest。 |
| 是否需 hotfix 路径 | 不需要 | 非阻断、非安全、非数据问题；常规 `fix-*` Change，双步操作仍可完成配置。 |

## 3. 批准理由

1. 根因清晰：`add-banner-management` 以双控件近似「可搜索」需求，未对齐 REQ-0016 原型单 `<select>` 形态与 AC-031 / AC-036 UX 语义。
2. 修复面集中：`BannerFormModal.tsx` 关联 SKU / 专题分支；MAY 新增 `shared/ui` SearchableSelect，无 API / DB 变更。
3. 编辑模式已选目标无法回显为附加风险，acceptance AC-005 已明确修复要求。
4. workaround 已说明「先搜 Enter → 再选下拉」临时路径，但不消除 UX 债务。

## 4. 修复门禁

| 项目 | 结论 |
|---|---|
| 是否允许 `/bug-opsx` | 是 |
| 是否允许进入 Sprint | 是 |
| 建议 Change ID | `fix-banner-modal-ui` |
| Change 类型 | `fix-*` |

## 5. 修复范围建议

1. 用单一 SearchableSelect / Combobox 替换 SKU / 专题双控件（移除独立搜索 `input`）。
2. 输入 debounce 调用 `fetchTileSkus({ keyword })` / `fetchTopics({ keyword })`，选中后在同一控件展示 label。
3. 编辑模式 preload 已选 `sku_id` / `topic_id`，确保不在默认前 20 条时仍能回显。
4. 保持 `handleSkuChange` 主图联动行为不变（AC-006）。
5. SHOULD 补充 `BannerFormModal.test.tsx` 单控件与无独立搜索 input 断言。
6. Change `trace.md` 记录与 `banner-management-modal-{sku-detail|topic-page}.png` 并排验收。

## 6. 后续动作

1. 执行 `/bug-opsx BUG-0034-banner-modal-link-selector-combined`（建议与 BUG-0030–0036 一并 opsx 合并 change）。
2. 修复完成后 `/opsx-apply` → 按 AC-001/AC-003/AC-010 并排验收 → `/opsx-archive`。
