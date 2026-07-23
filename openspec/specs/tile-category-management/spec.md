# 瓷砖类目管理规范

## Purpose
定义瓷砖类目树、类目列表筛选、创建更新、启停删除和错误码要求，确保类目层级、排序和 SKU 关联边界清晰。
## Requirements
### Requirement: 瓷砖类目数据模型

系统 MUST 在 SQLite/MySQL 中维护 `tile_categories` 表，用于存储瓷砖类目主数据。业务新增类目 MUST 最多两级；为兼容存量数据，表结构 MAY 保留历史 `level=3` 记录。表 MUST 包含字段：`id`、`parent_id`（可空，自引用 FK）、`name`（NOT NULL，新增/更新时最大 10 个用户可见字符且仅允许中文、英文和数字）、`code`（系统生成，UNIQUE NOT NULL，最大 32，MUST 以 `CAT-` 开头）、`sort_order`（正整数 NOT NULL）、`level`（新增仅允许 1 或 2，存量 MAY 为 3）、`description`（可选，最大 200）、`status`（`ENABLED` 或 `DISABLED`）、`sku_count`（非负整数，默认 0）、`path`（层级路径文本 NOT NULL）、`created_at`、`updated_at`。

#### Scenario: 一级类目无上级

- **WHEN** 创建类目且 `parent_id` 为空
- **THEN** `level` MUST 为 1
- **AND** `path` MUST 等于 `name` 或等价顶级路径

#### Scenario: 编码唯一约束

- **WHEN** 系统创建类目
- **THEN** 系统 MUST 自动生成唯一 `code`
- **AND** `code` MUST 以 `CAT-` 开头
- **AND** 前端请求 MUST NOT 决定或覆盖该编码

#### Scenario: 编码冲突兜底

- **WHEN** 生成的 `code` 与既有记录冲突
- **THEN** 系统 MUST 重试生成或拒绝并返回稳定业务错误
- **AND** 系统 MUST NOT 暴露数据库唯一约束原始异常

#### Scenario: 最大层级约束

- **WHEN** 在 `level=2` 的类目下创建子类目
- **THEN** 系统 MUST 拒绝并返回 `CATEGORY_MAX_DEPTH_EXCEEDED`

#### Scenario: 存量三级兼容

- **WHEN** 系统读取历史 `level=3` 类目
- **THEN** 系统 MAY 返回该存量数据用于运营识别
- **AND** 系统 MUST NOT 允许基于该类目继续创建子类目

#### Scenario: 类目名称格式约束

- **WHEN** 创建或更新类目时提交的 `name` 为空、超过 10 个用户可见字符，或包含中文、英文、数字之外的字符
- **THEN** 系统 MUST 拒绝请求并返回统一错误 envelope
- **AND** 错误消息 SHOULD 指向类目名称格式问题

#### Scenario: 同层级名称唯一

- **WHEN** 创建或更新类目导致同一 `parent_id` 下存在重复 `name`
- **THEN** 系统 MUST 拒绝请求并返回稳定业务错误
- **AND** 顶级类目 MUST 以 `parent_id = null` 作为同层级判断

#### Scenario: 编辑自身不误判重复

- **WHEN** 更新类目且名称未变化
- **THEN** 系统 MUST NOT 将该类目自身记录判定为重复名称

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

系统 MUST 提供 `POST /api/v1/admin/tile-categories`，接受 `parent_id`（可空）、`name`、`sort_order`、可选 `description`、`status`（默认 `ENABLED`），MUST NOT 要求或信任客户端提交 `code`。系统 MUST 根据 `parent_id` 计算 `level` 与 `path`，且 MUST NOT 创建三级类目。

#### Scenario: 创建类目成功

- **WHEN** 提交合法字段且创建后层级不超过 2
- **THEN** 系统返回 HTTP 200 与类目对象
- **AND** 返回对象 MUST 包含系统生成的 `code`
- **AND** 未指定 `status` 时 MUST 为 `ENABLED`

#### Scenario: 前端不提交编码

- **WHEN** 管理端创建类目请求未包含 `code`
- **THEN** 系统 MUST 正常进入创建流程
- **AND** 系统 MUST 在后端生成编码

#### Scenario: 忽略或拒绝客户端编码

- **WHEN** 客户端尝试提交 `code`
- **THEN** 系统 MUST NOT 使用该值作为最终编码
- **AND** 系统 MAY 通过请求校验拒绝该字段或在服务层忽略该字段

#### Scenario: 排序非法

- **WHEN** `sort_order` 非正整数
- **THEN** 系统 MUST 返回 HTTP 400，`CATEGORY_INVALID_SORT_ORDER`

#### Scenario: 拒绝创建三级类目

- **WHEN** 提交 `parent_id` 指向二级类目
- **THEN** 系统 MUST 返回 HTTP 422 与 `CATEGORY_MAX_DEPTH_EXCEEDED`
- **AND** 系统 MUST NOT 创建新类目

#### Scenario: 同层级名称重复

- **WHEN** 提交的 `name` 与同一上级类目下已有类目名称重复
- **THEN** 系统 MUST 返回 HTTP 409 或等价业务错误
- **AND** 错误码 SHOULD 为 `CATEGORY_NAME_DUPLICATED` 或等价已登记错误码

### Requirement: 管理端类目更新 API

系统 MUST 提供 `GET /api/v1/admin/tile-categories/{id}` 与 `PUT /api/v1/admin/tile-categories/{id}`。PUT MUST 允许更新 `name`、`sort_order`、`description`；MUST NOT 允许修改 `code`；MUST NOT 通过 PUT 直接修改 `status` 或 `parent_id`（层级变更留后续迭代）。更新 `name` 时 MUST 重新校验名称格式与同层级唯一，并在名称变化后维护 `path` 及子树路径。

#### Scenario: 更新类目资料

- **WHEN** PUT 合法字段
- **THEN** 系统返回 HTTP 200 与更新后对象
- **AND** `updated_at` MUST 已更新

#### Scenario: 更新时编码稳定

- **WHEN** 更新类目名称、排序权重或描述
- **THEN** 既有 `code` MUST 保持不变

#### Scenario: 更新为同层级重复名称

- **WHEN** PUT 的 `name` 与同一上级类目下其他类目重复
- **THEN** 系统 MUST 拒绝更新并返回稳定业务错误

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

系统 MUST 在 API 治理中登记以下错误码：`CATEGORY_CODE_DUPLICATED`、`CATEGORY_NAME_DUPLICATED`（或等价稳定同层级名称重复错误码）、`CATEGORY_DELETE_FORBIDDEN`、`CATEGORY_MAX_DEPTH_EXCEEDED`、`CATEGORY_INVALID_SORT_ORDER`、`CATEGORY_NOT_FOUND`。

#### Scenario: 类目不存在

- **WHEN** 请求不存在的 `{id}`
- **THEN** 系统 MUST 返回 HTTP 404，`CATEGORY_NOT_FOUND`

#### Scenario: 类目名称重复错误码已登记

- **WHEN** 开发者检查错误码登记表与实现
- **THEN** MUST 能找到同层级类目名称重复的稳定错误码
- **AND** 后端类目创建/更新逻辑 MUST 使用该错误码或等价业务错误

