## MODIFIED Requirements

### Requirement: 对象 Key 必须使用标准前缀

系统 MUST 使用 `rules/object-storage.md` 定义的单桶标准前缀生成对象 Key。图片类上传 MUST 使用 `images/`，原始视频 MUST 使用 `videos/`，视频封面 MUST 使用 `videos/covers/`，文件类资源 MUST 使用 `files/`，处理后资源 MUST 使用 `processed/` 或更具体标准前缀。系统 MUST NOT 使用用户原始文件名作为对象 Key。`original/` 仅允许作为存量兼容前缀，新上传 MUST NOT 使用。**Banner 运营图** MUST 使用 `images/default/banners/{uuid}.{ext}`（当 `update-object-storage-key-layout` 已生效时 MUST 使用 `images/` 语义前缀；未生效前实现 MUST 与 `build_upload_object_key()` 当前项目约定一致并在 apply 时对齐）。SKU 图片在新建前 MAY 使用 `images/default/tiles/pending/{uuid}.{ext}` 作为暂存 key；一旦绑定到 SKU 或进入公开展示，系统 MUST 使用可追溯到 SKU 的正式商品图片 key。品牌证书图片类对象 MUST 使用 `images/default/brand-certificates/{uuid}.{ext}` 或等价标准图片前缀；品牌证书 PDF 或其他文档类附件 MUST 使用 `files/` 前缀。

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
