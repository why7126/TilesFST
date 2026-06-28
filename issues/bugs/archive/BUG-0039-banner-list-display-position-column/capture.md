---
bug_id: BUG-0039-banner-list-display-position-column
status: captured
created_at: 2026-06-28 17:28:15
updated_at: 2026-06-28 17:28:15
severity_hint: medium
environment: local|docker
related_requirement: REQ-0016-banner-management
related_bug:
---

# 现象

Web 管理端「Banner 管理」列表页第一列将 **Banner 标题** 与 **展示位置** 挤在同一列中显示，信息混杂、可读性差。

# 复现步骤

1. 以 admin 登录 Web 管理端，进入「Banner 管理」列表页（侧栏 OPERATIONS → Banner 管理）。
2. 观察表格第一列单元格内容。
3. 对比其他管理列表（如用户管理、瓷砖 SKU）的列结构与信息密度。

# 期望 vs 实际

| | 说明 |
|---|---|
| **期望** | 第一列仅显示 Banner 标题；**展示位置** 单独占一列，表头与单元格文案清晰可辨。 |
| **实际** | 第一列同时展示 Banner 标题与展示位置，两项信息挤在一起，不利于扫读与对齐。 |

# 附件

- screenshots/（待补充）
- logs/
