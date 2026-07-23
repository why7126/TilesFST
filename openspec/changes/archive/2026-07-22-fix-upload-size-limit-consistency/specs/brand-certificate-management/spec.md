## MODIFIED Requirements

### Requirement: 品牌证书文件上传与预览

系统 MUST 支持品牌证书文件经后端鉴权上传至 MinIO/S3 兼容对象存储单桶。证书文件 MUST 支持 JPG、PNG、WebP 和 PDF。证书文件大小上限 MUST 使用文档 / 文件类 effective 上传限制（例如 `media.max_file_size_mb` merge `MAX_FILE_SIZE_MB`），并 MUST 与管理端系统设置、前端提示、后端校验和部署代理配置一致；MUST NOT 仅使用不可配置的 20MB 硬编码作为大小限制事实源。上传链路 MUST 校验 MIME、大小和对象 Key，MUST 返回可受控读取的 `file_url`、`file_key`、文件名、MIME 和大小。前端 MUST NOT 直连未授权对象存储。

#### Scenario: 上传合法证书文件

- **WHEN** 已授权管理端用户上传合法 JPG、PNG、WebP 或 PDF 证书文件，且文件大小在文档 / 文件类 effective 上限内
- **THEN** 系统 MUST 将对象写入对象存储单桶
- **AND** MUST 返回 `file_key` 和可读取的 `file_url`
- **AND** 对象 Key MUST NOT 使用用户原始文件名

#### Scenario: 上传约 23MB PDF 证书文件

- **GIVEN** effective 文档 / 文件上传上限大于等于 23MB
- **WHEN** 已授权管理端用户上传约 23MB 合法 PDF 证书文件
- **THEN** 上传 MUST 成功
- **AND** MUST NOT 被硬编码 20MB 限制拒绝

#### Scenario: 上传文件类型非法

- **WHEN** 用户上传非 JPG、PNG、WebP 或 PDF 文件
- **THEN** 系统 MUST 返回 HTTP 400
- **AND** 错误码 MUST 为 `CERTIFICATE_FILE_TYPE_INVALID` 或统一文件类型错误码

#### Scenario: 上传文件过大

- **WHEN** 用户上传超过文档 / 文件类 effective 上限的证书文件
- **THEN** 系统 MUST 返回 HTTP 400
- **AND** 错误码 MUST 为 `CERTIFICATE_FILE_TOO_LARGE` 或统一文件大小错误码
- **AND** 错误提示 MUST 包含当前有效大小限制或等价可诊断信息
- **AND** Web Docker 入口 MUST NOT 以 Nginx 413 作为业务校验结果

#### Scenario: 预览证书文件

- **WHEN** 管理员点击图片证书或 PDF 证书的预览入口
- **THEN** 图片证书 MUST 支持大图预览
- **AND** PDF 证书 MUST 支持新窗口或等价受控 URL 预览
- **AND** 预览失败时 MUST 展示稳定错误提示
