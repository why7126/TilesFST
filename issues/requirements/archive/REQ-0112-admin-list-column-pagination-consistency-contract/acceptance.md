---
requirement_id: REQ-0112-admin-list-column-pagination-consistency-contract
acceptance_status: passed
created_at: 2026-08-12 14:29:16
updated_at: 2026-08-12 22:03:11
owner: product
source: requirement.md
---

# 验收标准

## 功能 AC

- [ ] AC-001 形成管理端列表页列展示与分页一致性契约，明确适用页面、字段类型、强制项、例外项和验证方式。
- [ ] AC-002 首批覆盖页面至少包含 Banner 管理、日志审计和用户管理，并标记品牌、证书、SKU、分类是否纳入后续治理。
- [ ] AC-003 表头字段默认不换行；普通文本字段默认单行展示，长文本通过固定列宽、截断、省略号、tooltip 或等价方式处理。
- [ ] AC-004 有效期、投放周期等复合时间字段允许双行展示；普通更新时间、创建时间、最后登录时间等单时间字段保持单行。
- [ ] AC-005 有效期双行例外不得撑乱行高、挤压操作列或影响分页区域；新增换行例外必须在 design 中说明理由。
- [ ] AC-006 操作列在横向滚动、窄屏、hover、focus、disabled、loading 和权限不足状态下保持可见、可达和布局稳定。
- [ ] AC-007 分页 DOM 与用户管理基准一致，包含左侧 `page-summary` 和右侧 `page-right` 页码与每页条数。
- [ ] AC-008 分页总数使用后端真实总数；每页条数变化、筛选、搜索、排序、页码越界和空结果均有稳定恢复策略。
- [ ] AC-009 首批覆盖页面不得通过全量拉取后前端切片替代后端真实分页。
- [ ] AC-010 若列表分页请求参数或响应结构变化，必须同步 Pydantic Schema、OpenAPI、Orval、API 文档和测试；若无 API 变化，验收记录需说明 N/A。
- [ ] AC-011 若形成共享 class、AdminListPage prop、表格模板或 DS 组件约束，必须使用 semantic token，不得新增裸 Hex。
- [ ] AC-012 前端测试覆盖分页 DOM、nowrap 或等价单行约束、sticky 操作列关键行为、真实分页请求参数和筛选后分页重置。
- [ ] AC-013 knowledge-base 必须回填本需求形成的列展示、有效期例外、sticky 操作列和后端分页 gate。

## 横切 AC（knowledge-base）

> 来源：`docs/knowledge-base/best-practices/admin-list-page-consistency.md` — 预防 Sprint 002/003/015/022 复发类缺陷

- [ ] AC-XCUT-001 分页 DOM 必须与用户管理基准对齐：左侧 `page-summary` 展示真实总数，右侧 `page-right` 展示页码与每页条数。
- [ ] AC-XCUT-002 操作成功/失败反馈必须使用 fixed toast，不得使用文档流 notice 推挤 page hero、筛选区、表格或分页区域。
- [ ] AC-XCUT-003 冻结、启停、上架/下架、删除、重置密码等状态或危险操作必须使用 Design System confirm modal。
- [ ] AC-XCUT-004 源码中不得新增 `window.confirm`；若代表页面已有历史用法，必须在实现阶段列为待治理项或同步修复。
- [ ] AC-XCUT-005 摘要指标卡如在代表列表页出现，DOM 必须使用 `.metric-label`、`.metric-value`、`.metric-desc`；无摘要指标卡页面记录为 N/A — 页面无指标卡。
- [ ] AC-XCUT-006 筛选下拉如在代表列表页出现，必须复用 `AdminFilterSelect`、`SearchableSelect` 或等价 shared wrapper，并覆盖 open/select/clear/reset 与 query 语义不变；无筛选下拉页面记录为 N/A — 页面无筛选下拉。
- [ ] AC-XCUT-007 筛选弹层不得被表格、滚动容器、弹窗、sticky action column 或页面容器裁切。
- [ ] AC-XCUT-008 操作列、分页结构和 sticky action cell 不得因新增列、nowrap 或有效期双行例外出现遮挡、错位或窄屏不可操作。
- [ ] AC-XCUT-009 Vitest 或等价前端测试必须覆盖分页结构 smoke、代表页 sticky 操作列、状态操作 confirm/toast 不回退，以及本需求新增的真实分页契约。

## 验收结果回填

```yaml
acceptance_status: passed
accepted_at: 2026-08-12 22:03:11
accepted_by: workflow-sync
source_change: update-admin-list-column-pagination-consistency-contract
source_sprint: sprint-023
evidence: []
failed_items: []
source_event: sprint.archive
notes: 由 Workflow Sync 根据 Change/Sprint 状态回填。
```

