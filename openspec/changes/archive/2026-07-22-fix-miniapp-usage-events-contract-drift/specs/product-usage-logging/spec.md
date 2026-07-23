## MODIFIED Requirements

### Requirement: 产品使用行为事件采集
系统 SHALL 按人工定义的事件字典采集产品使用行为事件。事件字典 SHALL 支持 Web 管理端既有事件，并 SHALL 支持微信小程序首页、首页样式信息架构优化、分类页、商品列表页、商品详情、搜索、收藏列表、品牌详情页、商品卡片组件和品牌卡片组件的详情访问、分享、咨询、快捷入口、瀑布流、搜索交互、收藏交互、品牌入口、卡片曝光、卡片点击和安全降级事件，用于小程序热销推荐统计、分类入口效果分析、搜索体验分析、收藏行为分析、品牌入口效果分析和后续产品优先级判断。

#### Scenario: 接受已登记事件
- **WHEN** 客户端提交的 usage event 存在于事件字典且包含全部必填属性
- **THEN** 系统 SHALL 校验该事件
- **AND** 持久化事件，同时写入服务端推导的用户、角色、client type、request id、timestamp、user agent 摘要和 IP 摘要。

#### Scenario: 拒绝未知事件
- **WHEN** 客户端提交的 usage event 未在事件字典中定义
- **THEN** 系统 SHALL 使用已文档化的校验错误拒绝该事件
- **AND** 拒绝埋点 SHALL NOT 中断用户主业务流程。

#### Scenario: 阻断禁止属性
- **WHEN** usage event 包含 token、password、authorization、cookie、raw payload 或 raw filename 等禁止属性
- **THEN** 系统 SHALL 按服务端校验策略在持久化前拒绝或移除这些属性
- **AND** SHALL NOT 将前端脱敏作为安全边界。

#### Scenario: 小程序收藏列表行为事件
- **WHEN** 微信小程序用户浏览收藏页、点击收藏项、取消收藏、点击空状态行动入口或收藏页加载失败
- **THEN** 系统 SHALL 接受已登记或等价预留的 `favorite_list_page_view`、`favorite_list_item_click`、`favorite_list_remove`、`favorite_list_empty_action_click` 和 `favorite_list_load_failed` 事件
- **AND** 事件 SHALL 仅携带 terminal、objectType、objectId、index、sourcePage、hasLogin、resultCount、requestId、client type 和必要页面上下文
- **AND** 事件 SHALL NOT 包含手机号、地址、客户姓名、Authorization header、Cookie、raw payload、raw object key、密钥、`.env` 内容或其它不必要个人敏感信息
- **AND** 埋点失败 SHALL NOT 阻断收藏页浏览、跳转或取消收藏主流程。

#### Scenario: 小程序品牌详情页行为事件
- **WHEN** 微信小程序用户浏览品牌详情页、切换 Tab、加载品牌商品、加载更多品牌商品、加载品牌证书、点击证书或发生对应加载失败
- **THEN** 系统 SHALL 接受已登记或等价预留的 `brand_detail_view`、`brand_detail_tab_click`、`brand_products_load`、`brand_products_load_more`、`brand_products_load_failed`、`brand_certificates_load`、`brand_certificates_load_failed` 和 `brand_certificate_click` 事件
- **AND** 事件 SHALL 仅携带 sourcePage、sourceModule、brandId、brandName、tab、page、pageSize、resultCount、index、requestId、client type 和必要页面上下文
- **AND** 事件 SHALL NOT 包含手机号、地址、客户姓名、Authorization header、Cookie、raw payload、raw object key、内部备注或其它不必要个人敏感信息
- **AND** 埋点失败 SHALL NOT 阻断品牌页加载、Tab 切换、商品跳转、证书预览或详情跳转。

#### Scenario: 小程序商品卡片组件行为事件
- **WHEN** 微信小程序商品卡片发生曝光、可用点击、不可用点击或图片加载失败
- **THEN** 系统 SHALL 接受已登记或等价预留的 `product_card_exposure`、`product_card_click`、`product_card_unavailable_click` 和 `product_card_image_failed` 事件
- **AND** 事件 SHALL 仅携带 skuId、skuCode、sourcePage、sourceModule、listContext、index、categoryId、brandId、keyword、requestId、client type 和必要上下文
- **AND** 事件 SHALL NOT 包含手机号、Authorization header、Cookie、raw payload、raw object key、内部备注或其它不必要个人敏感信息
- **AND** 埋点失败 SHALL NOT 阻断商品卡片展示或详情跳转。

#### Scenario: 小程序品牌卡片组件行为事件
- **WHEN** 微信小程序品牌卡片发生可用点击、不可用点击或图片加载失败
- **THEN** 系统 SHALL 接受已登记或等价预留的 `brand_card_click`、`brand_card_unavailable_click` 和 `brand_card_image_failed` 事件
- **AND** 事件 SHALL 仅携带 brandId、brandName、sourcePage、sourceModule、skuId、listContext、index、requestId、unavailableReason、client type 和必要上下文
- **AND** 事件 SHALL NOT 包含手机号、Authorization header、Cookie、raw payload、raw object key、内部备注或其它不必要个人敏感信息
- **AND** 埋点失败 SHALL NOT 阻断品牌卡片展示、品牌详情跳转或 fallback 跳转。

#### Scenario: 小程序事件字典防漂移
- **WHEN** 小程序新增或修改 `track()` 事件
- **THEN** 系统 SHALL 通过测试、静态校验或等价机制发现小程序事件名未在后端事件字典中登记的情况
- **AND** 对动态事件名调用点 SHALL 维护代表性样例并纳入测试
- **AND** 测试 SHALL 同时覆盖未知事件仍被拒绝和禁止字段仍被拒绝。
