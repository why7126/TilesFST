## ADDED Requirements

### Requirement: 管理端上传必须写入 MinIO 单桶

系统 MUST 将管理端上传的头像、品牌 Logo、SKU 图片、SKU 视频和后续媒体对象写入 MinIO 单桶 `MINIO_BUCKET`。默认 Bucket MUST 为 `tile-info-platform`。上传链路 MUST 经后端授权、MIME 校验、对象 Key 校验和对象存储适配层写入；前端 MUST NOT 直连未授权 MinIO。系统 MUST NOT 仅将业务上传对象保存到本地 `UPLOAD_DIR` 后即返回成功。

#### Scenario: 品牌 Logo 上传进入 MinIO

- **GIVEN** Docker Compose 环境已启动且 `minio-init` 已创建 `tile-info-platform`
- **WHEN** `admin` 或 `employee` 上传合法品牌 Logo
- **THEN** 系统 MUST 将对象写入 `MINIO_BUCKET`
- **AND** 对象 Key MUST 以 `original/` 开头
- **AND** MinIO bucket 中 MUST 能查询到该对象
- **AND** API 响应 MUST 返回 `object_key` 与可访问 URL

#### Scenario: SKU 图片上传进入 MinIO

- **WHEN** `admin` 或 `employee` 上传合法 SKU 图片
- **THEN** 系统 MUST 将对象写入 `MINIO_BUCKET`
- **AND** 对象 Key MUST 以 `original/` 开头
- **AND** 创建或更新 SKU 时可使用该 `object_key` 关联图片

#### Scenario: SKU 视频上传进入 MinIO

- **WHEN** `admin` 或 `employee` 上传合法 MP4 视频
- **THEN** 系统 MUST 将对象写入 `MINIO_BUCKET`
- **AND** 对象 Key MUST 以 `videos/` 开头
- **AND** 创建或更新 SKU 时可使用该 `object_key` 关联视频

#### Scenario: 对象存储不可用

- **GIVEN** MinIO 不可连接或目标 Bucket 不可用
- **WHEN** 用户上传合法文件
- **THEN** 系统 MUST 返回统一错误结构
- **AND** 错误码 MUST 表示对象存储不可用
- **AND** 响应 MUST NOT 暴露 MinIO AccessKey、SecretKey、内部 endpoint 或服务器绝对路径

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

系统 MUST 使用 `rules/object-storage.md` 定义的单桶标准前缀生成对象 Key。原始图片和文件 MUST 使用 `original/`，原始视频 MUST 使用 `videos/`，视频封面 MUST 使用 `videos/covers/`，处理后资源 MUST 使用 `processed/` 或更具体标准前缀。系统 MUST NOT 使用用户原始文件名作为对象 Key。

#### Scenario: 图片对象 Key 生成

- **WHEN** 用户上传头像、品牌 Logo 或 SKU 图片
- **THEN** 对象 Key MUST 使用 `original/` 前缀
- **AND** 对象 Key MUST 包含租户或默认命名空间、资源类型、日期片段和随机文件名
- **AND** 文件扩展名 MUST 来自后端 MIME 白名单映射

#### Scenario: 视频对象 Key 生成

- **WHEN** 用户上传 SKU 视频
- **THEN** 对象 Key MUST 使用 `videos/` 前缀
- **AND** 文件扩展名 MUST 来自后端 MIME 白名单映射

#### Scenario: 不新增业务 Bucket

- **WHEN** 上传头像、品牌 Logo、SKU 图片或 SKU 视频
- **THEN** 系统 MUST 使用同一个 `MINIO_BUCKET`
- **AND** MUST NOT 创建 `tile-images`、`tile-videos`、`tile-documents` 等额外业务 Bucket，除非后续 OpenSpec Change 明确要求
