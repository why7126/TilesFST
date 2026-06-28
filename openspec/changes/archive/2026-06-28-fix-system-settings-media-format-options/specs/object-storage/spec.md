## MODIFIED Requirements

### Requirement: 管理端上传必须写入 MinIO 单桶

图片上传大小上限 MUST 由 **effective** 配置 `media.max_image_size_mb` 决定（SQLite `system_settings` 覆盖值 merge 环境变量 `MAX_IMAGE_SIZE_MB` 默认值）；视频上传大小上限 MUST 由 **effective** `media.max_video_size_mb` merge `MAX_VIDEO_SIZE_MB` 决定。图片 MIME 白名单 MUST 由 **effective** `media.allowed_image_types` merge `ALLOWED_IMAGE_TYPES` 决定，env 默认 MUST 至少包含 `image/jpeg,image/png,image/webp,image/gif,image/svg+xml,image/bmp,image/tiff,image/heic`；视频 MIME 白名单 MUST 由 **effective** `media.allowed_video_types` merge `ALLOWED_VIDEO_TYPES` 决定，env 默认 MUST 至少包含 `video/mp4,video/quicktime,video/x-msvideo,video/webm,video/x-matroska,video/mpeg,video/3gpp`。Effective 值 MUST 在每次上传请求时读取。超限或 MIME 不符 MUST 返回 400 及 `FILE_SIZE_EXCEEDED` / `FILE_TYPE_NOT_ALLOWED`。

#### Scenario: 扩展图片 MIME 校验

- **GIVEN** effective `allowed_image_types` 含 `image/gif`
- **WHEN** 上传 `image/gif` 文件
- **THEN** MUST 接受
- **WHEN** 上传未启用 MIME
- **THEN** MUST 400 `FILE_TYPE_NOT_ALLOWED`

#### Scenario: 扩展视频 MIME 校验

- **GIVEN** effective `allowed_video_types` 含 `video/webm`
- **WHEN** 上传 `video/webm` 文件
- **THEN** MUST 接受
