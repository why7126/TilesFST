## ADDED Requirements

### Requirement: 商品列表页微信分享
商品列表页 SHALL 支持分享给微信朋友和分享到微信朋友圈，并 SHALL 保留当前搜索、分类、品牌和榜单上下文。

#### Scenario: 商品列表分享给微信朋友
- **WHEN** 用户在商品列表页触发微信朋友分享
- **THEN** 小程序 SHALL 返回微信原生分享对象
- **AND** 分享标题 SHALL 反映当前搜索、分类、品牌、榜单或全部商品语义
- **AND** 分享路径 SHALL 指向商品列表页并保留可恢复当前列表的白名单 query 参数
- **AND** 白名单参数 SHOULD 包含 `categoryId`、`categoryLevel`、`categoryName`、`brandId`、`keyword`、`section` 和 `sourcePage` 中适用字段。

#### Scenario: 商品列表分享到朋友圈
- **WHEN** 用户在商品列表页触发分享到朋友圈
- **THEN** 小程序 SHALL 返回朋友圈分享配置
- **AND** 点击朋友圈入口后 SHALL 进入商品列表页
- **AND** 页面标题、筛选结果、空状态和错误态 SHALL 与分享参数语义一致
- **AND** 缺失可选参数时 SHALL 降级为可浏览列表或明确错误态，不得白屏。

#### Scenario: 商品列表分享参数编码
- **WHEN** 商品列表分享路径包含中文分类名、品牌名或搜索词
- **THEN** 小程序 SHALL 对 query 参数进行安全编码
- **AND** 被分享用户打开页面后 SHALL 正确解码并恢复列表语义
- **AND** 分享路径 SHALL NOT 包含 raw payload、Authorization header、Cookie、手机号、raw object key 或未授权素材路径。

#### Scenario: 商品列表分享埋点非阻断
- **WHEN** 商品列表页记录分享行为
- **THEN** 事件 SHOULD 包含页面路径、分享渠道、分类、品牌、关键词、榜单和结果上下文中的可用字段
- **AND** 埋点失败 SHALL NOT 阻断分享
- **AND** 分享行为 SHALL NOT 影响下拉刷新、加载更多、商品卡片点击或错误重试。
