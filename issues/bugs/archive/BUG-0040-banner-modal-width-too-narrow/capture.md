---
bug_id: BUG-0040-banner-modal-width-too-narrow
status: captured
created_at: 2026-06-28 17:28:15
updated_at: 2026-06-28 17:28:15
severity_hint: medium
environment: local|docker
related_requirement: REQ-0016-banner-management
related_bug:
---

# 现象

Web 管理端「Banner 管理」新增/编辑弹窗整体宽度偏小，表单与媒体区域显得拥挤；应与瓷砖 SKU 弹窗宽度对齐以保持一致的管理端弹窗体验。

# 复现步骤

1. 以 admin 登录 Web 管理端，进入「Banner 管理」列表页。
2. 点击「新增 Banner」或某行「编辑」，打开 Banner 弹窗。
3. 对比「瓷砖 SKU 管理」新增/编辑弹窗的宽度与内容区留白。

# 期望 vs 实际

| | 说明 |
|---|---|
| **期望** | Banner 弹窗宽度与 SKU 弹窗一致（或采用同一 `Dialog`/`AdminEdit` 宽度 token），表单字段与图片区有足够横向空间。 |
| **实际** | Banner 弹窗明显窄于 SKU 弹窗，内容拥挤，与同类管理弹窗不一致。 |

# 附件

- screenshots/（待补充）
- logs/
