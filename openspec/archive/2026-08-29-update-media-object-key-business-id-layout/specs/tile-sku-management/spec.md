## MODIFIED Requirements

### Requirement: SKU 图片与视频上传

系统 MUST 支持 SKU 图片与视频经后端授权上传至 MinIO。图片 MIME MUST 包含 JPG、PNG、WebP；视频 MUST 支持 MP4（见 `rules/media.md`）。前端 MUST NOT 直连未授权对象存储。每个 SKU MUST 支持多张图片并指定一张主图；MUST 支持多个视频。SKU 弹窗商品图片区 MUST 支持移除任意已添加图片。设置某张图片为主图后，该图片 MUST 立即成为唯一主图并移动到图片列表第一位；移除当前主图后，如果仍有其它图片，系统 MUST 自动选择新主图并将其置于第一位。图片移除 MUST 只解除 SKU 关联，不触发对象存储物理删除。

SKU 图片在 `tile_id` 已存在时 MUST 使用 `images/default/tiles/{tile_id}/{uuid}.{ext}`，SKU 视频在 `tile_id` 已存在时 MUST 使用 `videos/default/tiles/{tile_id}/{uuid}.{ext}`。新建 SKU 前上传的图片或视频 MUST 使用对应 pending 目录，并在 SKU 创建成功后 formalize 到正式 `tiles/{tile_id}` 目录。SKU 图片上传链路 SHALL 生成真实同目录缩略图；对于尺寸大于缩略图目标尺寸的支持图片，`.thumb` 对象 SHALL 经过后端 resize / compress 处理，SHALL NOT 只是原图 bytes 的复制品。历史 SKU pending 主图、旧目录视频 key 和过渡目录 MUST 保持读取兼容，迁移或正式化 MUST 保持主图顺序、主图唯一和视频元数据。

#### Scenario: SKU 图片上传生成真实缩略图

- **GIVEN** 管理端上传一张尺寸大于缩略图目标尺寸的 SKU 图片
- **WHEN** 上传接口成功写入原图对象
- **THEN** 后端 SHALL 在同一 SKU 业务对象目录或 pending 目录写入 `.thumb` 缩略图对象
- **AND** 缩略图 SHALL 保持比例并限制在约定最大宽高内
- **AND** 缩略图 bytes SHALL NOT 与原图 bytes 完全一致
- **AND** 上传响应中的原图 `/media/{object_key}` SHALL 继续可读取。

#### Scenario: 新建 SKU 保存后正式化图片和视频

- **GIVEN** 新建 SKU 表单引用 pending 图片或 pending 视频
- **WHEN** SKU 创建成功并获得 `tile_id`
- **THEN** 系统 MUST 将 SKU 图片 formalize 到 `images/default/tiles/{tile_id}/`
- **AND** 系统 MUST 将 SKU 视频 formalize 到 `videos/default/tiles/{tile_id}/`
- **AND** `tile_images` 与 `tile_videos` 引用 MUST 指向 formalize 后的正式 key
- **AND** 主图唯一、图片排序、视频排序和公开状态校验 MUST 保持不变。
