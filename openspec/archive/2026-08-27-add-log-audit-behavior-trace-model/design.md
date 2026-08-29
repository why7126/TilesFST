---
change_id: add-log-audit-behavior-trace-model
source_requirement: REQ-0124-log-audit-behavior-trace-model
sprint: sprint-026
created_at: 2026-08-25 22:47:46
updated_at: 2026-08-25 22:47:46
---

# 设计

## 设计目标

本 Change 将日志审计的数据采集模型统一为四层链路：

```text
行为事件 -> API 请求 -> 任务链路 -> 流程节点
```

界面触发入口使用 `behavior_trace_id` 串联一次用户行为引发的多个请求；直接 API 调用不伪造行为事件，继续从后端可信 `request_id` 进入请求与任务排障。底层仍使用 `task_trace_spans` 表达任务内部节点，管理端中文展示为“流程节点”。

## 链路模型

### 界面触发

```text
usage_events.behavior_trace_id
  -> request_logs.behavior_trace_id
      -> task_traces.parent_request_id
          -> task_trace_spans
```

- `behavior_trace_id` 表示一次用户行为链路，一次点击、页面访问或表单提交触发多个 API 请求时共享。
- `behavior_event_id` 表示 `usage_events` 中单条行为事件。
- `parent_behavior_event_id` 表示某条请求来源于哪条行为事件。
- `request_id` 仍由后端生成，是服务端可信单次 HTTP 请求 ID。

### 直接 API 调用

```text
request_logs.request_id
  -> task_traces.parent_request_id
      -> task_trace_spans
```

直接 API 调用、外部系统、脚本或后台调用允许 `behavior_trace_id` 与 `parent_behavior_event_id` 为空；如果触发任务，`task_traces.parent_request_id` 继续引用 `request_logs.request_id`。

## 字段与生成边界

| 字段 | 生成方 | 可信边界 | 用途 |
|---|---|---|---|
| `behavior_trace_id` | 前端行为采集上下文生成，后端校验格式并持久化 | 归因字段，不作为鉴权或审计身份来源 | 关联一次用户行为触发的多个请求 |
| `behavior_event_id` | 前端行为事件生成，后端校验格式并持久化 | 行为事件标识，不替代请求 ID | 标识 `usage_events` 单条事件 |
| `parent_behavior_event_id` | 后端从请求头或等价上下文读取并校验后写入 | 请求来源归因字段 | 让 `request_logs` 回指来源行为事件 |
| `request_id` | 后端请求中间件生成 | 服务端可信 | 标识单次 HTTP 请求 |
| `client_request_id` | 客户端或外部调用方生成 | 排障辅助，不可信 | 对齐客户端日志和服务端日志 |
| `task_trace_id` | 后端任务入口生成或绑定 | 服务端任务链路事实 | 串联任务摘要和流程节点 |

ID 格式应使用不含业务敏感信息、不可枚举、长度受控的字符串；非法、超长或格式不合规的客户端链路字段应被忽略、脱敏记录或返回文档化校验错误，但不得影响后端生成可信 `request_id`。

## 数据库与迁移

- `usage_events` 新增 `behavior_trace_id`、`behavior_event_id`，并为常用查询路径建立索引。
- `request_logs` 新增 `behavior_trace_id`、`parent_behavior_event_id`，并继续保留 `client_request_id` 与服务端可信 `request_id` 的语义差异。
- `task_traces` 可冗余记录 `behavior_trace_id`，方便从行为链路直接定位任务。
- `task_trace_spans` 可冗余记录 `behavior_trace_id` 和当前 `request_id`，方便节点反查。
- SQLite schema、SQLite migration、MySQL baseline、MySQL migration / drift 修复路径和数据库文档必须保持字段、可空性、索引和兼容策略一致。
- 历史日志不强制回填，新增字段允许为空；页面和查询必须兼容空行为链路。

## API 与前端接入

- 前端请求封装在界面行为触发请求中透传 `behavior_trace_id` 与 `behavior_event_id`，推荐通过受控请求头或等价文档化字段传递。
- usage event 接收 API 接受并校验 `behavior_trace_id` 与 `behavior_event_id`。
- 请求日志中间件在请求完成时写入行为来源字段，直接 API 调用为空。
- 日志审计查询 API 增加 `behavior_trace_id` 精确查询入口，并保持 `request_id`、`task_trace_id` 入口。
- 日志审计详情 API 返回可展示的链路摘要：行为事件、请求摘要、任务摘要和流程节点。
- API 变更必须同步 OpenAPI、Orval、API 文档、后端测试和前端类型引用。

## UI Contract

| 项 | 合同 |
|---|---|
| 事实源优先级 | `prototype/web/context.md` > `acceptance.md` > `rules/ui-design.md` > `openspec/specs/product-usage-logging` 与 `web-client` 既有日志审计规格。当前无 HTML/PNG 原型。 |
| 页面与入口 | 复用管理端 `/admin/logs` 日志审计页；仅 admin 可访问，employee/store_owner/anonymous 不得查看日志数据。 |
| 信息架构 | 保持既有 Admin Shell、指标卡、筛选区、日志列表、分页和详情抽屉；新增链路查询入口和链路详情分组，不建设独立 BI 大屏。 |
| 视觉 token | 使用 Design System semantic token 和既有管理端列表样式；不得新增裸 Hex；长链路 ID 使用固定宽度、截断、tooltip/title 或详情展开。 |
| 交互状态 | 筛选变化重置分页；复制链路 ID 使用 fixed toast；查询失败、空结果、历史日志无行为链路和直接 API 无行为来源必须有清晰状态。 |
| 图标与文案 | 底层 span 展示为“流程节点”；行为链路、请求链路、任务链路文案保持中文，链路 ID 保留英文代码标识。 |
| Mock/API 边界 | 本 Change 以真实 API 和真实数据库为目标；不得用 Mock 数据替代链路查询验收。前端开发可用 fixture 测试，但验收必须覆盖真实 API。 |
| 权限规则 | 日志审计查询、详情和链路复制均遵守管理端 admin 权限；链路字段不作为身份或权限来源。 |
| 一致性参照 | `docs/knowledge-base/best-practices/admin-list-page-consistency.md`，重点覆盖后端真实分页、统一筛选控件、fixed toast、长字段 nowrap/截断和敏感字段脱敏。 |

## 原型与验收冲突报告

- 当前只有 `prototype/web/context.md`，未提供 HTML 或 PNG，因此不需要 CSS Port 或像素级对照。
- `context.md` 明确要求复用既有日志审计页，不新建独立页面；该结论与 `acceptance.md` 和 `rules/ui-design.md` 一致。
- 后续实现若扩展筛选控件，必须命中 `admin-filter-dropdown` gate；若仅增加文本查询输入，应保持现有筛选区布局和分页 DOM。
- 若实现过程中发现既有日志审计页无法承载链路详情，应先补充 UI Skeleton 和截图证据，不得直接扩大为独立观测大屏。

## 安全与脱敏

- metadata、请求摘要、响应摘要、错误摘要和流程节点摘要必须采用字段白名单、长度截断和敏感字段过滤。
- 后端脱敏是安全边界；前端脱敏只能作为展示优化。
- 不得保存或展示 Authorization、Cookie、Token、密码、真实密钥、数据库 DSN、MinIO AccessKey/SecretKey、完整请求体、完整响应体、本机绝对路径、完整内部对象 key 或真实客户敏感数据。
- 链路 ID 只用于排障归因，不得作为权限、身份、租户隔离或审计操作者的可信来源。

## 验收方式

- 后端测试覆盖界面触发一行为多请求、直接 API 无行为链路、任务链路 `parent_request_id`、三类 ID 查询和敏感字段脱敏。
- 数据库测试覆盖 SQLite / MySQL 字段、索引、可空兼容、迁移幂等和旧日志读取。
- 前端测试覆盖请求封装透传、日志审计三类 ID 查询、详情链路展示、空态、分页结构和 fixed toast。
- OpenAPI / Orval 生成物与 API 文档必须同步；若某字段只内部采集不暴露，必须在实现记录中说明不涉及 Orval 的原因。
