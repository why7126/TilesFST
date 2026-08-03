## MODIFIED Requirements

### Requirement: 媒体对象必须可受控读取

系统 SHALL 通过后端受控接口读取媒体对象，保护对象存储访问边界，并 SHALL 支持图片缓存、列表缩略图、媒体观测和视频 Range 请求。商品列表缩略图 SHALL 与原图位于同一对象目录，并 SHALL 通过文件名差异区分缩略图与原图；历史 `thumbnails/` 前缀 MAY 作为兼容读取或迁移来源，但新生成的商品列表缩略图 SHALL NOT 依赖 `thumbnails/default/tiles/pending/` 作为最终存储位置。公开 SKU 主图正式化后，公开端列表、搜索、首页推荐和品牌详情商品 Tab SHALL NOT 继续派生或返回 `images/default/tiles/pending/` 下的缩略图 URL，除非该对象仍是未绑定暂存态且不会进入公开商品响应。

#### Scenario: 通过后端读取媒体对象
- **WHEN** Web、小程序或管理端需要展示已授权媒体对象
- **THEN** 客户端 SHALL 通过后端公开或授权媒体 URL 读取媒体
- **AND** 客户端 SHALL NOT 直连未授权对象存储 endpoint、泄露 MinIO 凭据或绕过后端访问控制。

#### Scenario: 图片响应缓存
- **WHEN** 客户端通过 `/media/{object_key}` 或等价受控 URL 读取图片对象
- **THEN** 后端 SHOULD 返回合理的 `Cache-Control`、`ETag`、`Last-Modified` 或对象版本信息
- **AND** 同一版本图片重复读取 SHOULD 支持客户端或中间层缓存
- **AND** 图片替换或对象版本变化 SHALL 有明确失效策略，避免长期展示旧图。

#### Scenario: 列表缩略图读取
- **WHEN** 小程序商品卡片、搜索结果、首页推荐或品牌详情商品 Tab 读取商品列表图片
- **THEN** 后端 SHOULD 优先返回与原图同目录且文件名差异化的缩略图或等价轻量优化图片 URL
- **AND** 缩略图缺失时 SHALL 安全回退到原图、占位图或可观测的失败状态
- **AND** 缩略图读取 SHALL 遵守单 Bucket + 前缀策略和既有鉴权边界。

#### Scenario: pending 主图缩略图命名
- **GIVEN** 原图对象 key 为 `images/default/tiles/pending/<uuid>.<ext>`
- **WHEN** 系统为未绑定暂存图片生成或回填缩略图
- **THEN** 缩略图对象 key SHALL 保持在 `images/default/tiles/pending/` 同目录
- **AND** 缩略图文件名 SHALL 与原图文件名有明确差异
- **AND** 系统 SHALL NOT 机械生成 `/media/thumbnails/default/tiles/pending/<uuid>.<ext>` 作为最终列表缩略图 URL。

#### Scenario: 公开商品主图正式化后缩略图不在 pending
- **GIVEN** SKU 主图曾从 `images/default/tiles/pending/<uuid>.<ext>` 上传
- **WHEN** 该图片已绑定到 SKU 并进入公开商品响应
- **THEN** 公开端返回的缩略图 URL MUST NOT 位于 `images/default/tiles/pending/`
- **AND** 缩略图 MUST 与正式原图位于同一 SKU 商品图片目录，或在缺失时安全回退到正式原图、占位图或可观测失败状态。

#### Scenario: 媒体读取观测
- **WHEN** 后端受控媒体读取接口处理请求
- **THEN** 系统 SHOULD 记录状态码、耗时、对象是否存在、媒体类型和请求入口中的可用脱敏字段
- **AND** 日志 MUST NOT 输出对象存储密钥、Authorization header、Cookie、`.env` 内容或本机绝对路径。

### Requirement: 对象 Key 必须使用标准前缀

系统 MUST 使用 `rules/object-storage.md` 定义的单桶标准前缀生成对象 Key。图片类上传 MUST 使用 `images/`，原始视频 MUST 使用 `videos/`，视频封面 MUST 使用 `videos/covers/`，文件类资源 MUST 使用 `files/`，处理后资源 MUST 使用 `processed/` 或更具体标准前缀。系统 MUST NOT 使用用户原始文件名作为对象 Key。`original/` 仅允许作为存量兼容前缀，新上传 MUST NOT 使用。**Banner 运营图** MUST 使用 `images/default/banners/{uuid}.{ext}`（当 `update-object-storage-key-layout` 已生效时 MUST 使用 `images/` 语义前缀；未生效前实现 MUST 与 `build_upload_object_key()` 当前项目约定一致并在 apply 时对齐）。SKU 图片在新建前 MAY 使用 `images/default/tiles/pending/{uuid}.{ext}` 作为暂存 key；一旦绑定到 SKU 或进入公开展示，系统 MUST 使用可追溯到 SKU 的正式商品图片 key。

#### Scenario: 图片对象 Key 生成

- **WHEN** 用户上传头像、品牌 Logo 或 SKU 图片
- **THEN** 对象 Key MUST 使用 `images/` 前缀
- **AND** 对象 Key MUST 包含租户或默认命名空间、资源类型和随机文件名
- **AND** 文件扩展名 MUST 来自后端 MIME 白名单映射
- **AND** 新上传 MUST NOT 使用 `original/` 前缀

#### Scenario: SKU 图片从 pending 正式化

- **GIVEN** SKU 图片对象 key 位于 `images/default/tiles/pending/`
- **WHEN** 后端将该图片绑定到 SKU 或迁移存量公开主图
- **THEN** 目标对象 key MUST 位于 `images/default/tiles/{tile_id}/` 或等价 SKU 正式商品图片目录
- **AND** 目标 key MUST 由后端生成，不得由前端提交
- **AND** 系统 MUST NOT 使用用户原始文件名作为目标 key
- **AND** 对象复制、缩略图复制或生成、数据库引用更新必须通过后端受控逻辑完成。

#### Scenario: Banner 对象 Key 生成

- **WHEN** 用户上传 Banner 运营图
- **THEN** 对象 Key MUST 匹配 `images/default/banners/{uuid}.{ext}`（或与当期 `build_upload_object_key('images', 'banners', ...)` 等价形态）
- **AND** MUST NOT 使用用户原始文件名

#### Scenario: 视频对象 Key 生成

- **WHEN** 用户上传 SKU 视频
- **THEN** 对象 Key MUST 使用 `videos/` 前缀
- **AND** 文件扩展名 MUST 来自后端 MIME 白名单映射

#### Scenario: 不新增业务 Bucket

- **WHEN** 上传头像、品牌 Logo、SKU 图片、SKU 视频或 Banner 运营图
- **THEN** 系统 MUST 使用同一个对象存储 bucket
- **AND** MUST NOT 创建额外业务 Bucket，除非后续 OpenSpec Change 明确要求
