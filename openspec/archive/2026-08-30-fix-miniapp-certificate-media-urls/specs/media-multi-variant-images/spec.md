## MODIFIED Requirements

### Requirement: 媒体 API 必须提供多规格 URL 语义

商品、SKU 或媒体相关 API MUST 提供 `thumbnail_url`、`display_url`、`original_url` 或等价语义字段，使小程序、店主 Web 和管理端可以按场景选择图片规格。证书详情和品牌证书摘要等品牌证书媒体 API 也 MUST 遵守同一语义：图片证书卡片 MUST 使用 `thumbnail_url`、卡片专用小图 URL 或占位；详情普通展示 MUST 使用 `display_url` 或等价展示图；图片预览、文件打开或下载 MUST 使用 `original_url`、`preview_url`、`file_url` 或等价高清/文件 URL。API MUST 明确 URL 类型、签名、缓存、权限、过期、fallback 和 WebP 派生格式策略，并 MUST 同步 OpenAPI、Orval、API 文档和测试。

#### Scenario: 商品媒体响应包含多规格 URL

- **WHEN** 客户端请求包含图片媒体的商品、SKU 或媒体详情
- **THEN** 响应 MUST 提供轻量列表图、详情展示图和高清预览图的 URL 语义
- **AND** 新生成的轻量列表图和详情展示图 URL SHOULD 指向 WebP 派生对象
- **AND** 响应 MUST NOT 暴露原始 object key、对象存储 endpoint、bucket 名称、access key、secret key 或未授权素材路径
- **AND** 老客户端兼容策略 MUST 有文档和测试覆盖。

#### Scenario: 证书卡片不得使用原文件 fallback

- **WHEN** 小程序请求品牌证书摘要、证书列表或其他证书卡片数据
- **THEN** 图片证书卡片展示 MUST 优先使用 `thumbnail_url`、卡片专用小图 URL 或等价 WebP 轻量图片 URL
- **AND** 缩略图缺失、不可读、为空或图片加载失败时 MUST 展示统一占位或受控失败态
- **AND** 卡片图片 `src` MUST NOT 使用 `file_url`、`original_url`、`preview_url` 或等价原文件 URL 作为默认 fallback
- **AND** 原文件 URL MAY 继续用于详情、预览、打开或下载动作，但 MUST 与卡片展示字段语义分离。

#### Scenario: 图片证书列表 URL 从可信媒体来源派生

- **GIVEN** 品牌证书图片存在标准 `images/default/brand-certificates/` key、可信主图记录或可兼容旧单文件图片来源
- **WHEN** 后端生成品牌证书摘要、聚合证书列表或其他证书卡片数据
- **THEN** API MUST 从可信媒体 key 或受控 URL 派生 `thumbnail_url`
- **AND** 派生缩略图 URL MUST 指向同目录 `.thumb.webp` 或等价轻量图
- **AND** 当 `file_url` 为空但可信 `file_key` 存在时，系统 MUST NOT 因 `file_url` 为空而静默丢失可用 `thumbnail_url`
- **AND** 响应 MUST NOT 暴露完整 object key、bucket、内部 endpoint、Authorization header、Cookie、密钥、`.env` 内容或本机路径。

#### Scenario: API 字段变更同步

- **WHEN** 多规格 URL 字段、响应结构、Content-Type 示例或 fallback 规则发生变化
- **THEN** OpenAPI MUST 更新
- **AND** Orval 生成物 MUST 更新
- **AND** API 文档 MUST 说明字段语义、WebP 派生格式、fallback 和缓存边界
- **AND** 后端测试 MUST 覆盖响应字段与缺失规格回退。

### Requirement: 存量图片必须支持批量生成多规格资源

系统 MUST 支持对存量图片批量生成 `thumbnail` 与 `display`。批量生成 MUST 覆盖 SKU 图片、品牌 Logo、品牌证书图片、图片类证书文件，以及 Banner 自定义上传图。批量生成 MUST 采用 dry-run / apply 两阶段，MUST 默认只读，apply MUST 显式触发，并 MUST 提供幂等性、失败统计、重试建议、二次审计和脱敏输出。针对 JPEG、PNG、WebP 原图，批量生成的 `thumbnail` 与 `display` MUST 使用 WebP 派生格式；SVG、PDF、GIF、HEIC、TIFF、BMP 或不支持对象 MUST 记录跳过、拒绝或 fallback 分类。批量生成 MUST 保留原图格式、MIME 和访问语义，MUST NOT 将原图转码替换为 WebP。

#### Scenario: 存量图片 WebP dry-run 不写入

- **WHEN** 运维执行存量图片 WebP 多规格生成 dry-run
- **THEN** 输出 MUST 包含待处理数量、已存在 WebP 派生数量、缺失规格、跳过原因、失败分类、预计写入对象和风险摘要
- **AND** 当 Banner 自定义上传图缺少 `.thumb.webp` 或 `.display.webp` 时，输出 MUST 包含 Banner 候选来源
- **AND** dry-run MUST NOT 写数据库
- **AND** dry-run MUST NOT 写对象存储
- **AND** 输出 MUST NOT 包含真实密钥、数据库连接串、Authorization header、Cookie、真实 `.env`、本机绝对路径、未脱敏 object key 全量值或真实客户数据。

#### Scenario: 品牌证书图片历史媒体 dry-run 覆盖 URL 缺失

- **WHEN** 运维执行品牌证书图片历史媒体 dry-run 或等价审计
- **THEN** 输出 MUST 统计图片类证书总数、主图记录数量、空 `file_url` 数量、可信 `file_key` 数量、标准 key 数量、旧 key 数量、缺 `.thumb.webp` 数量和 object 缺失数量
- **AND** 输出 MUST 标识是否会导致公开证书列表 `thumbnail_url` 为空
- **AND** dry-run MUST NOT 写数据库或对象存储
- **AND** 输出 MUST 使用脱敏摘要，不得包含完整 object key、真实客户数据、密钥、连接串、Authorization header、Cookie、`.env` 内容或本机绝对路径。

#### Scenario: 存量图片 WebP apply 显式受控

- **GIVEN** dry-run 已完成且备份或风险确认已记录
- **WHEN** 运维显式执行 WebP 派生 apply
- **THEN** 系统 MUST 为支持格式生成缺失或不合格的 WebP `thumbnail` 与 WebP `display`
- **AND** Banner 自定义上传图的派生图 MUST 写入原图同目录，使用 `.thumb.webp` 与 `.display.webp` 后缀
- **AND** 输出 MUST 包含成功、失败、跳过、重试候选和失败原因统计
- **AND** 重复执行 MUST 保持幂等
- **AND** apply 后 MUST 支持二次审计验证 key、object、URL、render 和规格收益。
