---
requirement_id: REQ-0108-admin-banner-list-display-optimization
acceptance_status: passed
created_at: 2026-08-11 08:37:56
updated_at: 2026-08-12 00:15:15
---

# Acceptance Criteria

## 功能 AC

- [ ] AC-001 Banner 管理列表的 Banner 列只展示主图或缩略图，不展示标题、内部识别或其他文本信息。
- [ ] AC-002 展示位置、展示端、跳转类型、状态、有效期、排序、更新时间和操作列继续保留。
- [ ] AC-003 列表新增独立“跳转对象”列。
- [ ] AC-004 跳转类型为品牌详情时，“跳转对象”显示品牌名称。
- [ ] AC-005 跳转类型为 SKU 详情时，“跳转对象”显示 SKU 名称，且不显示 SKU 编码。
- [ ] AC-006 跳转类型为专题页时，“跳转对象”显示专题名称。
- [ ] AC-007 跳转类型为外部链接时，“跳转对象”显示链接地址，长链接不撑宽表格。
- [ ] AC-008 跳转类型为无跳转时，“跳转对象”显示 `-`。
- [ ] AC-009 管理端 Banner 列表 API 返回只读跳转对象展示字段，例如 `jump_target_label`，前端不按行额外请求对象详情。
- [ ] AC-010 新增响应字段同步 Pydantic Schema、OpenAPI、Orval 和前端 generated 类型。
- [ ] AC-011 创建/更新 Banner 请求体不新增运营必填字段，不改变现有跳转校验规则。
- [ ] AC-012 关键词搜索、展示端筛选、状态筛选、时间状态筛选和分页行为不因新增列回退。
- [ ] AC-013 图片加载失败时仍使用现有列表图片 fallback，不出现破图或布局塌陷。
- [ ] AC-014 关联对象不存在、不可用或名称为空时，列表显示明确兜底文案，不空白、不报错。
- [ ] AC-015 Banner 管理列表除“有效期”列保留起止时间换行外，所有表头字段和其他列表字段均不换行显示。

## 横切 AC（knowledge-base）

> 来源：`docs/knowledge-base/best-practices/admin-list-page-consistency.md` — 预防 Sprint 002/003/020 复发类缺陷

- [ ] AC-XCUT-001 Banner 列表分页 DOM 保持用户管理基准：左侧 `page-summary`，右侧 `page-right` 页码与每页条数。
- [ ] AC-XCUT-002 摘要指标卡 DOM 继续使用 `.metric-label` / `.metric-value` / `.metric-desc`，不得改回裸 `strong` / `span` 承载指标。
- [ ] AC-XCUT-003 本需求如调整关键词或筛选区，必须继续复用 `AdminFilterSelect`、`SearchableSelect` 或等价 shared wrapper，并覆盖 open/select/clear/reset 与 query 语义不变。
- [ ] AC-XCUT-004 筛选下拉不得新增页面级一次性弹层样式；弹层不得被表格、滚动容器、弹窗或 sticky action column 裁切。
- [ ] AC-XCUT-005 操作成功/失败反馈继续使用 fixed toast，不得使用会推挤 page hero 或表格的文档流 notice。
- [ ] AC-XCUT-006 上线、下线、删除等状态/危险操作继续使用 DS confirm modal；不得使用 `window.confirm`。
- [ ] AC-XCUT-007 操作列、分页结构和 sticky action cell 不因新增“跳转对象”列出现遮挡、错位或窄屏不可操作。
- [ ] AC-XCUT-008 Vitest 覆盖 Banner 列只显示图片、跳转对象列展示规则、分页 DOM 基准和状态操作 confirm/toast 不回退。

## 验收结果回填

```yaml
acceptance_status: passed
accepted_at: 2026-08-12 00:15:15
accepted_by: workflow-sync
source_change: update-admin-banner-list-display-optimization
source_sprint: sprint-022
evidence: []
failed_items: []
source_event: sprint.archive
notes: 由 Workflow Sync 根据 Change/Sprint 状态回填。
```

