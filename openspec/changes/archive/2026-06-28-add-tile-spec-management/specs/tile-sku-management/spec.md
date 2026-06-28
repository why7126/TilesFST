## MODIFIED Requirements

### Requirement: 瓷砖 SKU 数据模型

系统 MUST 在 SQLite 中维护 SKU 商品主数据。`tiles` 表 MUST 扩展或等价实现以下字段：`id`、`name`（SKU 名称 NOT NULL）、`sku_code`（UNIQUE NOT NULL）、`brand_id`（FK `brands.id` NOT NULL）、`category_id`（FK `tile_categories.id` NOT NULL）、`spec_id`（FK `tile_specs.id`，创建 SKU 时 SHOULD 非空；迁移失败历史记录 MAY 为 NULL 直至运营补选）、`size`（规格尺寸 NOT NULL，MUST 与所选规格 `display_name` 冗余同步）、`surface_finish`（表面工艺 NOT NULL，业务层允许空语义存 `"-"`）、`color_family`（可选）、`reference_price`（必填语义，REAL，≥0，两位小数；新建默认 0）、`remark`（可选）、`status`（`PUBLISHED` | `DRAFT` | `NEEDS_COMPLETION` | `DISABLED`）、`created_at`、`updated_at`。`tile_images` MUST 保留 `is_main` 与 `sort_order`。系统 MUST 维护 `tile_videos` 表存储 SKU 关联视频元数据（`tile_id`、`object_key`、`file_name`、`file_size_bytes`、`duration_seconds`、`sort_order`）。

#### Scenario: 新 SKU 默认草稿

- **WHEN** 通过 API 创建 SKU 且未指定 status
- **THEN** 数据库记录 `status` MUST 为 `DRAFT`

#### Scenario: SKU 编码唯一约束

- **WHEN** 插入或更新导致 `sku_code` 与已有记录冲突
- **THEN** 系统 MUST 拒绝并返回 `TILE_SKU_CODE_DUPLICATED`

#### Scenario: 主图标记

- **WHEN** SKU 有多张图片且其中一张 `is_main=1`
- **THEN** 列表与详情 MUST 将该图作为主图缩略图
- **AND** 同一 SKU MUST NOT 有多张 `is_main=1`（业务层保证唯一）

#### Scenario: 参考价格默认零

- **WHEN** 通过 create API 创建 SKU 且未显式修改参考价格
- **THEN** `reference_price` MUST 持久化为 `0`（非 null）

#### Scenario: spec_id 与 size 同步

- **WHEN** SKU 创建或更新提交有效 `spec_id`
- **THEN** `tiles.size` MUST 等于对应 `tile_specs.display_name`
- **AND** 对应规格 `sku_count` MUST 正确维护

### Requirement: 管理端 SKU 创建 API

系统 MUST 提供 `POST /api/v1/admin/tile-skus`，`admin` 与 `employee` 可调用。请求 MUST 接受 SKU 基础字段（含 `spec_id`）、图片列表（含 `is_main`）、视频列表，以及 `save_mode`（`draft` | `create`）。`save_mode=draft` 时 MUST 仅校验 SKU 名称必填；`save_mode=create` 时 MUST 校验名称、编码、品牌、类目、**spec_id**（所选规格 MUST 存在且 `ENABLED`）、**参考价格（含 0）** 必填；**表面工艺 MUST 为可选**（留空时业务层 MAY 存 `"-"`）。新 SKU `status` MUST 默认为 `DRAFT`；缺主图时 MAY 设为 `NEEDS_COMPLETION`。

#### Scenario: 保存草稿成功

- **WHEN** 提交 `save_mode=draft` 且 SKU 名称非空
- **THEN** 系统返回 HTTP 200 与 SKU 对象
- **AND** `status` MUST 为 `DRAFT`

#### Scenario: 创建 SKU 成功

- **WHEN** 提交 `save_mode=create` 且全部必填项合法（含 `spec_id` 指向 ENABLED 规格、`reference_price=0`、表面工艺可空）
- **THEN** 系统返回 HTTP 200
- **AND** `status` MUST 为 `DRAFT` 或 `NEEDS_COMPLETION`（缺主图时）
- **AND** `size` MUST 等于所选规格 display_name

#### Scenario: 创建 SKU 选择停用规格被拒绝

- **WHEN** 提交 `save_mode=create` 且 `spec_id` 指向 `DISABLED` 规格
- **THEN** 系统 MUST 返回 HTTP 409，错误码 `TILE_SPEC_DISABLED`

#### Scenario: 创建 SKU 缺少参考价格被拒绝

- **WHEN** 提交 `save_mode=create` 且 `reference_price` 为 null 或未提供
- **THEN** 系统 MUST 返回 HTTP 400

#### Scenario: SKU 编码重复

- **WHEN** `sku_code` 已存在
- **THEN** 系统 MUST 返回 HTTP 409，错误码 `TILE_SKU_CODE_DUPLICATED`

### Requirement: 管理端 SKU 更新 API

系统 MUST 提供 `GET /api/v1/admin/tile-skus/{id}` 与 `PUT /api/v1/admin/tile-skus/{id}`，`admin` 与 `employee` 可调用。PUT MUST 允许更新基础字段与图片/视频关联；MUST NOT 通过 PUT 直接修改 `status`（使用 publish/unpublish）。PUT MUST 要求 `reference_price` 非 null（含 `0.0`）；**MUST NOT** 因 surface_finish 留空而拒绝更新。若 PUT 变更 `spec_id` 至新规格，新规格 MUST 为 `ENABLED`；若保留原 `spec_id` 且该规格已 DISABLED，MAY 允许更新非规格字段。

#### Scenario: 更新 SKU 资料

- **WHEN** PUT 合法字段且 `sku_code` 不与他人冲突
- **THEN** 系统返回 HTTP 200 与更新后 SKU 对象
- **AND** `updated_at` MUST 已更新
- **AND** 若含 `spec_id`，`size` MUST 同步

#### Scenario: 更新缺少参考价格被拒绝

- **WHEN** PUT 请求将 `reference_price` 置为 null 或未提供合法数值
- **THEN** 系统 MUST 返回 HTTP 400

### Requirement: 管理端 SKU 上下架 API

系统 MUST 提供 `POST /api/v1/admin/tile-skus/{id}/publish` 与 `POST /api/v1/admin/tile-skus/{id}/unpublish`，`admin` 与 `employee` 可调用。

#### Scenario: 上架 SKU

- **WHEN** 对满足上架条件的 SKU 调用 publish
- **THEN** 系统返回 HTTP 200 且 `status` 为 `PUBLISHED`

#### Scenario: 上架缺少必填或主图被拒绝

- **WHEN** SKU 缺少名称/编码/规格等必填项或主图且调用 publish
- **THEN** 系统 MUST 返回 HTTP 409，错误码 `TILE_SKU_PUBLISH_FORBIDDEN`
- **AND** **MUST NOT** 因 surface_finish 留空或 `"-"` alone 而拒绝
- **AND** **`spec_id` 为空或 `size` 为空时 MUST 拒绝**

#### Scenario: 下架 SKU

- **WHEN** 对 `PUBLISHED` SKU 调用 unpublish
- **THEN** 系统返回 HTTP 200 且 `status` 为 `DISABLED` 或 `DRAFT`（实现定稿一种）
