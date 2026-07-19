## MODIFIED Requirements

### Requirement: 产品使用行为事件采集
系统 SHALL 按人工定义的事件字典采集产品使用行为事件。事件字典 SHALL 支持 Web 管理端既有事件，并 SHALL 支持微信小程序首页、首页样式信息架构优化和商品详情的详情访问、分享、咨询、快捷入口、瀑布流和安全降级事件，用于小程序热销推荐统计和后续产品优先级判断。

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

#### Scenario: 强制执行 MVP 事件字典
- **WHEN** 实现处理 MVP 事件
- **THEN** 系统 SHALL 至少支持 page_view、search_submit、filter_change、detail_view、copy_request_id、entity_create、entity_update、entity_delete、status_change、media_upload、login_success、login_failed 和 api_error。

#### Scenario: Web 管理端上报行为事件
- **WHEN** 已认证 admin 或 employee 打开任一已登记 Web 管理端页面
- **THEN** Web 客户端 SHALL 通过共享 tracking client 上报 `page_view` usage event，并携带 module、page path、route pattern、page title、entity type 和 entity id。
- **WHEN** 已认证 admin 修改日志审计筛选、执行查询、复制 request id 或打开详情抽屉
- **THEN** Web 客户端 SHALL 通过共享 tracking client 上报对应交互 usage event
- **AND** 埋点失败 SHALL NOT 阻断可见用户流程。

#### Scenario: 小程序首页与商品详情行为事件
- **WHEN** 微信小程序用户浏览商品详情、分享首页、分享商品、点击首页咨询或点击商品咨询
- **THEN** 系统 SHALL 接受已登记的 `product_detail_view`、`home_share`、`product_share`、`home_contact_click`、`product_contact_click` 事件
- **AND** 事件 SHALL 携带必要的商品 ID、页面标识、client type 和时间上下文
- **AND** 事件 SHALL NOT 包含聊天内容、Authorization header、Cookie、原始手机号或其它不必要个人敏感信息
- **AND** 埋点失败 SHALL NOT 阻断小程序浏览、分享或咨询主流程。

#### Scenario: 小程序首页样式与信息架构行为事件
- **WHEN** 微信小程序用户点击首页搜索、快捷入口、新品商品、热销商品、全部产品商品、收藏视觉图标或证书 Tab
- **THEN** 系统 SHALL 接受已登记或等价预留的 `miniapp_home_search_click`、`miniapp_home_quick_entry_click`、`miniapp_home_new_product_click`、`miniapp_home_hot_product_click`、`miniapp_home_waterfall_product_click`、`miniapp_home_favorite_visual_click` 和 `miniapp_certificate_tab_click` 事件
- **AND** 事件 SHALL 仅携带必要的入口标识、商品 ID、页面标识、client type 和时间上下文
- **AND** 事件 SHALL NOT 承诺或写入收藏持久化事实。

#### Scenario: 小程序瀑布流加载行为事件
- **WHEN** 全部产品瀑布流发生首屏加载、下一页加载、加载失败或无更多状态
- **THEN** 系统 SHALL 接受已登记或等价预留的 `miniapp_home_waterfall_load`、`miniapp_home_waterfall_load_failed` 和 `miniapp_home_waterfall_end_reached` 事件
- **AND** 埋点失败 SHALL NOT 阻断瀑布流展示、追加、重试或无更多提示。
