## MODIFIED Requirements

### Requirement: 品牌 Logo 上传

系统 MUST 支持品牌 Logo 经后端授权上传至 MinIO 单桶 `MINIO_BUCKET`，MIME 类型 MUST 包含 JPG、PNG、WebP。`logo_object_key` MUST 存于 `brands` 表；前端 MUST NOT 直连未授权对象存储。上传响应与品牌列表/详情响应 MUST 提供可被 Web 客户端实际加载的 `url`、`logo_url`、`thumbnail_url` 或等价 `preview_url`，并 MUST 符合对象存储单桶与标准业务前缀策略。

新上传品牌 Logo 在 `brand_id` 已存在时 MUST 写入 `images/default/brand-logos/{brand_id}/{uuid}.{ext}`；在品牌创建前上传时 MUST 写入 `images/default/brand-logos/pending/`，并在创建品牌成功后 formalize 到 `brand-logos/{brand_id}/`。系统 MUST 为新上传品牌图片生成真实轻量缩略图，品牌列表和小图预览 SHOULD 优先使用缩略图，原图预览 SHOULD 使用原图或原始受控 URL。对象存储写入链路修复后，品牌列表页和品牌编辑弹窗 MUST 仍能通过后端受控读取或安全 URL 展示 Logo；历史 `logo_object_key` 和过渡目录 MUST 保持读取兼容，并有明确迁移、缩略图补齐或重新上传策略。

#### Scenario: 上传 Logo 成功

- **WHEN** `admin` 或 `employee` 上传合法图片至品牌上传端点
- **THEN** 系统返回 object_key
- **AND** 系统 MUST 将对象写入 `MINIO_BUCKET`
- **AND** 当 `brand_id` 已存在时 object_key MUST 使用 `images/default/brand-logos/{brand_id}/` 正式目录
- **AND** 当 `brand_id` 尚未存在时 object_key MUST 使用品牌 Logo pending 目录
- **AND** 系统返回可被浏览器实际加载的 URL 引用
- **AND** 创建/更新品牌时可写入 `logo_object_key`。

#### Scenario: 品牌 Logo 保存后正式化

- **GIVEN** 新建品牌表单引用 pending Logo
- **WHEN** 品牌创建成功并获得 `brand_id`
- **THEN** 系统 MUST 将 Logo 原图和已生成派生图 formalize 到 `images/default/brand-logos/{brand_id}/`
- **AND** `brands.logo_object_key` MUST 指向正式目录 key
- **AND** 关闭并重新打开编辑弹窗后 MUST 回显正式受控 URL
- **AND** 历史 Logo key 在迁移前 MUST 继续可读。
