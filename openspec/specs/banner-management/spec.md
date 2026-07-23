# Banner 管理规范

## Purpose
定义 Banner 数据模型、展示位置、Topics 主数据、管理端 API、图片上传、错误码和上下线删除规则，确保运营位内容可控发布。
## Requirements
### Requirement: Banner 数据模型与业务规则

系统 MUST 提供 `banners` 表存储运营 Banner 配置，字段 MUST 包含：`title`、`display_client`、`position`、`image_object_key`、`image_source`、`jump_type`、条件跳转目标（`sku_id` / `brand_id` / `external_url` / `topic_id`）、`sort_order`、`valid_from`、`valid_to`、`status`、`remark`、时间戳。业务唯一键 MUST 为 `(display_client, position, title)`。新建 Banner MUST 默认 `status=DRAFT`。`display_client` 当前业务范围 MUST 仅支持小程序展示端，存储值 MAY 沿用兼容枚举 `MINIAPP_HOME`，管理端文案 MUST 显示为“小程序”。`position` MUST 仅支持 `MINIAPP_HOME_CAROUSEL` 与 `MINIAPP_BRAND_LIST_CAROUSEL`。`jump_type` MUST 为 `SKU_DETAIL`、`BRAND_DETAIL`、`EXTERNAL_LINK`、`TOPIC_PAGE`、`NO_JUMP` 之一。弹窗保存 MUST NOT 修改 `status`；上线/下线 MUST 仅通过列表 API 变更。生产 MySQL 既有表 MUST 具备保存 `BRAND_DETAIL` 所需的 `brand_id` 字段；缺失时 MUST 通过幂等迁移、启动前校验或发布前 drift 修复补齐，而不是让保存接口暴露原始数据库异常。

#### Scenario: 品牌详情 Banner 新增保存

- **GIVEN** 管理端用户具备 Banner 管理权限
- **AND** 存在 `ENABLED` 品牌
- **WHEN** 客户端 `POST /api/v1/admin/banners` 提交 `jump_type=BRAND_DETAIL`、合法 `brand_id`、合法图片来源、展示位置、排序和有效期
- **THEN** 服务端 MUST 创建 Banner 并返回统一成功响应
- **AND** 持久化记录 MUST 保留 `brand_id`、`jump_type`、`image_source` 和 `image_object_key`
- **AND** 新建 Banner MUST 默认 `status=DRAFT`。

#### Scenario: 品牌详情 Banner 编辑保存

- **GIVEN** 已存在品牌详情 Banner
- **AND** 新目标品牌存在且为 `ENABLED`
- **WHEN** 客户端 `PUT /api/v1/admin/banners/{id}` 修改品牌、图片来源、排序、有效期或备注
- **THEN** 服务端 MUST 保存修改后的品牌详情配置
- **AND** 管理端列表、详情和编辑弹窗 MUST 回显同一 `brand_id` 与图片配置。

#### Scenario: 品牌详情 Banner 图片来源校验

- **WHEN** `image_source=brand_logo`
- **THEN** `image_object_key` MUST 与所选品牌 `logo_object_key` 一致
- **AND** 品牌缺少 Logo 时 MUST 返回稳定业务错误而不是保存空引用
- **WHEN** `image_source=custom_upload`
- **THEN** `image_object_key` MUST 引用经后端授权上传的 Banner 图片对象
- **AND** 前端不得直连未授权对象存储。

#### Scenario: 品牌详情 Banner 失败提示

- **WHEN** 所选品牌不存在、未启用、品牌 Logo 缺失、Logo key 不匹配或标题重复
- **THEN** 服务端 MUST 返回统一错误 envelope 和稳定业务错误码或等价可定位错误
- **AND** 响应与日志 MUST NOT 泄露数据库密码、DSN、MinIO 凭据、原始 SQL 或内部堆栈。

#### Scenario: 品牌详情 Banner 展示读取一致

- **WHEN** 品牌详情 Banner 保存成功并上线且处于有效期内
- **THEN** 管理端列表与详情 MUST 读取到相同配置
- **AND** 小程序首页轮播或品牌列表页轮播查询 MUST 按 `position` 分流返回对应 Banner
- **AND** 公开查询结果 MUST 保留品牌详情跳转所需目标信息。

### Requirement: Topics 最小主数据

系统 MUST 提供 `topics` 表及 migration 种子数据（≥2 条 `ENABLED`），供 Banner 专题跳转关联。本期 MUST NOT 提供专题 CRUD 管理页。Admin Topics API MUST 为只读列表，供 Banner 弹窗搜索下拉。

#### Scenario: Topics 种子可读

- **WHEN** 部署 migration 完成
- **THEN** 数据库 MUST 存在 ≥2 条 `status=ENABLED` 的 topics
- **AND** `GET /api/v1/admin/topics` MUST 返回 ENABLED 专题列表

### Requirement: 管理端 Banner API

系统 MUST 提供 Admin Banners REST API，路径前缀 `/api/v1/admin/banners`。`admin` 与 `employee` MUST 可调用；`store_owner` MUST 403。列表 API MUST 支持 keyword、`display_client`、`status`、`time_status` 分页筛选，并返回 summary（总数、筛选数、已上线、待生效）。列表、summary 和分页 MUST 仅统计小程序首页轮播与小程序品牌列表页轮播范围内的 Banner。MUST 提供 online/offline 端点；删除 MUST 拒绝 `status=ONLINE` 的记录。

#### Scenario: 列表与 summary

- **WHEN** 客户端 `GET /api/v1/admin/banners` 带分页与筛选参数
- **THEN** MUST 返回 items、pagination 与 summary 统计
- **AND** 每项 MUST 含计算字段 `time_status`（`ACTIVE`/`PENDING`/`EXPIRED`）
- **AND** items、pagination.total 与 summary MUST NOT 包含已删除或旧范围 Banner。

#### Scenario: 上线前校验

- **WHEN** 客户端 `POST /api/v1/admin/banners/{id}/online`
- **THEN** 服务端 MUST 校验图片、跳转目标、排序、有效期逻辑和小程序展示位置合法组合
- **AND** 成功后 MUST 设置 `status=ONLINE`。

#### Scenario: 下线

- **WHEN** 客户端 `POST /api/v1/admin/banners/{id}/offline`
- **THEN** MUST 设置 `status=OFFLINE`。

#### Scenario: 删除条件

- **WHEN** 客户端 `DELETE /api/v1/admin/banners/{id}` 且 `status=ONLINE`
- **THEN** MUST 返回业务错误 `BANNER_DELETE_FORBIDDEN`
- **WHEN** `status` 为 `DRAFT`、`OFFLINE` 或 `EXPIRED`
- **THEN** MUST 允许删除。

#### Scenario: SKU 图库引用

- **WHEN** `image_source` 为 `sku_main_image` 或 `sku_gallery_image`
- **THEN** MUST 引用已有 `tile_images.object_key`，MUST NOT 重复上传文件
- **AND** `sku_gallery_image` MUST 记录 `sku_gallery_asset_id`。

#### Scenario: 小程序轮播公开查询分流

- **WHEN** 小程序首页查询 Banner
- **THEN** 后端 MUST 仅返回 `MINIAPP_HOME_CAROUSEL` 中已上线且有效期内的 Banner
- **AND** MUST NOT 返回 `MINIAPP_BRAND_LIST_CAROUSEL` 数据
- **WHEN** 小程序品牌列表页查询 Banner
- **THEN** 后端 MUST 仅返回 `MINIAPP_BRAND_LIST_CAROUSEL` 中已上线且有效期内的 Banner
- **AND** MUST NOT 使用首页轮播作为品牌列表页兜底。

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

### Requirement: 管理端 Banner 图片预览

Web 管理端 Banner 管理页面 MUST 在列表缩略图与新建/编辑弹窗中提供可用于运营确认的 Banner 图片预览。预览 MUST 优先保证图片主体与关键信息完整可识别，MUST 避免因固定容器、裁切型 `object-fit`、父容器 overflow 或表格/弹窗高度限制导致关键文字、Logo 或主体内容被裁掉。预览背景、边框、占位和空白区域 MUST 使用管理端 Design System semantic token。该要求 MUST NOT 改变 Banner API、数据库表结构、对象存储策略或展示端真实投放裁切策略。

#### Scenario: 列表缩略图完整预览

- **WHEN** 管理端用户访问 `/admin/banners` 列表
- **AND** 列表项存在 Banner 图片
- **THEN** 图片缩略图 MUST 完整呈现图片主体
- **AND** MUST NOT 裁掉关键文字、Logo 或主体内容
- **AND** 图片加载或比例变化 MUST NOT 改变表格行高、分页、筛选或操作按钮布局。

#### Scenario: 弹窗图片完整预览

- **WHEN** 管理端用户新建或编辑 Banner
- **AND** 弹窗中展示已选图片或上传后的图片
- **THEN** 弹窗预览 MUST 完整呈现当前图片
- **AND** 上传后预览与编辑回显 MUST 使用一致展示策略
- **AND** MUST NOT 遮挡表单字段、上传控件、弹窗滚动区域或底部保存按钮。

#### Scenario: 多比例和多来源图片预览

- **WHEN** Banner 图片为横幅图、方图、竖图或超宽图
- **OR** 图片来源为自定义上传图、品牌 Logo、SKU 主图或 SKU 图库图
- **THEN** 管理端预览 MUST 使用一致且可预期的适配策略
- **AND** MUST 避免明显拉伸、压扁或比例失真
- **AND** MUST 保留图片主体可识别性。

#### Scenario: 修复范围不影响业务配置

- **WHEN** 管理端用户在修复后的 Banner 弹窗中保存配置
- **THEN** Banner 新建、编辑、保存、上线、下线、排序和跳转类型配置 MUST 保持既有行为
- **AND** API 请求与响应契约 MUST 不因本预览修复发生变化。

