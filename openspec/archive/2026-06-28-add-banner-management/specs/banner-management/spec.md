## ADDED Requirements

### Requirement: Banner 数据模型与业务规则

系统 MUST 提供 `banners` 表存储运营 Banner 配置，字段 MUST 包含：`title`、`display_client`、`position`、`image_object_key`、`image_source`、`jump_type`、条件跳转目标（`sku_id` / `external_url` / `topic_id`）、`sort_order`、`valid_from`、`valid_to`、`status`、`remark`、时间戳。业务唯一键 MUST 为 `(display_client, position, title)`。新建 Banner MUST 默认 `status=DRAFT`。`jump_type` MUST 为 `SKU_DETAIL`、`EXTERNAL_LINK`、`TOPIC_PAGE`、`NO_JUMP` 之一。弹窗保存 MUST NOT 修改 `status`；上线/下线 MUST 仅通过列表 API 变更。

#### Scenario: 创建 Banner 默认草稿

- **WHEN** 客户端 `POST /api/v1/admin/banners` 提交合法 payload
- **THEN** 服务端 MUST 创建记录且 `status=DRAFT`
- **AND** MUST 校验 `(display_client, position, title)` 唯一性

#### Scenario: 跳转类型目标完整性

- **WHEN** `jump_type=SKU_DETAIL`
- **THEN** `sku_id` MUST 非空且 SKU 存在
- **WHEN** `jump_type=EXTERNAL_LINK`
- **THEN** `external_url` MUST 以 `https://` 开头且通过 URL 安全校验
- **WHEN** `jump_type=TOPIC_PAGE`
- **THEN** `topic_id` MUST 非空且 topic 为 `ENABLED`
- **WHEN** `jump_type=NO_JUMP`
- **THEN** `sku_id`、`external_url`、`topic_id` MUST 均为空

#### Scenario: 展示端与展示位置组合

- **WHEN** `display_client=WEB_HOME`
- **THEN** `position` MUST 为 `HOME_TOP_CAROUSEL` 或 `HOME_MID_SLOT`
- **WHEN** `display_client=MINIAPP_HOME`
- **THEN** `position` MUST 为 `MINIAPP_HOME_CAROUSEL`
- **WHEN** `display_client=TOPIC`
- **THEN** `position` MUST 为 `TOPIC_TOP_BANNER`

### Requirement: Topics 最小主数据

系统 MUST 提供 `topics` 表及 migration 种子数据（≥2 条 `ENABLED`），供 Banner 专题跳转关联。本期 MUST NOT 提供专题 CRUD 管理页。Admin Topics API MUST 为只读列表，供 Banner 弹窗搜索下拉。

#### Scenario: Topics 种子可读

- **WHEN** 部署 migration 完成
- **THEN** 数据库 MUST 存在 ≥2 条 `status=ENABLED` 的 topics
- **AND** `GET /api/v1/admin/topics` MUST 返回 ENABLED 专题列表

### Requirement: Admin Banners API

系统 MUST 提供 Admin Banners REST API，路径前缀 `/api/v1/admin/banners`。`admin` 与 `employee` MUST 可调用；`store_owner` MUST 403。列表 API MUST 支持 keyword、`display_client`、`status`、`time_status` 分页筛选，并返回 summary（总数、筛选数、已上线、待生效）。MUST 提供 online/offline 端点；删除 MUST 拒绝 `status=ONLINE` 的记录。

#### Scenario: 列表与 summary

- **WHEN** 客户端 `GET /api/v1/admin/banners` 带分页与筛选参数
- **THEN** MUST 返回 items、pagination 与 summary 统计
- **AND** 每项 MUST 含计算字段 `time_status`（`ACTIVE`/`PENDING`/`EXPIRED`）

#### Scenario: 上线前校验

- **WHEN** 客户端 `POST /api/v1/admin/banners/{id}/online`
- **THEN** 服务端 MUST 校验图片、跳转目标、排序与有效期逻辑
- **AND** 成功后 MUST 设置 `status=ONLINE`

#### Scenario: 下线

- **WHEN** 客户端 `POST /api/v1/admin/banners/{id}/offline`
- **THEN** MUST 设置 `status=OFFLINE`

#### Scenario: 删除条件

- **WHEN** 客户端 `DELETE /api/v1/admin/banners/{id}` 且 `status=ONLINE`
- **THEN** MUST 返回业务错误 `BANNER_DELETE_FORBIDDEN`
- **WHEN** `status` 为 `DRAFT`、`OFFLINE` 或 `EXPIRED`
- **THEN** MUST 允许删除

#### Scenario: SKU 图库引用

- **WHEN** `image_source` 为 `sku_main_image` 或 `sku_gallery_image`
- **THEN** MUST 引用已有 `tile_images.object_key`，MUST NOT 重复上传文件
- **AND** `sku_gallery_image` MUST 记录 `sku_gallery_asset_id`

### Requirement: Banner 图片上传

Banner 自定义上传 MUST 经后端授权写入 MinIO 单桶，object_key MUST 使用 `images/default/banners/{uuid}.{ext}` 形态（与 `update-object-storage-key-layout` 语义前缀一致）。上传 MUST 受 `MAX_IMAGE_SIZE_MB` 与 `ALLOWED_IMAGE_TYPES` 约束。

#### Scenario: Banner 图上传成功

- **WHEN** `admin` 经 `POST /api/v1/admin/uploads/banner-images` 上传合法 JPG/PNG/WebP
- **THEN** MUST 返回 `object_key` 与 `/media/{object_key}` URL
- **AND** object_key MUST 以 `images/default/banners/` 开头

### Requirement: Banner 管理错误码

系统 MUST 为 Banner 业务规则提供统一错误码：`BANNER_TITLE_DUPLICATED`、`BANNER_JUMP_TARGET_INVALID`、`BANNER_DELETE_FORBIDDEN`、`BANNER_NOT_FOUND`、`BANNER_EXTERNAL_URL_INVALID`，并登记 `docs/standards/error-codes.md`。

#### Scenario: 标题重复

- **WHEN** 创建或更新导致 `(display_client, position, title)` 冲突
- **THEN** MUST 返回 `BANNER_TITLE_DUPLICATED`

#### Scenario: 非法外链

- **WHEN** `external_url` 非 `https://` 或含非法 scheme
- **THEN** MUST 返回 `BANNER_EXTERNAL_URL_INVALID`
