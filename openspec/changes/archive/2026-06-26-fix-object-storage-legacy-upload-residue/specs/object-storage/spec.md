## MODIFIED Requirements

### Requirement: 管理端上传必须写入 MinIO 单桶

系统 MUST 将管理端上传的头像、品牌 Logo、SKU 图片、SKU 视频和后续媒体对象写入 MinIO 单桶 `MINIO_BUCKET`。默认 Bucket MUST 为 `tile-info-platform`。上传链路 MUST 经后端授权、MIME 校验、对象 Key 校验和对象存储适配层写入；前端 MUST NOT 直连未授权 MinIO。系统 MUST NOT 仅将业务上传对象保存到本地 `UPLOAD_DIR` 后即返回成功。对象存储迁移完成后，项目 MUST 提供 legacy 本地上传残留（`data/uploads` 业务孤儿文件）的清理策略或脚本，并 MUST 在文档中澄清 `data/minio` 与 `data/uploads` 的职责边界；清理 MUST NOT 删除 MinIO 中仍被数据库引用的有效对象。

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

#### Scenario: legacy uploads 孤儿清理

- **GIVEN** 本地或 Docker 环境存在 BUG-0006 修复前写入的 `data/uploads` 业务文件
- **WHEN** 执行项目提供的 legacy 清理步骤或脚本
- **THEN** MUST 删除或标记清除与数据库媒体字段无关联的 uploads 孤儿文件
- **AND** MUST NOT 删除 MinIO 中仍被引用的有效对象
- **AND** 清理后新上传 MUST 仍仅写入 `MINIO_BUCKET`

#### Scenario: 新上传不得写入 data/uploads

- **GIVEN** 对象存储迁移与 legacy 清理已完成
- **WHEN** 管理端上传头像、品牌 Logo、SKU 图片或 SKU 视频
- **THEN** 对象 MUST 仅写入 MinIO
- **AND** `data/uploads` 下 MUST NOT 新增与 object key 对应的业务媒体文件
