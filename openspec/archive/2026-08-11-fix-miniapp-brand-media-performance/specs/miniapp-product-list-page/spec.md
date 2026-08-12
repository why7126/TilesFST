# miniapp-product-list-page Delta

## MODIFIED Requirements

### Requirement: 商品卡片

商品列表页 SHALL 使用统一商品卡片展示公开 SKU，并 SHALL 为商品主图、名称、品牌/规格、价格、状态标识、图片加载性能和失败降级提供稳定体验。公开 SKU 有真实主图时，列表接口返回给商品卡片的 `cover_image` SHALL 是可通过后端 `/media/{object_key}` 或等价受控链路读取的图片 URL。列表缩略图或等价轻量优化图片 SHALL 是真实轻量资源；系统 SHALL NOT 仅以 `.thumb` 对象存在但内容等同原图的资源作为图片加载性能优化完成标准。从品牌列表页进入的品牌分类商品列表页 SHALL 继续复用商品卡片缩略图优先策略。

#### Scenario: 品牌分类商品列表保持缩略图优先

- **WHEN** 用户从品牌列表页点击品牌类目并进入商品列表页
- **AND** 商品列表请求携带 `brandId` 与 `categoryId`
- **THEN** 商品卡片 SHALL 优先使用列表缩略图或等价轻量优化图片 URL
- **AND** 商品卡片 SHALL NOT 因品牌过滤、分类过滤或入口参数组合而直接回退原图字段
- **AND** 非首屏商品卡片图片 SHALL 启用小程序 `lazy-load` 或等价延迟加载策略
- **AND** 商品详情、图片预览或分享场景 SHALL 保留原图或安全高清 URL。

#### Scenario: 品牌分类商品列表媒体性能 evidence

- **WHEN** 团队验收品牌分类商品列表页图片加载性能
- **THEN** evidence SHALL 覆盖商品卡片图片 URL、HTTP 状态、资源大小、加载耗时和小程序渲染结果
- **AND** evidence SHALL 区分请求 `.thumb` URL、实际 resolved key 和是否回退原图
- **AND** 缩略图缺失、0 字节、体积无收益或回退原图 SHALL 标记为性能风险或失败项。
