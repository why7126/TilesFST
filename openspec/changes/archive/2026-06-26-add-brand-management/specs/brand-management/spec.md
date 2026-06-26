## ADDED Requirements

### Requirement: 瓷砖品牌数据模型

系统 MUST 在 SQLite 中维护 `brands` 表，用于存储瓷砖品牌主数据。表 MUST 包含字段：`id`、`name`（UNIQUE NOT NULL，最大 50 字符）、`sort_order`（正整数 NOT NULL）、`short_name`（可选，最大 30）、`english_name`（可选，最大 80）、`logo_object_key`（可选）、`description`（可选，最大 500）、`status`（`ENABLED` 或 `DISABLED`）、`sku_count`（非负整数，默认 0）、`created_at`、`updated_at`。

#### Scenario: 新品牌默认字段

- **WHEN** 通过 API 创建品牌且未指定 status
- **THEN** 数据库记录 `status` MUST 为 `ENABLED`
- **AND** `sku_count` MUST 默认为 0（SKU 模块未上线时）

#### Scenario: 品牌名称唯一约束

- **WHEN** 插入或更新导致 `name` 与已有记录冲突
- **THEN** 数据库或业务层 MUST 拒绝并返回 `BRAND_NAME_DUPLICATED`

### Requirement: 管理端品牌列表与筛选 API

系统 MUST 提供 `GET /api/v1/admin/brands`，`admin` 与 `employee` 可调用。接口 MUST 支持分页（默认 `page_size=20`，可选 20/50/100）、关键词模糊搜索（`name`、`short_name`、`english_name`）与状态筛选（全部/`ENABLED`/`DISABLED`）。响应 MUST 包含 `items`、`pagination` 与 `summary`（品牌总数、启用数、停用数、未关联 SKU 数）。

#### Scenario: 运营人员查询品牌列表

- **WHEN** `employee` 携带有效 token 请求 `GET /api/v1/admin/brands`
- **THEN** 系统返回 HTTP 200，`data` 包含分页列表与 summary

#### Scenario: 非管理端用户被拒绝

- **WHEN** `store_owner` 或未认证用户请求 `GET /api/v1/admin/brands`
- **THEN** 系统 MUST 返回 HTTP 401 或 403

#### Scenario: 分页默认值

- **WHEN** 请求未指定 `page_size`
- **THEN** 系统 MUST 默认每页 20 条

### Requirement: 管理端品牌创建 API

系统 MUST 提供 `POST /api/v1/admin/brands`，`admin` 与 `employee` 可调用。请求 MUST 接受 `name`、`sort_order`、可选 `short_name`、`english_name`、`logo_object_key`、`description`。新品牌 `status` MUST 默认为 `ENABLED`。

#### Scenario: 创建品牌成功

- **WHEN** 提交合法 `name`（非空、≤50）与正整数 `sort_order`
- **THEN** 系统返回 HTTP 200 与品牌对象
- **AND** `status` MUST 为 `ENABLED`

#### Scenario: 品牌名称重复

- **WHEN** `name` 已存在
- **THEN** 系统 MUST 返回 HTTP 409，错误码 `BRAND_NAME_DUPLICATED`

#### Scenario: 排序非法

- **WHEN** `sort_order` 非正整数（0、负数、小数、非数字）
- **THEN** 系统 MUST 返回 HTTP 400，错误码 `BRAND_INVALID_SORT_ORDER`

### Requirement: 管理端品牌更新 API

系统 MUST 提供 `GET /api/v1/admin/brands/{id}` 与 `PUT /api/v1/admin/brands/{id}`，`admin` 与 `employee` 可调用。PUT MUST 允许更新 `name`、`sort_order`、`short_name`、`english_name`、`logo_object_key`、`description`；MUST NOT 通过 PUT 直接修改 `status`（使用 enable/disable 端点）。

#### Scenario: 更新品牌资料

- **WHEN** PUT 合法字段且 `name` 不与他人冲突
- **THEN** 系统返回 HTTP 200 与更新后品牌对象
- **AND** `updated_at` MUST 已更新

#### Scenario: 更新时名称冲突

- **WHEN** PUT 的 `name` 与其他品牌 id 重复
- **THEN** 系统 MUST 返回 HTTP 409，`BRAND_NAME_DUPLICATED`

### Requirement: 管理端品牌启停 API

系统 MUST 提供 `POST /api/v1/admin/brands/{id}/enable` 与 `POST /api/v1/admin/brands/{id}/disable`，`admin` 与 `employee` 可调用。

#### Scenario: 停用品牌

- **WHEN** 对 `ENABLED` 品牌调用 disable
- **THEN** 系统返回 HTTP 200 且 `status` 为 `DISABLED`

#### Scenario: 启用品牌

- **WHEN** 对 `DISABLED` 品牌调用 enable
- **THEN** 系统返回 HTTP 200 且 `status` 为 `ENABLED`

### Requirement: 管理端品牌条件删除 API

系统 MUST 提供 `DELETE /api/v1/admin/brands/{id}`，`admin` 与 `employee` 可调用。仅当 `sku_count = 0` 且 `status = DISABLED` 时 MUST 允许删除；否则 MUST 返回 `BRAND_DELETE_FORBIDDEN`。

#### Scenario: 允许删除

- **WHEN** 品牌 `sku_count` 为 0 且 `status` 为 `DISABLED`
- **THEN** 系统 MUST 删除记录并返回 HTTP 200

#### Scenario: 禁止删除已关联 SKU

- **WHEN** 品牌 `sku_count` > 0
- **THEN** 系统 MUST 返回 HTTP 409，错误码 `BRAND_DELETE_FORBIDDEN`

#### Scenario: 禁止删除启用状态品牌

- **WHEN** 品牌 `status` 为 `ENABLED` 且 `sku_count` 为 0
- **THEN** 系统 MUST 返回 HTTP 409，错误码 `BRAND_DELETE_FORBIDDEN`

### Requirement: 品牌管理 PNG 视觉验收 Gate

品牌管理页视觉对齐 MUST 通过 HTML 原型并排验收 gate；PNG golden reference 补齐后 MUST 纳入 sprint acceptance-report。

#### Scenario: 列表页并排验收

- **WHEN** 团队在 1280px 视口并排对比 `/admin/brands` 与 `brand-management.html`（或 `brand-management.png`）
- **THEN** diff checklist（Shell、Sidebar active、无导出批量、4 指标卡、筛选行、表格列、删除置灰规则、分页含 page_size）MUST 全部 pass
- **AND** 结果 MUST 记录在 change `trace.md`

#### Scenario: 弹窗并排验收

- **WHEN** 打开新增/编辑弹窗并排 `brand-management-modal.html`（或 PNG）
- **THEN** checklist（720px、字段顺序、无状态字段、Logo/介绍通栏同宽、固定头尾滚动）MUST pass
