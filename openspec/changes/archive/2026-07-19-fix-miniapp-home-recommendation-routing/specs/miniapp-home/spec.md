## MODIFIED Requirements

### Requirement: Banner 与快捷入口
小程序首页 SHALL 复用已有后台 Banner 配置能力，并展示固定默认快捷业务入口。

#### Scenario: 快捷入口点击策略
- **WHEN** 用户点击四个快捷入口之一
- **THEN** “选瓷砖” SHALL 进入分类 Tab、筛选页或已有分类能力
- **AND** “品牌馆” SHALL 安全降级到搜索、筛选或占位提示，直到完整品牌馆能力另行建设
- **AND** “新品榜” SHALL 进入商品列表页并带入 `section=new`
- **AND** “热销榜” SHALL 进入商品列表页并带入 `section=hot`
- **AND** 新品榜和热销榜入口 SHALL NOT 使用 `/pages/search/index?section=...` 承接
- **AND** 任一目标不可达时 SHALL 安全降级且不得出现白屏或路由错误。

### Requirement: 新品热销与全部产品承接
小程序首页 SHALL 在 Banner 与快捷入口后展示新品推荐、热销推荐和全部产品瀑布流，使用户可以连续浏览公开 SKU。

#### Scenario: 新品推荐查看更多
- **WHEN** 用户点击首页「新品推荐」模块的「查看更多」
- **THEN** 小程序 SHALL 进入商品列表页并带入 `section=new`
- **AND** 商品列表页 SHALL 展示新品榜或等价新品推荐商品列表标题
- **AND** 该入口 SHALL NOT 进入 `/pages/search/index?section=new`。

#### Scenario: 热销推荐查看更多
- **WHEN** 用户点击首页「热销推荐」模块的「查看更多」
- **THEN** 小程序 SHALL 进入商品列表页并带入 `section=hot`
- **AND** 商品列表页 SHALL 展示热销榜或等价热销推荐商品列表标题
- **AND** 该入口 SHALL NOT 进入 `/pages/search/index?section=hot`。
