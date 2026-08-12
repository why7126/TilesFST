---
req_id: REQ-0108-admin-banner-list-display-optimization
status: archived
created_at: 2026-08-11 08:33:52
updated_at: 2026-08-11 23:20:43
recorded_by: product
source: 用户反馈
priority_hint: P1
parent_requirement:
---

# 一句话

Web 管理后台 Banner 列表页优化显示内容：Banner 列只显示主图，并新增独立“跳转对象”列展示可读对象名称或链接。

# 原始描述

Web管理后台 Banner列表页显示内容优化：Banner列只显示主图；新增跳转对象展示字段，按跳转类型显示品牌名称、SKU名称、专题名称、外部链接地址或“-”。

补充约束：

- Banner 列仅调整自身内容为只显示主图；展示位置、状态、排序等其他未提及修改的列全部保留。
- 跳转对象单独新增一列。
- SKU 名称不需要显示 SKU 编码。

# 待澄清

- [ ] 跳转对象列是否需要参与关键词搜索。
- [ ] 跳转对象名称为空、对象已下架或已删除时，是否显示 `-`、对象 ID，还是显示“对象不可用”。
- [ ] 跳转对象列在窄屏或横向滚动下的列宽与截断策略。

# 探索结论

前置探索判断该需求需要后端列表接口补充只读跳转对象展示字段，例如 `jump_target_label`，因为当前 Banner 列表响应仅包含 `sku_id`、`brand_id`、`topic_id` 与 `external_url`，不包含品牌、SKU、专题名称。推荐由后端列表查询关联现有品牌、SKU、专题表一次性返回展示文案，前端新增独立列渲染。
