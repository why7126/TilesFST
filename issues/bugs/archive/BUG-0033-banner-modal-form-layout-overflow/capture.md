---
bug_id: BUG-0033-banner-modal-form-layout-overflow
status: captured
created_at: 2026-06-28 16:04:18
updated_at: 2026-06-28 16:04:18
severity_hint: high
environment: local|docker
related_requirement: REQ-0016-banner-management
related_bug:
---

# 现象

Banner 新增/编辑弹窗表单布局存在问题，导致内容溢出弹窗可视区域：

1. **运营备注**：文本框宽度未占满整行；占位文字字号偏大。
2. **底部操作区**：「取消」「保存 Banner」按钮已超出弹窗底部，弹窗未提供纵向滚动条，用户无法完整查看或点击底部按钮。

# 复现步骤

1. 以 admin 登录 Web 管理端，进入「Banner 管理」列表页。
2. 点击「+ 新增 Banner」或编辑已有 Banner 打开弹窗。
3. 观察「运营备注」文本框宽度与占位符字号。
4. 向下滚动或缩小视口，观察底部「取消」「保存 Banner」是否被裁切；尝试在弹窗内纵向滚动。

# 期望 vs 实际

| | 说明 |
|---|---|
| **期望** | 运营备注占满整行、占位符字号与其他字段一致；弹窗内容区可纵向滚动，底部操作按钮始终可访问。 |
| **实际** | 备注框宽度不足、占位符偏大；底部按钮超出弹窗且无纵向滚动。 |

# 附件

- （弹窗截图待补充）
