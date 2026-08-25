## MODIFIED Requirements

### Requirement: 媒体对象必须可受控读取

系统 SHALL 通过后端受控接口读取媒体对象，保护对象存储访问边界，并 SHALL 支持图片缓存、列表缩略图、详情展示图、媒体观测、对象存储直出和视频 Range 请求。商品列表缩略图、品牌图片缩略图、Banner 图片缩略图、图片类品牌证书缩略图和图片 `display` 派生图 SHALL 与原图位于同一对象目录或等价可追溯对象路径，并 SHALL 通过文件名差异、规格目录或等价稳定规则区分 `thumbnail`、`display` 与 `original`。

系统 SHALL 生成真实轻量缩略图与详情展示图：对于尺寸大于目标尺寸的支持图片，派生图 SHALL 经过后端图片处理生成，像素宽高 SHALL 小于或等于对应规格约定最大宽高，且 SHALL NOT 只是原图 bytes 的复制品。无法达到目标体积时 SHALL NOT 默认阻断原图上传或业务保存，且 SHALL 记录 warning 或可复核失败原因。

新生成的图片 `thumbnail` 与 `display` 派生对象 SHALL 使用 WebP 内容格式和 `image/webp` MIME。派生对象 key SHALL 与内容格式一致，推荐使用同目录 `.thumb.webp` 与 `.display.webp` 或等价稳定 WebP key。系统 SHALL NOT 新生成 `.thumb.jpg`、`.thumb.png`、`.display.jpg` 或 `.display.png` 但对象内容为 WebP 的不一致状态。历史同格式派生 key MAY 作为读取 fallback 候选保留。

对象存储直出 SHALL 作为受控媒体读取形态之一，仅能由后端媒体服务或对象存储适配层生成。系统 SHALL 明确签名 URL、公开 URL、后端 `/media` 代理 URL 的选择条件、过期策略、缓存策略和 fallback。客户端 SHALL NOT 直连未授权对象存储，响应 SHALL NOT 暴露对象存储密钥、bucket 权限细节或内部 endpoint 白名单。

#### Scenario: 多规格图片读取 URL 可追溯

- **WHEN** 客户端请求图片媒体 URL
- **THEN** 系统 SHALL 能返回或派生 `thumbnail`、`display`、`original` 三类 URL 语义
- **AND** 新生成的 `thumbnail` 与 `display` URL SHALL 指向 WebP 派生对象或明确为空并触发受控 fallback
- **AND** 每类 URL SHALL 可追溯到同一媒体记录或业务对象
- **AND** 响应 SHALL NOT 暴露原始 object key、对象存储 endpoint、bucket 名称、access key、secret key 或未授权素材路径。

#### Scenario: WebP 派生 key 与 MIME 一致

- **WHEN** 系统为 JPEG、PNG 或 WebP 原图生成 `thumbnail` 或 `display`
- **THEN** 派生对象 key SHALL 使用 `.webp` 扩展名或等价明确 WebP 标识
- **AND** 对象存储 Content-Type SHALL 为 `image/webp`
- **AND** 后端受控读取响应 SHALL 返回与对象内容一致的 WebP MIME
- **AND** 验收 SHALL 同时记录脱敏 key、扩展名、MIME、对象大小和图片尺寸。

#### Scenario: 对象存储直出失败可回退

- **GIVEN** 当前媒体使用对象存储直出 URL
- **WHEN** 直出 URL 过期、对象不可读或权限校验失败
- **THEN** 客户端或后端 SHALL 按明确策略回退到受控 `/media` 代理 URL 或安全占位
- **AND** 回退事件 SHALL 可观测
- **AND** 验收 SHALL 记录 URL 类型、HTTP 状态、业务状态和用户可见表现。

#### Scenario: 派生图不是原图复制

- **WHEN** 系统生成 WebP `thumbnail` 或 WebP `display`
- **THEN** 派生图 SHALL 经过后端图片处理
- **AND** 对大于目标尺寸的支持图片，派生图像素或 bytes SHALL 体现对应规格收益
- **AND** 验收 SHALL NOT 将与原图同 bytes 或无收益的派生图写作性能通过。

### Requirement: 对象 Key 必须使用标准前缀

系统 MUST 使用 `rules/object-storage.md` 定义的单桶标准前缀生成对象 Key。图片类上传 MUST 使用 `images/`，原始视频 MUST 使用 `videos/`，视频封面 MUST 使用 `videos/covers/`，文件类资源 MUST 使用 `files/`，处理后资源 MUST 使用 `processed/` 或更具体标准前缀。系统 MUST NOT 使用用户原始文件名作为对象 Key。`original/` 仅允许作为存量兼容前缀，新上传 MUST NOT 使用。**Banner 运营图** MUST 使用 `images/default/banners/{uuid}.{ext}`（当 `update-object-storage-key-layout` 已生效时 MUST 使用 `images/` 语义前缀；未生效前实现 MUST 与 `build_upload_object_key()` 当前项目约定一致并在 apply 时对齐）。SKU 图片在新建前 MAY 使用 `images/default/tiles/pending/{uuid}.{ext}` 作为暂存 key；一旦绑定到 SKU 或进入公开展示，系统 MUST 使用可追溯到 SKU 的正式商品图片 key。品牌证书图片类对象 MUST 使用 `images/default/brand-certificates/{uuid}.{ext}` 或等价标准图片前缀；品牌证书 PDF 或其他文档类附件 MUST 使用 `files/` 前缀。针对 BUG-0116，系统 MUST 支持对历史公开 SKU pending 主图和历史图片类证书 files 前缀进行受控 dry-run、apply、二次审计和幂等修复。

新生成的图片派生 key MUST 在原图所在目录或等价可追溯目录中表达规格与 WebP 格式，例如 `{base}.thumb.webp` 与 `{base}.display.webp`。原图 key MUST 保留上传扩展名和 MIME；派生 key 不得使用用户原始文件名，也不得暴露真实 object key 全量值到用户可见错误或维护任务摘要。

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
- **AND** 原图与同目录 WebP `.thumb` 缩略图引用 MUST 保持同一图片资源归属
- **AND** 重复执行 MUST 幂等跳过已迁移或不适用记录。

#### Scenario: 新上传图片派生 key 保留原图归属

- **WHEN** 系统写入新上传 JPEG、PNG 或 WebP 图片及其派生图
- **THEN** 原图 key MUST 保留上传扩展名
- **AND** `thumbnail` 派生 key MUST 使用 `.thumb.webp` 或等价 WebP 缩略图标识
- **AND** `display` 派生 key MUST 使用 `.display.webp` 或等价 WebP 展示图标识
- **AND** 三个 key MUST 能追溯到同一业务对象、租户或资源目录。
