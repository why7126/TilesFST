---
bug_id: BUG-0038-tile-sku-modal-spec-hint-styling
status: captured
created_at: 2026-06-28 16:59:15
updated_at: 2026-06-28 16:59:15
severity_hint: low
environment: local|docker
related_requirement: REQ-0006-tile-sku-management
related_bug:
---

# 现象

Web 管理端 SKU 新增/编辑弹窗中，「瓷砖规格」下拉框下方出现提示文案「历史 SKU 未匹配规格，请手动选择后保存」时，该提示文字**字号偏大**（接近正文/输入框文字，高于辅助说明应有的视觉层级），且**颜色偏亮/偏白**，与 Design System 中表单辅助提示（muted、较小字号）不一致，视觉过于抢眼。

# 复现步骤

1. 以 admin 登录 Web 管理端，进入「瓷砖 SKU」列表页。
2. 打开一条**历史 SKU**（无有效 `spec_id` 或未匹配当前规格列表）的「编辑 SKU」弹窗。
3. 观察「瓷砖规格 *」下拉框下方提示「历史 SKU 未匹配规格，请手动选择后保存」的字号与颜色。

# 期望 vs 实际

| | 说明 |
|---|---|
| **期望** | 辅助提示使用较小字号（如 `text-xs` / `text-muted` 语义 token），颜色为次要文字色（`text-muted` 或 `text-secondary`），与弹窗内其他字段说明、Design System 表单 hint 规范一致。 |
| **实际** | 提示文字字号明显大于标签与常规辅助文案，颜色接近主文字白色，在暗色弹窗中过于突出。 |

# 附件

- screenshots/tile-sku-modal-spec-hint-styling.png
