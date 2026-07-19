---
req_id: REQ-0041-miniapp-home
status: done
created_at: 2026-07-16 09:09:51
updated_at: 2026-07-17 22:58:09
recorded_by: product
source: 附件原型与需求包
priority_hint: P1
parent_requirement:
---

# 微信小程序首页

开发面向终端客户、设计师、装修业主和门店销售的菲尚特瓷砖微信小程序首页，作为对外数字化瓷砖展厅入口，支持用户快速浏览、筛选、收藏、分享并咨询门店。

# 原始描述

用户要求：开发微信小程序的首页，具体内容详见附件，无须理会文档里面的版本号。

附件包含：

- `/Users/why7126/Downloads/feishangte-miniapp-home-v2/requirement.md`
- `/Users/why7126/Downloads/feishangte-miniapp-home-v2/context.md`
- `/Users/why7126/Downloads/feishangte-miniapp-home-v2/prototype.html`
- `/Users/why7126/Downloads/feishangte-miniapp-home-v2/prototype.png`
- `/Users/why7126/Downloads/feishangte-miniapp-home-v2/README.md`

核心需求摘要：

- 首页面向终端客户，不承载后台编辑、库存、订单、客户管理等管理功能。
- 首屏需要建立品牌可信度，并在 10 秒内让用户找到常用选砖入口。
- 页面结构包含顶部品牌导航、搜索入口、品牌 Banner、快捷找砖入口、新品推荐、热销推荐、品牌服务与咨询入口、底部 TabBar。
- 搜索范围覆盖商品名称、商品编号、品牌名称、规格、系列名称，点击进入搜索页。
- Banner 支持后台配置图片、标题、副标题、跳转类型、跳转目标、排序、上下架状态与生效时间，支持轮播、手势切换和按配置跳转。
- 快捷入口默认包含按空间、按规格、按风格、按颜色、全部分类，入口顺序、名称和图标可由后台配置。
- 新品推荐默认展示 3 到 6 个商品卡片，展示主图、编号、名称、规格、价格或到店询价，并支持新品角标与更多入口。
- 热销推荐使用大卡片或双列卡片，支持收藏按钮；推荐策略优先后台人工置顶，未配置时按详情访问量、收藏量与咨询量综合排序。
- 品牌服务区展示正品保障、免费选砖建议、到店预约、联系门店；联系门店支持微信客服、电话或复制微信号。
- 底部 TabBar 固定：首页、分类、找砖、收藏、我的，首页为品牌金选中态。
- 商品卡片字段需能映射后台 SKU 数据，包括 `productId`、`productName`、`skuCode`、`coverImage`、`specification`、`categoryName`、`brandName`、`styleTags`、`applicableSpaces`、`retailPrice`、`priceDisplayMode`、`isNew`、`isHot`、`isFavorite`。
- 建议提供首页聚合接口 `GET /api/miniapp/home`，返回 `store`、`banners`、`quickEntries`、`newProducts`、`hotProducts`、`serviceEntries`。
- 建议埋点 `home_view`、`home_search_click`、`home_banner_click`、`home_quick_entry_click`、`home_product_click`、`home_more_click`、`home_favorite_click`、`home_contact_click`、`home_share`。
- 页面状态需覆盖正常、骨架屏加载、推荐为空时模块隐藏、全部为空时品牌插画空状态、网络异常重试、图片失败占位图。
- 非功能要求包括首屏可交互建议小于 2 秒、首屏图片优先 WebP 并按设备宽度裁剪、点击区域不小于 44x44 pt、支持微信分享、支持后台内容上下架后快速同步。
- 视觉参照 `prototype.png` 和 `prototype.html`：暖白背景、墨黑主视觉、品牌金点缀、现代轻奢、专业建材展厅质感；原型版本号不作为项目需求版本事实。

多条需求评估：本输入虽包含搜索、Banner、推荐、收藏、咨询等多个模块，但它们共同构成微信小程序首页这一单一页面交付单元，验收闭环一致，因此记录为一条 REQ，不拆分 peer 需求。

# 待澄清

- [x] 小程序技术形态确认使用原生微信小程序。
- [x] 首页数据复用现有店主端/后台接口聚合；若新增聚合/事件接口，需同步 API 文档、OpenAPI、Orval 和测试。
- [x] Banner 后台配置能力已有；快捷入口、服务入口后台配置缺口拆分后台配置需求。
- [x] 门店信息、搜索页、商品详情页、分享、咨询、热销行为统计纳入首页首期闭环；收藏和预约表单不纳入本期。
- [x] 热销推荐统计纳入本期，但不包含收藏量；以详情访问、分享、咨询等本期行为为基础，统计不足时人工配置或时间/排序字段降级。
- [ ] 价格展示规则、客服/电话/微信号/导航配置来源需要产品确认；到店询价规则暂不纳入本期。
- [x] 已将附件中的 prototype 复制到本 REQ 的 `prototype/miniapp/` 目录。

# 探索结论

- 小程序技术形态确认使用原生微信小程序。
- 首页数据复用现有店主端/后台接口聚合。
- Banner 后台配置能力已具备；快捷入口、服务入口后台配置能力另拆后台配置需求。
- 门店信息、搜索页、商品详情页纳入首页首期闭环。
- 分享功能、咨询功能、热销行为统计按产品确认纳入本期需求范围。
- 收藏、预约表单、到店询价规则、快捷入口后台配置、服务入口后台配置仍不纳入本期。
- 热销行为统计以详情访问、分享、咨询等本期可产生行为为基础；收藏量不纳入，因为收藏功能仍不做。
- 已将附件原型沉淀到 `prototype/miniapp/`。
