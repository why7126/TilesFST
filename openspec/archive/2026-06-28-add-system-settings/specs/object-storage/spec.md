## MODIFIED Requirements

### Requirement: 管理端上传必须写入 MinIO 单桶

系统 MUST 将管理端上传的头像、品牌 Logo、SKU 图片、SKU 视频和后续媒体对象写入 MinIO 单桶 `MINIO_BUCKET`。默认 Bucket MUST 为 `tile-info-platform`。上传链路 MUST 经后端授权、MIME 校验、对象 Key 校验和对象存储适配层写入；前端 MUST NOT 直连未授权 MinIO。系统 MUST NOT 仅将业务上传对象保存到本地 `UPLOAD_DIR` 后即返回成功。对象存储迁移完成后，项目 MUST 提供 legacy 本地上传残留（`data/uploads` 业务孤儿文件）的清理策略或脚本，并 MUST 在文档中澄清 `data/minio` 与 `data/uploads` 的职责边界；清理 MUST NOT 删除 MinIO 中仍被数据库引用的有效对象。

图片上传大小上限 MUST 由 **effective** 配置 `media.max_image_size_mb` 决定（SQLite `system_settings` 覆盖值 merge 环境变量 `MAX_IMAGE_SIZE_MB` 默认值）；视频上传大小上限 MUST 由 **effective** `media.max_video_size_mb` merge `MAX_VIDEO_SIZE_MB` 决定。图片 MIME 白名单 MUST 由 **effective** `media.allowed_image_types` merge `ALLOWED_IMAGE_TYPES` 决定；视频 MIME 白名单 MUST 由 **effective** `media.allowed_video_types` merge `ALLOWED_VIDEO_TYPES` 决定。Effective 值 MUST 在每次上传请求时读取，MUST NOT 仅使用进程启动时的 env snapshot。超限或 MIME 不符 MUST 由后端返回 400 及统一错误码（`FILE_SIZE_EXCEEDED` / `FILE_TYPE_NOT_ALLOWED`），MUST NOT 依赖 Nginx 413 作为业务校验手段。

#### Scenario: 图片上传受 effective 大小与 MIME 约束

- **GIVEN** 管理员已通过系统设置将 effective `max_image_size_mb` 设为 5
- **WHEN** 客户端经授权上传接口提交 6MB 合法 MIME 图片
- **THEN** MUST 返回 400 及 `FILE_SIZE_EXCEEDED`
- **AND** MUST NOT 仍按旧 env 默认值校验

#### Scenario: 视频上传受 env 大小与 MIME 约束

- **GIVEN** 后端已加载 effective `MAX_VIDEO_SIZE_MB` 与 allowed video types
- **WHEN** 客户端经授权上传接口提交 SKU 视频
- **THEN** MIME 不在白名单 MUST 返回 400 及 `FILE_TYPE_NOT_ALLOWED`
- **AND** 超过 effective 上限 MUST 返回 400 及 `FILE_SIZE_EXCEEDED`
- **AND** 合法视频在限制内 MUST 写入 `MINIO_BUCKET` 且对象 Key MUST 以 `videos/` 开头

#### Scenario: Docker Web 路径大体积 MP4 可达后端

- **GIVEN** Docker Compose Web 入口 `http://localhost:3000` 与 Nginx 已配置足够大的 `client_max_body_size`
- **WHEN** `admin` 上传 2MB～50MB 合法 MP4（在 effective `MAX_VIDEO_SIZE_MB` 内）
- **THEN** `POST /api/v1/admin/uploads/tile-videos` MUST 返回 200
- **AND** MUST NOT 返回 413 Request Entity Too Large
