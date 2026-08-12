# Banner 管理规范

## Purpose
定义 Banner 数据模型、展示位置、Topics 主数据、管理端 API、图片上传、错误码和上下线删除规则，确保运营位内容可控发布。
## Requirements
### Requirement: Banner 数据模型与业务规则

系统 MUST 提供 `banners` 表存储运营 Banner 配置，字段 MUST 包含：`title`、`display_client`、`position`、`image_object_key`、`image_source`、`sku_gallery_asset_id`、`jump_type`、条件跳转目标（`sku_id` / `brand_id` / `external_url` / `topic_id`）、`sort_order`、`valid_from`、`valid_to`、`status`、`remark`、时间戳。业务唯一键 MUST 为 `(display_client, position, title)`。`title` 在当前阶段 MUST 作为系统内部兼容字段保留，MUST NOT 作为运营必须手工维护的前台展示标题；当管理端隐藏标题字段但保存链路仍需要 `title` 时，系统 MUST 自动生成、保留或补齐内部标题，并在冲突时兜底生成新的唯一值，而不是要求运营手动填写标题。新建 Banner MUST 默认 `status=DRAFT`。`display_client` 当前业务范围 MUST 仅支持小程序展示端，存储值 MAY 沿用兼容枚举 `MINIAPP_HOME`，管理端文案 MUST 显示为“小程序”。`position` MUST 仅支持 `MINIAPP_HOME_CAROUSEL` 与 `MINIAPP_BRAND_LIST_CAROUSEL`。`jump_type` MUST 为 `SKU_DETAIL`、`BRAND_DETAIL`、`EXTERNAL_LINK`、`TOPIC_PAGE`、`NO_JUMP` 之一。弹窗保存 MUST NOT 修改 `status`；上线/下线 MUST 仅通过列表 API 变更。生产 MySQL 既有 `banners` 表 MUST 具备创建和编辑 Banner 所需的全部写入字段，至少包括 `image_source`、`sku_gallery_asset_id`、`topic_id`、`brand_id`、`valid_from`、`valid_to`、`remark`；缺失时 MUST 通过幂等迁移、启动前校验或发布前 drift 修复补齐，而不是让保存接口暴露原始数据库异常。

#### Scenario: 隐藏标题后的 Banner 保存

- **GIVEN** 管理端用户具备 Banner 管理权限
- **AND** 新增或编辑 Banner 弹窗不展示标题输入框
- **WHEN** 用户完成图片、展示位置、跳转类型、排序和有效期等字段后保存
- **THEN** 系统 MUST 创建或更新 Banner
- **AND** 系统 MUST 自动生成、保留或补齐内部 `title`
- **AND** 保存失败提示 MUST NOT 要求运营填写 Banner 标题。

#### Scenario: 内部标题唯一性兜底

- **GIVEN** Banner 保存链路仍使用 `(display_client, position, title)` 唯一键
- **WHEN** 自动生成或保留的内部标题发生唯一性冲突
- **THEN** 系统 MUST 兜底生成新的唯一内部标题或返回可运维错误
- **AND** 系统 MUST NOT 要求运营手工修改隐藏字段。

### Requirement: Topics 最小主数据

系统 MUST 提供 `topics` 表及 migration 种子数据（≥2 条 `ENABLED`），供 Banner 专题跳转关联。本期 MUST NOT 提供专题 CRUD 管理页。Admin Topics API MUST 为只读列表，供 Banner 弹窗搜索下拉。

#### Scenario: Topics 种子可读

- **WHEN** 部署 migration 完成
- **THEN** 数据库 MUST 存在 ≥2 条 `status=ENABLED` 的 topics
- **AND** `GET /api/v1/admin/topics` MUST 返回 ENABLED 专题列表

### Requirement: 管理端 Banner API

系统 MUST 提供 Admin Banners REST API，路径前缀 `/api/v1/admin/banners`。`admin` 与 `employee` MUST 可调用；`store_owner` MUST 403。列表 API MUST 支持 keyword、`display_client`、`status`、`time_status` 分页筛选，并返回 summary（总数、筛选数、已上线、待生效）。列表、summary 和分页 MUST 仅统计小程序首页轮播与小程序品牌列表页轮播范围内的 Banner。MUST 提供 online/offline 端点；删除 MUST 拒绝 `status=ONLINE` 的记录。

管理端 Banner 列表项存在图片时，响应 MUST 新增 `image_thumbnail_url` 或等价 Banner 图片缩略图字段，并保留 `image_url` 与 `image_object_key` 原有语义。`image_thumbnail_url` MUST 基于最终 `image_object_key` 派生，图片来源为 SKU 主图、SKU 图集、品牌 Logo、专题封面或自定义上传时，缩略图字段 MUST 与最终展示图片一致，不得改用跳转目标的其它图片。新增字段 MUST 同步 OpenAPI、Orval、接口文档和测试。

管理端 Banner 列表项 MUST 返回只读跳转对象展示字段，例如 `jump_target_label`。该字段 MUST 根据 `jump_type` 生成：品牌详情显示品牌名称，SKU 详情显示 SKU 名称，专题页显示专题名称，外部链接显示链接地址，无跳转显示 `-`。该字段 MUST 仅作为响应展示字段，不得要求创建或更新 Banner 时提交。新增或修改字段 MUST 同步 Pydantic Schema、OpenAPI、Orval、接口文档和测试。

#### Scenario: 列表与 summary

- **WHEN** `admin` 或 `employee` 请求 Banner 列表
- **THEN** 系统返回分页 Banner 列表、分页信息和 summary
- **AND** items、pagination.total 与 summary MUST NOT 包含已删除或旧范围 Banner。

#### Scenario: 创建或更新 Banner 校验

- **WHEN** 创建或更新 Banner
- **THEN** 服务端 MUST 校验图片、跳转目标、排序、有效期逻辑和小程序展示位置合法组合

#### Scenario: Banner 图片来源为 SKU 图片

- **WHEN** `image_source` 为 `sku_main_image` 或 `sku_gallery_image`
- **THEN** MUST 引用已有 `tile_images.object_key`，MUST NOT 重复上传文件
- **AND** `sku_gallery_image` MUST 记录 `sku_gallery_asset_id`。

#### Scenario: 小程序 Banner 查询

- **WHEN** 小程序首页查询 Banner
- **THEN** 后端 MUST 仅返回 `MINIAPP_HOME_CAROUSEL` 中已上线且有效期内的 Banner

#### Scenario: Banner 列表图片缩略图优先

- **GIVEN** Banner 列表项存在 `image_object_key`
- **WHEN** 管理端请求 Banner 列表
- **THEN** 响应项 MUST 包含 `image_thumbnail_url`
- **AND** 响应项 MUST 保留 `image_url`
- **AND** Web 管理端列表 MUST 优先加载 `image_thumbnail_url`

#### Scenario: Banner 列表缩略图回退

- **GIVEN** Banner 列表项存在 `image_url` 但 `image_thumbnail_url` 为空、404 或加载失败
- **WHEN** 管理端渲染 Banner 列表图片
- **THEN** 页面 MUST 回退原图或既有缺图占位
- **AND** 页面 MUST NOT 显示浏览器默认破图
- **AND** 表格行高、分页、筛选和操作列布局 MUST 保持稳定

#### Scenario: Banner 列表跳转对象展示字段

- **GIVEN** Banner 列表项配置了品牌详情、SKU 详情、专题页、外部链接或无跳转
- **WHEN** 管理端请求 Banner 列表
- **THEN** 响应项 MUST 包含 `jump_target_label` 或等价跳转对象展示字段
- **AND** 品牌详情 MUST 返回品牌名称
- **AND** SKU 详情 MUST 返回 SKU 名称且不得拼接 SKU 编码
- **AND** 专题页 MUST 返回专题名称
- **AND** 外部链接 MUST 返回链接地址
- **AND** 无跳转 MUST 返回 `-` 或可由前端稳定渲染为 `-` 的空值。

#### Scenario: Banner 列表跳转对象兜底

- **GIVEN** Banner 关联的品牌、SKU 或专题不存在、不可用或名称为空
- **WHEN** 管理端请求 Banner 列表
- **THEN** 服务端 MUST 返回稳定兜底展示值
- **AND** 响应 MUST NOT 泄露内部 SQL、对象 key、未授权字段或内部堆栈
- **AND** 列表渲染 MUST NOT 因兜底值为空而报错。

### Requirement: Banner 图片上传

Banner 自定义上传 MUST 经后端授权写入 MinIO 单桶，object_key MUST 使用 `images/default/banners/{uuid}.{ext}` 形态（与 `update-object-storage-key-layout` 语义前缀一致）。上传 MUST 受 `MAX_IMAGE_SIZE_MB` 与 `ALLOWED_IMAGE_TYPES` 约束。

#### Scenario: Banner 图上传成功

- **WHEN** `admin` 经 `POST /api/v1/admin/uploads/banner-images` 上传合法 JPG/PNG/WebP
- **THEN** MUST 返回 `object_key` 与 `/media/{object_key}` URL
- **AND** object_key MUST 以 `images/default/banners/` 开头

### Requirement: Banner 管理错误码

系统 MUST 为 Banner 业务规则提供统一错误码：`BANNER_TITLE_DUPLICATED`、`BANNER_JUMP_TARGET_INVALID`、`BANNER_DELETE_FORBIDDEN`、`BANNER_NOT_FOUND`、`BANNER_EXTERNAL_URL_INVALID`，并登记 `docs/standards/error-codes.md`。标题重复错误码 MAY 继续用于内部标题冲突，但管理端隐藏标题字段后，用户可见提示 MUST 转换为系统自动重试、内部保存失败或联系管理员类文案，MUST NOT 要求运营填写或修改 Banner 标题。

#### Scenario: 内部标题重复

- **WHEN** 创建或更新导致 `(display_client, position, title)` 冲突
- **THEN** 系统 SHOULD 自动生成新的内部标题并重试保存
- **AND** 如无法自动恢复，错误提示 MUST NOT 暴露为“Banner 标题重复，请修改标题”。

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

