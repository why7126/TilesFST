---
bug_id: BUG-0034-banner-modal-link-selector-combined
status: captured
created_at: 2026-06-28 16:04:18
updated_at: 2026-06-28 16:04:18
severity_hint: medium
environment: local|docker
related_requirement: REQ-0016-banner-management
related_bug:
---

# 现象

Banner 新增/编辑弹窗中，跳转类型为「关联专题」或「关联 SKU」时，搜索框与目标选择下拉框被拆成两个独立控件，交互不合理；期望合并为单一可搜索选择组件（Combobox / Select with search）。

# 复现步骤

1. 以 admin 登录 Web 管理端，进入「Banner 管理」，打开新增/编辑弹窗。
2. 将「跳转类型」设为「关联专题」或「关联 SKU」。
3. 观察关联目标选择区域：是否存在独立的搜索输入框与独立的下拉选择框。

# 期望 vs 实际

| | 说明 |
|---|---|
| **期望** | 搜索与选择在同一控件内完成（输入关键词即筛选并选择目标专题/SKU）。 |
| **实际** | 搜索框与下拉框分离为两个框，操作割裂。 |

# 附件

- （弹窗截图待补充）
