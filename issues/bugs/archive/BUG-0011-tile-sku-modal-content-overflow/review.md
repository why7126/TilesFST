---
bug_id: BUG-0011-tile-sku-modal-content-overflow
review_id: REV-BUG-0011-001
status: approved
reviewed_at: 2026-06-27 09:23:13
reviewer: ai-agent
decision: approve
severity: high
hotfix_required: false
---

# 缺陷评审

## 1. 评审结论

`BUG-0011-tile-sku-modal-content-overflow` 评审通过，状态变更为 `approved`。

该缺陷应进入修复流程，后续可执行：

```text
/bug-opsx BUG-0011-tile-sku-modal-content-overflow
```

建议修复 Change：

```text
fix-tile-sku-modal-content-overflow
```

## 2. 评审清单

| 检查项 | 结论 | 说明 |
|---|---|---|
| 可复现或根因充分 | 通过 | `bug.md` 给出明确复现路径；`root-cause.md` 已定位 `.sku-modal-card` flex 布局缺少可滚动 `.modal-body`，并关联 REQ-0006 AC-022。 |
| 严重等级合理 | 通过 | 矮视口下无法完成 SKU 创建/编辑，阻塞核心主数据维护，`high` 合理；高于 BUG-0009/0010 等 UI 一致性 medium 缺陷。 |
| 回归验收明确 | 通过 | `acceptance.md` AC-001～AC-008 覆盖滚动、头尾固定、全字段可达、矮视口矩阵、纯前端范围与 AC-022 对齐。 |
| 是否需 hotfix 路径 | 不需要 | 影响管理端 SKU 弹窗可用性，但未达生产 blocker；可通过常规 `fix-*` Change 在 Sprint 内修复，无需独立 hotfix 分支。 |

## 3. 批准理由

1. 实现缺口明确：已有 `max-height` 约束但主体不可滚动，与 REQ-0006 AC-022 直接冲突。
2. 无可靠 workaround，产品验收与运营使用均受阻。
3. 修复面集中（CSS 布局 + 可选组件测试），不涉及 API/DB 变更。
4. 与 `REQ-0006-tile-sku-management` / `add-tile-sku-management` 强关联，适合作为独立 `fix-*` Change 修复。

## 4. 后续要求

1. `/bug-opsx` 创建 `fix-tile-sku-modal-content-overflow`，delta spec 引用 AC-022 与 BUG acceptance。
2. 修复 MUST 保持 `.modal-head` / `.modal-footer` 固定，仅 `.modal-body` 滚动。
3. 在 1280×720、1440×900 等矮视口完成手工验收后再 `/opsx-archive`。
4. 建议与 BUG-0009/0010/0012 一并纳入 Sprint，但 BUG-0011 优先级最高。
