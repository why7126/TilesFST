# tile-category-management Specification

## Purpose
TBD - created by archiving change add-tile-category-management. Update Purpose after archive.
## Requirements
### Requirement: 瓷砖类目数据模型

系统 MUST 在 SQLite 中维护 `tile_categories` 表，用于存储最多三级的瓷砖类目主数据。表 MUST 包含字段：`id`、`parent_id`（可空，自引用 FK）、`name`（NOT NULL，最大 30 字符）、`code`（UNIQUE NOT NULL，最大 32）、`sort_order`（正整数 NOT NULL）、`level`（1、2 或 3）、`description`（可选，最大 200）、`status`（`ENABLED` 或 `DISABLED`）、`sku_count`（非负整数，默认 0）、`path`（层级路径文本 NOT NULL）、`created_at`、`updated_at`。

#### Scenario: 一级类目无上级

- **WHEN** 创建类目且 `parent_id` 为空
- **THEN** `level` MUST 为 1
- **AND** `path` MUST 等于 `name` 或等价顶级路径

#### Scenario: 编码唯一约束

- **WHEN** 插入或更新导致 `code` 与已有记录冲突
- **THEN** 系统 MUST 拒绝并返回 `CATEGORY_CODE_DUPLICATED`

#### Scenario: 最大层级约束

- **WHEN** 在 `level=3` 的类目下创建子类目
- **THEN** 系统 MUST 拒绝并返回 `CATEGORY_MAX_DEPTH_EXCEEDED`

### Requirement: 管理端类目树 API

系统 MUST 提供 `GET /api/v1/admin/tile-categories/tree`，`admin` 与 `employee` 可调用。响应 MUST 返回类目树结构，每个节点 MUST 包含 `id`、`name`、`code`、`level`、`status`、`sku_count`（含子级汇总的 SKU 数）及 `children`（若有）。

#### Scenario: 获取完整类目树

- **WHEN** `employee` 携带有效 token 请求 tree 端点
- **THEN** 系统返回 HTTP 200 与树形数据
- **AND** 根级 MAY 包含虚拟「全部类目」汇总或前端自行汇总

#### Scenario: 非管理端用户被拒绝

- **WHEN** `store_owner` 或未认证用户请求 tree
- **THEN** 系统 MUST 返回 HTTP 401 或 403

### Requirement: 管理端类目列表与筛选 API

系统 MUST 提供 `GET /api/v1/admin/tile-categories`，支持分页（默认 `page_size=10`，可选 10/20/50）、关键词模糊搜索（`name`、`code`）、状态筛选、层级筛选（1/2/3）与 `parent_id`（选中树节点）。响应 MUST 包含 `items`、`pagination` 与 `summary`（类目总数、启用数、绑定 SKU 总数、最大层级固定为 3）。

#### Scenario: 按树节点筛选列表

- **WHEN** 请求带 `parent_id={id}`
- **THEN** 返回的 `items` MUST 包含该节点及其所有子孙类目（分页）

#### Scenario: 分页默认值

- **WHEN** 请求未指定 `page_size`
- **THEN** 系统 MUST 默认每页 10 条

### Requirement: 管理端类目创建 API

系统 MUST 提供 `POST /api/v1/admin/tile-categories`，接受 `parent_id`（可空）、`name`、`code`、`sort_order`、可选 `description`、`status`（默认 `ENABLED`）。系统 MUST 根据 `parent_id` 计算 `level` 与 `path`。

#### Scenario: 创建类目成功

- **WHEN** 提交合法字段且未超过三级深度
- **THEN** 系统返回 HTTP 200 与类目对象
- **AND** 未指定 `status` 时 MUST 为 `ENABLED`

#### Scenario: 编码重复

- **WHEN** `code` 已存在
- **THEN** 系统 MUST 返回 HTTP 409，`CATEGORY_CODE_DUPLICATED`

#### Scenario: 排序非法

- **WHEN** `sort_order` 非正整数
- **THEN** 系统 MUST 返回 HTTP 400，`CATEGORY_INVALID_SORT_ORDER`

### Requirement: 管理端类目更新 API

系统 MUST 提供 `GET /api/v1/admin/tile-categories/{id}` 与 `PUT /api/v1/admin/tile-categories/{id}`。PUT MUST 允许更新 `name`、`sort_order`、`description`；MUST NOT 允许修改 `code`（本期）；MUST NOT 通过 PUT 直接修改 `status` 或 `parent_id`（层级变更留后续迭代）。

#### Scenario: 更新类目资料

- **WHEN** PUT 合法字段
- **THEN** 系统返回 HTTP 200 与更新后对象
- **AND** `updated_at` MUST 已更新

### Requirement: 管理端类目启停 API

系统 MUST 提供 `POST /api/v1/admin/tile-categories/{id}/enable` 与 `POST /api/v1/admin/tile-categories/{id}/disable`。

#### Scenario: 停用类目

- **WHEN** 对 `ENABLED` 类目调用 disable
- **THEN** 系统返回 HTTP 200 且 `status` 为 `DISABLED`

#### Scenario: 启用类目

- **WHEN** 对 `DISABLED` 类目调用 enable
- **THEN** 系统返回 HTTP 200 且 `status` 为 `ENABLED`

### Requirement: 管理端类目条件删除 API

系统 MUST 提供 `DELETE /api/v1/admin/tile-categories/{id}`。仅当 `sku_count=0` 且 `status=DISABLED` 时 MUST 允许删除；否则 MUST 返回 `CATEGORY_DELETE_FORBIDDEN`。

#### Scenario: 允许删除

- **WHEN** 类目 `sku_count=0` 且 `DISABLED`
- **THEN** 系统返回 HTTP 200 并删除记录

#### Scenario: 禁止删除有 SKU

- **WHEN** `sku_count>0`
- **THEN** 系统 MUST 返回 HTTP 409，`CATEGORY_DELETE_FORBIDDEN`

#### Scenario: 禁止删除启用状态

- **WHEN** `status=ENABLED` 即使 `sku_count=0`
- **THEN** 系统 MUST 返回 HTTP 409，`CATEGORY_DELETE_FORBIDDEN`

### Requirement: 管理端类目管理错误码

系统 MUST 在 API 治理中登记以下错误码：`CATEGORY_CODE_DUPLICATED`、`CATEGORY_DELETE_FORBIDDEN`、`CATEGORY_MAX_DEPTH_EXCEEDED`、`CATEGORY_INVALID_SORT_ORDER`、`CATEGORY_NOT_FOUND`。

#### Scenario: 类目不存在

- **WHEN** 请求不存在的 `{id}`
- **THEN** 系统 MUST 返回 HTTP 404，`CATEGORY_NOT_FOUND`

