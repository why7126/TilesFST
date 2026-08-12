---
change_id: add-product-recall-list-pin-priority
source_requirement: REQ-0103-product-recall-list-pin-priority
related_sprint: sprint-022
status: proposed
created_at: 2026-08-07 23:12:00
updated_at: 2026-08-07 23:12:00
---

# 测试计划

## 后端测试

- 管理端 SKU create/update/detail 覆盖召回排序值默认 `9999`、正整数校验、开始时间晚于结束时间拒绝、保存回显。
- SQLite 和 MySQL schema / migration 覆盖新增字段存在、默认值一致、可空语义一致。
- `/api/v1/miniapp/products` 覆盖全部商品、分类、品牌、普通关键词列表的召回置顶排序。
- `/api/v1/miniapp/search` 覆盖 SKU Tab / SKU 分区结果的召回置顶排序。
- 过滤约束覆盖关键词、品牌、类目、规格、价格区间、SKU 未上架、品牌停用、类目停用、规格不可用。
- 边界覆盖默认值 `9999`、有效期未开始、有效期已结束、开始为空、结束为空、排序值相同、超过 4 个候选。
- 回归覆盖 `section=new`、`section=hot`、价格升序 / 降序不应用召回置顶。
- 分页测试覆盖排序在分页前生效，加载更多无重复、漏项或已加载顺序跳动。

## 管理端 Web 测试

- SKU 新建 / 编辑弹窗展示召回置顶字段组。
- 排序值字段只允许正整数，空值按 `9999` 保存或回显。
- 有效期错误展示字段级校验提示。
- 保存成功关闭或刷新行为沿用既有 SKU 弹窗契约。
- fixed toast 不造成列表、弹窗、表格纵向位移。
- 矮视口下弹窗主体可滚动且 footer 按钮可见。

## 小程序测试

- 商品列表页和搜索结果页按接口顺序展示，不做本地跨页重排。
- 商品卡片不展示“置顶”“推荐”“召回”等新增标识。
- 下拉刷新和上拉加载更多不产生重复、漏项或顺序跳动。
- 新品榜、热销榜入口保持原榜单顺序。

## 文档与生成物校验

- OpenSpec 校验通过。
- `python scripts/validate-openspec-language.py` 通过。
- OpenAPI / Orval 生成物与接口字段同步。
- 数据库文档记录 SQLite / MySQL 字段与迁移策略。
