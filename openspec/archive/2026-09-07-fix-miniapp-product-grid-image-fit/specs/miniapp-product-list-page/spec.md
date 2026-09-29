## MODIFIED Requirements

### Requirement: 商品卡片
商品列表页 SHALL 使用统一商品卡片展示公开 SKU，并 SHALL 为商品主图、名称、品牌/规格、价格、状态标识、图片加载性能和失败降级提供稳定体验。公开 SKU 有真实主图时，列表接口返回给商品卡片的 `cover_image` SHALL 是可通过后端 `/media/{object_key}` 或等价受控链路读取的图片 URL。列表缩略图或等价轻量优化图片 SHALL 是真实轻量资源；系统 SHALL NOT 仅以 `.thumb` 对象存在但内容等同原图的资源作为图片加载性能优化完成标准。从品牌列表页进入的品牌分类商品列表页、首页推荐、搜索结果、收藏列表和普通商品列表 SHALL 继续复用商品卡片缩略图优先策略。

#### Scenario: 商品列表保持缩略图优先

- **WHEN** 用户从品牌列表页、首页推荐、搜索结果、收藏列表或普通商品列表查看商品卡片
- **THEN** 商品卡片 SHALL 优先使用列表缩略图或等价轻量优化图片 URL
- **AND** 商品卡片 SHALL NOT 因 SKU 详情页改用高清展示图而直接回退原图字段
- **AND** 非首屏商品卡片图片 SHALL 启用小程序 `lazy-load` 或等价延迟加载策略
- **AND** 商品详情、图片预览或分享场景 SHALL 保留原图或安全高清 URL。

#### Scenario: grid 商品卡片完整显示整图

- **WHEN** 用户在商品列表页查看 `density="grid"` 商品卡片
- **THEN** 商品卡片图片 SHALL 使用完整适配展示整张商品图
- **AND** 商品图片主体 SHALL NOT 因铺满图片框而被上下或左右裁切
- **AND** 图片 SHALL NOT 被拉伸变形
- **AND** 图片完整适配产生的留白或背景 SHALL 与卡片视觉一致，不出现破图、透明空洞或突兀高对比空白
- **AND** 商品卡片 SHALL 继续优先使用列表缩略图或等价轻量优化图片 URL。

#### Scenario: grid 商品卡片图片区域比例稳定

- **WHEN** 团队验收 320、375 和 430px 逻辑宽度下的双列 grid 商品卡片
- **THEN** 每行 SHALL 稳定展示 2 个商品卡片
- **AND** grid 商品卡片图片区域 SHALL 具备足以完整展示方形瓷砖主体的稳定比例或等价高度
- **AND** 骨架屏、加载中、无图占位和加载失败态 SHALL 与最终 grid 图片区域比例一致
- **AND** 商品名称、品牌、规格和参考价格 SHALL 保持可读，不横向溢出、不互相遮挡。

#### Scenario: grid 商品卡片复用场景一致

- **WHEN** 商品列表页、品牌详情商品 Tab 或首页全部产品区域复用 `density="grid"` 商品卡片
- **THEN** 三类场景 SHALL 使用一致的 grid 图片完整适配展示契约
- **AND** 品牌详情商品 Tab 的商品卡片 SHALL 与商品列表页表现一致
- **AND** 首页全部产品区域的商品卡片 SHALL 与商品列表页表现一致
- **AND** 首页新品推荐、热销推荐等 `density="compact"` 商品卡片和搜索页 `density="list"` 商品卡片 SHALL NOT 被本契约强制改动。
