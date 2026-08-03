## MODIFIED Requirements

### Requirement: 新品热销与全部产品承接

小程序首页 SHALL 展示新品推荐、热门商品和全部商品瀑布流，并 SHALL 控制多分区商品卡片图片的首屏加载压力、失败降级和重复数据回退。首页商品分区返回的商品卡片 `cover_image` SHALL 与商品列表页共用同一可访问缩略图解析策略。

#### Scenario: 首页商品分区展示
- **WHEN** 首页获取到新品、热门商品或全部商品数据
- **THEN** 首页 SHALL 按设计展示新品推荐、热门商品和全部商品瀑布流中的可见分区
- **AND** 商品卡片 SHALL 复用统一商品卡片核心展示商品图片、名称、品牌/规格、价格和状态标识。

#### Scenario: 首页商品图片加载优先级
- **WHEN** 首页同时存在 Banner、新品推荐、热门商品和全部商品瀑布流
- **THEN** 首页 SHALL 优先加载首屏可见商品卡片图片
- **AND** 首屏外或后续瀑布流卡片图片 SHALL 使用懒加载或等价延迟加载策略
- **AND** 首页 SHALL NOT 在初始化阶段一次性触发所有分区、所有卡片的图片请求。

#### Scenario: 首页 pending 主图缩略图可访问
- **GIVEN** 首页新品、热门商品或全部商品分区中的公开 SKU 主图 object key 为 `images/default/tiles/pending/<uuid>.<ext>`
- **WHEN** 首页接口生成商品卡片 `cover_image`
- **THEN** 首页 SHALL 返回同目录文件名差异化的可访问缩略图 URL，或在缩略图缺失时回退到可访问原主图
- **AND** 首页 SHALL NOT 返回已知不可访问的 `/media/thumbnails/default/tiles/pending/<uuid>.<ext>`。

#### Scenario: 首页商品图片失败降级
- **WHEN** 首页商品卡片图片缺失、对象不存在、加载超时或解码失败
- **THEN** 首页 SHALL 展示统一占位图或品牌化缺图状态
- **AND** 首页 SHALL 保留商品名称、品牌/规格、价格、分区标题和商品点击能力
- **AND** 图片失败 SHALL NOT 阻断 Banner、商品分区、瀑布流分页或其他已加载内容展示。

#### Scenario: 首页商品去重与兜底
- **WHEN** 新品、热门商品和全部商品存在重复 SKU、缺少图片字段或分区数据为空
- **THEN** 首页 SHALL 按既定规则去重或兜底展示
- **AND** 缺少图片字段 SHALL 降级为占位图或缩略图缺失回退
- **AND** 页面 SHALL NOT 因单个分区图片异常导致其他分区不可用。
