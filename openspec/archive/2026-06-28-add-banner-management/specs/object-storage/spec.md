## MODIFIED Requirements

### Requirement: 管理端上传必须写入 MinIO 单桶

系统 MUST 将管理端上传的头像、品牌 Logo、SKU 图片、SKU 视频、**Banner 运营图**和后续媒体对象写入 MinIO 单桶 `MINIO_BUCKET`。默认 Bucket MUST 为 `tile-info-platform`。上传链路 MUST 经后端授权、MIME 校验、对象 Key 校验和对象存储适配层写入；前端 MUST NOT 直连未授权 MinIO。系统 MUST NOT 仅将业务上传对象保存到本地 `UPLOAD_DIR` 后即返回成功。对象存储迁移完成后，项目 MUST 提供 legacy 本地上传残留（`data/uploads` 业务孤儿文件）的清理策略或脚本，并 MUST 在文档中澄清 `data/minio` 与 `data/uploads` 的职责边界；清理 MUST NOT 删除 MinIO 中仍被数据库引用的有效对象。

图片上传大小上限 MUST 由环境变量 `MAX_IMAGE_SIZE_MB` 控制；视频上传大小上限 MUST 由环境变量 `MAX_VIDEO_SIZE_MB` 控制。图片 MIME 白名单 MUST 由 `ALLOWED_IMAGE_TYPES`（逗号分隔）控制；视频 MIME 白名单 MUST 由 `ALLOWED_VIDEO_TYPES`（逗号分隔）控制。超限或 MIME 不符 MUST 由后端返回 400 及统一错误码（`FILE_SIZE_EXCEEDED` / `FILE_TYPE_NOT_ALLOWED`），MUST NOT 依赖 Nginx 413 作为业务校验手段。

#### Scenario: 图片上传受 env 大小与 MIME 约束

- **GIVEN** 后端已加载 `MAX_IMAGE_SIZE_MB` 与 `ALLOWED_IMAGE_TYPES`
- **WHEN** 客户端经授权上传接口提交图片
- **THEN** MIME 不在白名单 MUST 返回 400 及 `FILE_TYPE_NOT_ALLOWED`
- **AND** 超过 `MAX_IMAGE_SIZE_MB` MUST 返回 400 及 `FILE_SIZE_EXCEEDED`
- **AND** 合法图片在限制内 MUST 写入 `MINIO_BUCKET` 并返回 `object_key`

#### Scenario: Banner 运营图上传

- **WHEN** 客户端经 `POST /api/v1/admin/uploads/banner-images` 提交 Banner 运营图
- **THEN** 对象 MUST 写入 `MINIO_BUCKET`
- **AND** 返回的 `object_key` MUST 可用于 `banners.image_object_key`

#### Scenario: 视频上传受 env 大小与 MIME 约束

- **GIVEN** 后端已加载 `MAX_VIDEO_SIZE_MB` 与 `ALLOWED_VIDEO_TYPES`
- **WHEN** 客户端经授权上传接口提交 SKU 视频
- **THEN** MIME 不在白名单 MUST 返回 400 及 `FILE_TYPE_NOT_ALLOWED`
- **AND** 超过 `MAX_VIDEO_SIZE_MB` MUST 返回 400 及 `FILE_SIZE_EXCEEDED`
- **AND** 合法视频在限制内 MUST 写入 `MINIO_BUCKET` 且对象 Key MUST 以 `videos/` 开头

#### Scenario: Docker Web 路径大体积 MP4 可达后端

- **GIVEN** Docker Compose Web 入口 `http://localhost:3000` 与 Nginx 已配置足够大的 `client_max_body_size`
- **WHEN** `admin` 上传 2MB～50MB 合法 MP4（在 `MAX_VIDEO_SIZE_MB` 内）
- **THEN** `POST /api/v1/admin/uploads/tile-videos` MUST 返回 200
- **AND** MUST NOT 返回 413 Request Entity Too Large

### Requirement: 对象 Key 必须使用标准前缀

系统 MUST 使用 `rules/object-storage.md` 定义的单桶标准前缀生成对象 Key。原始图片和文件 MUST 使用 `original/`，原始视频 MUST 使用 `videos/`，视频封面 MUST 使用 `videos/covers/`，处理后资源 MUST 使用 `processed/` 或更具体标准前缀。系统 MUST NOT 使用用户原始文件名作为对象 Key。**Banner 运营图** MUST 使用 `images/default/banners/{uuid}.{ext}`（当 `update-object-storage-key-layout` 已生效时 MUST 使用 `images/` 语义前缀；未生效前实现 MUST 与 `build_upload_object_key()` 当前项目约定一致并在 apply 时对齐）。

#### Scenario: 图片对象 Key 生成

- **WHEN** 用户上传头像、品牌 Logo 或 SKU 图片
- **THEN** 对象 Key MUST 使用 `original/` 前缀
- **AND** 对象 Key MUST 包含租户或默认命名空间、资源类型、日期片段和随机文件名
- **AND** 文件扩展名 MUST 来自后端 MIME 白名单映射

#### Scenario: Banner 对象 Key 生成

- **WHEN** 用户上传 Banner 运营图
- **THEN** 对象 Key MUST 匹配 `images/default/banners/{uuid}.{ext}`（或与当期 `build_upload_object_key('images', 'banners', ...)` 等价形态）
- **AND** MUST NOT 使用用户原始文件名

#### Scenario: 视频对象 Key 生成

- **WHEN** 用户上传 SKU 视频
- **THEN** 对象 Key MUST 使用 `videos/` 前缀
- **AND** 文件扩展名 MUST 来自后端 MIME 白名单映射

#### Scenario: 不新增业务 Bucket

- **WHEN** 上传头像、品牌 Logo、SKU 图片、SKU 视频或 Banner 运营图
- **THEN** 系统 MUST 使用同一个 `MINIO_BUCKET`
- **AND** MUST NOT 创建额外业务 Bucket，除非后续 OpenSpec Change 明确要求
