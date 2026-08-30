## MODIFIED Requirements

### Requirement: Banner 图片上传

Banner 自定义上传 MUST 经后端授权写入 MinIO 单桶。新上传 Banner 图片在 `banner_id` 已存在时 MUST 使用 `images/default/banners/{banner_id}/{uuid}.{ext}` 正式目录；在 Banner 创建前上传时 MUST 使用 `images/default/banners/pending/`，并在 Banner 创建成功后 formalize 到正式目录。上传 MUST 受 `MAX_IMAGE_SIZE_MB` 与 `ALLOWED_IMAGE_TYPES` 约束，并 MUST 继续返回 `object_key` 与 `/media/{object_key}` 或等价受控 URL。

历史 `images/default/banners/{uuid}.{ext}` 或等价旧目录 Banner 图片 MUST 保持读取兼容。存量迁移若改写 `banners.image_object_key`，MUST 通过 dry-run、apply、二次审计和幂等复跑验证；旧对象删除必须单独确认。

#### Scenario: Banner 图上传成功

- **WHEN** `admin` 经 `POST /api/v1/admin/uploads/banner-images` 上传合法 JPG/PNG/WebP
- **THEN** MUST 返回 `object_key` 与 `/media/{object_key}` URL
- **AND** 当 `banner_id` 已存在时 object_key MUST 以 `images/default/banners/{banner_id}/` 开头
- **AND** 当 `banner_id` 尚未存在时 object_key MUST 使用 Banner pending 目录
- **AND** 响应 MUST NOT 暴露对象存储 raw URL 或内部 endpoint。

#### Scenario: Banner 保存后正式化

- **GIVEN** 新建 Banner 表单引用 pending 自定义图片
- **WHEN** Banner 创建成功并获得 `banner_id`
- **THEN** 系统 MUST 将 Banner 图片原图和派生图 formalize 到 `images/default/banners/{banner_id}/`
- **AND** `banners.image_object_key` MUST 指向正式目录 key
- **AND** 小程序公开 Banner 查询继续返回后端受控 URL
- **AND** 历史 Banner 图片在迁移前 MUST 继续可读。
