---
bug_id: BUG-0037-tile-spec-status-confirm-ui-inconsistency
status: captured
created_at: 2026-06-28 16:06:42
updated_at: 2026-06-28 16:06:42
severity_hint: medium
environment: local|docker
related_requirement: REQ-0009-tile-spec-management
related_bug:
---

# 现象

瓷砖规格管理页「启用 / 停用 / 删除」操作的二次确认弹窗，在 UI 结构、标题区交互、描述文案、主按钮文案等方面，与瓷砖类目管理页同类确认弹窗的 UI/UE 设计方案不一致，破坏管理端确认 Dialog 统一性。

已知差异（以停用为例，启用/删除同理）：

- 规格页弹窗使用 `confirm-card` 变体，标题区无关闭（×）按钮；类目页为标准 `modal-card` 且含 `modal-close`。
- 规格页主按钮文案为泛化「确认」；类目页为「确认启用 / 确认停用 / 删除类目」等语义化文案。
- 规格页停用描述仅「确认停用规格「…」？」；类目页停用描述含「停用后前台将不再展示该类目。」补充说明。
- 规格页删除主按钮为「删除」+ `danger` 样式；类目页为「删除类目」且与品牌页一致的主按钮样式。
- 规格页描述区未使用 `page-desc` 样式类，Typography 与类目页不一致。

# 复现步骤

1. 以 admin 登录管理端。
2. 进入「瓷砖规格」列表页，对某启用规格点击「停用」。
3. 观察二次确认弹窗（标题、描述、主/次按钮、关闭按钮、间距等）。
4. 进入「瓷砖类目」列表页，对某启用类目点击「停用」。
5. 观察二次确认弹窗样式与文案结构。
6. 分别在规格页、类目页触发「启用」「删除」确认弹窗，并排对比 UI/UE 是否一致。

# 期望 vs 实际

| | 说明 |
|---|---|
| **期望** | 规格页启用/停用/删除确认弹窗 MUST 与类目页同类弹窗采用一致的 Confirm Dialog 结构、Design System 规范（标题区含关闭、描述 `page-desc`、语义化主按钮文案、停用补充说明）。 |
| **实际** | 规格页确认弹窗视觉与交互形态、文案结构与类目页明显不一致（见截图）。 |

# 附件

- screenshots/tile-spec-disable-confirm-dialog.png
