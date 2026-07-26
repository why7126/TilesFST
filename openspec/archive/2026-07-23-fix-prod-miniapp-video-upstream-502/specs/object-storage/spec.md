## MODIFIED Requirements

### Requirement: 媒体对象必须可受控读取

系统 MUST 提供受控媒体读取能力，使上传响应中的 URL 能从 MinIO 读取对象并返回给授权或允许访问的客户端。读取链路 MUST 校验 object_key 或签名有效性，MUST 防止路径穿越、绝对路径读取、反斜杠绕过、重复斜杠绕过和内部路径泄露。

#### Scenario: 读取已上传对象

- **GIVEN** 对象已写入 MinIO `MINIO_BUCKET`
- **WHEN** 客户端访问上传响应返回的 `/media/{object_key}` 或等价 URL
- **THEN** 系统 MUST 从 MinIO 读取对象
- **AND** 返回内容的 MIME Type MUST 与对象类型匹配或可被浏览器正确处理
- **AND** 对视频对象，生产或生产等价 smoke MUST 确认响应不是 Nginx 502 HTML 页面。

#### Scenario: 对象不存在

- **WHEN** 客户端请求不存在的媒体对象
- **THEN** 系统 MUST 返回 404 或等价媒体不存在错误
- **AND** MUST NOT 暴露内部存储路径、Bucket 权限细节或 MinIO 原始错误堆栈
- **AND** 该错误 MUST 可从后端日志或运维证据中与生产 upstream 502 区分。

### Requirement: 生产 MinIO 必须持久化并保持单桶策略

生产 Docker Compose MUST 继续使用 MinIO 存储媒体对象，MUST 为 MinIO 配置持久化 volume，MUST 通过 `minio-init` 或等价初始化流程创建单桶 `MINIO_BUCKET`，并 MUST 将桶权限设置为最小权限。生产环境 `MINIO_ACCESS_KEY` 与 `MINIO_SECRET_KEY` MUST 使用非默认值。生产环境上传、媒体 URL、`object_key` 前缀和受控读取规则 MUST 与既有 object-storage capability 保持兼容。

#### Scenario: 生产媒体上传和读取可用

- **GIVEN** 生产 backend 已连接外部 MySQL 和 MinIO
- **WHEN** `admin` 完成一次图片或视频上传
- **THEN** 对象 MUST 写入 `MINIO_BUCKET`
- **AND** 上传响应中的 `/media/{object_key}` 或等价 URL MUST 可读取该对象
- **AND** 重启 backend、web、minio 后对象 MUST 仍可访问
- **AND** 小程序视频播放所需的实际 `/media/{object_key}` MUST 返回可播放视频 Content-Type，而不是 Nginx 502 或 SPA HTML。
