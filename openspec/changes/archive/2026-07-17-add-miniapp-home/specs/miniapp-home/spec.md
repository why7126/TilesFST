## ADDED Requirements

### Requirement: 微信小程序首页首屏
系统 SHALL 提供原生微信小程序首页，用于面向终端客户展示菲尚特品牌、搜索入口、Banner、快捷找砖入口、新品推荐、热销推荐、品牌服务区和底部 TabBar。

#### Scenario: 首页首屏展示核心模块
- **WHEN** 用户打开微信小程序首页
- **THEN** 页面 SHALL 展示品牌 Logo、门店名称、搜索入口、Banner、快捷找砖入口和至少一个推荐模块
- **AND** 页面 SHALL NOT 展示新增、编辑、上下架、库存、订单或客户管理入口。

#### Scenario: 首页移动视口可用
- **WHEN** 团队在 375x812、390x844 和 320 到 430 pt 宽度范围验收首页
- **THEN** 页面 SHALL 无页面级横向滚动、明显内容截断、控件重叠或底部 TabBar 遮挡
- **AND** 所有主要点击区域 SHALL 不小于 44x44 pt。

### Requirement: 首页聚合数据
系统 SHALL 为小程序首页提供公开数据聚合能力，复用现有品牌、门店、SKU、规格、类目、Banner 和媒体数据源，不新增重复业务数据源。

#### Scenario: 首页聚合接口返回公开数据
- **WHEN** 小程序请求首页聚合数据
- **THEN** 后端 SHALL 返回门店摘要、可展示 Banner、默认快捷入口、新品推荐、热销推荐和服务展示所需字段
- **AND** 响应 SHALL NOT 暴露后台内部字段、库存管理、内部备注、未授权素材或敏感配置。

#### Scenario: 首页数据失败可降级
- **WHEN** Banner、推荐商品或图片模块加载失败
- **THEN** 小程序 SHALL 对失败模块做模块级降级
- **AND** 其他首页模块 SHALL 继续可见或可重试。

### Requirement: Banner 与快捷入口
小程序首页 SHALL 复用已有后台 Banner 配置能力，并展示固定默认快捷找砖入口。

#### Scenario: Banner 跳转安全降级
- **WHEN** 用户点击 Banner 且跳转目标属于商品详情、搜索结果或门店信息
- **THEN** 小程序 SHALL 跳转到对应页面
- **AND** 当配置目标不可达或指向本期未实现能力时，小程序 SHALL 安全降级且不得出现空白页或路由错误。

#### Scenario: 快捷入口进入筛选结果
- **WHEN** 用户点击按空间、按规格、按风格、按颜色或全部分类入口
- **THEN** 小程序 SHALL 进入搜索页或筛选结果页
- **AND** SHALL 带入对应预置筛选条件。

### Requirement: 搜索页与商品详情闭环
系统 SHALL 提供小程序搜索页和商品详情页，使首页搜索、快捷入口、推荐商品和有效 Banner 可进入商品详情。

#### Scenario: 搜索结果进入详情
- **WHEN** 用户通过商品名称、商品编号、品牌名称、规格或系列名称搜索商品
- **THEN** 小程序 SHALL 展示匹配的公开商品结果
- **AND** 用户点击结果 SHALL 进入对应商品详情页。

#### Scenario: 商品详情展示公开字段
- **WHEN** 用户打开商品详情页
- **THEN** 页面 SHALL 展示商品名称、商品编号、主图或纹理图、规格、品牌、类目、适用空间、风格标签和价格展示信息
- **AND** 页面 SHALL NOT 暴露后台管理字段、库存管理、内部备注或未授权素材。

### Requirement: 分享与咨询
小程序首页和商品详情 SHALL 支持微信原生分享与门店咨询入口，并记录对应行为事件。

#### Scenario: 分享商品
- **WHEN** 用户在商品详情页触发分享
- **THEN** 小程序 SHALL 使用微信原生分享或等价分享入口
- **AND** 分享路径 SHOULD 回到对应商品详情页
- **AND** 系统 SHALL 记录商品分享行为。

#### Scenario: 咨询门店
- **WHEN** 用户在首页服务区或商品详情页触发咨询
- **THEN** 小程序 SHALL 至少提供微信客服、拨打电话或复制微信号中的一种可用咨询方式
- **AND** 缺少配置的咨询方式 SHALL 隐藏或安全降级
- **AND** 系统 SHALL 记录咨询行为。

### Requirement: 热销推荐与行为统计
小程序首页 SHALL 展示热销推荐，并使用人工配置优先、行为统计辅助的排序策略。

#### Scenario: 热销推荐排序
- **WHEN** 首页请求热销推荐商品
- **THEN** 系统 SHALL 优先使用人工配置的热销排序
- **AND** 当人工配置不足时，系统 SHALL 使用详情访问、分享、咨询等行为统计或时间/排序字段降级展示
- **AND** 系统 SHALL NOT 依赖收藏量。

#### Scenario: 行为统计脱敏
- **WHEN** 系统记录详情访问、分享或咨询行为
- **THEN** 事件 SHALL 至少包含事件类型、商品 ID 或页面标识、客户端类型和时间
- **AND** SHALL NOT 存储用户敏感信息、聊天内容、Authorization header、Cookie 或原始手机号等不必要个人信息。

### Requirement: 原型与范围控制
小程序首页实现 SHALL 参考 `issues/requirements/archive/REQ-0041-miniapp-home/prototype/miniapp/` 下的 HTML、PNG 和 context，但以本 Change 的 acceptance 范围控制为准。

#### Scenario: 收藏能力不进入本期
- **WHEN** 实现小程序首页或商品详情
- **THEN** 系统 SHALL NOT 提供可用收藏按钮、收藏 Tab、收藏状态、收藏列表或收藏统计
- **AND** 原型中的收藏心形 SHALL 被移除、隐藏或置为非交互展示。

#### Scenario: 不做项不被误纳入
- **WHEN** 团队验收本 Change
- **THEN** 验收 SHALL 确认预约表单、到店询价规则、快捷入口后台配置、服务入口后台配置、复杂用户画像和收藏驱动热销算法未被实现。
