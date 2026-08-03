---
bug_id: BUG-0090-admin-sku-list-publish-sort-order
status: done
review_result: approved
reviewed_at: 2026-07-30 23:19:33
reviewer: AI
created_at: 2026-07-30 23:19:33
updated_at: 2026-07-31 00:18:16
related_requirement: REQ-0006-tile-sku-management
related_change:
related_bug:
---

# 评审结论

确认修复，状态批准为 `approved`。

该缺陷属于 Web 管理端 SKU 列表已交付能力中的默认排序行为偏差。现有 `bug.md`、`root-cause.md` 和 `acceptance.md` 已能支撑复现、根因判断和回归验收：后端 SKU 列表查询当前按 `updated_at DESC` 排序，而业务期望为已发布 SKU 按发布时间降序、未发布 SKU 按创建时间降序。

# 评审清单

| 检查项 | 结论 | 说明 |
|---|---|---|
| 可复现或根因充分 | 通过 | 已定位后端仓储层 `list_skus()` 使用 `ORDER BY t.updated_at DESC`，Web 端未传排序参数且不做本地业务排序 |
| 严重等级合理 | 通过 | `medium` 合理；问题影响管理端运营浏览和定位 SKU 的效率，但不阻断新增、编辑、上架、下架或删除 |
| 回归验收明确 | 通过 | acceptance.md 已覆盖已发布、未发布、混排、筛选、分页、稳定兜底排序和操作行为不受影响 |
| 是否需 hotfix 路径 | 不需要 | 当前无数据丢失、权限绕过、接口不可用或核心链路阻断证据，按常规 BUG 修复流程推进 |

# 修复前置说明

- 可进入 `/bug-opsx BUG-0090-admin-sku-list-publish-sort-order` 创建修复 Change。
- 可纳入后续 Sprint 正式范围。
- 修复应优先在后端 SKU 列表查询中统一默认排序，避免前端仅排序当前页导致分页顺序不稳定。
- 若仅调整默认排序 SQL 且不新增请求/响应字段，预计不需要 Orval；若新增排序参数，必须同步 OpenAPI / Orval / API 文档与测试。
- 实现阶段需明确已发布与未发布混排时的分组先后规则，以及 `published_at` 为空或主排序时间相同时的稳定兜底字段。

# 评审记录

| 时间 | 命令 | 结果 |
|---|---|---|
| 2026-07-30 23:19:33 | /bug-review --approve | approved |
