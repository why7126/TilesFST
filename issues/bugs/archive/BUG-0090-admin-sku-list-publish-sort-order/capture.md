---
bug_id: BUG-0090-admin-sku-list-publish-sort-order
status: done
created_at: 2026-07-30 22:53:04
updated_at: 2026-07-31 00:18:16
severity_hint: medium
environment: web
related_requirement: REQ-0006-tile-sku-management
related_bug: null
lifecycle_stage: plan
captured_via: capture
classification_rationale: 瓷砖 SKU 列表属于已交付的 Web 端管理能力，用户明确指出当前列表排序字段不符合期望排序规则，属于既有行为偏差，因此判定为 BUG。
---

# 现象

Web 端（电脑端）瓷砖 SKU 列表当前不应按更新时间排序；已发布 SKU 应按发布时间降序展示，未发布 SKU 应按创建时间降序展示。

# 复现步骤

1. 在 Web 端打开瓷砖 SKU 列表。
2. 准备多条 SKU：包含已发布、未发布、更新时间不同、发布时间不同、创建时间不同的记录。
3. 观察列表默认排序结果。

# 期望 vs 实际

- 期望：已发布 SKU 按 `published_at` 降序排列；未发布 SKU 按 `created_at` 降序排列。
- 实际：当前列表按更新时间或等价更新时间字段排序，导致发布顺序和未发布草稿顺序不符合业务预期。

# 影响范围

- Web 端瓷砖 SKU 列表默认排序。
- 后端 SKU 列表查询排序逻辑或前端列表排序参数。
- 可能影响管理端运营人员查找最新发布或最新创建的 SKU。

# 初步线索

- 需确认排序应由后端统一返回，还是 Web 端显式传参控制。
- 需确认已发布和未发布是否在同一列表中混排；若混排，需要定义已发布与未发布分组的先后规则。
- 需确认发布时间为空、重复发布时间、重复创建时间时的稳定兜底排序字段。

# 建议验收或复现要点

- [ ] 已发布 SKU 默认按发布时间降序显示。
- [ ] 未发布 SKU 默认按创建时间降序显示。
- [ ] 同一时间值下列表顺序稳定，不因刷新或分页加载跳动。
- [ ] 列表分页、搜索、筛选后仍遵循同一默认排序策略。
- [ ] 本次调整不改变 SKU 新增、编辑、上下架、删除等操作行为。

# 附件

暂无。
