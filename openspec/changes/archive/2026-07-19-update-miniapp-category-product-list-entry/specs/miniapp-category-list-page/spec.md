## MODIFIED Requirements

### Requirement: 分类跳转与埋点
分类页 SHALL 支持一级分类聚合商品列表入口和二级分类精确商品列表入口，并记录必要行为事件。

#### Scenario: 一级分类商品列表入口
- **WHEN** 用户查看当前一级分类对应的右侧标题区或等价入口区域
- **THEN** 页面 SHALL 提供进入该一级分类商品列表的入口
- **AND** 该入口 SHALL 与左侧一级分类切换操作清晰区分
- **AND** 可点击区域 SHALL 不小于 44px 或小程序等效尺寸
- **AND** 页面 SHALL NOT 将左侧一级分类点击改为直接进入商品列表。

#### Scenario: 一级分类跳转
- **WHEN** 用户点击一级分类商品列表入口
- **THEN** 小程序 SHALL 跳转 `pages/product-list/index?categoryId={primaryCategoryId}&categoryName={encodedName}&categoryLevel=primary&sourcePage=category` 或等价商品列表页
- **AND** 点击期间 SHALL 提供原生按压反馈或等价反馈
- **AND** 300ms 内重复点击 SHALL 只触发一次跳转。

#### Scenario: 二级分类跳转
- **WHEN** 用户点击二级分类卡片
- **THEN** 小程序 SHALL 跳转 `pages/product-list/index?categoryId={secondaryCategoryId}&categoryName={encodedName}&categoryLevel=secondary&sourcePage=category` 或等价商品列表页
- **AND** 整个二级分类卡片 SHALL 为点击热区
- **AND** 点击期间 SHALL 提供原生按压反馈
- **AND** 300ms 内重复点击 SHALL 只触发一次跳转。

#### Scenario: 分类跳转失败
- **WHEN** 一级或二级分类目标页面不可达或跳转失败
- **THEN** 小程序 SHALL 展示“页面打开失败，请重试”或等价提示
- **AND** 页面 SHALL 保留当前分类页状态
- **AND** 页面 SHALL NOT 白屏、路由报错或丢失返回能力。

#### Scenario: 分类页行为埋点
- **WHEN** 用户浏览、切换或点击分类页
- **THEN** 系统 SHALL 记录 `category_page_view`、`primary_category_click`、`primary_category_product_list_click`、`secondary_category_click` 和 `category_load_failed` 中适用的事件
- **AND** 一级分类商品入口点击 MAY 在既有 `primary_category_click` 中携带 `action=product_list_entry` 作为等价实现
- **AND** 二级分类点击 SHALL 携带 `action=product_list_entry` 或等价商品列表跳转上下文
- **AND** 事件 SHALL 只包含必要分类 ID、分类名称、分类层级、索引、来源、错误码和是否有缓存
- **AND** 事件 SHALL NOT 包含用户敏感信息、Authorization header、Cookie、手机号、聊天内容或原始 payload。

### Requirement: 分类商品列表承接
分类页 SHALL 将一级分类聚合商品浏览和二级分类精确商品浏览交由小程序商品列表页承接，分类页自身不实现商品列表、筛选或排序。

#### Scenario: 一级分类进入商品列表页
- **WHEN** 用户点击当前一级分类的商品列表入口
- **THEN** 小程序 SHALL 跳转到 `pages/product-list/index?categoryId={primaryCategoryId}&categoryName={encodedName}&categoryLevel=primary&sourcePage=category` 或等价商品列表页
- **AND** 商品列表页 SHALL 负责加载该一级分类下所有启用二级分类的公开 SKU 聚合结果、筛选、排序、分页和状态展示。

#### Scenario: 二级分类进入商品列表页
- **WHEN** 用户点击二级分类卡片
- **THEN** 小程序 SHALL 跳转到 `pages/product-list/index?categoryId={secondaryCategoryId}&categoryName={encodedName}&categoryLevel=secondary&sourcePage=category` 或等价商品列表页
- **AND** 商品列表页 SHALL 负责加载该二级分类下公开 SKU、筛选、排序、分页和状态展示。

#### Scenario: 分类页不重复商品列表能力
- **WHEN** 团队验收分类页与商品列表页边界
- **THEN** 分类页 SHALL NOT 实现商品卡片、价格、商品分页、商品筛选、商品排序或商品列表埋点
- **AND** 分类页 SHALL 只负责分类结构展示、分类切换、一级分类商品入口和二级分类跳转。
