---
change_id: optimize-admin-media-list-thumbnails
capability: banner-management
created_at: 2026-08-05 09:40:00
updated_at: 2026-08-05 09:40:00
---

## MODIFIED Requirements

### Requirement: 管理端 Banner API

系统 MUST 提供 Admin Banners REST API，路径前缀 `/api/v1/admin/banners`。`admin` 与 `employee` MUST 可调用；`store_owner` MUST 403。列表 API MUST 支持 keyword、`display_client`、`status`、`time_status` 分页筛选，并返回 summary（总数、筛选数、已上线、待生效）。列表、summary 和分页 MUST 仅统计小程序首页轮播与小程序品牌列表页轮播范围内的 Banner。MUST 提供 online/offline 端点；删除 MUST 拒绝 `status=ONLINE` 的记录。

管理端 Banner 列表项存在图片时，响应 MUST 新增 `image_thumbnail_url` 或等价 Banner 图片缩略图字段，并保留 `image_url` 与 `image_object_key` 原有语义。`image_thumbnail_url` MUST 基于最终 `image_object_key` 派生，图片来源为 SKU 主图、SKU 图集、品牌 Logo、专题封面或自定义上传时，缩略图字段 MUST 与最终展示图片一致，不得改用跳转目标的其它图片。新增字段 MUST 同步 OpenAPI、Orval、接口文档和测试。

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
