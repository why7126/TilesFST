## MODIFIED Requirements

### Requirement: 媒体 API 必须提供多规格 URL 语义

商品、SKU 或媒体相关 API MUST 提供 `thumbnail_url`、`display_url`、`original_url` 或等价语义字段，使小程序、店主 Web 和管理端可以按场景选择图片规格。证书详情和品牌证书摘要等品牌证书媒体 API 也 MUST 遵守同一语义：图片证书卡片 MUST 使用 `thumbnail_url`、卡片专用小图 URL 或占位；详情普通展示 MUST 使用 `display_url` 或等价展示图；图片预览、文件打开或下载 MUST 使用 `original_url`、`preview_url`、`file_url` 或等价高清/文件 URL。API MUST 明确 URL 类型、签名、缓存、权限、过期和 fallback 策略，并 MUST 同步 OpenAPI、Orval、API 文档和测试。

#### Scenario: 商品媒体响应包含多规格 URL

- **WHEN** 客户端请求包含图片媒体的商品、SKU 或媒体详情
- **THEN** 响应 MUST 提供轻量列表图、详情展示图和高清预览图的 URL 语义
- **AND** 响应 MUST NOT 暴露原始 object key、对象存储 endpoint、bucket 名称、access key、secret key 或未授权素材路径
- **AND** 老客户端兼容策略 MUST 有文档和测试覆盖。

#### Scenario: 证书卡片不得使用原文件 fallback

- **WHEN** 小程序请求品牌证书摘要、证书列表或其他证书卡片数据
- **THEN** 图片证书卡片展示 MUST 优先使用 `thumbnail_url`、卡片专用小图 URL 或等价轻量图片 URL
- **AND** 缩略图缺失、不可读、为空或图片加载失败时 MUST 展示统一占位或受控失败态
- **AND** 卡片图片 `src` MUST NOT 使用 `file_url`、`original_url`、`preview_url` 或等价原文件 URL 作为默认 fallback
- **AND** 原文件 URL MAY 继续用于详情、预览、打开或下载动作，但 MUST 与卡片展示字段语义分离。

#### Scenario: API 字段变更同步

- **WHEN** 多规格 URL 字段或响应结构发生变化
- **THEN** OpenAPI MUST 更新
- **AND** Orval 生成物 MUST 更新
- **AND** API 文档 MUST 说明字段语义、fallback 和缓存边界
- **AND** 后端测试 MUST 覆盖响应字段与缺失规格回退。
