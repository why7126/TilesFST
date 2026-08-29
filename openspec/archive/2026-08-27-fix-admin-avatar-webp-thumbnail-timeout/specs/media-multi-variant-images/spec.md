## MODIFIED Requirements

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
