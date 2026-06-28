---
bug_id: BUG-0030-banner-list-ui-inconsistency
status: captured
created_at: 2026-06-28 16:04:18
updated_at: 2026-06-28 16:04:18
severity_hint: medium
environment: local|docker
related_requirement: REQ-0016-banner-management
related_bug:
---

# 现象

Web 管理端「Banner 管理」列表页与用户管理页等标准管理列表在 UI 上不一致：

1. **分页交互**：底部分页控件样式/交互与用户管理页不一致。
2. **多余标题**：表格区域上方存在「Banner 列表」区块标题，用户管理页无此类标题。
3. **多余统计行**：标题下方存在「当前显示 0-0 / 0」一行，用户管理页无此行。

# 复现步骤

1. 以 admin 登录 Web 管理端，进入「Banner 管理」列表页（侧栏 OPERATIONS → Banner 管理）。
2. 观察表格上方是否存在「Banner 列表」标题及「当前显示 … / …」行。
3. 观察底部分页区域，对比「用户管理」列表页分页组件。

# 期望 vs 实际

| | 说明 |
|---|---|
| **期望** | 分页与用户管理页一致（`AdminListPage` + 统一 `Pagination`）；无「Banner 列表」标题；无标题下方「当前显示 …」行。 |
| **实际** | 分页与用户管理页不一致；存在多余「Banner 列表」标题及「当前显示 …」统计行。 |

# 附件

- screenshots/banner-list-ui-inconsistency.png
