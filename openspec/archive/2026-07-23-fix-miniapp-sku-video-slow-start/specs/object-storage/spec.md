## MODIFIED Requirements

### Requirement: 媒体对象必须可受控读取

系统 MUST 提供受控媒体读取能力，使上传响应中的 URL 能从 MinIO/S3 兼容对象存储读取对象并返回给授权或允许访问的客户端。读取链路 MUST 校验 object_key 或签名有效性，MUST 防止路径穿越、绝对路径读取、反斜杠绕过、重复斜杠绕过和内部路径泄露。对视频媒体对象，受控读取链路 MUST 支持播放器所需的 Range 分段读取能力，避免大视频必须整文件读取后才能起播。

#### Scenario: 读取已上传对象

- **GIVEN** 对象已写入对象存储 bucket
- **WHEN** 客户端访问上传响应返回的 `/media/{object_key}` 或等价 URL
- **THEN** 系统 MUST 从对象存储读取对象
- **AND** 返回内容的 MIME Type MUST 与对象类型匹配或可被浏览器正确处理
- **AND** 对视频对象，生产或生产等价 smoke MUST 确认响应不是 Nginx 502 HTML 页面。

#### Scenario: 视频 Range 分段读取

- **GIVEN** 对象存储中存在合法视频对象
- **WHEN** 客户端请求 `/media/{object_key}` 并携带 `Range: bytes=0-1023`
- **THEN** 系统 MUST 返回 `206 Partial Content`
- **AND** 响应 MUST 包含 `Accept-Ranges: bytes`
- **AND** 响应 MUST 包含合法 `Content-Range`
- **AND** 响应 `Content-Length` MUST 与返回分段字节数一致
- **AND** 响应 `Content-Type` MUST 为视频对象可播放 MIME Type
- **AND** 系统 MUST NOT 为满足 Range 请求暴露对象存储 endpoint、bucket 名称、access key、secret key 或 raw object URL。

#### Scenario: 非 Range 视频读取兼容

- **GIVEN** 对象存储中存在合法视频对象
- **WHEN** 客户端不携带 `Range` 请求 `/media/{object_key}`
- **THEN** 系统 MAY 返回完整视频对象
- **AND** 响应 MUST 保持可播放 `Content-Type`
- **AND** 图片、PDF 或其他非视频媒体读取 SHALL NOT 因视频 Range 支持而回归。

#### Scenario: 非法或不可满足 Range

- **WHEN** 客户端对视频对象发起格式非法或超出对象大小范围的 Range 请求
- **THEN** 系统 SHOULD 返回 `416 Range Not Satisfiable` 或等价可诊断错误
- **AND** 响应 MUST NOT 暴露内部存储路径、Bucket 权限细节或底层 SDK 堆栈。

#### Scenario: 对象不存在

- **WHEN** 客户端请求不存在的媒体对象
- **THEN** 系统 MUST 返回 404 或等价媒体不存在错误
- **AND** MUST NOT 暴露内部存储路径、Bucket 权限细节或 MinIO/S3 原始错误堆栈
- **AND** 该错误 MUST 可从后端日志或运维证据中与生产 upstream 502 区分。
