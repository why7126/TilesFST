## Context

REQ-0056 是 `REQ-0047-product-list-common-component-application` 的体验收敛需求，已通过评审并纳入 `sprint-009`。既有 `miniapp-product-list-page` spec 要求商品列表页提供筛选、排序和搜索上下文保留；当前产品决策调整为商品列表页只负责直接浏览商品，搜索/筛选能力留在搜索页或入口前置页面。

原型位于 `issues/requirements/archive/REQ-0056-product-list-card-only-layout/prototype/miniapp/`，优先级为 HTML > context.md > acceptance.md > `rules/ui-design.md` > 既有 spec。当前需求为小程序端，不触发 Web UI Explore Gate。

## Goals / Non-Goals

**Goals:**

- 移除商品列表页内搜索、筛选、排序控件，减少首屏干扰。
- 将商品列表页改为一行 2 个商品卡片的双列浏览布局。
- 复用现有商品卡片 `grid` 展示密度，并对齐首页“热销推荐”的信息层级。
- 保留入口上下文、分页、刷新、加载更多、空态、错误态和详情跳转。
- 分类入口中，一级分类查询需覆盖本级直接挂载 SKU 与启用二级子分类 SKU。
- 明确搜索页自身能力不受影响，避免误删搜索页筛选或结果页功能。

**Non-Goals:**

- 不改造微信小程序搜索页 `pages/search/index`。
- 不新增或修改后端商品列表 API、数据库、对象存储、Web 管理端或 Orval 生成物。
- 不新增收藏、询价、购物车、在线下单、客服找砖或复杂推荐算法。
- 不重建商品卡片组件；如现有 `product-card` 可满足，应优先调整列表页调用与布局。

## Decisions

### D1. 商品列表页作为轻量浏览页

实现阶段 MUST 删除或隐藏商品列表页内搜索框、筛选按钮、排序 tabs、筛选 chips 和筛选抽屉入口。入口参数仍作为初始查询上下文存在，例如分类、品牌、首页推荐 section 或搜索页传入 keyword，但列表页不提供二次检索/筛选控件。

备选方案是保留搜索/筛选并折叠为二级入口，但这仍会让商品列表页承担工具型列表职责，违背 REQ-0056 的“直接浏览”目标，因此不采用。

### D2. 双列布局复用商品卡片 grid 密度

实现阶段 SHOULD 在 `pages/product-list/index.wxml` 中使用双列 grid 容器，并将 `product-card` 以 `density="grid"` 或等价视觉密度渲染。卡片信息、图片占位、价格强调和点击跳转应沿用现有商品卡片能力，避免为商品列表页复制新的卡片 DOM。

### D3. 查询与接口保持兼容

商品列表页继续请求现有商品列表接口，但仅传入入口上下文、分页和必要默认排序。不得因为页面不展示筛选控件而破坏搜索页或后端已有筛选接口；若实现发现现有请求构造强依赖筛选字段，应在实现中用空筛选快照或默认值兼容，而不是改 API 契约。

分类查询语义保持在现有商品列表接口内兼容修正：`categoryLevel=primary` SHALL 返回该一级分类自身直接挂载的公开 SKU，以及该一级分类下启用二级分类的公开 SKU；`categoryLevel=secondary` SHALL 精确返回当前二级分类公开 SKU。该修正不新增接口参数、不改变响应 Schema、不触发 Orval。

### D4. 埋点收敛

保留 `product_list_page_view`、商品曝光、商品点击、刷新、加载更多和加载失败等浏览类埋点。商品列表页不再触发筛选打开、筛选应用、排序切换等交互埋点；搜索页自身埋点保持原样。

### D5. 原型冲突决议

- 既有 spec 中 `筛选与排序` 要求被 REQ-0056 覆盖，本 Change 使用 `REMOVED Requirements` 移除商品列表页筛选/排序交互契约。
- 既有 spec 中搜索入口进入商品列表页要求“筛选、排序和分页请求继续携带关键词”，本 Change 修改为商品列表页保留关键词上下文并用于初始查询和展示，但不提供页面内筛选/排序控件。
- 既有 spec 商品卡片字段要求包含 SKU 编码；REQ-0056 与首页热销推荐对齐，双列卡片中 SKU 编码不再是必展字段，可由品牌/规格等辅助信息承接扫读。
- prototype HTML 表达双列卡片密度；PNG 未导出，后续实现验收以 HTML/context/acceptance 为基准，并补充 320 / 375 / 430 pt evidence。

## Risks / Trade-offs

- [Risk] 移除商品列表页筛选后，用户从分类入口缩小范围的能力下降 → Mitigation: 搜索/筛选能力保留在搜索页或入口前置页面；商品列表页聚焦快速浏览。
- [Risk] 搜索页跳转商品列表时 keyword 语义被误删 → Mitigation: 商品列表页继续支持 `keyword` 初始查询与标题/空态文案，但不展示二次搜索控件。
- [Risk] 一级分类下存在直挂 SKU 时被误判为空 → Mitigation: 后端 `categoryLevel=primary` 过滤同时包含本级分类 ID 与启用二级子分类 ID，并用回归测试覆盖。
- [Risk] 双列卡片在 320 pt 小屏挤压文字 → Mitigation: 商品名称限制 2 行，辅助信息单行截断，图片使用稳定比例。
- [Risk] 实现误删搜索页筛选逻辑 → Mitigation: tasks 明确搜索页为非目标，并补静态回归检查。

## Migration Plan

1. 调整商品列表页 WXML/WXSS，移除搜索/筛选/排序控件并改为双列 grid。
2. 调整商品列表页 TS/JS 状态与事件，删除页面内筛选/排序交互路径，保留入口上下文和分页状态。
3. 保持搜索页自身能力与列表接口兼容。
4. 补充静态测试和人工 evidence，覆盖控件移除、双列布局、入口上下文、分页刷新和搜索页能力不回归。

Rollback 策略：如双列布局导致严重可用性问题，可在同一 Change 中回退商品列表页布局到上一版本；搜索页与 API 不应受到本 Change 影响。
