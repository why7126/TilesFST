---
requirement_id: REQ-0060-brand-list-page
status: done
created_at: 2026-07-19 23:28:20
updated_at: 2026-07-20 22:47:59
owner: product
source: requirement.md
---

# 验收清单

## 功能 AC

- [ ] AC-001 小程序存在可进入品牌列表页的“品牌”入口。
- [ ] AC-002 原“找砖”入口文案已调整为“品牌”，且页面标题、导航标题和入口语义一致。
- [ ] AC-003 点击“品牌”入口进入品牌列表页，不得继续降级进入搜索页、分类页或找砖页。
- [ ] AC-004 品牌列表页顶部展示品牌轮播区域。
- [ ] AC-005 品牌轮播支持自动播放、循环播放和指示点，交互与首页轮播一致。
- [ ] AC-006 品牌轮播图片、标题、副标题和跳转目标按接口或配置渲染。
- [ ] AC-007 点击有效品牌轮播项可进入配置目标；目标不可达时安全降级并提示。
- [ ] AC-008 品牌列表以一行 2 个卡片展示。
- [ ] AC-009 品牌卡片至少展示品牌 Logo 和品牌名称。
- [ ] AC-010 品牌卡片可展示品牌简介、品牌标语、商品数量或“查看品牌主页”等辅助信息。
- [ ] AC-011 品牌列表仅展示启用且公开可见的品牌。
- [ ] AC-012 点击品牌卡片优先进入品牌详情页/主页；若未交付，可进入品牌商品列表并携带品牌筛选参数。
- [ ] AC-013 已下架、未公开或缺少有效跳转目标的品牌不得打开无效页面。
- [ ] AC-014 品牌列表支持首次加载、加载中、加载失败、空状态和重试。
- [ ] AC-015 若品牌数量较多，页面支持分页或上拉加载更多；若一次加载，需说明品牌数量容量边界。

## 数据与接口 AC

- [ ] AC-DATA-001 品牌列表复用现有品牌管理数据源，不新增重复品牌表。
- [ ] AC-DATA-002 品牌轮播优先复用已有 Banner 管理能力；若实现品牌页专属轮播位，OpenSpec design 必须说明配置来源。
- [ ] AC-DATA-003 小程序端通过后端接口获取品牌和轮播数据，不得直连未授权对象存储。
- [ ] AC-DATA-004 图片 URL 必须是公开安全 URL 或后端授权 URL，不暴露 MinIO 原始 object key。
- [ ] AC-DATA-005 API 响应不得暴露管理端内部字段、内部备注、未公开品牌或未授权素材。
- [ ] AC-DATA-006 若新增或调整 API，必须同步 OpenAPI、Orval、接口文档和测试；若复用现有 API，Change 中需说明复用依据。

## UI / 体验 AC

- [ ] AC-UI-001 页面视觉沿用小程序首页的暗色旗舰风与品牌金强调，不使用大面积促销红、纯黑或纯白。
- [ ] AC-UI-002 品牌轮播高度比例、圆角、指示点和标题层级与首页轮播对齐。
- [ ] AC-UI-003 双列品牌卡片在 320、375、430 pt 宽度下无横向滚动、文字重叠或卡片挤压变形。
- [ ] AC-UI-004 品牌 Logo 区域尺寸稳定，图片加载前后不造成列表布局跳动。
- [ ] AC-UI-005 品牌 Logo 加载失败时展示品牌名称首字、品牌占位或统一占位图，不展示破图。
- [ ] AC-UI-006 品牌名称最多展示 1 到 2 行，超长内容使用省略号或合理换行。
- [ ] AC-UI-007 品牌卡片整卡可点击，点击区域不小于 44x44 pt，并有小程序按压反馈。
- [ ] AC-UI-008 页面顶部、轮播、列表和底部安全区不与自定义导航或 TabBar 重叠。
- [ ] AC-UI-009 空状态、错误态和加载态在小屏下不遮挡导航、TabBar 或主要操作。

## 小程序导航与设备验收 AC

> 来源：`docs/knowledge-base/best-practices/miniapp-custom-navigation.md`

- [ ] AC-MINIAPP-001 品牌列表页按页面形态确认导航策略，标题、返回按钮和右侧原生胶囊 reserve 不重叠。
- [ ] AC-MINIAPP-002 页面主体使用统一导航 offset 或 spacer，首屏轮播和加载/空/错态不被 fixed 或 sticky 导航遮挡。
- [ ] AC-MINIAPP-003 返回按钮如出现，需支持页面栈返回；分享或外部直达无页面栈时有首页兜底。
- [ ] AC-MINIAPP-004 DevTools 至少覆盖 320、375、430 pt 视口，记录首屏内容、胶囊避让、双列卡片和 TabBar 遮挡结论。
- [ ] AC-MINIAPP-005 真机验收不可用时必须标记 blocked 或 follow_up，不得把 DevTools 截图写作真机通过。

## 埋点 AC

- [ ] AC-TRACK-001 品牌列表页曝光记录 `brand_list_page_view` 或等价事件。
- [ ] AC-TRACK-002 品牌轮播点击记录轮播 ID、跳转类型和位置索引。
- [ ] AC-TRACK-003 品牌卡片点击记录品牌 ID、位置索引和来源入口。
- [ ] AC-TRACK-004 埋点不得记录手机号、地址、微信号、授权凭据等与品牌浏览无关的敏感信息。

## 文档与原型 AC

- [ ] AC-DOC-001 `user-stories.md`、`business-flow.md`、`acceptance.md`、`trace.md` 均已补齐并保持 `pending_review` 状态。
- [ ] AC-DOC-002 `prototype/miniapp/context.md` 与 `prototype/miniapp/prototype.html` 可作为后续设计与实现验收参考。
- [ ] AC-DOC-003 `prototype/miniapp/prototype.png` 可在后续从 HTML 导出；缺 PNG 不阻塞评审。
- [ ] AC-DOC-004 后续 `/req-opsx` 的 design.md 必须引用 `trace.md` 中的 `knowledge_base_refs`。

## 横切 AC（knowledge-base）

本 REQ 为微信小程序访客端品牌列表页，不命中 `req-complete` 规定的 `admin-list`、`admin-form`、`admin-modal`、`media-upload` 标签；无需要转化的管理端横切 AC。小程序导航相关知识库要求已转化到上方“小程序导航与设备验收 AC”。
