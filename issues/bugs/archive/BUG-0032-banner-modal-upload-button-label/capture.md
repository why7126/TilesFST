---
bug_id: BUG-0032-banner-modal-upload-button-label
status: captured
created_at: 2026-06-28 16:04:18
updated_at: 2026-06-28 16:04:18
severity_hint: low
environment: local|docker
related_requirement: REQ-0016-banner-management
related_bug: BUG-0031-banner-modal-image-section-label
---

# 现象

Banner 新增/编辑弹窗「Banner 图片」模块中，自定义上传按钮当前文案为「自定义上传 浏览…」，与管理端其他上传控件（如品牌 Logo「选择」/「更换」）不一致。

# 复现步骤

1. 以 admin 登录 Web 管理端，进入「Banner 管理」列表页。
2. 点击「+ 新增 Banner」打开弹窗。
3. 在「Banner 图片」模块观察自定义上传按钮文案。

# 期望 vs 实际

| | 说明 |
|---|---|
| **期望** | 未选图时按钮文案为「选择」；已有图片时文案为「更换」。 |
| **实际** | 按钮显示「自定义上传 浏览…」。 |

# 附件

- （弹窗截图待补充）
