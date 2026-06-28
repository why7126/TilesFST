---
bug_id: BUG-0035-banner-modal-sku-hero-image-no-effect
status: captured
created_at: 2026-06-28 16:04:18
updated_at: 2026-06-28 16:04:18
severity_hint: high
environment: local|docker
related_requirement: REQ-0016-banner-management
related_bug: BUG-0032-banner-modal-upload-button-label
---

# 现象

Banner 新增/编辑弹窗「Banner 图片」模块中，点击「使用 SKU 主图」按钮无任何可见效果：未回填 SKU 主图预览、未更新表单字段、无 loading 或错误提示。

# 复现步骤

1. 以 admin 登录 Web 管理端，进入「Banner 管理」，打开新增/编辑弹窗。
2. 将跳转类型设为「关联 SKU」并选择有效 SKU（或编辑已关联 SKU 的 Banner）。
3. 在「Banner 图片」区域点击「使用 SKU 主图」。
4. 观察图片预览区与表单值是否变化。

# 期望 vs 实际

| | 说明 |
|---|---|
| **期望** | 点击后加载所选 SKU 主图并回显为 Banner 图片；失败时给出明确提示。 |
| **实际** | 点击后界面无任何变化。 |

# 附件

- （弹窗截图待补充）
