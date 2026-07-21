## MODIFIED Requirements

### Requirement: 首页聚合数据
系统 SHALL 为小程序首页提供公开数据聚合能力，复用现有品牌、门店、SKU、规格、类目、Banner 和媒体数据源，不新增重复业务数据源。首页聚合数据中的 Banner SHALL 仅来自小程序首页轮播位置。

#### Scenario: 首页聚合接口返回公开数据
- **WHEN** 小程序请求首页聚合数据
- **THEN** 后端 SHALL 返回门店摘要、可展示 Banner、默认快捷入口、新品推荐、热销推荐和服务展示所需字段
- **AND** Banner SHALL 仅来自小程序首页轮播位置（`MINIAPP_HOME_CAROUSEL` 或等价首页轮播枚举）
- **AND** 响应 SHALL NOT 包含品牌列表页轮播位置 Banner
- **AND** 响应 SHALL NOT 暴露后台内部字段、库存管理、内部备注、未授权素材或敏感配置。

#### Scenario: 首页数据失败可降级
- **WHEN** Banner、推荐商品或图片模块加载失败
- **THEN** 小程序 SHALL 对失败模块做模块级降级
- **AND** 其他首页模块 SHALL 继续可见或可重试。

#### Scenario: 无商品数据时保留非商品模块
- **WHEN** 首页聚合接口可访问但推荐商品为空
- **THEN** 小程序 SHALL 隐藏推荐商品模块或展示品牌化空状态
- **AND** Banner、快捷入口和品牌服务区 SHALL 继续按可用数据展示或安全降级
- **AND** 页面 SHALL NOT 因商品为空而丢失全部动态模块。

### Requirement: Banner 与快捷入口
小程序首页 SHALL 复用已有后台 Banner 配置能力，并展示固定默认快捷业务入口。首页 Banner SHALL 只读取小程序首页轮播位置；品牌入口 SHALL 进入品牌列表页，品牌列表页轮播 SHALL 使用独立位置。

#### Scenario: 快捷入口点击策略
- **WHEN** 用户点击四个快捷入口之一
- **THEN** “选瓷砖” SHALL 进入分类 Tab、筛选页或已有分类能力
- **AND** “品牌馆”或“品牌” SHALL 进入品牌列表页
- **AND** “新品榜” SHALL 进入商品列表页并带入 `section=new`
- **AND** “热销榜” SHALL 进入商品列表页并带入 `section=hot`
- **AND** 新品榜和热销榜入口 SHALL NOT 使用 `/pages/search/index?section=...` 承接
- **AND** 任一目标不可达时 SHALL 安全降级且不得出现白屏或路由错误。

#### Scenario: 首页轮播与品牌列表页轮播隔离
- **WHEN** 小程序首页加载 Banner
- **THEN** 首页 SHALL 只展示小程序首页轮播位置中已上线且有效期内的 Banner
- **AND** 首页 SHALL NOT 展示品牌列表页轮播位置 Banner
- **WHEN** 品牌列表页无轮播数据
- **THEN** 首页轮播 SHALL NOT 被用作品牌列表页兜底。

#### Scenario: Banner 品牌详情跳转
- **WHEN** 后端公开 Banner 响应包含 `jump_type=brand` 和 `target_id`
- **THEN** 小程序首页和品牌列表页 SHALL 跳转到 `pages/brand-detail/index?brandId={target_id}`
- **AND** SHALL 保持商品详情跳转、搜索跳转、门店跳转和无跳转的既有行为。
