## MODIFIED Requirements

### Requirement: 微信小程序商品列表页入口
系统 SHALL 提供微信小程序商品列表页，用于承接分类、搜索、品牌和首页推荐等入口的公开 SKU 浏览。

#### Scenario: 品牌和推荐入口进入商品列表
- **WHEN** 用户从品牌相关页面、首页推荐、新品榜或热销榜进入商品列表
- **THEN** 页面 SHALL 使用 `brandId`、`source`、`section` 或等价上下文加载公开 SKU
- **AND** 当 `section=new` 时，页面 SHALL 请求新品公开 SKU 并展示「新品榜」或等价标题
- **AND** 当 `section=hot` 时，页面 SHALL 请求热销公开 SKU 并展示「热销榜」或等价标题
- **AND** 目标入口不可用时 SHALL 安全降级到可返回提示或已有可用页面。
