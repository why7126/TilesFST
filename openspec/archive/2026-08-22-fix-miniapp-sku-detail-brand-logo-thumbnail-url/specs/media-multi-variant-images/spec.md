## MODIFIED Requirements

### Requirement: 媒体 API 必须提供多规格 URL 语义

商品、SKU、品牌、证书或媒体相关 API MUST 提供 `thumbnail_url`、`display_url`、`original_url` 或等价语义字段，使小程序、店主 Web 和管理端可以按场景选择图片规格。API MUST 明确 URL 类型、签名、缓存、权限、过期和 fallback 策略，并 MUST 同步 OpenAPI、Orval、API 文档和测试。小程序 SKU 详情接口中的品牌 Logo MUST 暴露 `brand_logo_thumbnail_url` 或等价轻量字段。

#### Scenario: API 返回三规格 URL

- **WHEN** 客户端请求商品、SKU、品牌、证书或媒体详情
- **THEN** API SHOULD 返回对应资源的 `thumbnail_url`、`display_url`、`original_url` 或等价字段
- **AND** 小程序 SKU 详情接口 SHALL 在 `data.brand.brand_logo_thumbnail_url` 返回品牌 Logo 缩略图或等价轻量 URL
- **AND** API 文档 MUST 说明字段语义、fallback 和缓存边界
- **AND** OpenAPI / Orval 生成物 MUST 与后端 Schema 保持一致
- **AND** 客户端 MUST 按场景选择对应规格，列表、卡片和轻量展示 SHALL NOT 默认使用原图。

#### Scenario: 品牌 Logo 小图展示禁止原图 fallback

- **WHEN** 小程序商品详情页、品牌列表或品牌详情页展示品牌 Logo 小图
- **THEN** 客户端 SHALL 优先使用 `brand_logo_thumbnail_url` 或等价缩略图字段
- **AND** 缩略图缺失、为空或不可访问时 SHALL 使用安全占位或受控降级
- **AND** 验收记录 MUST NOT 将 `brand_logo_url` 原图直接请求视为缩略图性能通过。
