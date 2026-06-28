---
bug_id: BUG-0036-banner-modal-datetime-picker
status: captured
created_at: 2026-06-28 16:04:18
updated_at: 2026-06-28 16:04:18
severity_hint: medium
environment: local|docker
related_requirement: REQ-0016-banner-management
related_bug:
---

# 现象

Banner 新增/编辑弹窗「有效期开始」「有效期结束」字段要求格式 `yyyy/mm/dd hh:mm:ss`，但当前日期选择器无法选择时、分、秒，仅能选日期或交互不完整，无法满足精确生效时间配置。

# 复现步骤

1. 以 admin 登录 Web 管理端，进入「Banner 管理」，打开新增/编辑弹窗。
2. 点击「有效期开始」或「有效期结束」日期控件。
3. 尝试选择具体的小时、分钟、秒。

# 期望 vs 实际

| | 说明 |
|---|---|
| **期望** | 使用可同时选择年-月-日 时-分-秒的 DateTime 组件；展示/提交格式为 `yyyy/mm/dd hh:mm:ss`。 |
| **实际** | 现有日期选择器无法选择时分秒，或格式与需求不符。 |

# 附件

- （弹窗截图待补充）
