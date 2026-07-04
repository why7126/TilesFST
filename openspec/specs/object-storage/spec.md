# 对象存储规范

## Purpose
定义对象存储单桶策略、管理端上传写入、媒体受控读取和对象 Key 前缀规则，确保图片、视频与后续媒体资源统一经后端授权写入 MinIO。
## Requirements
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

### Requirement: 媒体对象必须可受控读取

系统 MUST 提供受控媒体读取能力，使上传响应中的 URL 能从 MinIO 读取对象并返回给授权或允许访问的客户端。读取链路 MUST 校验 object_key 或签名有效性，MUST 防止路径穿越、绝对路径读取、反斜杠绕过、重复斜杠绕过和内部路径泄露。

#### Scenario: 读取已上传对象

- **GIVEN** 对象已写入 MinIO `MINIO_BUCKET`
- **WHEN** 客户端访问上传响应返回的 `/media/{object_key}` 或等价 URL
- **THEN** 系统 MUST 从 MinIO 读取对象
- **AND** 返回内容的 MIME Type MUST 与对象类型匹配或可被浏览器正确处理

#### Scenario: 拒绝非法 object_key

- **WHEN** 客户端请求包含 `..`、绝对路径、空路径、反斜杠或重复斜杠的媒体 URL
- **THEN** 系统 MUST 拒绝请求并返回 4xx 错误
- **AND** MUST NOT 查询本地任意路径或 MinIO 任意未校验对象

#### Scenario: 对象不存在

- **WHEN** 客户端请求不存在的媒体对象
- **THEN** 系统 MUST 返回 404 或等价媒体不存在错误
- **AND** MUST NOT 暴露内部存储路径、Bucket 权限细节或 MinIO 原始错误堆栈

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

### Requirement: 生产 MinIO 必须持久化并保持单桶策略

生产 Docker Compose MUST 继续使用 MinIO 存储媒体对象，MUST 为 MinIO 配置持久化 volume，MUST 通过 `minio-init` 或等价初始化流程创建单桶 `MINIO_BUCKET`，并 MUST 将桶权限设置为最小权限。生产环境 `MINIO_ACCESS_KEY` 与 `MINIO_SECRET_KEY` MUST 使用非默认值。生产环境上传、媒体 URL、`object_key` 前缀和受控读取规则 MUST 与既有 object-storage capability 保持兼容。

#### Scenario: 生产 Compose 初始化单桶

- **WHEN** 运维启动生产 Compose
- **THEN** `minio-init` 或等价流程 MUST 创建 `MINIO_BUCKET`
- **AND** MUST NOT 创建额外业务 Bucket
- **AND** MinIO 数据 MUST 写入持久化 volume

#### Scenario: 生产媒体上传和读取可用

- **GIVEN** 生产 backend 已连接外部 MySQL 和 MinIO
- **WHEN** `admin` 完成一次图片上传
- **THEN** 对象 MUST 写入 `MINIO_BUCKET`
- **AND** 上传响应中的 `/media/{object_key}` 或等价 URL MUST 可读取该对象
- **AND** 重启 backend、web、minio 后对象 MUST 仍可访问

### Requirement: 外部 MinIO 生产部署必须保持单桶和受控读取策略

当生产环境使用客户已提供的外部 MinIO/S3 兼容对象存储时，系统 MUST 仍使用单桶 `MINIO_BUCKET` 与既有对象 Key 前缀策略。外部 bucket MUST 由运维提前创建，并设置最小权限；backend MUST 通过授权凭据读写对象，Web MUST 继续通过 backend `/media/{object_key}` 反代受控读取，不得要求前端直连对象存储写入。

#### Scenario: 外部 MinIO 上传和读取可用

- **GIVEN** backend 已通过 `MINIO_ENDPOINT` 连接外部 MinIO
- **AND** `MINIO_BUCKET` 已存在且凭据具备读写权限
- **WHEN** `admin` 完成一次图片上传
- **THEN** 对象 MUST 写入外部 `MINIO_BUCKET`
- **AND** 上传响应中的 `/media/{object_key}` MUST 可通过 backend 读取
