# favorite-list-page Specification

## Purpose
TBD - created by archiving change add-favorite-list-page. Update Purpose after archive.
## Requirements
### Requirement: 用户侧收藏列表页
系统 SHALL 提供用户侧收藏列表页，用于集中展示当前用户已收藏的对象，并支持用户从收藏列表回到对应详情页继续查看。

#### Scenario: 用户进入收藏列表
- **WHEN** 用户从产品确认的入口进入收藏列表页
- **THEN** 系统 SHALL 展示收藏列表页标题和收藏上下文
- **AND** 系统 SHALL 根据当前登录态或访客态加载对应收藏数据
- **AND** 未登录状态 SHALL NOT 被误展示为空收藏状态。

#### Scenario: 收藏列表展示收藏对象
- **WHEN** 当前用户存在收藏对象
- **THEN** 收藏列表 SHALL 展示每个收藏对象的主图或占位图、名称、对象类型和关键辅助信息
- **AND** 首期若仅支持 SKU / 商品收藏，列表项 SHALL 按 SKU / 商品语义展示
- **AND** 首期若支持多对象收藏，列表项 SHALL 展示对象类型标签。

#### Scenario: 收藏对象进入详情
- **WHEN** 用户点击收藏列表项的主要区域
- **THEN** 系统 SHALL 携带完整跳转参数进入对应详情页或列表页
- **AND** 对象不可访问时 SHALL 展示可恢复提示
- **AND** 页面 SHALL NOT 白屏、路由报错或展示内部错误。

### Requirement: 收藏列表取消收藏
系统 SHALL 允许用户在收藏列表中取消收藏或移除收藏项，并在操作结果返回后保持列表状态可理解、可恢复。

#### Scenario: 取消收藏成功
- **WHEN** 用户在收藏列表中取消某个收藏项
- **THEN** 系统 SHALL 从当前列表移除该收藏项或展示明确的已取消状态
- **AND** 系统 SHALL 更新收藏数量或等价上下文
- **AND** 系统 SHALL 给出轻量成功反馈。

#### Scenario: 取消收藏失败
- **WHEN** 用户取消收藏请求失败
- **THEN** 系统 SHALL 保留原收藏项
- **AND** 系统 SHALL 提示用户重试
- **AND** 系统 SHALL NOT 将本地 UI 误更新为已取消。

### Requirement: 收藏列表状态治理
收藏列表页 SHALL 区分加载、空收藏、未登录、网络异常、对象失效和加载更多失败状态，避免用户误判当前状态。

#### Scenario: 无收藏内容
- **WHEN** 当前用户没有收藏内容
- **THEN** 页面 SHALL 展示无收藏空状态
- **AND** 页面 SHALL 提供去首页、分类或搜索的行动入口
- **AND** 文案 SHALL 引导用户先收藏感兴趣的产品或对象。

#### Scenario: 未登录状态
- **WHEN** 收藏能力需要登录且当前用户未登录
- **THEN** 页面 SHALL 展示登录引导或受控访客提示
- **AND** 页面 SHALL NOT 展示无收藏空状态代替未登录状态。

#### Scenario: 网络异常
- **WHEN** 收藏列表首屏加载失败
- **THEN** 页面 SHALL 展示错误状态和重试入口
- **AND** 页面 SHALL NOT 长期停留在无反馈加载状态。

#### Scenario: 加载更多失败
- **WHEN** 收藏列表增量加载失败
- **THEN** 页面 SHALL 保留已加载收藏项
- **AND** 页面 SHALL 提供重试入口
- **AND** 页面 SHALL NOT 清空当前列表。

#### Scenario: 收藏对象失效
- **WHEN** 收藏对象已下架、删除或不可访问
- **THEN** 页面 SHALL 使用灰态、隐藏或明确提示策略稳定降级
- **AND** 页面 SHALL NOT 因单个失效对象导致整页不可用。

### Requirement: 收藏状态一致性
系统 SHALL 保证收藏列表与对象详情页的收藏状态保持一致，避免用户看到冲突的收藏结果。

#### Scenario: 详情页更新后进入收藏列表
- **WHEN** 用户在详情页新增或取消收藏后进入收藏列表
- **THEN** 收藏列表 SHALL 反映最新收藏状态
- **AND** 页面 SHALL NOT 展示长期过期的收藏结果。

#### Scenario: 收藏列表取消后返回详情
- **WHEN** 用户在收藏列表取消收藏后返回对应详情页
- **THEN** 详情页 SHALL 同步最新收藏状态或触发刷新
- **AND** 详情页 SHALL NOT 继续展示已收藏状态。

### Requirement: 收藏列表视觉与导航验收
收藏列表页 SHALL 延续用户侧深色高端展示体系，并在触控端保持可读、可点、无遮挡。

#### Scenario: 视觉结构
- **WHEN** 用户查看收藏列表页
- **THEN** 页面 SHALL 使用与现有用户侧页面一致的深色背景、卡片层、主文字、辅助文字和品牌金语义
- **AND** 列表项主图区域 SHALL 使用稳定比例
- **AND** 取消收藏操作 SHALL 清晰可见但不得抢占对象主要信息。

#### Scenario: 小程序导航验收
- **WHEN** 收藏列表页在微信小程序实现
- **THEN** 页面 SHALL 按 `docs/knowledge-base/best-practices/miniapp-custom-navigation.md` 验收状态栏、胶囊 reserve、返回兜底和页面 offset
- **AND** 首屏、加载态、空状态、错误态和网络失败提示 SHALL NOT 被顶部导航遮挡。

#### Scenario: 触控与视口
- **WHEN** 团队在移动端或小程序视口验收收藏列表
- **THEN** 主要点击目标 SHALL 不小于 44x44px 或平台等效尺寸
- **AND** 页面 SHALL 无横向滚动、内容重叠、关键文字溢出或底部安全区遮挡。

### Requirement: 收藏列表埋点与隐私
系统 SHOULD 记录收藏列表核心行为埋点，并 SHALL 避免记录与收藏浏览无关的个人敏感信息。

#### Scenario: 收藏列表行为埋点
- **WHEN** 用户浏览或操作收藏列表
- **THEN** 系统 SHOULD 记录收藏列表浏览、收藏项点击、取消收藏、空状态行动点击和加载失败事件
- **AND** 埋点参数 SHOULD 包含 terminal、objectType、objectId、index、sourcePage、hasLogin、resultCount 和 requestId。

#### Scenario: 埋点隐私边界
- **WHEN** 系统记录收藏列表相关日志或埋点
- **THEN** 日志和埋点 SHALL NOT 记录手机号、地址、客户姓名、Authorization header、Cookie、密钥或 `.env` 内容。

