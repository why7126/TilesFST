---
bug_id: BUG-0053-api-docs-list-layout-pagination-inconsistent
status: captured
created_at: 2026-07-01 09:09:32
updated_at: 2026-07-01 09:09:32
severity_hint: medium
environment: local
related_requirement: REQ-0022-admin-api-docs-menu
related_bug:
captured_via: capture
classification_rationale: 接口文档列表存在冗余首行且分页交互/UI 未与瓷砖 SKU 页一致，属于既有列表页 UI 与交互规范偏差。
---

# 现象

接口文档列表页存在第一行【系统接口】信息，且列表当前不是与瓷砖 SKU 页一致的分页交互和 UI 样式。

# 复现步骤

1. 打开 Web 管理端接口文档页。
2. 查看接口列表第一行是否存在【系统接口】信息。
3. 查看列表是否提供分页，并对照瓷砖 SKU 页分页交互与 UI 样式。

# 期望 vs 实际

- 期望：列表页不展示第一行【系统接口】信息；接口列表采用分页功能，交互与 UI 样式保持与瓷砖 SKU 页一致。
- 实际：列表页出现不需要的【系统接口】信息；分页功能与瓷砖 SKU 页不一致或缺失。

# 影响范围

- Web 管理端 `/admin/api-docs`
- 影响接口列表可读性、管理端列表页一致性与分页操作体验。

# 附件

暂无。

# 分类说明（/capture）

“系统接口”冗余行与分页一致性均属于接口文档列表页的已交付 UI/交互偏差，修复面集中在同一列表组件，因此合并为单条 BUG。
