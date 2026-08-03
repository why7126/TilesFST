# 瓷砖类目管理规范

## Purpose
定义瓷砖类目树、类目列表筛选、创建更新、启停删除和错误码要求，确保类目层级、排序和 SKU 关联边界清晰。
## Requirements
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

### Requirement: 类目名称输入长度上限

管理端类目创建与更新 MUST 使用统一的业务输入规则：类目名称 trim 后 MUST 非空，MUST 允许 1 到 15 个用户可见字符，且 MUST 允许中文、英文、数字和常见可见特殊字符；常见可见特殊字符 MUST 包含英文括号 `(`、`)` 与中文全角括号 `（`、`）`。超过 15 个用户可见字符时 MUST 拒绝保存。系统 MUST 禁止换行、制表符、不可见控制字符和仅由空白组成的输入。该规则不改变同层级唯一、编码自动生成、层级、排序权重、启停和删除要求。

#### Scenario: 创建特殊字符类目名称

- **WHEN** 管理端提交创建类目请求，`name` 包含合法特殊字符且不超过 15 个用户可见字符
- **THEN** 系统 MUST 接受该名称并创建类目
- **AND** 响应 MUST 返回统一 response envelope 与创建后的类目对象

#### Scenario: 更新特殊字符类目名称

- **WHEN** 管理端提交更新类目请求，`name` 包含合法特殊字符且不超过 15 个用户可见字符
- **THEN** 系统 MUST 接受该名称并更新类目
- **AND** 系统 MUST 继续保持既有 `code` 不变

#### Scenario: 创建 16 字符类目名称

- **WHEN** 管理端提交创建类目请求，`name` 超过 15 个用户可见字符
- **THEN** 系统 MUST 拒绝创建
- **AND** 响应 MUST 使用统一 response envelope 返回稳定业务错误
- **AND** 错误 message MUST 表达类目名称最多 15 个字符

#### Scenario: 更新 16 字符类目名称

- **WHEN** 管理端提交更新类目请求，`name` 超过 15 个用户可见字符
- **THEN** 系统 MUST 拒绝更新
- **AND** 响应 MUST 使用统一 response envelope 返回稳定业务错误
- **AND** 错误 message MUST 表达类目名称最多 15 个字符

#### Scenario: 拒绝控制字符类目名称

- **WHEN** 管理端提交创建或更新类目请求，`name` 包含换行、制表符、不可见控制字符或 trim 后为空
- **THEN** 系统 MUST 拒绝创建或更新
- **AND** 响应 MUST 使用统一 response envelope 返回稳定业务错误
- **AND** 错误 message MUST 表达类目名称仅支持中文、英文、数字和特殊字符或等价字段级错误

#### Scenario: 前端弹窗字符集校验

- **WHEN** 后台用户在新增或编辑类目弹窗输入合法特殊字符类目名称
- **THEN** Web 管理端 MUST 允许提交
- **AND** 字段级错误 MUST NOT 因特殊字符出现

#### Scenario: 前端弹窗非法字符校验

- **WHEN** 后台用户在新增或编辑类目弹窗输入换行、制表符、不可见控制字符或 16 个用户可见字符的类目名称
- **THEN** Web 管理端 MUST 在保存前阻止提交
- **AND** 字段级错误 MUST 展示在类目名称字段或字段组下方

#### Scenario: 展示端特殊字符名称兼容

- **WHEN** 系统存在包含合法特殊字符的类目名称
- **THEN** 管理端类目列表、类目树和类目选择器 MUST NOT 因该名称发生文字重叠、操作遮挡或容器横向撑破
- **AND** 小程序分类入口与 Web 展示端分类入口 MUST NOT 因该名称发生文字重叠、操作遮挡或容器横向撑破

#### Scenario: 创建中文括号类目名称

- **WHEN** 管理端提交创建类目请求，`name` 为 `墙砖（哑光）`
- **THEN** 系统 MUST 接受该名称并创建类目
- **AND** 响应 MUST 返回统一 response envelope 与创建后的类目对象
- **AND** 返回的类目名称 MUST 完整保留中文括号

#### Scenario: 更新中文括号类目名称

- **WHEN** 管理端提交更新类目请求，`name` 为 `地砖（防滑）`
- **THEN** 系统 MUST 接受该名称并更新类目
- **AND** 系统 MUST 继续保持既有 `code` 不变
- **AND** 再次读取该类目时名称 MUST 完整保留中文括号

