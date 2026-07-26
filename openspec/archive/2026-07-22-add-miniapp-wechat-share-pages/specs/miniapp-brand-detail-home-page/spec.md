## ADDED Requirements

### Requirement: 品牌详情页微信分享
品牌详情页 SHALL 支持分享给微信朋友和分享到微信朋友圈，并 SHALL 保留当前品牌参数、标题兜底和分享直达异常态。

#### Scenario: 品牌详情分享给微信朋友
- **WHEN** 用户在品牌详情页触发微信朋友分享
- **THEN** 小程序 SHALL 返回微信原生分享对象
- **AND** 分享路径 SHALL 指向当前品牌详情页并携带有效 `brandId` 和 `source=share` 或等价来源参数
- **AND** 分享标题 SHALL 优先使用品牌名称，品牌数据未加载完成时 SHALL 使用稳定兜底标题
- **AND** 用户点击分享卡片后 SHALL 进入对应品牌详情页。

#### Scenario: 品牌详情分享到朋友圈
- **WHEN** 用户在品牌详情页触发分享到朋友圈
- **THEN** 小程序 SHALL 返回朋友圈分享配置
- **AND** 朋友圈入口 SHALL 保留当前 `brandId`
- **AND** 被分享用户打开后 SHALL 进入对应品牌详情页
- **AND** 品牌不存在、不可公开或参数无效时 SHALL 展示可返回或可重试状态而不是白屏。

#### Scenario: 品牌分享埋点与安全
- **WHEN** 品牌详情页记录分享行为
- **THEN** 事件 SHOULD 包含页面路径、分享渠道和 `brandId`
- **AND** 埋点失败 SHALL NOT 阻断分享
- **AND** 分享路径和埋点 SHALL NOT 包含 Authorization header、Cookie、真实客户隐私、内部字段或本机绝对路径。
