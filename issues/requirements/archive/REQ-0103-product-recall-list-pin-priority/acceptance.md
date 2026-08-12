---
requirement_id: REQ-0103-product-recall-list-pin-priority
acceptance_status: passed
created_at: 2026-08-07 22:35:04
updated_at: 2026-08-12 00:15:15
---

# 验收标准

## 功能 AC

- [ ] AC-001 管理端 SKU 维护入口支持配置召回排序值，字段标签为“排序”，放在参考价格之后，标记必填，只允许正整数，未配置时按默认值 `9999` 处理，并通过问号帮助图标 hover 展示说明；非法值提示必须在排序字段下方以红色显示“排序值必须为正整数”，不得展示到弹窗顶部全局错误区。
- [ ] AC-002 管理端 SKU 维护入口支持配置召回置顶生效开始时间和结束时间，并对无效时间范围给出字段级校验提示。
- [ ] AC-003 小程序普通商品列表中，处于有效期内且排序值低于默认值的 SKU 排在非召回商品之前。
- [ ] AC-004 小程序搜索结果 SKU 列表中，处于有效期内且排序值低于默认值的 SKU 排在非召回商品之前。
- [ ] AC-005 召回排序值越低，商品排序越靠前；排序值相同的商品使用稳定兜底排序。
- [ ] AC-006 同一请求下生效召回置顶商品默认少于 5 个，超过上限时仅排序值最靠前且有效的商品参与置顶。
- [ ] AC-007 召回置顶商品仍必须满足当前关键词、品牌、类目、规格、价格等筛选条件，不匹配时不展示。
- [ ] AC-008 召回置顶商品仍必须满足 SKU 已上架、品牌启用、类目启用、规格可用等公开条件。
- [ ] AC-009 新品榜 `section=new` 不应用召回置顶排序，保持原新品榜排序。
- [ ] AC-010 热销榜 `section=hot` 不应用召回置顶排序，保持原热销榜排序。
- [ ] AC-011 小程序商品卡片不展示“置顶”“推荐”“召回”等新增 UI 标识，只体现接口返回顺序。
- [ ] AC-012 小程序端不实现跨页本地重排，加载更多后无重复、漏项或已加载顺序跳动。
- [ ] AC-013 API、Pydantic Schema、OpenAPI、Orval、数据库 schema / migration 和数据库文档按实际字段变化同步。
- [ ] AC-014 后端测试覆盖默认值 `9999`、正整数校验、有效期未开始、有效期已结束、排序值相同、超过上限、筛选条件过滤、榜单例外和分页前排序。

## 横切 AC（knowledge-base）

> 来源：`docs/knowledge-base/best-practices/admin-list-page-consistency.md`、`docs/knowledge-base/best-practices/admin-modal-width-css-cascade.md`、`docs/knowledge-base/best-practices/miniapp-product-list-sorting.md`

- [ ] AC-XCUT-001 管理端 SKU 列表新增排序字段列时，分页 DOM 仍与用户管理基准对齐。
- [ ] AC-XCUT-002 管理端配置保存成功或失败反馈使用 fixed toast，不引起 hero、表格或弹窗布局纵向位移。
- [ ] AC-XCUT-003 召回配置如涉及状态变更、恢复默认或批量操作，必须使用 DS confirm modal；无 `window.confirm`。
- [ ] AC-XCUT-004 管理端新增或调整筛选下拉时，复用 `AdminFilterSelect`、`SearchableSelect` 或等价 shared wrapper；若不新增筛选下拉，记录 N/A — 本期不改筛选控件。
- [ ] AC-XCUT-005 SKU 编辑弹窗如承载召回排序字段，TSX 不得同时挂载 `modal-card` 与专属弹窗类。
- [ ] AC-XCUT-006 SKU 编辑弹窗 computed width 与 SKU 弹窗基准一致，矮视口下 body scroll 无回归。
- [ ] AC-XCUT-007 后端公开 SKU 查询是分页排序事实源，小程序端不得在分页追加后做跨页重排。
- [ ] AC-XCUT-008 品牌、分类、普通关键词和搜索 SKU 入口必须分别覆盖召回置顶排序验收。
- [ ] AC-XCUT-009 首页全部产品、新品榜、热销榜、价格升序 / 降序等不影响分支必须有回归证据。
- [ ] AC-XCUT-010 管理端 SKU 列表状态字段中的“已上架”“已下架”必须单行显示，不允许换行。

## 验收结果回填

```yaml
acceptance_status: passed
accepted_at: 2026-08-12 00:15:15
accepted_by: workflow-sync
source_change: add-product-recall-list-pin-priority
source_sprint: sprint-022
evidence: []
failed_items: []
source_event: sprint.archive
notes: 由 Workflow Sync 根据 Change/Sprint 状态回填。
```

