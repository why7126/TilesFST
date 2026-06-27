---
bug_id: BUG-0015-admin-list-status-tips-layout-shift
review_id: REV-BUG-0015-001
status: approved
reviewed_at: 2026-06-27 12:47:06
reviewer: ai-agent
decision: approve
severity: medium
hotfix_required: false
---

# 缺陷评审

## 1. 评审结论

`BUG-0015-admin-list-status-tips-layout-shift` 评审通过，状态变更为 `approved`。

该缺陷应进入修复流程，后续可执行：

```text
/bug-opsx BUG-0015-admin-list-status-tips-layout-shift
```

建议修复 Change：

```text
fix-admin-list-status-toast-layout
```

## 2. 评审清单

| 检查项 | 结论 | 说明 |
|---|---|---|
| 可复现或根因充分 | 通过 | 用户/类目/SKU 三页可稳定复现文档流 Tips 推挤；`root-cause.md` 已定位 `.admin-notice` + 3.2s 定时清除机制；品牌页已有 fixed toast 先例，纳入统一改造与回归。 |
| 严重等级合理 | 通过 | 影响四页连续操作体验，不阻断 API/数据写入；与 BUG-0003 Tips 子问题同类，`medium` 合理。 |
| 回归验收明确 | 通过 | `acceptance.md` AC-001～AC-014 覆盖四页 fixed toast、布局稳定性、视觉一致、品牌不回归、共享样式、Vitest、冒烟及 OpenSpec 流程。 |
| 是否需 hotfix 路径 | 不需要 | 纯前端布局模式问题；workaround 为操作习惯规避；走常规 `fix-*` Change 即可。 |

## 3. 批准理由

1. 缺陷包完整：capture → bug → root-cause → workaround → acceptance 齐全，修复面与范围（品牌/用户/类目/SKU 四页）已由用户确认。
2. 根因清晰：自动消失反馈误用文档流 `.admin-notice`；BUG-0003 品牌 toast 修复未推广至其他列表页，有 archived change 可参考。
3. 修复成本低：默认纯前端 CSS/DOM + 可选共享 `AdminToast`；无需 API、DB、Orval 变更。
4. 与 BUG-0016/BUG-0017 职责独立，可同 Sprint 编排但不阻塞本 fix 独立交付。

## 4. 后续要求

1. `/bug-opsx` 创建 `fix-admin-list-status-toast-layout`，对齐 `acceptance.md` AC-001～AC-010 与 BUG-0003 AC-004/AC-005 四页扩展。
2. 将 `.admin-toast-region` / `.admin-toast` 提升至管理端共享样式；用户/类目/SKU 三页对齐品牌页结构。
3. 保留 `BrandManagementPage.test.tsx` 现有 toast 断言；为用户/类目/SKU 各补至少 1 条 Vitest。
4. 修复时 MUST NOT 回归品牌 Logo 展示、上传进度及 BUG-0003 已归档能力。
5. 建议纳入 Sprint 正式范围（与 BUG-0016 等同批 UI 交互改进可选）。
