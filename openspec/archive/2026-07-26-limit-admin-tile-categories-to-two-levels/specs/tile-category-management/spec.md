## MODIFIED Requirements

### Requirement: 瓷砖类目数据模型

系统 MUST 在 SQLite 中维护 `tile_categories` 表，用于存储瓷砖类目主数据。业务新增类目 MUST 最多两级；为兼容存量数据，表结构 MAY 保留历史 `level=3` 记录。表 MUST 包含字段：`id`、`parent_id`（可空，自引用 FK）、`name`（NOT NULL，最大 30 字符）、`code`（UNIQUE NOT NULL，最大 32）、`sort_order`（正整数 NOT NULL）、`level`（新增仅允许 1 或 2，存量 MAY 为 3）、`description`（可选，最大 200）、`status`（`ENABLED` 或 `DISABLED`）、`sku_count`（非负整数，默认 0）、`path`（层级路径文本 NOT NULL）、`created_at`、`updated_at`。

#### Scenario: 一级类目无上级

- **WHEN** 创建类目且 `parent_id` 为空
- **THEN** `level` MUST 为 1
- **AND** `path` MUST 等于 `name` 或等价顶级路径

#### Scenario: 编码唯一约束

- **WHEN** 插入或更新导致 `code` 与已有记录冲突
- **THEN** 系统 MUST 拒绝并返回 `CATEGORY_CODE_DUPLICATED`

#### Scenario: 最大层级约束

- **WHEN** 在 `level=2` 的类目下创建子类目
- **THEN** 系统 MUST 拒绝并返回 `CATEGORY_MAX_DEPTH_EXCEEDED`

#### Scenario: 存量三级兼容

- **WHEN** 系统读取历史 `level=3` 类目
- **THEN** 系统 MAY 返回该存量数据用于运营识别
- **AND** 系统 MUST NOT 允许基于该类目继续创建子类目

### Requirement: 管理端类目列表与筛选 API

系统 MUST 提供 `GET /api/v1/admin/tile-categories`，支持分页（默认 `page_size=10`，可选 10/20/50）、关键词模糊搜索（`name`、`code`）、状态筛选、层级筛选（1/2）与 `parent_id`（选中树节点）。响应 MUST 包含 `items`、`pagination` 与 `summary`（类目总数、启用数、绑定 SKU 总数、最大层级固定为 2）。

#### Scenario: 按树节点筛选列表

- **WHEN** 请求带 `parent_id={id}`
- **THEN** 返回的 `items` MUST 包含该节点及其所有子孙类目（分页）

#### Scenario: 分页默认值

- **WHEN** 请求未指定 `page_size`
- **THEN** 系统 MUST 默认每页 10 条

#### Scenario: 层级筛选拒绝三级

- **WHEN** 请求 `GET /api/v1/admin/tile-categories?level=3`
- **THEN** 系统 MUST 返回 HTTP 422 与 `CATEGORY_MAX_DEPTH_EXCEEDED`

### Requirement: 管理端类目创建 API

系统 MUST 提供 `POST /api/v1/admin/tile-categories`，接受 `parent_id`（可空）、`name`、`code`、`sort_order`、可选 `description`、`status`（默认 `ENABLED`）。系统 MUST 根据 `parent_id` 计算 `level` 与 `path`，且 MUST NOT 创建三级类目。

#### Scenario: 创建类目成功

- **WHEN** 提交合法字段且创建后层级不超过 2
- **THEN** 系统返回 HTTP 200 与类目对象
- **AND** 未指定 `status` 时 MUST 为 `ENABLED`

#### Scenario: 编码重复

- **WHEN** `code` 已存在
- **THEN** 系统 MUST 返回 HTTP 409，`CATEGORY_CODE_DUPLICATED`

#### Scenario: 排序非法

- **WHEN** `sort_order` 非正整数
- **THEN** 系统 MUST 返回 HTTP 400，`CATEGORY_INVALID_SORT_ORDER`

#### Scenario: 拒绝创建三级类目

- **WHEN** 提交 `parent_id` 指向二级类目
- **THEN** 系统 MUST 返回 HTTP 422 与 `CATEGORY_MAX_DEPTH_EXCEEDED`
- **AND** 系统 MUST NOT 创建新类目
