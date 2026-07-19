## ADDED Requirements

### Requirement: 商品列表进入 SKU 详情
SKU 详情页 SHALL 支持从小程序商品列表页商品卡片进入，并保持公开字段、安全媒体 URL 和不可公开状态边界。

#### Scenario: 商品列表卡片进入详情页
- **WHEN** 用户在商品列表页点击商品卡片
- **THEN** 小程序 SHALL 携带 `skuId` 和可用来源参数进入 SKU 详情页
- **AND** SKU 详情页 SHALL 按既有公开数据契约加载详情。

#### Scenario: 商品列表来源参数
- **WHEN** SKU 详情页由商品列表页打开
- **THEN** 页面 SHALL 记录可用来源参数
- **AND** 来源参数 SHALL NOT 包含 Authorization header、Cookie、手机号、raw payload 或其他敏感信息。

#### Scenario: 不可公开 SKU
- **WHEN** 商品列表页进入的 SKU 不存在、已下架或不允许公开展示
- **THEN** SKU 详情页 SHALL 展示“商品暂不可查看”或等价空状态
- **AND** 页面 SHALL 提供返回商品列表或返回上一页入口。
