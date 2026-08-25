## MODIFIED Requirements

### Requirement: SKU 详情页微信分享

SKU 详情页 SHALL 支持分享给微信朋友和分享到微信朋友圈，并 SHALL 保留当前 SKU 参数、分享图兜底和分享直达异常态。分享图字段 SHALL 与详情普通展示字段解耦，默认 SHALL 优先使用明确分享轻量字段、`display_url`、`thumbnail_url` 或安全兜底图；不得因兼容旧字段而默认下发原图。

#### Scenario: SKU 详情分享给微信朋友

- **WHEN** 用户在 SKU 详情页触发微信朋友分享
- **THEN** 小程序 SHALL 返回微信原生分享对象
- **AND** 分享路径 SHALL 指向当前 SKU 详情页并携带有效 `skuId` 和 `source=share` 或等价来源参数
- **AND** 分享标题 SHALL 优先使用商品分享标题，未配置时 SHALL 使用 SKU 名称与品牌名称组合
- **AND** 分享图 SHALL 优先使用明确分享轻量字段、商品主图 `display_url`、`thumbnail_url` 或安全兜底图
- **AND** 分享图 SHALL NOT 默认回退到 `original_url`、`preview_url` 或原始 `media[].url`
- **AND** 若平台限制要求高清分享图，验收 SHALL 将该行为记录为分享入口例外，并证明普通展示未受影响。

#### Scenario: SKU 分享图原图 fallback 回归测试

- **GIVEN** SKU 主图同时存在 `.jpg` 原图和 `.thumb.webp` 或 `.display.webp` 派生图
- **WHEN** 小程序加载 SKU 详情并生成分享对象
- **THEN** `share.image_url` SHALL 优先指向轻量分享图、`display_url`、`thumbnail_url` 或安全兜底图
- **AND** `share.image_url` SHALL NOT 在默认路径中指向原图 `.jpg`
- **AND** AppData、Network 或等价 evidence SHALL 记录分享图 URL 类型与页面渲染结果。
