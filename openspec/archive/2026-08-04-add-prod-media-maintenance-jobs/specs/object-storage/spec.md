## MODIFIED Requirements

### Requirement: 对象 Key 必须使用标准前缀

系统 MUST 使用 `rules/object-storage.md` 定义的单桶标准前缀生成对象 Key。图片类上传 MUST 使用 `images/`，原始视频 MUST 使用 `videos/`，视频封面 MUST 使用 `videos/covers/`，文件类资源 MUST 使用 `files/`，处理后资源 MUST 使用 `processed/` 或更具体标准前缀。系统 MUST NOT 使用用户原始文件名作为对象 Key。`original/` 仅允许作为存量兼容前缀，新上传 MUST NOT 使用。**Banner 运营图** MUST 使用 `images/default/banners/{uuid}.{ext}`（当 `update-object-storage-key-layout` 已生效时 MUST 使用 `images/` 语义前缀；未生效前实现 MUST 与 `build_upload_object_key()` 当前项目约定一致并在 apply 时对齐）。SKU 图片在新建前 MAY 使用 `images/default/tiles/pending/{uuid}.{ext}` 作为暂存 key；一旦绑定到 SKU 或进入公开展示，系统 MUST 使用可追溯到 SKU 的正式商品图片 key。品牌证书图片类对象 MUST 使用 `images/default/brand-certificates/{uuid}.{ext}` 或等价标准图片前缀；品牌证书 PDF 或其他文档类附件 MUST 使用 `files/` 前缀。历史对象迁移作业 MUST 支持 dry-run/apply、分批、幂等、生产 MySQL 和对象存储 provider 适配，并 MUST 脱敏输出。

#### Scenario: 图片对象 Key 生成

- **WHEN** 用户上传头像、品牌 Logo、SKU 图片或图片类品牌证书
- **THEN** 对象 Key MUST 使用 `images/` 前缀
- **AND** 对象 Key MUST 包含租户或默认命名空间、资源类型和随机文件名
- **AND** 文件扩展名 MUST 来自后端 MIME 白名单映射
- **AND** 新上传 MUST NOT 使用 `original/` 前缀

#### Scenario: 品牌证书图片对象 Key 生成

- **WHEN** 已授权管理端用户上传 JPG、PNG 或 WebP 品牌证书图片
- **THEN** 原图对象 Key MUST 位于 `images/default/brand-certificates/` 或等价标准图片前缀
- **AND** 缩略图对象 Key MUST 与原图保持同一图片资源归属，使用同目录 `.thumb` 或等价可追溯图片路径
- **AND** 系统 MUST NOT 为图片类品牌证书生成 `files/default/brand-certificates/` 或 `original/` 前缀的新对象 Key
- **AND** 上传响应、数据库引用和受控媒体 URL MUST 指向同一套新 Key。

#### Scenario: 品牌证书文档对象 Key 生成

- **WHEN** 已授权管理端用户上传 PDF 或其他文档类品牌证书附件
- **THEN** 对象 Key MUST 使用 `files/` 前缀
- **AND** 系统 MUST NOT 将文档类证书附件写入 `images/`
- **AND** 文件扩展名 MUST 来自后端 MIME 白名单映射。

#### Scenario: 历史品牌证书图片 Key 审计与迁移

- **GIVEN** 存量图片类品牌证书对象位于 `files/`、`original/` 或其他非标准图片前缀
- **WHEN** 运维执行历史 key 审计 dry-run
- **THEN** 输出 MUST 汇总待迁移图片数量、跳过数量、缺失对象数量和失败原因
- **AND** dry-run MUST NOT 写数据库或对象存储
- **WHEN** 运维执行迁移 apply
- **THEN** 系统 MUST 复制或移动对象到标准 `images/` 前缀并更新数据库引用
- **AND** 原图与缩略图引用 MUST 保持一致
- **AND** 重复执行 MUST 保持幂等
- **AND** 输出 MUST NOT 泄露密钥、Authorization header、Cookie、`.env` 内容、真实客户数据或本机绝对路径。

#### Scenario: 生产历史对象迁移适配 MySQL 和云上对象存储

- **GIVEN** 生产环境使用外部 MySQL 与腾讯云 COS 或 S3 兼容对象存储
- **WHEN** 运维执行历史对象迁移 dry-run 或 apply
- **THEN** 迁移作业 MUST 使用生产 `DATABASE_URL` 与 `OBJECT_STORAGE_*` 配置
- **AND** MUST NOT 依赖 SQLite 数据库文件路径或本地 MinIO 默认值
- **AND** 对象 copy、remove、put、stat MUST 通过对象存储适配层或明确 provider 能力检查执行
- **AND** provider 不满足一致性或权限要求时 MUST 阻断 apply 或降级为只读审计。

### Requirement: 媒体对象必须可受控读取

系统 SHALL 通过后端受控接口读取媒体对象，保护对象存储访问边界，并 SHALL 支持图片缓存、列表缩略图、媒体观测和视频 Range 请求。商品列表缩略图、品牌图片缩略图和图片类品牌证书缩略图 SHALL 与原图位于同一对象目录或等价可追溯对象路径，并 SHALL 通过文件名差异区分缩略图与原图；历史 `thumbnails/` 前缀 MAY 作为兼容读取或迁移来源，但新生成的列表缩略图 SHALL NOT 依赖 `thumbnails/default/tiles/pending/` 作为最终存储位置。系统 SHALL 生成真实轻量缩略图：对于尺寸大于缩略图目标尺寸的支持图片，缩略图 SHALL 经过后端图片处理生成，像素宽高 SHALL 小于或等于约定最大宽高，且 SHALL NOT 只是原图 bytes 的复制品。历史缩略图回填或重生成作业 MUST 支持 dry-run/apply、分批、幂等、生产 provider 适配和脱敏输出。

#### Scenario: 历史品牌与证书缩略图审计与重生成

- **GIVEN** 存量品牌图片或图片类品牌证书已存在原图对象
- **WHEN** 运维执行历史缩略图审计 dry-run
- **THEN** 输出 SHALL 包含原图存在、缩略图存在、疑似同 size、疑似同 bytes、需要生成或重生成、跳过、失败原因等摘要
- **AND** dry-run SHALL NOT 写数据库或对象存储
- **WHEN** 运维执行重生成 apply
- **THEN** 系统 SHALL 只生成或重生成需要处理的缩略图对象
- **AND** 重复执行 SHALL 保持幂等，不破坏已合格缩略图
- **AND** 输出 SHALL NOT 泄露密钥、Authorization header、Cookie、`.env` 内容、真实客户数据或本机绝对路径。

#### Scenario: 生产缩略图回填按批处理

- **GIVEN** 生产环境存在大量品牌、证书或 SKU 图片对象
- **WHEN** 运维执行缩略图回填或重生成作业
- **THEN** 作业 MUST 支持 limit、batch size、范围过滤或等价分批控制
- **AND** 作业 MUST 输出成功、失败、跳过、重试候选和失败原因统计
- **AND** 失败项 MUST 保留脱敏对象标识和建议恢复动作。
