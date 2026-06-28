---
bug_id: BUG-0027-tile-spec-list-ui-inconsistency
status: captured
created_at: 2026-06-28 13:13:16
updated_at: 2026-06-28 13:13:16
severity_hint: medium
environment: local|docker
related_requirement: REQ-0009-tile-spec-management
related_bug:
---

# 现象

Web 管理端「瓷砖规格」列表页与用户管理页等标准管理列表在 UI 上不一致，主要体现在：

1. **分页交互**：底部分页控件样式/交互与用户管理页不一致（当前为简化分页条，缺少与用户管理页一致的分页组件体验）。
2. **表格字体**：「尺寸名称」列文字字号偏大、视觉权重高于同表其他列及用户管理列表主列，与管理端列表统一规范不符。

# 复现步骤

1. 以 admin 登录 Web 管理端，进入「瓷砖规格」列表页（`/admin/tile-specs` 或侧栏 OPERATIONS → 瓷砖规格）。
2. 观察底部分页区域交互与样式，对比「用户管理」列表页分页。
3. 观察表格「尺寸名称」列（如 `600x1200mm`）字号，对比用户管理列表主列文字大小。

# 期望 vs 实际

| | 说明 |
|---|---|
| **期望** | 分页组件与用户管理页一致（`AdminListPage` + 统一 `Pagination`）；表格各列字号、字重与同类管理列表一致。 |
| **实际** | 分页交互/样式与用户管理页不一致；尺寸名称列字体明显偏大。 |

# 附件

- screenshots/tile-spec-list-pagination-font-inconsistency.png
