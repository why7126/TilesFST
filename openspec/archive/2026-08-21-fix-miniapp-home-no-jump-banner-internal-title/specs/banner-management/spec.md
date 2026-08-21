## MODIFIED Requirements

### Requirement: Banner 数据模型与业务规则

系统 MUST 提供 `banners` 表存储运营 Banner 配置，字段 MUST 包含：`title`、`display_client`、`position`、`image_object_key`、`image_source`、`sku_gallery_asset_id`、`jump_type`、条件跳转目标（`sku_id` / `brand_id` / `external_url` / `topic_id`）、`sort_order`、`valid_from`、`valid_to`、`status`、`remark`、时间戳。业务唯一键 MUST 为 `(display_client, position, title)`。`title` 在当前阶段 MUST 作为系统内部兼容字段保留，MUST NOT 作为运营必须手工维护的前台展示标题；当管理端隐藏标题字段但保存链路仍需要 `title` 时，系统 MUST 自动生成、保留或补齐内部标题，并在冲突时兜底生成新的唯一值，而不是要求运营手动填写标题。内部标题 MUST 与公开展示标题隔离；任何小程序公开查询、公开 DTO、前台搜索兜底、分享文案或埋点展示摘要 MUST NOT 直接暴露自动生成的内部标题。新建 Banner MUST 默认 `status=DRAFT`。`display_client` 当前业务范围 MUST 仅支持小程序展示端，存储值 MAY 沿用兼容枚举 `MINIAPP_HOME`，管理端文案 MUST 显示为“小程序”。`position` MUST 仅支持 `MINIAPP_HOME_CAROUSEL` 与 `MINIAPP_BRAND_LIST_CAROUSEL`。`jump_type` MUST 为 `SKU_DETAIL`、`BRAND_DETAIL`、`EXTERNAL_LINK`、`TOPIC_PAGE`、`NO_JUMP` 之一。弹窗保存 MUST NOT 修改 `status`；上线/下线 MUST 仅通过列表 API 变更。生产 MySQL 既有 `banners` 表 MUST 具备创建和编辑 Banner 所需的全部写入字段，至少包括 `image_source`、`sku_gallery_asset_id`、`topic_id`、`brand_id`、`valid_from`、`valid_to`、`remark`；缺失时 MUST 通过幂等迁移、启动前校验或发布前 drift 修复补齐，而不是让保存接口暴露原始数据库异常。

#### Scenario: 内部标题不进入公开端

- **GIVEN** Banner 保存链路自动生成或保留了 `internal-*` 内部标题
- **WHEN** 小程序首页或品牌列表页查询公开 Banner 数据
- **THEN** 后端 MUST 保留后台管理所需的内部标题兼容能力
- **AND** 公开响应 MUST NOT 直接返回该内部标题作为用户可见标题、搜索关键词或展示摘要
- **AND** 无跳转 Banner 的公开字段 MUST 使用安全空值、公开展示名或明确的非展示字段替代内部标题。

### Requirement: 管理端 Banner API

系统 MUST 提供 Admin Banners REST API，路径前缀 `/api/v1/admin/banners`。`admin` 与 `employee` MUST 可调用；`store_owner` MUST 403。列表 API MUST 支持 keyword、`display_client`、`status`、`time_status` 分页筛选，并返回 summary（总数、筛选数、已上线、待生效）。列表、summary 和分页 MUST 仅统计小程序首页轮播与小程序品牌列表页轮播范围内的 Banner。MUST 提供 online/offline 端点；删除 MUST 拒绝 `status=ONLINE` 的记录。管理端 API MAY 继续返回内部标题用于内部识别、搜索和编辑兼容，但该字段不得被解释为公开展示标题。

#### Scenario: 小程序 Banner 查询净化内部标题

- **WHEN** 小程序首页或品牌列表页查询 Banner
- **THEN** 后端 MUST 仅返回对应位置中已上线且有效期内的 Banner
- **AND** 后端 MUST 对自动生成或内部兼容标题进行公开端净化
- **AND** 响应 MUST NOT 暴露 `internal-*`、后台枚举、时间戳或等价内部识别值。
