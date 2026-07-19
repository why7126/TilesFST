## MODIFIED Requirements

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

#### Scenario: 首页运行入口执行业务逻辑
- **WHEN** 微信开发者工具预览 `pages/index/index`
- **THEN** 实际运行脚本 SHALL 初始化首页状态并触发首页聚合数据加载
- **AND** 实际运行脚本 SHALL NOT 保持空模板 `Page({ data: {}, onLoad() {} })`
- **AND** 首页动态模块 SHALL 基于运行时数据或模块级降级策略展示。

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

#### Scenario: 无商品数据时保留非商品模块
- **WHEN** 首页聚合接口可访问但推荐商品为空
- **THEN** 小程序 SHALL 隐藏推荐商品模块或展示品牌化空状态
- **AND** Banner、快捷入口和品牌服务区 SHALL 继续按可用数据展示或安全降级
- **AND** 页面 SHALL NOT 因商品为空而丢失全部动态模块。

## ADDED Requirements

### Requirement: 小程序运行入口质量门禁
小程序页面实现 SHALL 保证微信开发者工具实际加载的运行脚本与业务源码一致，避免空模板 `.js` 覆盖已实现的 `.ts` 逻辑。

#### Scenario: 关键页面运行脚本不为空模板
- **WHEN** 团队运行小程序静态测试或等价校验
- **THEN** 首页、搜索页、商品详情页和门店信息页的运行脚本 SHALL NOT 保持微信开发者工具空模板
- **AND** 校验 SHALL 能发现 `.ts` 包含业务逻辑但 `.js` 仍为空模板的脱节状态。

#### Scenario: 运行事实源明确
- **WHEN** 小程序页面同时存在 `.ts` 与 `.js`
- **THEN** 项目 SHALL 明确 `.js` 同步策略或 TypeScript 编译链
- **AND** 微信开发者工具实际加载的脚本 SHALL 包含对应页面的关键业务数据、生命周期和交互方法。
