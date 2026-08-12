## MODIFIED Requirements

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

### Requirement: 管理端 Banner API

系统 MUST 提供 Admin Banners REST API，路径前缀 `/api/v1/admin/banners`。`admin` 与 `employee` MUST 可调用；`store_owner` MUST 403。列表 API MUST 支持 keyword、`display_client`、`status`、`time_status` 分页筛选，并返回 summary（总数、筛选数、已上线、待生效）。列表、summary 和分页 MUST 仅统计小程序首页轮播与小程序品牌列表页轮播范围内的 Banner。MUST 提供 online/offline 端点；删除 MUST 拒绝 `status=ONLINE` 的记录。

管理端 Banner 列表项存在图片时，响应 MUST 新增 `image_thumbnail_url` 或等价 Banner 图片缩略图字段，并保留 `image_url` 与 `image_object_key` 原有语义。`image_thumbnail_url` MUST 基于最终 `image_object_key` 派生，图片来源为 SKU 主图、SKU 图集、品牌 Logo、专题封面或自定义上传时，缩略图字段 MUST 与最终展示图片一致，不得改用跳转目标的其它图片。新增字段 MUST 同步 OpenAPI、Orval、接口文档和测试。公开小程序 Banner 响应 MAY 继续返回 `title` 以兼容旧客户端，但当前小程序页面 MUST NOT 将该字段渲染为 Banner 主标题。

#### Scenario: 创建或更新 Banner 校验

- **WHEN** 创建或更新 Banner
- **THEN** 服务端 MUST 校验展示端、展示位置、图片、跳转目标、排序和有效期
- **AND** 管理端隐藏标题字段后，服务端或客户端 MUST 确保请求仍具备合法内部 `title`，或服务端 MUST 接受缺省标题并自动补齐
- **AND** 如果请求 schema 因标题缺省发生变化，OpenAPI、Orval、接口文档和测试 MUST 同步。

### Requirement: Banner 管理错误码

系统 MUST 为 Banner 业务规则提供统一错误码：`BANNER_TITLE_DUPLICATED`、`BANNER_JUMP_TARGET_INVALID`、`BANNER_DELETE_FORBIDDEN`、`BANNER_NOT_FOUND`、`BANNER_EXTERNAL_URL_INVALID`，并登记 `docs/standards/error-codes.md`。标题重复错误码 MAY 继续用于内部标题冲突，但管理端隐藏标题字段后，用户可见提示 MUST 转换为系统自动重试、内部保存失败或联系管理员类文案，MUST NOT 要求运营填写或修改 Banner 标题。

#### Scenario: 内部标题重复

- **WHEN** 创建或更新导致 `(display_client, position, title)` 冲突
- **THEN** 系统 SHOULD 自动生成新的内部标题并重试保存
- **AND** 如无法自动恢复，错误提示 MUST NOT 暴露为“Banner 标题重复，请修改标题”。
