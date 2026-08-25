## MODIFIED Requirements

### Requirement: 媒体 API 必须提供多规格 URL 语义

商品、SKU 或媒体相关 API MUST 提供 `thumbnail_url`、`display_url`、`original_url` 或等价语义字段，使小程序、店主 Web 和管理端可以按场景选择图片规格。证书详情等品牌证书媒体 API 也 MUST 遵守同一语义：图片证书详情普通展示 MUST 使用 `display_url` 或等价展示图，图片预览 MUST 使用 `original_url`、`preview_url` 或等价高清 URL，PDF/文档证书 MUST 使用文件打开或占位策略而不是图片 `display_url`。API MUST 明确 URL 类型、签名、缓存、权限、过期和 fallback 策略，并 MUST 同步 OpenAPI、Orval、API 文档和测试。

#### Scenario: 商品媒体响应包含多规格 URL

- **WHEN** 客户端请求包含图片媒体的商品、SKU 或媒体详情
- **THEN** 响应 MUST 提供轻量列表图、详情展示图和高清预览图的 URL 语义
- **AND** 响应 MUST NOT 暴露原始 object key、对象存储 endpoint、bucket 名称、access key、secret key 或未授权素材路径
- **AND** 老客户端兼容策略 MUST 有文档和测试覆盖。

#### Scenario: 证书详情图片媒体响应包含 display URL

- **WHEN** 小程序请求图片类品牌证书详情
- **THEN** 证书详情响应 MUST 为图片媒体项提供 `display_url` 或等价详情展示图 URL
- **AND** 响应 MUST 为图片预览提供 `original_url`、`preview_url` 或等价高清 URL
- **AND** 详情普通展示 fallback MUST 使用 `thumbnail_url` 或安全占位，不得直接使用原图 URL 作为默认兜底
- **AND** 图片证书和 PDF/文档证书的字段语义 MUST 可由 `media_type`、MIME 或等价字段区分。

#### Scenario: API 字段变更同步

- **WHEN** 多规格 URL 字段或响应结构发生变化
- **THEN** OpenAPI MUST 更新
- **AND** Orval 生成物 MUST 更新
- **AND** API 文档 MUST 说明字段语义、fallback 和缓存边界
- **AND** 后端测试 MUST 覆盖响应字段与缺失规格回退。
