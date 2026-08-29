## 背景

REQ-0124 已在本项目中落地日志审计行为链路模型，但该模型目前仍停留在项目内实现经验，尚未沉淀为可复用的跨产品数据采集与链路观测规范。后续小程序、店主端、App、Web 管理端和后端 API 如果缺少统一口径，会重复讨论行为事件、请求日志、Task Trace、保留周期和脱敏边界。

## 变更内容

- 新增“通用产品数据采集与链路观测规范”能力，定义跨端行为事件、API 请求日志、任务链路和流程节点的统一模型。
- 明确两类入口：界面触发入口通过 `behavior_trace_id` 串联行为和请求；直接 API 调用不伪造行为事件，通过 `request_id` 进入任务链路。
- 明确所有业务 API 请求必须记录 `request_logs`，并列出健康检查、静态资源、OpenAPI 文档资源、预检 OPTIONS、内部探活等可排除项。
- 明确 Task Trace 分级覆盖策略、默认数据保留周期、禁止采集字段、后端脱敏安全边界和新产品接入 checklist。
- 不直接改造所有历史产品，不接入外部 APM / OpenTelemetry，不建设第三方埋点平台、实时告警、BI 大屏、复杂用户画像或历史数据强制回填。

## 能力范围

### 新增能力

- `product-data-collection-observability-standard`: 定义通用产品数据采集、请求日志、Task Trace、保留周期、脱敏边界和后续引用门禁。

### 修改能力

- 无。本 Change 新增规范能力；既有 `product-usage-logging` 和 `api-governance` 作为参考能力，不在本 Change 中修改其既有需求语义。

## 影响

- 文档：新增长期标准文档，更新文档索引和相关 standards 引用。
- OpenSpec：新增能力 spec，后续 REQ、BUG、OpenSpec Change 和 Sprint 可引用该规范。
- API / DB / Orval：本 Change 本身不新增接口或表结构；规范要求后续具体产品接入时按变更影响同步 API、数据库、OpenAPI、Orval 和测试。
- Web / 小程序 / App：本 Change 不直接修改端侧代码；规范要求后续具体端接入行为事件 helper / SDK 和请求头透传时遵守统一模型。
- 安全：新增禁止采集和禁止展示字段清单，强调后端脱敏是安全边界。
