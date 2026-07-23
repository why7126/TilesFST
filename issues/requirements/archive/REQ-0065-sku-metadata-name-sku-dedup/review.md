---
review_id: REV-REQ-0065-001
date: 2026-07-21
participants:
  - product
result: approved
created_at: 2026-07-21 17:57:47
updated_at: 2026-07-21 17:57:47
---

# REQ-0065 需求评审

## 评审结论

通过。

本需求范围清晰，明确将 SKU 编码定位为系统自动生成的唯一识别字段，将商品名称定位为运营填写并面向用户展示的字段；Out of Scope 已明确不删除底层编码字段、不引入外部 ERP 编码、不新增商品别名体系。

验收标准覆盖管理端表单与列表、小程序/店主端展示、分享标题、API/DB/Orval 兼容、历史数据和测试要求；UI 类原型策略已提供 `prototype/web/` HTML 与 context；已按 knowledge-base 写入 `admin-list`、`admin-modal` 横切 AC。

## 评审检查清单

- [x] 范围清晰，Out of Scope 明确。
- [x] 验收标准可测试。
- [x] 优先级与依赖合理。
- [x] UI 类原型或实现策略已决。
- [x] 无与现有 REQ 重复未说明；本需求作为 `REQ-0006-tile-sku-management` 的 refinement 独立推进。

## 条件通过项

- [ ] 后续 `/req-opsx` 的 design.md 必须引用 `knowledge_base_refs`，并保留 `admin-list`、`admin-modal` 横切验收。
- [ ] 若实现时调整管理端创建请求体，使前端不再传入 `sku_code`，必须同步 OpenAPI、Orval、接口文档和测试。
- [ ] 若实现时涉及数据库迁移或历史数据补齐，必须同步 SQLite/MySQL 文档、迁移脚本和测试。

## 后续动作

1. `/req-opsx REQ-0065-sku-metadata-name-sku-dedup`
2. `/sprint-propose` 纳入迭代后再开发
