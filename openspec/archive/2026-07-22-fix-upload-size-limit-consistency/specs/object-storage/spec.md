## MODIFIED Requirements

### Requirement: 管理端上传必须写入 MinIO 单桶

系统 MUST 将管理端上传的头像、品牌 Logo、SKU 图片、SKU 视频、品牌证书文件和后续媒体对象写入 MinIO/S3 兼容对象存储单桶。上传链路 MUST 经后端授权、MIME 校验、大小校验、对象 Key 校验和对象存储适配层写入；前端、小程序和管理端 MUST NOT 直连未授权对象存储写入。系统 MUST NOT 仅将业务上传对象保存到本地 `UPLOAD_DIR` 后即返回成功。

图片上传大小上限 MUST 由 **effective** 配置 `media.max_image_size_mb` 决定（SQLite `system_settings` 覆盖值 merge 环境变量 `MAX_IMAGE_SIZE_MB` 默认值）；视频上传大小上限 MUST 由 **effective** `media.max_video_size_mb` merge `MAX_VIDEO_SIZE_MB` 决定；文档 / 文件 / 证书类上传大小上限 MUST 由 **effective** `media.max_file_size_mb` 或等价文件类配置 merge 环境变量默认值决定。图片 MIME 白名单 MUST 由 **effective** `media.allowed_image_types` merge `ALLOWED_IMAGE_TYPES` 决定；视频 MIME 白名单 MUST 由 **effective** `media.allowed_video_types` merge `ALLOWED_VIDEO_TYPES` 决定；文档类 MIME 白名单 MUST 与对应业务上传入口显式定义并返回可诊断错误。Effective 值 MUST 在每次上传请求时读取，MUST NOT 仅使用进程启动时的 env snapshot 或不可配置的硬编码大小上限。

超限、MIME 不符或对象存储不可用 MUST 由后端返回统一结构错误响应和明确错误码，MUST NOT 依赖 Nginx 413 作为业务校验手段。Docker / Nginx / 生产代理请求体大小和超时配置 MUST 大于等于后端最大 effective 上传限制。

#### Scenario: 图片上传受 effective 大小与 MIME 约束

- **GIVEN** 管理员已通过系统设置将 effective `max_image_size_mb` 设为 25
- **WHEN** 客户端经授权上传接口提交 23MB 合法 MIME 图片
- **THEN** 上传 MUST 成功并写入对象存储
- **AND** 上传响应 MUST 返回 `/media/{object_key}` 或等价受控读取 URL

#### Scenario: 视频上传受 effective 大小与 MIME 约束

- **GIVEN** 后端已加载 effective `MAX_VIDEO_SIZE_MB` 与 allowed video types
- **WHEN** 客户端经授权上传接口提交 23MB 合法 MP4
- **THEN** 上传 MUST 成功并写入对象存储
- **AND** 对象 Key MUST 以 `videos/` 开头
- **AND** MIME 不在白名单或超过 effective 上限时 MUST 返回统一错误响应

#### Scenario: 文档上传受 effective 文件类大小约束

- **GIVEN** 管理员已通过系统设置或环境变量将 effective 文件类上传上限设为 25MB
- **WHEN** 客户端经授权上传接口提交 23MB 合法 PDF 或证书文件
- **THEN** 上传 MUST 成功并写入对象存储
- **AND** 对象 Key MUST 使用 `files/` 或对应标准文件前缀
- **AND** MUST NOT 被不可配置的 20MB 硬编码限制拒绝

#### Scenario: 超限错误可诊断

- **WHEN** 客户端上传超过当前类型 effective 上限的图片、视频或文档
- **THEN** 后端 MUST 返回 400 和统一文件大小错误码
- **AND** 错误提示 MUST 包含当前类型的有效大小限制或等价可诊断信息
- **AND** MUST NOT 返回 500、无响应、上传卡住或暴露内部路径

#### Scenario: Docker Web 路径大体积文件可达后端

- **GIVEN** Docker Compose Web 入口与 Nginx 已配置足够大的 `client_max_body_size`
- **WHEN** `admin` 上传 23MB 合法图片、视频或文档（在对应 effective 限制内）
- **THEN** 对应上传接口 MUST 返回 200
- **AND** MUST NOT 返回 413 Request Entity Too Large
