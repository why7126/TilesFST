## MODIFIED Requirements

### Requirement: 微信小程序品牌主页信息区
系统 SHALL 提供单品牌主页/详情页，并在页面上半部分展示可公开品牌图片和品牌基础信息。品牌主页顶部品牌图位 SHALL 作为首屏 Hero 大图展示位，普通展示 SHALL 优先使用后端受控 `display` 规格；品牌列表、品牌卡、商品详情品牌入口和证书详情品牌入口等小 Logo 场景 SHALL 继续优先使用后端受控真实缩略图。品牌主页信息区 SHALL 区分 Hero 展示 URL、小 Logo 展示 URL、高清预览或分享 URL，避免首屏直接加载原图。

#### Scenario: 品牌详情顶部 Hero 展示使用 display 规格

- **WHEN** 用户进入品牌主页/详情页且品牌存在 Logo 或品牌图片
- **THEN** 页面上半部分顶部 Hero SHALL 优先请求 `brand_hero_display_url` 或等价 `display` 规格 URL
- **AND** `display` 规格缺失、为空或加载失败时 SHALL 降级请求 `brand_hero_thumbnail_url` 或等价轻量缩略图
- **AND** `display` 与 `thumbnail` 均不可用时 SHALL 展示安全视图占位、品牌名占位或可理解失败态
- **AND** 品牌主页顶部 Hero SHALL NOT 通过 `brand_logo_url`、`original_url`、`preview_url`、旧 `url`、语义不明 `image_url` 或不存在的本地静态资源冷加载原图或失败占位。
