## ADDED Requirements

### Requirement: 证书详情页品牌卡片点击事件上下文

系统 SHALL 使用已登记的 `brand_card_click` 记录证书详情页所属品牌入口点击。证书详情页 SHALL NOT 使用页面私有品牌点击事件名。事件参数 SHALL 仅携带品牌、来源、证书和 request id 等允许上下文，且埋点失败 SHALL NOT 阻断品牌入口跳转。

#### Scenario: 证书详情页上报品牌卡片点击

- **WHEN** 用户点击证书详情页可用品牌卡片
- **THEN** 小程序 SHALL 上报 `brand_card_click`
- **AND** 事件参数 SHALL 包含可用的 `brandId`、`brandName`、`sourcePage`、`sourceModule`、`certificateId`、`requestId` 和 client type
- **AND** `sourcePage` SHALL 标识证书详情页或等价来源
- **AND** 小程序 SHALL NOT 上报未登记的页面私有品牌点击事件名。

#### Scenario: 证书详情页品牌点击埋点安全边界

- **WHEN** 小程序提交证书详情页品牌卡片点击事件
- **THEN** 事件 SHALL NOT 包含手机号、地址、客户姓名、Authorization header、Cookie、raw payload、raw object key、内部备注或其它不必要个人敏感信息
- **AND** 埋点失败 SHALL NOT 阻断品牌卡片展示或品牌详情跳转。

