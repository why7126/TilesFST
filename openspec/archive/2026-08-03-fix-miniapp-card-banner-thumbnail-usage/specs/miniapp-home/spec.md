## MODIFIED Requirements

### Requirement: Banner 与快捷入口

小程序首页 SHALL 复用已有后台 Banner 配置能力，并展示固定默认快捷业务入口。首页 Banner SHALL 只读取小程序首页轮播位置；品牌入口 SHALL 进入品牌列表页，品牌列表页轮播 SHALL 使用独立位置。Banner 图片 SHALL 使用后端授权、公开安全且符合性能策略的展示图 URL；若存在缩略图、展示图或压缩图字段，首页 Banner SHALL 优先使用该字段。

#### Scenario: 首页轮播与品牌列表页轮播隔离
- **WHEN** 小程序首页加载 Banner
- **THEN** 首页 SHALL 只展示小程序首页轮播位置中已上线且有效期内的 Banner
- **AND** 首页 SHALL NOT 展示品牌列表页轮播位置 Banner
- **WHEN** 品牌列表页无轮播数据
- **THEN** 首页轮播 SHALL NOT 被用作品牌列表页兜底。

#### Scenario: Banner 图片性能策略
- **WHEN** 小程序首页或品牌列表页展示 Banner 图片
- **THEN** Banner SHALL 优先使用后端提供的缩略图、展示图、压缩图或等价轻量安全 URL
- **AND** 自定义上传 Banner 图片时后端 SHALL 生成可访问的同目录缩略图对象供小程序 Banner 使用
- **AND** 若 Banner 只能使用原图 URL，原图 SHALL 满足项目确认的尺寸、压缩或运营上传约束
- **AND** Banner 图片缺失、缩略图缺失或加载失败时 SHALL 展示稳定占位或隐藏当前 Banner 项
- **AND** Banner 图片失败 SHALL NOT 阻断快捷入口、商品分区、品牌列表或页面其他内容展示
- **AND** Banner 跳转、指示点、轮播切换和既有点击行为 SHALL 保持可用。

### Requirement: 新品热销与全部产品承接

小程序首页 SHALL 展示新品推荐、热门商品和全部商品瀑布流，并 SHALL 控制多分区商品卡片图片的首屏加载压力、失败降级和重复数据回退。首页商品分区返回的商品卡片 `cover_image` SHALL 与商品列表页共用同一可访问缩略图解析策略。

#### Scenario: 首页商品图片加载优先级
- **WHEN** 首页同时存在 Banner、新品推荐、热门商品和全部商品瀑布流
- **THEN** 首页 SHALL 优先加载首屏可见商品卡片图片
- **AND** 首屏外或后续瀑布流卡片图片 SHALL 使用懒加载或等价延迟加载策略
- **AND** 首页商品卡片 SHALL 优先使用与商品列表页一致的缩略图或等价轻量优化图片 URL
- **AND** 首页 SHALL NOT 在初始化阶段一次性触发所有分区、所有卡片的图片请求。
