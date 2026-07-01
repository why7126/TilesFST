---
bug_id: BUG-0052-api-docs-metric-cards-inconsistent
status: captured
created_at: 2026-07-01 09:09:32
updated_at: 2026-07-01 09:09:32
severity_hint: medium
environment: local
related_requirement: REQ-0022-admin-api-docs-menu
related_bug:
captured_via: capture
classification_rationale: 接口文档页标题下方指标卡样式与瓷砖 SKU 页同类指标卡不一致，属于既有 UI 规范偏差。
---

# 现象

接口文档页标题下方的指标卡样式，与瓷砖 SKU 页的指标卡样式不一致。

# 复现步骤

1. 打开 Web 管理端接口文档页。
2. 查看标题下方的指标卡区域。
3. 对照瓷砖 SKU 页的指标卡样式。

# 期望 vs 实际

- 期望：接口文档页指标卡复用或对齐瓷砖 SKU 页同类指标卡的 UI 样式，包括布局、间距、边框、圆角、文字层级与 semantic token。
- 实际：接口文档页指标卡样式与瓷砖 SKU 页不一致。

# 影响范围

- Web 管理端 `/admin/api-docs`
- 影响管理端页面一致性与 Design System 验收。

# 附件

暂无。

# 分类说明（/capture）

该条目明确以已交付的瓷砖 SKU 页同类组件作为参照基线，属于页面样式与既有规范不一致，因此判定为 BUG。
