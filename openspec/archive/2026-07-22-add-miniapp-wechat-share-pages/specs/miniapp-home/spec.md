## ADDED Requirements

### Requirement: 首页微信分享
小程序首页 SHALL 支持分享给微信朋友和分享到微信朋友圈，并 SHALL 保持首页品牌语义、来源标识和埋点非阻断规则。

#### Scenario: 首页分享给微信朋友
- **WHEN** 用户在首页触发微信朋友分享
- **THEN** 小程序 SHALL 返回微信原生分享对象
- **AND** 分享标题 SHALL 优先使用门店或品牌名称，数据未加载时 SHALL 使用稳定兜底标题
- **AND** 分享路径 SHALL 指向首页并携带分享来源标识
- **AND** 分享 SHALL NOT 破坏首页加载、添加到我的小程序引导、原生胶囊避让或首页滚动状态。

#### Scenario: 首页分享到朋友圈
- **WHEN** 用户在首页触发分享到朋友圈
- **THEN** 小程序 SHALL 返回朋友圈分享配置
- **AND** 朋友圈标题 SHALL 与首页品牌语义一致
- **AND** 用户点击朋友圈入口后 SHALL 进入首页
- **AND** 页面 SHALL NOT 白屏、路由报错或暴露内部错误。

#### Scenario: 首页分享埋点非阻断
- **WHEN** 首页分享触发行为埋点
- **THEN** 事件 SHOULD 包含页面路径、分享渠道和来源标识
- **AND** 埋点失败 SHALL NOT 阻断微信分享对象返回
- **AND** 事件 SHALL NOT 包含 Authorization header、Cookie、真实客户隐私或本机绝对路径。
