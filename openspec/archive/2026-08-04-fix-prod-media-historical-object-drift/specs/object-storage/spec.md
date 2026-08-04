## MODIFIED Requirements

### Requirement: 媒体对象必须可受控读取

系统 SHALL 通过后端受控接口读取媒体对象，保护对象存储访问边界，并 SHALL 支持图片缓存、列表缩略图、媒体观测和视频 Range 请求。商品列表缩略图、品牌图片缩略图和图片类品牌证书缩略图 SHALL 与原图位于同一对象目录或等价可追溯对象路径，并 SHALL 通过文件名差异区分缩略图与原图；历史 `thumbnails/` 前缀 MAY 作为兼容读取或迁移来源，但新生成的列表缩略图 SHALL NOT 依赖 `thumbnails/default/tiles/pending/` 作为最终存储位置。系统 SHALL 生成真实轻量缩略图：对于尺寸大于缩略图目标尺寸的支持图片，缩略图 SHALL 经过后端图片处理生成，像素宽高 SHALL 小于或等于约定最大宽高，且 SHALL NOT 只是原图 bytes 的复制品。针对 `BUG-0116-prod-media-historical-object-drift`，系统 SHALL 支持对 SKU 商品图片、品牌 Logo 和品牌证书图片的历史缩略图漂移进行 dry-run 审计、受控回填、二次审计和幂等重复执行。

#### Scenario: BUG-0116 历史缩略图审计覆盖三类对象

- **GIVEN** 生产等价数据库与对象存储配置可用
- **WHEN** 运维执行 BUG-0116 历史缩略图审计 dry-run
- **THEN** 输出 SHALL 分别统计 SKU 商品图片、品牌 Logo 和品牌证书图片
- **AND** 输出 SHALL 包含原图存在、缩略图存在、疑似同 size、疑似同 bytes、需要生成或重生成、跳过、失败原因和重试候选摘要
- **AND** dry-run SHALL NOT 写数据库或对象存储
- **AND** 输出 SHALL NOT 包含生产密钥、数据库 DSN、Authorization header、Cookie、`.env` 内容、本机绝对路径或真实客户数据。

#### Scenario: BUG-0116 历史缩略图回填幂等

- **GIVEN** BUG-0116 dry-run 已确认可回填的 SKU 商品图片、品牌 Logo 或品牌证书图片
- **WHEN** 运维在完成备份后执行受控 apply
- **THEN** 系统 SHALL 仅为需要处理且原图可读的图片生成或重生成同目录 `.thumb` 缩略图
- **AND** 缩略图 SHALL 由后端图片处理逻辑生成，SHALL NOT 只是原图 bytes 复制品
- **AND** 重复执行 SHALL 保持幂等，不破坏已合格缩略图
- **AND** 对原图缺失、MIME 不支持、对象存储不可用或 provider 能力不足的记录 SHALL 输出 fail 或 blocked 摘要。

### Requirement: 对象 Key 必须使用标准前缀

系统 MUST 使用 `rules/object-storage.md` 定义的单桶标准前缀生成对象 Key。图片类上传 MUST 使用 `images/`，原始视频 MUST 使用 `videos/`，视频封面 MUST 使用 `videos/covers/`，文件类资源 MUST 使用 `files/`，处理后资源 MUST 使用 `processed/` 或更具体标准前缀。系统 MUST NOT 使用用户原始文件名作为对象 Key。`original/` 仅允许作为存量兼容前缀，新上传 MUST NOT 使用。**Banner 运营图** MUST 使用 `images/default/banners/{uuid}.{ext}`（当 `update-object-storage-key-layout` 已生效时 MUST 使用 `images/` 语义前缀；未生效前实现 MUST 与 `build_upload_object_key()` 当前项目约定一致并在 apply 时对齐）。SKU 图片在新建前 MAY 使用 `images/default/tiles/pending/{uuid}.{ext}` 作为暂存 key；一旦绑定到 SKU 或进入公开展示，系统 MUST 使用可追溯到 SKU 的正式商品图片 key。品牌证书图片类对象 MUST 使用 `images/default/brand-certificates/{uuid}.{ext}` 或等价标准图片前缀；品牌证书 PDF 或其他文档类附件 MUST 使用 `files/` 前缀。针对 BUG-0116，系统 MUST 支持对历史公开 SKU pending 主图和历史图片类证书 files 前缀进行受控 dry-run、apply、二次审计和幂等修复。

#### Scenario: BUG-0116 公开 SKU pending 主图正式化

- **GIVEN** 公开 SKU 主图仍引用 `images/default/tiles/pending/`
- **WHEN** 运维执行 BUG-0116 SKU pending 主图修复 apply
- **THEN** 系统 MUST 将可迁移主图正式化到 `images/default/tiles/{tile_id}/` 或等价商品目录
- **AND** 系统 MUST 同步更新 `tile_images.object_key` 与 `tile_images.url`
- **AND** 目标 URL MUST 使用 `/media/{target_key}` 或等价后端受控读取方式
- **AND** 二次审计中公开 SKU 主图 pending 数量 MUST 为 0，或每个剩余项 MUST 记录 fail / blocked 原因和重试条件。

#### Scenario: BUG-0116 图片类证书从 files 前缀迁移

- **GIVEN** 历史品牌证书图片 key 位于 `files/default/brand-certificates/`
- **WHEN** 运维执行 BUG-0116 证书图片 key 迁移 apply
- **THEN** JPG、JPEG、PNG、WebP 图片类证书 MUST 迁移到 `images/default/brand-certificates/` 或等价标准图片前缀
- **AND** `brand_certificates.file_key` 与 `brand_certificate_images.file_key` 中的可迁移图片引用 MUST 同步更新
- **AND** PDF 或其他文档类证书 MUST 继续保留在 `files/default/brand-certificates/`
- **AND** 原图与同目录 `.thumb` 缩略图引用 MUST 保持同一图片资源归属
- **AND** 重复执行 MUST 幂等跳过已迁移或不适用记录。
