## MODIFIED Requirements

### Requirement: 产品使用行为事件采集
系统 SHALL 按人工定义的事件字典采集产品使用行为事件。事件字典 SHALL 支持 Web 管理端既有事件，并 SHALL 支持微信小程序首页、首页样式信息架构优化、分类页、商品列表页、商品详情、搜索、收藏列表、品牌详情页、商品卡片组件和品牌卡片组件的详情访问、分享、咨询、快捷入口、瀑布流、搜索交互、收藏交互、品牌入口、卡片曝光、卡片点击和安全降级事件，用于小程序热销推荐统计、分类入口效果分析、搜索体验分析、收藏行为分析、品牌入口效果分析和后续产品优先级判断。搜索体验相关事件 SHALL 覆盖小程序与 Web 管理端的搜索入口点击、搜索输入停顿、搜索提交、联想曝光、联想点击、结果曝光、结果点击、无结果、列表筛选和重置。

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

#### Scenario: 搜索体验事件
- **WHEN** 微信小程序或 Web 管理端上报搜索入口、搜索提交、联想、结果曝光、无结果、列表筛选或重置事件
- **THEN** 系统 SHALL 接受已登记或等价预留的稳定搜索事件名
- **AND** 事件属性 SHALL 包含 `sourcePage`、`scope`、`keywordDigest` 或等价关键词脱敏摘要、`resultCount`、`selectedTab`、筛选条件摘要、`requestId`、client type 和必要页面上下文中的可用字段
- **AND** 事件 SHALL NOT 包含未脱敏关键词原文、Authorization、Cookie、Token、密码、完整请求体、完整响应体、raw object key、密钥、`.env` 内容或本机绝对路径
- **AND** 埋点失败 SHALL NOT 阻断搜索、筛选、跳转、联想或结果点击。

### Requirement: API 请求日志采集
系统 SHALL 为后端业务 API 请求采集脱敏请求日志。搜索和列表筛选请求 SHALL 保存安全查询摘要、结果数量、分页、耗时、client type、`behavior_trace_id`、`parent_behavior_event_id`、`client_request_id` 和服务端 `request_id` 中的可用字段，用于关联搜索行为与请求结果。

#### Scenario: 生成或透传 request_id
- **WHEN** 业务 API 请求进入后端
- **THEN** 系统 SHALL 生成服务端可信 `request_id`
- **AND** 客户端传入的 `client_request_id` SHALL 仅作为辅助字段保存，不得覆盖服务端 `request_id`。

#### Scenario: 搜索请求日志摘要
- **WHEN** 后端处理小程序搜索、列表内搜索或管理端列表搜索请求
- **THEN** request log SHALL 保存路由、状态码、耗时、分页、结果数量、搜索范围和脱敏查询摘要
- **AND** 若请求来自界面行为，request log SHALL 保存 `behavior_trace_id` 和 `parent_behavior_event_id` 或等价字段
- **AND** request log SHALL NOT 保存完整关键词原文、完整 query string、完整请求体、完整响应体、Authorization、Cookie、Token、密码、密钥、`.env` 内容、本机绝对路径或未授权对象存储地址。
