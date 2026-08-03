## MODIFIED Requirements

### Requirement: 管理端类目树 API

系统 MUST 提供 `GET /api/v1/admin/tile-categories/tree`，`admin` 与 `employee` 可调用。响应 MUST 返回类目树结构，每个节点 MUST 包含 `id`、`name`、`code`、`level`、`status`、`sku_count`（含子级汇总的 SKU 数）、`children_count`（直接子类目数量）及 `children`（若有）。`sku_count` 与 `children_count` MUST 表达不同语义：`sku_count` 只用于商品/SKU 数量统计和删除规则判断，`children_count` 只用于类目树层级数量展示。

#### Scenario: 获取完整类目树

- **WHEN** `employee` 携带有效 token 请求 tree 端点
- **THEN** 系统返回 HTTP 200 与树形数据
- **AND** 每个类目节点 MUST 返回直接子类目数量字段 `children_count`
- **AND** 根级 MAY 包含虚拟「全部类目」汇总或前端自行汇总

#### Scenario: 类目树节点区分 SKU 数量与子类目数量

- **GIVEN** 某一级类目有 3 个直接子类目且含子级汇总 SKU 数为 21
- **WHEN** 系统返回该类目树节点
- **THEN** `children_count` MUST 为 `3`
- **AND** `sku_count` MAY 为 `21`
- **AND** 系统 MUST NOT 用 `sku_count` 覆盖 `children_count`

#### Scenario: 叶子类目子类目数量为 0

- **GIVEN** 某类目没有直接子类目
- **WHEN** 系统返回该类目树节点
- **THEN** `children_count` MUST 为 `0`
- **AND** 即使该类目存在关联 SKU，`children_count` 也 MUST NOT 显示商品数量
