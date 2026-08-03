---
bug_id: BUG-0104-admin-sku-list-headers-wrap
status: done
created_at: 2026-08-03 08:13:39
updated_at: 2026-08-03 09:14:50
severity_hint: low
environment: admin-sku-list
related_requirement: REQ-0006-tile-sku-management
related_bug: null
lifecycle_stage: plan
captured_via: capture
classification_rationale: 管理后台 SKU 列表已存在，用户反馈表头字段换行破坏列表可读性，是既有列表展示样式不符合预期，属于 BUG。
---

# 现象

管理后台 SKU 列表中，部分表头字段发生换行显示。

# 复现步骤

1. 登录管理后台。
2. 进入 SKU 列表页面。
3. 查看列表所有表头字段。
4. 调整到常用桌面宽度，观察表头是否换行。

# 期望 vs 实际

- 期望：所有表头字段不换行，均在一行内显示。
- 实际：部分表头字段换行，影响表格扫描和字段对齐。

# 影响范围

- 管理后台 SKU 列表。
- 表格表头样式、列宽、横向滚动或响应式布局。

# 初步线索

- 需要检查表格 header cell 的 `white-space`、列宽约束和横向滚动容器。
- 修复时应避免压缩数据列导致正文内容重叠。

# 建议验收或复现要点

- [ ] SKU 列表所有表头在桌面管理端常用宽度下均单行显示。
- [ ] 表头与内容列保持对齐。
- [ ] 列数较多时表格可通过既有横向滚动或布局策略完整查看。
- [ ] 修改不影响排序、筛选、分页和操作列。

# 附件

- 暂无。
