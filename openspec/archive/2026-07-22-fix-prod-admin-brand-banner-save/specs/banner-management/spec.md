---
created_at: 2026-07-21 15:28:51
updated_at: 2026-07-21 15:28:51
---

# banner-management Specification Delta

## MODIFIED Requirements

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
