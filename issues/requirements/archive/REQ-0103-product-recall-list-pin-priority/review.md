---
review_id: REV-REQ-0103-001
date: 2026-08-07
participants:
  - product
result: approved
created_at: 2026-08-07 22:41:24
updated_at: 2026-08-07 22:41:24
---

# 需求评审

## 评审结论

REQ-0103 商品召回列表支持少量商品排序置顶评审通过。

该需求范围清晰：管理端运营维护瓷砖 SKU 召回排序字段与有效期，小程序普通商品列表和搜索 SKU 结果按后端排序结果优先展示少量生效召回商品；新品榜、热销榜不允许召回置顶覆盖原排序，小程序不展示额外 UI 标识。

## 评审检查清单

- [x] 范围清晰，Out of Scope 明确。
- [x] 验收标准可测试，覆盖排序值、有效期、上限、筛选、榜单例外与分页稳定性。
- [x] 优先级与依赖合理，父需求为 `REQ-0006-tile-sku-management`。
- [x] UI 类实现策略已决：管理端 SKU 维护入口增加字段，小程序不新增 UI 标识。
- [x] 无与现有 REQ 重复未说明；已区分 `REQ-0087` 管理端 SKU 列表排序优化。

## 条件通过项

- [x] 后续 OpenSpec design 必须明确 SKU 新增字段、SQLite/MySQL migration、Pydantic Schema、OpenAPI/Orval、管理端字段校验与小程序排序查询的同步范围。
- [x] 后续 Sprint 纳入前需确认容量覆盖 DB、API、管理端、小程序和测试。

## 下一步

评审通过后，先执行 `/sprint-propose` 纳入 Sprint，再执行 `/req-opsx` 创建 OpenSpec Change。
