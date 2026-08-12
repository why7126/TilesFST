## ADDED Requirements

### Requirement: Web 真实用户性能采集与观测
Web 客户端 SHALL 为管理端和店主展示端提供真实用户页面加载性能采集，并 SHALL 支持管理端性能观测入口或后续看板所需的查询预留。

#### Scenario: Web 管理端采集 RUM 指标
- **WHEN** 管理端用户进入已接入的 `/admin/*` 页面
- **THEN** Web 客户端 SHALL 采集受控页面 key、端类型、版本、首屏可用、完整加载、关键接口或关键资源耗时
- **AND** 端类型 SHALL 标记为 `web_admin`
- **AND** 版本号 SHALL 与管理端左上角产品版本徽标同源
- **AND** 每个 RUM 事件 SHALL 生成受控 `request_id`
- **AND** 采集和上报失败 SHALL NOT 影响管理端路由守卫、权限校验、列表、表单、弹窗、上传或保存行为。

#### Scenario: 店主 Web 展示端采集 RUM 指标
- **WHEN** 店主 Web 展示端用户进入已接入的公开页面
- **THEN** Web 客户端 SHALL 采集受控页面 key、端类型、版本、首屏可用、完整加载、关键接口或关键资源耗时
- **AND** 端类型 SHALL 标记为 `web_catalog`
- **AND** 匿名访问 SHALL NOT 因性能上报获得管理端权限或内部性能查询能力。

#### Scenario: 管理端性能观测入口
- **WHEN** 管理端实现真实用户性能观测页面
- **THEN** 页面 SHALL 使用 Design System semantic token 和既有管理端组件
- **AND** 页面 SHALL 支持时间范围、端类型、页面、版本和网络筛选
- **AND** 页面 SHALL 展示样本量、分位耗时、慢页面排行、版本对比、空数据、加载失败、权限不足和样本不足状态
- **AND** 页面 SHALL 将页面 key 与版本号拆分为独立列，并使用右侧冻结“操作”列打开明细
- **AND** 页面 SHALL 使用后端真实分页展示聚合列表
- **AND** 页面 SHALL 支持从聚合行跳转独立性能样本页查看最近安全样本明细，样本字段 SHALL 使用“版本号”命名
- **AND** 性能样本页 SHALL 使用管理端列表样式展示聚合筛选上下文和样本列表
- **AND** 页面筛选项 SHALL 使用与其他管理页一致的显式 Label
- **AND** 页面标题 SHALL 与管理端导航保持“性能观测”一致
- **AND** 页面 SHALL NOT 展示敏感字段原值、完整 URL 查询参数、签名 URL、Authorization、Cookie 或 Token。

#### Scenario: Web RUM 测试覆盖
- **WHEN** Web 测试运行
- **THEN** 测试 SHALL 覆盖采集事件字段、采样或降级策略和上报失败不阻断主流程
- **AND** 若管理端性能观测页面纳入实现，测试或浏览器 smoke SHALL 覆盖主要筛选、摘要、慢页面排行、空态和权限态。
