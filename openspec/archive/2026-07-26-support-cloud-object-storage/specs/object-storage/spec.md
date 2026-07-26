## ADDED Requirements

### Requirement: 对象存储配置必须支持云上 S3 兼容服务

系统 MUST 支持通过后端对象存储适配层连接 MinIO、自建 S3 兼容服务、腾讯云 COS、火山云 TOS 等云上对象存储。应用配置 MUST 统一使用 `OBJECT_STORAGE_*` 表达 provider、endpoint、access key、secret key、bucket、secure/TLS、region、path-style/virtual-host 风格、bucket 自动创建策略和对象前缀。后端应用 MUST NOT 同时暴露重复的 `MINIO_*` 应用配置；MinIO 容器自身所需的 `MINIO_ROOT_USER` / `MINIO_ROOT_PASSWORD` 不属于后端应用配置。配置摘要不得在日志、接口响应、文档示例或前端页面中暴露 secret key。

#### Scenario: 腾讯云 COS 使用 S3 兼容配置上传

- **GIVEN** 生产环境已配置腾讯云 COS 的 S3 兼容 endpoint、region、bucket、TLS 和最小权限凭据
- **AND** `OBJECT_STORAGE_AUTO_CREATE_BUCKET=false`
- **WHEN** 管理员通过后端授权上传接口上传品牌 Logo
- **THEN** 对象 MUST 写入配置的 COS bucket
- **AND** 上传响应 MUST 继续返回 `/media/{object_key}` 形式的受控读取 URL
- **AND** 响应 MUST NOT 暴露 COS secret key、bucket 权限细节或 raw signed URL

#### Scenario: 火山云 TOS 使用 S3 兼容配置读取

- **GIVEN** 生产环境已配置火山云 TOS 的 S3 兼容 endpoint、region、bucket、TLS 和最小权限凭据
- **AND** bucket 中存在已上传对象
- **WHEN** 客户端访问 `/media/{object_key}`
- **THEN** 后端 MUST 从 TOS 读取对象并返回媒体内容
- **AND** 前端 MUST NOT 直连 TOS 写入或读取未授权对象

#### Scenario: 云上对象存储不自动创建 bucket

- **GIVEN** provider 配置为云上 S3 兼容对象存储
- **AND** `OBJECT_STORAGE_AUTO_CREATE_BUCKET=false`
- **WHEN** bucket 不存在、region 不匹配或凭据无权访问 bucket
- **THEN** 上传 MUST 返回对象存储不可用错误
- **AND** 系统 MUST NOT 尝试在云上隐式创建业务 bucket
- **AND** 错误响应 MUST NOT 暴露底层凭据、内部 endpoint 白名单或完整 SDK 堆栈

## MODIFIED Requirements

### Requirement: 对象 Key 必须使用标准前缀

系统 MUST 使用 `rules/object-storage.md` 定义的单桶标准前缀生成对象 Key。图片类上传 MUST 使用 `images/`，原始视频 MUST 使用 `videos/`，视频封面 MUST 使用 `videos/covers/`，文件类资源 MUST 使用 `files/`，处理后资源 MUST 使用 `processed/` 或更具体标准前缀。系统 MUST NOT 使用用户原始文件名作为对象 Key。`original/` 仅允许作为存量兼容前缀，新上传 MUST NOT 使用。**Banner 运营图** MUST 使用 `images/default/banners/{uuid}.{ext}`（当 `update-object-storage-key-layout` 已生效时 MUST 使用 `images/` 语义前缀；未生效前实现 MUST 与 `build_upload_object_key()` 当前项目约定一致并在 apply 时对齐）。

#### Scenario: 图片对象 Key 生成

- **WHEN** 用户上传头像、品牌 Logo 或 SKU 图片
- **THEN** 对象 Key MUST 使用 `images/` 前缀
- **AND** 对象 Key MUST 包含租户或默认命名空间、资源类型和随机文件名
- **AND** 文件扩展名 MUST 来自后端 MIME 白名单映射
- **AND** 新上传 MUST NOT 使用 `original/` 前缀

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
- **THEN** 系统 MUST 使用同一个对象存储 bucket
- **AND** MUST NOT 创建额外业务 Bucket，除非后续 OpenSpec Change 明确要求

### Requirement: 外部 MinIO 生产部署必须保持单桶和受控读取策略

当生产环境使用客户已提供的外部 MinIO、自建 S3 兼容服务或云上对象存储（如腾讯云 COS、火山云 TOS）时，系统 MUST 仍使用单桶 `OBJECT_STORAGE_BUCKET` 与既有对象 Key 前缀策略。外部 bucket MUST 由运维提前创建，并设置最小权限；backend MUST 通过授权凭据读写对象，Web MUST 继续通过 backend `/media/{object_key}` 反代受控读取，不得要求前端直连对象存储写入。

#### Scenario: 外部对象存储上传和读取可用

- **GIVEN** backend 已通过对象存储 endpoint 连接外部 MinIO、COS、TOS 或其他 S3 兼容服务
- **AND** 配置的 bucket 已存在且凭据具备最小读写权限
- **WHEN** `admin` 完成一次图片上传
- **THEN** 对象 MUST 写入配置的外部 bucket
- **AND** 上传响应中的 `/media/{object_key}` MUST 可通过 backend 读取

#### Scenario: 前端不暴露云存储连接细节

- **GIVEN** 系统使用云上对象存储承载媒体
- **WHEN** 管理端、店主端或小程序展示上传后的媒体
- **THEN** 客户端 MUST 使用后端返回的受控媒体 URL
- **AND** 客户端 MUST NOT 依赖云厂商 endpoint、bucket 名称、access key、secret key 或 raw object URL
