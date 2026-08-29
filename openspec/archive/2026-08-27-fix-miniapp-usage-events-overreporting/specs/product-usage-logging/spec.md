## MODIFIED Requirements

### Requirement: 产品使用行为事件采集

系统 SHALL 按人工定义的事件字典采集产品使用行为事件。事件字典 SHALL 支持 Web 管理端既有事件，并 SHALL 支持微信小程序首页、首页样式信息架构优化、分类页、商品列表页、商品详情、搜索、收藏列表、品牌详情页、商品卡片组件和品牌卡片组件的详情访问、分享、咨询、快捷入口、瀑布流、搜索交互、收藏交互、品牌入口、卡片曝光、卡片点击和安全降级事件，用于小程序热销推荐统计、分类入口效果分析、搜索体验分析、收藏行为分析、品牌入口效果分析和后续产品优先级判断。微信小程序端 SHALL 对高频曝光类事件采用去重、队列批量、节流或等价压力控制策略，避免首屏渲染、组件属性重复更新、搜索输入连续变化或搜索结果重复渲染造成 usage-events 请求数量线性放大。

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

#### Scenario: 小程序商品列表曝光口径收敛
- **WHEN** 微信小程序商品列表页首屏、分页、刷新或筛选后展示 SKU 列表
- **THEN** 小程序 SHALL 明确 `product_list_item_exposure` 与 `product_card_exposure` 的层级或互斥关系
- **AND** 同一 SKU、同一页面、同一来源模块、同一列表上下文和同一曝光窗口 SHALL NOT 被无边界重复计入两套曝光口径
- **AND** 若保留页面级列表曝光，事件 SHALL 表达页面级或列表级聚合语义，不得与商品卡 SKU 级曝光重复解释为两次真实曝光。

#### Scenario: 小程序搜索输入频控
- **WHEN** 微信小程序用户在搜索页连续输入关键词且尚未提交搜索
- **THEN** `search_input` SHALL 通过防抖、合并、采样或等价策略控制上报频率
- **AND** usage-events 请求数量 SHALL NOT 与字符变化次数一比一增长
- **AND** 清空、取消、提交搜索等关键行为 MAY 按独立事件或受控 payload 正常记录
- **AND** 埋点失败 SHALL NOT 阻断输入、建议加载、搜索提交或结果展示。

#### Scenario: 小程序搜索结果与商品卡曝光边界
- **WHEN** 微信小程序搜索结果展示 SKU 并同时存在 `search_result_exposure` 与 `product_card_exposure`
- **THEN** `search_result_exposure` SHALL 表达结果集合、模块或状态语义
- **AND** `product_card_exposure` SHALL 表达 SKU 卡片语义
- **AND** 同一关键词、同一 `requestId`、同一结果模块和同一 SKU 的重复渲染 SHALL NOT 重复上报商品卡曝光
- **AND** 切换关键词、重新提交搜索、筛选变化、分页或列表上下文变化时 SHALL 按明确规则重置或延续去重窗口。

#### Scenario: 小程序曝光去重键覆盖关键上下文
- **WHEN** 商品列表页、搜索结果页或商品卡片组件产生曝光类 usage event
- **THEN** 小程序 SHALL 使用页面、来源模块、列表上下文、SKU、搜索关键词或列表请求上下文、`requestId` 等必要维度构成去重键或等价判断
- **AND** 同一列表实例内重复渲染、属性 observer 重复触发或相同数据重复 setData SHALL NOT 重复上报
- **AND** 同一 SKU 出现在不同模块、不同列表上下文、不同关键词或不同 `requestId` 时 MAY 按业务语义分别记录。

#### Scenario: 小程序商品卡片组件行为事件
- **WHEN** 微信小程序商品卡片发生曝光、可用点击、不可用点击或图片加载失败
- **THEN** 系统 SHALL 接受已登记或等价预留的 `product_card_exposure`、`product_card_click`、`product_card_unavailable_click` 和 `product_card_image_failed` 事件
- **AND** 事件 SHALL 仅携带 skuId、skuCode、sourcePage、sourceModule、listContext、index、categoryId、brandId、keyword、requestId、client type 和必要上下文
- **AND** 事件 SHALL NOT 包含手机号、Authorization header、Cookie、raw payload、raw object key、内部备注或其它不必要个人敏感信息
- **AND** 埋点失败 SHALL NOT 阻断商品卡片展示或详情跳转。

#### Scenario: 小程序事件字典防漂移
- **WHEN** 小程序新增或修改 `track()` 事件
- **THEN** 系统 SHALL 通过测试、静态校验或等价机制发现小程序事件名未在后端事件字典中登记的情况
- **AND** 对动态事件名调用点 SHALL 维护代表性样例并纳入测试
- **AND** 测试 SHALL 同时覆盖未知事件仍被拒绝和禁止字段仍被拒绝。
