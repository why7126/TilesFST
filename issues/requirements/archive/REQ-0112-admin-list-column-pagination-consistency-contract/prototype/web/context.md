---
requirement_id: REQ-0112-admin-list-column-pagination-consistency-contract
created_at: 2026-08-12 14:29:16
updated_at: 2026-08-12 14:29:16
owner: product
source: requirement.md
---

# Prototype Context

## 1. 原型策略

本需求是管理端列表页列展示与分页一致性契约，不新增独立业务页面，也不要求制作单独 HTML 视觉原型。

后续 OpenSpec design / apply 阶段应以代表页面作为视觉验收对象：

- Banner 管理列表
- 日志审计列表
- 用户管理列表

## 2. UI Contract 草案

| 区域 | 契约 |
|---|---|
| 表头 | 默认单行，不换行，不因长文案撑宽整表。 |
| 普通字段 | 默认单行截断，必要时提供 tooltip 或 title。 |
| 有效期 | 允许起止时间双行展示；列宽固定，行高稳定。 |
| 操作列 | 横向滚动时可达；不遮挡相邻列、弹层、toast 或分页。 |
| 分页 | DOM 使用 `page-summary` + `page-right`，展示真实总数、页码和每页条数。 |
| 反馈 | 操作结果使用 fixed toast；危险操作使用 DS confirm modal。 |

## 3. 视觉验收建议

- 1440×1024：代表页分页 DOM 与用户管理基准并排检查。
- 窄屏或横向滚动：确认 sticky 操作列可达且不遮挡文本。
- 长文本样例：确认普通字段单行截断，有效期仅在允许字段双行。
- 筛选弹层样例：确认弹层不被 sticky 操作列或表格滚动容器裁切。

## 4. Mock / API 边界

- 若只实现前端布局契约，可用 mock 数据验证列宽、nowrap、有效期例外和操作列。
- 若实现后端真实分页，必须使用真实分页 API 或测试替身验证请求参数、响应总数和页码边界。
- 前端不得以全量拉取后本地切片作为真实分页验收证据。
