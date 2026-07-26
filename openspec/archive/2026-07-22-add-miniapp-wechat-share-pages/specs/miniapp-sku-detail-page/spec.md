## ADDED Requirements

### Requirement: SKU 详情页微信分享
SKU 详情页 SHALL 支持分享给微信朋友和分享到微信朋友圈，并 SHALL 保留当前 SKU 参数、分享图兜底和分享直达异常态。

#### Scenario: SKU 详情分享给微信朋友
- **WHEN** 用户在 SKU 详情页触发微信朋友分享
- **THEN** 小程序 SHALL 返回微信原生分享对象
- **AND** 分享路径 SHALL 指向当前 SKU 详情页并携带有效 `skuId` 和 `source=share` 或等价来源参数
- **AND** 分享标题 SHALL 优先使用商品分享标题，未配置时 SHALL 使用 SKU 名称与品牌名称组合
- **AND** 分享图 SHALL 优先使用商品分享图或商品主图，缺失时 SHALL 使用安全兜底图。

#### Scenario: SKU 详情分享到朋友圈
- **WHEN** 用户在 SKU 详情页触发分享到朋友圈
- **THEN** 小程序 SHALL 返回朋友圈分享配置
- **AND** 朋友圈入口 SHALL 保留当前 SKU 的必要参数
- **AND** 被分享用户打开后 SHALL 进入对应 SKU 详情页
- **AND** SKU 不存在、下架、不可公开或参数无效时 SHALL 展示可理解错误或空状态而不是白屏。

#### Scenario: SKU 分享埋点与安全
- **WHEN** SKU 详情页记录分享行为
- **THEN** 事件 SHOULD 包含页面路径、分享渠道和 `skuId`
- **AND** 埋点失败 SHALL NOT 阻断分享
- **AND** 分享路径、分享图和埋点 SHALL NOT 暴露原始 object key、Authorization header、Cookie、手机号或未授权素材地址。
