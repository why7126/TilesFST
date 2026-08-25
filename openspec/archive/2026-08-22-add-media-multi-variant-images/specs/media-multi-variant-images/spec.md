## ADDED Requirements

### Requirement: 媒体图片必须支持多规格展示图

系统 MUST 支持 `thumbnail`、`display`、`original` 三类媒体图片规格。`thumbnail` MUST 用于列表、卡片和轻量预览；`display` MUST 用于详情普通展示和图册浏览；`original` MUST 保留上传原图或等价高清资源，用于高清预览、下载或需要保真的场景。三类规格 MUST 可追溯到同一媒体记录或业务对象，并 MUST 明确 key、MIME、尺寸、质量、体积上限、生成状态和失败原因的记录方式。

#### Scenario: 新上传图片生成三规格资源

- **WHEN** 管理端用户上传合法图片
- **THEN** 系统 MUST 保留 `original`
- **AND** 系统 MUST 生成或调度生成 `thumbnail` 与 `display`
- **AND** 三规格资源 MUST 能追溯到同一媒体记录或业务对象
- **AND** 生成失败 MUST 有可观测记录和明确降级策略
- **AND** 错误响应或日志摘要 MUST NOT 暴露对象存储密钥、Authorization header、Cookie、真实 `.env`、本机绝对路径或真实客户数据。

#### Scenario: 派生规格缺失时可安全回退

- **GIVEN** 目标规格 URL 缺失、生成失败或对象不可读
- **WHEN** 客户端请求列表、详情或预览媒体
- **THEN** 系统 MUST 按明确 fallback 顺序返回可用 URL 或安全占位
- **AND** fallback 事件 MUST 可观测
- **AND** 验收记录 MUST NOT 将 fallback 原图视为轻量规格性能通过。

### Requirement: 媒体 API 必须提供多规格 URL 语义

商品、SKU 或媒体相关 API MUST 提供 `thumbnail_url`、`display_url`、`original_url` 或等价语义字段，使小程序、店主 Web 和管理端可以按场景选择图片规格。API MUST 明确 URL 类型、签名、缓存、权限、过期和 fallback 策略，并 MUST 同步 OpenAPI、Orval、API 文档和测试。

#### Scenario: 商品媒体响应包含多规格 URL

- **WHEN** 客户端请求包含图片媒体的商品、SKU 或媒体详情
- **THEN** 响应 MUST 提供轻量列表图、详情展示图和高清预览图的 URL 语义
- **AND** 响应 MUST NOT 暴露原始 object key、对象存储 endpoint、bucket 名称、access key、secret key 或未授权素材路径
- **AND** 老客户端兼容策略 MUST 有文档和测试覆盖。

#### Scenario: API 字段变更同步

- **WHEN** 多规格 URL 字段或响应结构发生变化
- **THEN** OpenAPI MUST 更新
- **AND** Orval 生成物 MUST 更新
- **AND** API 文档 MUST 说明字段语义、fallback 和缓存边界
- **AND** 后端测试 MUST 覆盖响应字段与缺失规格回退。

### Requirement: 存量图片必须支持批量生成多规格资源

系统 MUST 支持对存量图片批量生成 `thumbnail` 与 `display`。批量生成 MUST 采用 dry-run / apply 两阶段，MUST 默认只读，apply MUST 显式触发，并 MUST 提供幂等性、失败统计、重试建议、二次审计和脱敏输出。

#### Scenario: 存量图片 dry-run 不写入

- **WHEN** 运维执行存量图片多规格生成 dry-run
- **THEN** 输出 MUST 包含待处理数量、缺失规格、跳过原因、失败分类、预计写入对象和风险摘要
- **AND** dry-run MUST NOT 写数据库
- **AND** dry-run MUST NOT 写对象存储
- **AND** 输出 MUST NOT 包含真实密钥、数据库连接串、Authorization header、Cookie、真实 `.env`、本机绝对路径或真实客户数据。

#### Scenario: 存量图片 apply 显式受控

- **GIVEN** dry-run 已完成且备份或风险确认已记录
- **WHEN** 运维显式执行 apply
- **THEN** 系统 MUST 生成缺失或不合格的 `thumbnail` 与 `display`
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
