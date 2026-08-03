## MODIFIED Requirements

### Requirement: 商品卡片

商品列表页 SHALL 使用统一商品卡片展示公开 SKU，并 SHALL 为商品主图、名称、品牌/规格、价格、状态标识、图片加载性能和失败降级提供稳定体验。公开 SKU 有真实主图时，列表接口返回给商品卡片的 `cover_image` SHALL 是可通过后端 `/media/{object_key}` 或等价受控链路读取的图片 URL。列表缩略图或等价轻量优化图片 SHALL 是真实轻量资源；系统 SHALL NOT 仅以 `.thumb` 对象存在但内容等同原图的资源作为图片加载性能优化完成标准。

#### Scenario: 商品卡片信息展示
- **WHEN** 商品列表页获取到公开 SKU 数据
- **THEN** 每个商品卡片 SHALL 展示商品主图或统一占位图、商品名称、品牌/规格摘要、价格信息和必要状态标识
- **AND** 商品卡片 SHALL NOT 以 SKU 编码作为主要展示标题。

#### Scenario: 卡片图片稳定展示
- **WHEN** 商品卡片图片加载中、加载完成或加载失败
- **THEN** 卡片图片区域 SHALL 保持稳定比例和尺寸
- **AND** 页面 SHALL NOT 因图片状态变化产生明显布局跳动、文字遮挡或横向滚动。

#### Scenario: 卡片图片加载失败
- **WHEN** 商品主图缺失、对象不存在、网络超时或图片解码失败
- **THEN** 商品卡片 SHALL 展示统一占位图或品牌化缺图状态
- **AND** 页面 SHALL 保留商品名称、品牌/规格、价格和点击能力
- **AND** 图片失败 SHALL NOT 阻断列表分页、筛选、搜索或跳转。

#### Scenario: 卡片图片缩略图优先
- **WHEN** 小程序商品卡片展示列表、搜索结果、首页推荐或品牌详情商品 Tab 中的公开 SKU
- **THEN** 商品卡片 SHOULD 优先使用列表缩略图或等价轻量优化图片 URL
- **AND** 缩略图缺失时 SHALL 安全回退到原主图或统一占位图
- **AND** 详情页、图片预览或需要高清展示的场景 SHALL NOT 被强制降级为列表缩略图。

#### Scenario: 卡片缩略图为真实轻量资源
- **GIVEN** 公开 SKU 主图对应的同目录 `.thumb` 对象存在
- **WHEN** 商品列表、搜索结果、首页推荐或品牌详情商品 Tab 返回该 `.thumb` URL 作为 `cover_image`
- **THEN** 该 `.thumb` 对象 SHOULD 是经过后端缩放或压缩的轻量图片
- **AND** 对尺寸大于缩略图目标尺寸的原图，`.thumb` bytes SHALL NOT 与原图 bytes 完全一致
- **AND** 系统验收 SHALL NOT 仅以 `.thumb` URL 可访问或对象存在作为图片性能优化通过条件。

#### Scenario: pending 主图返回可访问列表图
- **GIVEN** 公开 SKU 主图 object key 为 `images/default/tiles/pending/<uuid>.<ext>`
- **WHEN** 后端生成商品列表、搜索结果或品牌商品列表的 `cover_image`
- **THEN** 后端 SHALL 优先返回同目录文件名差异化的可访问缩略图 URL
- **AND** 当该缩略图不存在时 SHALL 回退到可访问原主图或统一占位语义
- **AND** 后端 SHALL NOT 返回已知不可访问的 `/media/thumbnails/default/tiles/pending/<uuid>.<ext>`。

#### Scenario: 卡片图片懒加载
- **WHEN** 商品卡片位于首屏外、分页后续内容或用户尚未滚动到的列表区域
- **THEN** 小程序 SHALL 使用原生 `lazy-load` 或等价视口触发策略延迟加载图片
- **AND** 首屏外卡片 SHALL NOT 在页面初始化时一次性触发全部图片请求
- **AND** 懒加载期间 SHALL 展示稳定占位，不影响用户继续浏览文本信息。
