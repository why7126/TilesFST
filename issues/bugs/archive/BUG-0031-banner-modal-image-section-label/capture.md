---
bug_id: BUG-0031-banner-modal-image-section-label
status: captured
created_at: 2026-06-28 16:04:18
updated_at: 2026-06-28 16:04:18
severity_hint: low
environment: local|docker
related_requirement: REQ-0016-banner-management
related_bug: BUG-0032-banner-modal-upload-button-label
---

# 现象

Banner 新增/编辑弹窗中，「Banner 图片」模块首行存在「自定义上传 / SKU 主图」类说明文案，与原型及同类弹窗（如品牌 Logo 上传区）不一致，该首行文案不需要展示。

# 复现步骤

1. 以 admin 登录 Web 管理端，进入「Banner 管理」列表页。
2. 点击「+ 新增 Banner」或某行「编辑」打开弹窗。
3. 观察「Banner 图片」模块首行是否显示「自定义上传 / SKU 主图」文案。

# 期望 vs 实际

| | 说明 |
|---|---|
| **期望** | Banner 图片模块无该首行说明文案，直接展示上传/选择控件与「使用 SKU 主图」等操作。 |
| **实际** | 模块首行仍显示「自定义上传 / SKU 主图」文案。 |

# 附件

- （弹窗截图待补充）
