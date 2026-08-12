## 设计目标

本 Change 以轻量自建 RUM 为首期方案，优先建立可持续采集和可查询的真实性能数据闭环，而不是接入第三方 APM 或建设复杂 BI。设计目标包括：

- 端侧采集真实用户页面加载关键节点；
- 后端接收匿名、结构化、受控的性能事件；
- 支持基础聚合、慢页面定位和版本对比；
- 不采集敏感身份、原始 URL 参数、签名 URL、Header、Cookie 或完整 payload；
- RUM 上报失败不影响用户主流程；
- API、数据库、Orval、docs 和测试同步进入实现门禁。

## 影响分析

```yaml
impact:
  backend: true
  web: true
  miniapp: true
  admin: true
  database: true
  storage: false
  api: true
capabilities:
  new:
    - real-user-performance-monitoring
  modified:
    - product-usage-logging
    - web-client
    - api-governance
    - database
```

## 关键决策

### D1 采集策略

Web 端采用浏览器 Performance API 与业务自定义节点结合的策略：

- `navigation`、`load` 等浏览器节点作为技术基线；
- `first_content_ready`、`first_api_done` 等业务节点作为主指标；
- 店主展示端和管理端分别标记 `web_catalog`、`web_admin`。

小程序端采用 App/page 生命周期与关键接口包装策略：

- 记录页面进入、`onLoad`、`onShow`、`onReady`；
- 记录首个关键业务接口完成；
- 通过业务自定义节点标记首屏渲染就绪或页面可交互；
- 不依赖 Web 浏览器专属 API。

### D2 指标口径

首期主指标为“首屏可用耗时”，完整加载耗时作为辅助指标。原因是图片、视频、懒加载资源可能拖长完整 load，但用户感知更依赖首屏关键内容是否可看、可操作。

### D3 上报与隐私

性能事件使用受控字段模型，上报 payload 只包含端类型、页面 key、版本、网络类型、设备类别、指标名、耗时、采样率和事件时间。后端必须校验字段长度、枚举和数值范围，并拒绝或移除敏感字段。

公开端与小程序上报为匿名性能事件，不得借由客户端字段获得管理端权限。管理端聚合查询必须鉴权。

### D4 数据存储与聚合

首期采用关系型表存储性能事件，SQLite demo 与 MySQL 生产保持兼容。聚合查询优先按时间范围、端类型、页面、版本、网络和设备类别过滤，再计算样本量、平均值、最大值和分位指标。

如果当前数据库能力不适合直接计算精确 P95/P99，允许实现阶段采用可说明的近似分位或应用层受限聚合，但必须记录口径、样本限制和后续优化路径。

### D5 管理端入口

首期倾向提供管理端性能观测入口，页面结构参考 `issues/requirements/archive/REQ-0107-real-user-page-load-rum/prototype/web/context.md`：

- 标题：管理端导航名和页面 H1 统一为“性能观测”，副标题承载真实用户 RUM 说明；
- 筛选：时间范围、端类型、页面、版本、网络；每个筛选控件使用与其他管理页一致的显式 `field-label`。
- 摘要：样本量、P75/P95 首屏可用、慢页面数、上报失败率；
- 趋势：首屏可用 P75/P95；
- 排行：慢页面、慢指标；
- 明细：页面维度聚合表、版本号独立列、右侧冻结“操作”列、后端真实分页、样本不足状态；点击“查看样本”跳转到独立性能样本页，使用管理端列表样式展示聚合筛选上下文、最近安全样本明细和后端真实分页；样本页 `request_id` 复用日志审计页复制样式与复制行为；日志审计不承载 RUM 单次明细。
- 帮助：筛选模块不展示“数据边界”和“页面如何解读”两块信息；重置按钮复用既有管理端筛选 actions 容器与按钮尺寸。

Web RUM 上报的 `app_version` 必须复用管理端左上角产品版本徽标同源常量，避免页面列表、样本页与实际前端版本不一致；每个性能事件生成受控 `request_id`，用于样本页定位单次事件，不携带完整 URL、Header、Cookie 或签名 URL。

若实现阶段因容量拆分不包含页面，后端接口与数据结构仍需支撑后续管理端看板。

## 原型冲突处理

`prototype/web/` 存在，优先级按 HTML > context > acceptance > `rules/ui-design.md` > 正式规格处理。

- `performance-rum-dashboard.html` 是信息架构与视觉占位，不是像素级最终稿。
- `context.md` 明确 Design System semantic token、指标口径和样本量展示要求。
- `acceptance.md` 的 API、DB、Orval、小程序真实环境证据要求优先作为实现门禁。
- 若 prototype HTML 中存在裸 hex，仅作为离线原型占位；真实 Web 实现必须使用 semantic token 和现有组件。

## 风险与缓解

| 风险 | 缓解 |
|---|---|
| 上报量过大影响业务接口 | 默认采样、批量上报、节流、服务端限流和数据保留周期 |
| 采集字段误含敏感信息 | 服务端 Schema 白名单、禁止字段扫描、脱敏和测试 |
| 小程序真实体验难以自动化 | 发布前记录 DevTools/体验版 Network evidence，并标记人工来源 |
| 分位统计口径不一致 | 在接口响应、文档和管理端说明样本量、计算口径与样本不足状态 |
| 与现有日志/行为事件混淆 | 性能事件单独建模，保留与 request_id/client_type 的弱关联但不替代审计日志 |

## 验证策略

- 后端测试覆盖性能事件上报成功、非法 payload、敏感字段拒绝、批量上报、聚合查询和权限边界。
- 数据库测试覆盖 SQLite schema、MySQL schema/migration、索引和空数据聚合。
- Web 测试覆盖采集工具、采样降级、管理端入口空态/错误态/样本不足态。
- 小程序静态测试覆盖页面生命周期埋点、请求封装、上报失败不阻断主流程。
- API 变更后运行 OpenAPI/Orval 生成并检查 generated 文件只由工具产生。
