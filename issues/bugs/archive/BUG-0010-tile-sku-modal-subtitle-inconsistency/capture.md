---
bug_id: BUG-0010-tile-sku-modal-subtitle-inconsistency
status: captured
recorded_at: 2026-06-27 08:56:54
severity_hint: medium
environment: local|docker
related_requirement: REQ-0006-tile-sku-management
related_change: null
---

# 现象

瓷砖 SKU 新增/编辑弹窗的副标题（Dialog Description）样式与「新增品牌」弹窗副标题不一致，未遵循管理端弹窗统一视觉规范，与整体 Design System 不符。

# 复现步骤

1. 以 admin 登录管理端。
2. 进入「瓷砖SKU」列表页，点击「新增SKU」或某行「编辑」，打开 SKU 弹窗。
3. 观察弹窗标题下方的副标题文字样式（字号、颜色、行高、间距等）。
4. 进入「瓷砖品牌」列表页，点击「添加品牌」，打开品牌新增弹窗。
5. 对比两弹窗副标题区域的 Typography 与间距是否一致。
6. 对照 `rules/ui-design.md` 与管理端 Design System 弹窗规范。

# 期望 vs 实际

| | 说明 |
|---|---|
| **期望** | SKU 弹窗副标题应使用与品牌新增弹窗相同的 semantic token（如 `text-muted`、`text-secondary`）、字号与上下间距，保持管理端弹窗标题区视觉一致。 |
| **实际** | SKU 弹窗副标题样式与品牌弹窗副标题明显不一致，破坏弹窗组件统一性。 |

# 影响范围

- Web 管理端：瓷砖 SKU 新增/编辑弹窗。
- 关联需求：REQ-0006-tile-sku-management。
- 参考实现：品牌管理新增弹窗（BUG-0002 相关修复后样式）。

# 初步分类（待 /bug-generate 确认）

| 判断 | 结论 |
|---|---|
| 缺陷类型 | UI 视觉一致性缺陷 |
| 严重程度建议 | medium |
| 可能修复面 | SKU 弹窗 DialogHeader / Description 样式对齐品牌弹窗 |
| 设计约束 | 对齐 `rules/ui-design.md`、Design System 弹窗组件、品牌管理弹窗既有实现 |

# 附件

- 暂无截图。
- 参考原型：`issues/requirements/archive/REQ-0006-tile-sku-management/prototype/web/tile-sku-create-modal.html`
- 参考页面：品牌管理添加品牌弹窗
