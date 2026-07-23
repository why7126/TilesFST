# miniapp-category-list-page Specification

## Purpose
TBD - created by archiving change add-miniapp-category-list-page. Update Purpose after archive.
## Requirements
### Requirement: 微信小程序分类列表页入口
系统 SHALL 提供微信小程序 `pages/category/index` 分类列表页，作为底部 TabBar「分类」一级频道，用于展示一级与二级瓷砖分类结构。

#### Scenario: 分类 Tab 进入页面
- **WHEN** 用户点击底部 TabBar「分类」
- **THEN** 小程序 SHALL 打开 `pages/category/index`
- **AND** 页面 SHALL 展示页面标题、左右双栏分类主体和底部 TabBar
- **AND** 页面 SHALL NOT 展示商品卡片、价格、收藏按钮、筛选排序栏、热门分类模块、订单、库存、新增、编辑或上下架入口。
- **AND** 页面 SHALL NOT 展示店铺 Logo/Header 模块或分类页搜索框。

#### Scenario: 分类页保持小程序首页视觉一致
- **WHEN** 用户查看分类页
- **THEN** 页面 SHALL 延续小程序首页深色高端视觉
- **AND** 底部 TabBar 顺序 SHALL 为“首页、分类、找砖、收藏、证书”
- **AND** 当前“分类”Tab SHALL 使用品牌金或等价高亮表示选中态。

### Requirement: 一级与二级分类展示

分类页 SHALL 以左侧一级分类导航和右侧二级分类宫格展示两级启用分类，使用户可以快速定位目标品类；二级分类名称 SHALL 在主流小程序视口中保持可辨识，超过 4 个字时不得因过早省略导致用户无法判断分类含义。

#### Scenario: 二级分类宫格

- **WHEN** 当前一级分类存在二级分类
- **THEN** 右侧区域 SHALL 展示当前一级分类名称
- **AND** 二级分类 SHALL 按三列宫格展示
- **AND** 每个二级分类 SHALL 展示分类名称
- **AND** 4 字以内二级分类名称 SHALL 正常显示且布局不得回退
- **AND** 5-8 字二级分类名称 SHALL 可被用户完整识别或以业务可接受方式清晰展示
- **AND** 超过 8 字二级分类名称 SHALL 不遮挡相邻分类、商品列表、导航栏或其他操作区
- **AND** 二级分类名称 SHALL NOT 在超过 4 个字时仅展示前 4 个字并以 `...` 省略导致含义不可辨识
- **AND** 页面 SHALL NOT 展示二级分类商品数量、简介、价格或运营 Banner。

#### Scenario: 二级分类长名称移动可用性

- **WHEN** 团队在微信开发者工具、iOS 真机、Android 真机或 320 到 430 pt 宽度范围验收分类页
- **THEN** 二级分类长名称 SHALL 保持可辨识
- **AND** 二级分类卡片 SHALL 不发生文本重叠、横向滚动、点击热区错位或底部 TabBar 遮挡
- **AND** 点击长名称二级分类 SHALL 进入对应二级分类商品列表
- **AND** 跳转参数中的 `categoryId`、`categoryName`、`categoryLevel=secondary` 和 `sourcePage=category` SHALL 与当前二级分类一致。

### Requirement: 小程序公开分类树数据
系统 SHALL 为分类页提供公开分类树数据，复用后台类目主数据并过滤内部字段和停用分类。

#### Scenario: 分类树接口返回两级公开分类
- **WHEN** 小程序请求公开分类树数据
- **THEN** 后端 SHALL 返回最多两级启用分类
- **AND** 每个一级分类 SHALL 至少包含 `id`、`name`、`sort` 和 `children`
- **AND** 每个二级分类 SHALL 至少包含 `id`、`name` 和 `sort`
- **AND** 每个二级分类 MAY 包含兼容字段 `coverUrl`
- **AND** 响应 SHALL 包含数据版本号 `version`
- **AND** 响应 SHALL NOT 暴露后台内部字段、内部备注、未授权素材、原始 object key、Authorization header、Cookie 或敏感配置。

#### Scenario: 分类排序与状态过滤
- **WHEN** 分类树中存在停用分类或不同排序值
- **THEN** 后端 SHALL 过滤 `status` 非启用的一级和二级分类
- **AND** 一级和二级分类 SHALL 分别按排序值升序排列
- **AND** 排序值相同时 SHALL 按创建时间升序排列。

#### Scenario: 二级分类图片兼容字段
- **WHEN** 二级分类响应包含 `coverUrl`
- **THEN** 后端 SHALL 返回可公开访问的安全 URL
- **AND** 小程序分类列表页 SHALL NOT 渲染该图片资源
- **AND** 小程序 SHALL NOT 使用原始大图或原始 object key
- **AND** 前端 SHALL NOT 自动取第一款商品主图替代分类展示图。

### Requirement: 缓存、刷新与页面恢复
分类页 SHALL 支持本地缓存优先渲染、版本号静默刷新和页面返回状态恢复，避免网络波动导致白屏或闪动。

#### Scenario: 缓存优先渲染
- **WHEN** 用户进入分类页且本地存在有效分类缓存
- **THEN** 小程序 SHALL 先渲染缓存数据
- **AND** 同时 MAY 静默请求最新分类树
- **AND** 刷新失败 SHALL NOT 清空已展示缓存。

#### Scenario: 无缓存首次加载
- **WHEN** 用户首次进入分类页且没有可用缓存
- **THEN** 页面 SHALL 展示与最终布局一致的骨架屏
- **AND** 左栏和右栏 SHALL 分别展示深色骨架块
- **AND** 骨架屏 SHALL NOT 使用亮白闪烁。

#### Scenario: 版本变化后无闪动更新
- **WHEN** 后端返回的分类树 `version` 与本地缓存不同
- **THEN** 小程序 SHALL 更新分类数据和缓存
- **AND** 更新过程 SHALL 避免整体闪动
- **AND** 若当前一级分类仍存在，SHALL 保留当前一级分类。

#### Scenario: 返回分类页恢复状态
- **WHEN** 用户从分类商品列表页或 SKU 详情页返回分类页
- **THEN** 页面 SHALL 恢复当前一级分类、左侧滚动位置和右侧滚动位置
- **AND** 缓存有效时 SHALL NOT 重新显示骨架屏。

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

### Requirement: 分类页异常状态与移动可用性
分类页 SHALL 在空分类、网络异常和小程序主流视口中保持可用。

#### Scenario: 一级分类无二级分类
- **WHEN** 当前一级分类没有可展示二级分类
- **THEN** 右侧 SHALL 保留当前一级分类标题
- **AND** 页面 SHALL 展示“该分类暂未配置二级分类”或等价空状态
- **AND** 页面 SHALL NOT 自动跳转其他一级分类。

#### Scenario: 二级分类不渲染图片
- **WHEN** 当前一级分类存在二级分类
- **THEN** 页面 SHALL NOT 渲染二级分类图片、图片占位或破图图标
- **AND** 分类名称和点击能力 SHALL 保持可用。

#### Scenario: 网络异常降级
- **WHEN** 分类树请求失败且没有可用缓存
- **THEN** 页面 SHALL 展示错误说明和重新加载入口
- **WHEN** 分类树请求失败但存在可用缓存
- **THEN** 页面 SHALL 继续展示缓存，并 MAY 轻提示网络异常。

#### Scenario: 分类下架后回退
- **WHEN** 当前选中一级分类在最新分类树中已不可见
- **THEN** 页面 SHALL 默认选中新的第一个可用一级分类
- **AND** 页面 SHALL NOT 保留不可见分类的空白状态。

#### Scenario: 移动视口与触控可用
- **WHEN** 团队在 375x812、390x844 和 320 到 430 pt 宽度范围验收分类页
- **THEN** 页面 SHALL 无横向滚动、内容重叠、底部 TabBar 遮挡或底部露白
- **AND** 一级分类按钮高度 SHALL 在 56 到 60px 范围
- **AND** 二级分类卡片可访问名称 SHALL 为 `{分类名称}`。

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

