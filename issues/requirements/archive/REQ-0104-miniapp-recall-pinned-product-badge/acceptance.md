---
requirement_id: REQ-0104-miniapp-recall-pinned-product-badge
acceptance_status: passed
created_at: 2026-08-08 09:25:35
updated_at: 2026-08-12 00:15:15
---

# 验收标准

## 功能 AC

- [x] AC-001 普通商品列表中，实际生效的召回置顶商品展示“置顶”标识。
- [x] AC-002 普通商品列表中，非置顶商品不展示“置顶”标识。
- [x] AC-003 搜索 SKU 结果中，实际生效的召回置顶商品展示“置顶”标识。
- [x] AC-004 搜索实时联想不展示“置顶”标识。
- [x] AC-005 新品商品列表没有置顶逻辑，不展示“置顶”标识。
- [x] AC-006 热销商品列表没有置顶逻辑，不展示“置顶”标识。
- [x] AC-007 仅配置召回排序值但当前列表未应用置顶逻辑的商品不展示“置顶”标识。
- [x] AC-008 置顶配置取消、失效、未到生效时间、超过置顶数量上限后，列表刷新不再展示“置顶”标识。
- [x] AC-009 API 响应字段表达“当前列表实际生效的召回置顶展示状态”，小程序不得根据排序位置推断标识。
- [x] AC-010 API 缺少置顶字段时，小程序默认不展示“置顶”标识。
- [x] AC-011 “置顶”标识复用商品卡片角标区域或等价轻量位置，不遮挡商品主图核心内容、名称、品牌、规格和参考价格。
- [x] AC-012 标识展示不影响整卡点击、曝光埋点、点击埋点、图片加载失败兜底、下拉刷新和加载更多。
- [x] AC-013 分页加载更多后，已加载商品不重复、不错位、不遗留错误“置顶”标识。
- [x] AC-014 新增或调整响应字段时，同步 Pydantic Schema、OpenAPI、Orval、小程序类型定义和接口文档。

## 领域回归 AC（knowledge-base）

> 来源：`docs/knowledge-base/best-practices/miniapp-product-list-sorting.md`。该文档不属于 req-complete 固定 admin/media 横切标签，但与本需求的小程序商品列表排序事实源强相关。

- [x] AC-DOMAIN-001 小程序端不在分页追加后做跨页重排，商品顺序以后端公开 SKU 查询结果为准。
- [x] AC-DOMAIN-002 品牌、分类、普通关键词入口的默认排序在非置顶商品分支保持既有稳定兜底规则。
- [x] AC-DOMAIN-003 首页全部产品、新品榜、热销榜、价格升序 / 降序等回归分支不因“置顶”标识改动而改变排序语义。
- [x] AC-DOMAIN-004 后端测试或小程序静态测试覆盖加载更多后无重复、漏项或已加载顺序跳动。

## 横切 AC（knowledge-base）

- N/A — 本需求不涉及管理端列表、管理端表单、管理端弹窗或媒体上传，不命中 `req-complete` 固定横切标签。

## 验收结果回填

```yaml
acceptance_status: passed
accepted_at: 2026-08-12 00:15:15
accepted_by: workflow-sync
source_change: update-miniapp-recall-pinned-product-badge
source_sprint: sprint-022
evidence: []
failed_items: []
source_event: sprint.archive
notes: 由 Workflow Sync 根据 Change/Sprint 状态回填。
```

