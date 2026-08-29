# media-multi-variant-images Specification

## Purpose
TBD - created by archiving change add-media-multi-variant-images. Update Purpose after archive.
## Requirements
### Requirement: 媒体图片必须支持多规格展示图

系统 MUST 支持 `thumbnail`、`display`、`original` 三类媒体图片规格。`thumbnail` MUST 用于列表、卡片和轻量预览；`display` MUST 用于详情普通展示和图册浏览；`original` MUST 保留上传原图或等价高清资源，用于高清预览、下载或需要保真的场景。三类规格 MUST 可追溯到同一媒体记录或业务对象，并 MUST 明确 key、MIME、尺寸、质量、体积上限、生成状态、失败原因和生成阶段耗时的记录方式。

系统 MUST 在支持的图片上传链路中保留 `original` 上传格式，并将新生成的 `thumbnail` 与 `display` 派生图编码为 WebP。首期支持 JPEG、PNG、WebP 输入生成 WebP 派生图；SVG、PDF MUST 跳过 WebP 图片派生；GIF、HEIC、TIFF、BMP 首期 MUST NOT 自动转码，且 MUST 记录跳过、拒绝或 fallback 策略。PNG 透明图的透明度处理 MUST 在实现与验收记录中明确。对于 WebP 输入，系统 MUST 避免 thumbnail 生成出现 20 秒以上长尾；无法在合理时间生成时 MUST 进入可观测失败、跳过或降级路径，而不是静默阻塞上传接口到 30 秒级。

系统 MUST 沉淀 Web 与微信小程序统一的图片三规格消费矩阵。矩阵字段 MUST 至少包括：页面、位置、图对象、是否缩略图、是否 display 图、是否原图、优化方案。矩阵 MUST 覆盖微信小程序真实页面、Web 管理端真实媒体展示位置，并为店主 Web 展示端提供明确的预留规范。矩阵中的每个页面位置 MUST 只表达一个主消费规格；普通展示、高清预览、下载或原文件查看使用不同规格时，MUST 拆成独立行。

非原图目标场景 MUST NOT fallback 到 `original` 并写作性能通过。当列表、卡片、推荐位、小 Logo 等 `thumbnail` 目标场景，或详情普通展示、图册浏览、表单大预览等 `display` 目标场景缺少目标规格时，系统 MUST 使用安全占位、补齐 WebP 派生图或在矩阵优化方案中标记后续修正；验收 MUST 区分 WebP 派生通过、fallback、blocked 和 no-benefit。

#### Scenario: 新上传图片生成 WebP 三规格资源

- **WHEN** 管理端用户上传合法 JPEG、PNG 或 WebP 图片
- **THEN** 系统 MUST 保留 `original` 的上传格式、MIME 和高清预览语义
- **AND** 系统 MUST 生成或调度生成 WebP `thumbnail` 与 WebP `display`
- **AND** `thumbnail` 与 `display` 的 key、扩展名、Content-Type 和实际 bytes MUST 表达 WebP
- **AND** 三规格资源 MUST 能追溯到同一媒体记录或业务对象
- **AND** 生成失败 MUST 有可观测记录和明确降级策略
- **AND** 错误响应或日志摘要 MUST NOT 暴露对象存储密钥、Authorization header、Cookie、真实 `.env`、本机绝对路径或真实客户数据。

#### Scenario: WebP thumbnail 生成长尾必须受控

- **GIVEN** 用户上传合法 WebP 图片且链路需要生成 WebP thumbnail
- **WHEN** thumbnail 生成进入解码、缩放或编码阶段
- **THEN** 系统 MUST 通过实现策略避免 `thumbnail_generate` 出现 20 秒以上长尾
- **AND** 若触发失败、跳过或降级，系统 MUST 记录 `thumbnail_generate` 的状态、耗时和脱敏原因
- **AND** 系统 MUST NOT 将 `thumbnail_generate` 耗时只聚合到对象存储 `put_object` 阶段
- **AND** 验收 MUST 区分对象写入耗时与派生图生成耗时

#### Scenario: 特殊格式按首期策略跳过或降级

- **WHEN** 用户上传 SVG、PDF、GIF、HEIC、TIFF、BMP 或其他首期不支持转码格式
- **THEN** 系统 MUST NOT 静默生成错误的 WebP 派生图
- **AND** SVG 和 PDF MUST 跳过 WebP 图片派生
- **AND** GIF、HEIC、TIFF、BMP MUST 按现有上传策略拒绝、跳过或仅提供受控 fallback
- **AND** 上传、维护任务或验收记录 MUST 能定位跳过原因、拒绝原因或 fallback 策略。

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

#### Scenario: API 字段变更同步

- **WHEN** 多规格 URL 字段、响应结构、Content-Type 示例或 fallback 规则发生变化
- **THEN** OpenAPI MUST 更新
- **AND** Orval 生成物 MUST 更新
- **AND** API 文档 MUST 说明字段语义、WebP 派生格式、fallback 和缓存边界
- **AND** 后端测试 MUST 覆盖响应字段与缺失规格回退。

### Requirement: 存量图片必须支持批量生成多规格资源

系统 MUST 支持对存量图片批量生成 `thumbnail` 与 `display`。批量生成 MUST 采用 dry-run / apply 两阶段，MUST 默认只读，apply MUST 显式触发，并 MUST 提供幂等性、失败统计、重试建议、二次审计和脱敏输出。针对 JPEG、PNG、WebP 原图，批量生成的 `thumbnail` 与 `display` MUST 使用 WebP 派生格式；SVG、PDF、GIF、HEIC、TIFF、BMP 或不支持对象 MUST 记录跳过、拒绝或 fallback 分类。

#### Scenario: 存量图片 WebP dry-run 不写入

- **WHEN** 运维执行存量图片 WebP 多规格生成 dry-run
- **THEN** 输出 MUST 包含待处理数量、已存在 WebP 派生数量、缺失规格、跳过原因、失败分类、预计写入对象和风险摘要
- **AND** dry-run MUST NOT 写数据库
- **AND** dry-run MUST NOT 写对象存储
- **AND** 输出 MUST NOT 包含真实密钥、数据库连接串、Authorization header、Cookie、真实 `.env`、本机绝对路径、未脱敏 object key 全量值或真实客户数据。

#### Scenario: 存量图片 WebP apply 显式受控

- **GIVEN** dry-run 已完成且备份或风险确认已记录
- **WHEN** 运维显式执行 WebP 派生 apply
- **THEN** 系统 MUST 为支持格式生成缺失或不合格的 WebP `thumbnail` 与 WebP `display`
- **AND** 输出 MUST 包含成功、失败、跳过、重试候选和失败原因统计
- **AND** 重复执行 MUST 保持幂等
- **AND** apply 后 MUST 支持二次审计验证 key、object、URL、render 和规格收益。

### Requirement: 对象存储直出必须受控

系统 MUST 支持对象存储直出 URL 作为媒体读取形态之一，但 MUST 通过后端媒体服务或对象存储适配层生成受控 URL。对象存储直出 MUST 明确签名、过期、缓存、公开范围、fallback 和后端 `/media` 代理兼容边界。客户端 MUST NOT 直连未授权对象存储。

#### Scenario: 直出 URL 不暴露存储凭据

- **WHEN** 后端为媒体资源生成对象存储直出 URL
- **THEN** URL MUST 符合当前资源公开范围和权限策略
- **AND** 响应 MUST NOT 暴露 access key、secret key、bucket 权限细节、内部 endpoint 白名单或完整 SDK 堆栈
- **AND** 客户端 MUST 能在直出失败时回退到受控 `/media` 代理或安全占位。

#### Scenario: CDN 正式接入仅作为预留

- **WHEN** 团队实现多规格 URL 适配层
- **THEN** 字段语义 SHOULD 支持后续切换 CDN URL
- **AND** 本 Change MUST NOT 要求生产 CDN 正式接入
- **AND** 验收 MUST 记录 CDN 为预留能力而非本期通过项。

### Requirement: 证书详情品牌入口必须消费品牌 Logo 缩略图

证书详情 API 或小程序数据适配层 MUST 为所属品牌数据提供 `brand_logo_thumbnail_url` 或等价品牌 Logo 缩略图 URL。证书详情页品牌卡片普通展示 MUST 优先消费该缩略图字段。缩略图缺失、不可读或加载失败时，系统 MUST 使用安全占位、品牌首字或统一失败态；验收 MUST NOT 将品牌 Logo 原图 fallback 写作缩略图性能通过。

#### Scenario: 证书详情 brand 数据包含品牌缩略图字段

- **WHEN** 小程序请求证书详情并响应包含所属品牌
- **THEN** 响应或页面适配后的 `brand` 数据 MUST 包含 `brand_logo_thumbnail_url` 或等价缩略图字段
- **AND** 该字段 MUST 表示适合品牌卡片小图展示的受控 URL 或安全静态资源
- **AND** 响应 MUST NOT 暴露对象存储原始 Key、本机路径、后台备注、内部审计字段或真实存储凭据。

#### Scenario: 证书详情品牌卡片不使用原图 fallback

- **WHEN** 证书详情页品牌卡片渲染品牌 Logo
- **THEN** 小程序 MUST 优先请求 `brand_logo_thumbnail_url` 或等价缩略图 URL
- **AND** 缩略图缺失、为空或加载失败时 MUST 使用安全占位或统一失败态
- **AND** 小图展示场景 MUST NOT 请求品牌 Logo 原图作为默认 fallback。

#### Scenario: 证书详情品牌 Logo 四联验收

- **WHEN** 团队验收证书详情页品牌入口
- **THEN** 验收 SHALL 记录品牌 Logo 缩略图的 key、object、URL 和 render 四联证据，无法适用的维度 SHALL 明确标注 N/A 原因
- **AND** Network evidence SHALL 记录 URL 类型、HTTP 状态、资源大小、耗时和渲染结论
- **AND** 验收记录 SHALL NOT 包含 Authorization header、Cookie、真实 `.env`、本机绝对路径或未脱敏 object key。

