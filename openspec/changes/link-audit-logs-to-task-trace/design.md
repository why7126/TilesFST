## Context

REQ-0075 来自已评审需求 `issues/requirements/review/REQ-0075-audit-log-task-trace-linking/`。平台已经有 `product-usage-logging` 能力、日志审计页、Task Trace 模型，以及已归档的 `add-task-trace-audit-log-view` 变更；当前缺口不在“是否能展示 Task Trace”，而在 `audit_logs` 写入链路没有稳定接收和持久化 `task_trace_id` / `task_type`。

现有事实：

- `audit_logs` 表结构已预留 `task_trace_id` 与 `task_type`。
- 日志查询和日志审计页已具备 Task Trace 筛选、复制和详情时间线基础。
- 系统设置、品牌证书、媒体/上传、SKU、Banner 等管理端敏感操作存在写审计日志的位置。
- REQ-0075 命中 `admin-list` 横切标签，需引用 `docs/knowledge-base/best-practices/admin-list-page-consistency.md` 与 `docs/knowledge-base/retrospectives/sprint-010-retrospective.md`。

## Goals / Non-Goals

**Goals:**

- 让审计写入接口支持可选 `task_trace_id` 与 `task_type`，并在存在任务上下文时写入 `audit_logs`。
- 明确首批敏感操作接入清单和兼容策略：任务型操作透传任务上下文，普通审计操作保持空字段兼容。
- 保持 audit 类型日志在列表和详情中与 request / usage_event 类型拥有一致的 Task Trace 展示能力。
- 确认 SQLite/MySQL schema 与索引一致，并同步 API、OpenAPI、Orval、数据库文档和测试。
- 将 REQ-0075 的 `admin-list` 横切 AC 前置到实现验收。

**Non-Goals:**

- 不新增独立审计页面。
- 不回填历史 audit log 的任务字段。
- 不扩大全量任务型接口覆盖；该范围继续由 `REQ-0074-task-trace-coverage-expansion` 承接。
- 不重做 Task Trace 主模型；主请求与子请求强关联继续与 `REQ-0073-task-trace-parent-request-model` 对齐。
- 不保存完整请求体、完整响应体或未脱敏 metadata。

## Decisions

### D1. UI 策略：复用现有日志审计页和 DS 组件

采用 DS reuse 策略，不做 CSS Port，也不创建新页面。后续实现应复用现有 `/admin/logs` 页面、列表模板、详情抽屉、fixed toast、复制 helper 和 semantic token。

原型冲突报告：

| 来源 | 决策 |
|---|---|
| HTML 原型 `prototype/web/audit-log-task-trace.html` | 用作信息结构草图，优先级最高；表达列表 Task Trace 列、筛选、详情抽屉 Task Trace 分组和 fixed toast。 |
| PNG Golden Reference | 当前未提供，非阻断；实现阶段以 HTML/context/acceptance 为准。 |
| `prototype/web/context.md` | 作为交互策略来源，明确无 `task_trace_id`、已过期、查询失败等状态。 |
| `acceptance.md` | 作为功能 AC 与横切 AC 事实源。 |
| `rules/ui-design.md` | 约束 semantic token、管理端列表结构和不新增营销式页面。 |
| 现有 `openspec/specs/product-usage-logging/spec.md` | 保持既有日志审计页与 Task Trace 能力，新增 audit 类型写入链路要求。 |

### D2. 审计写入接口向后兼容

`AuditLogRepository.insert()` 或等价写入入口新增可选 `task_trace_id` 与 `task_type` 参数。调用方不提供时保持现有审计写入行为；提供时统一校验、脱敏 metadata 并参数化写入。

备选方案是只在 metadata 保存任务字段。该方案会导致查询和索引退化，不满足 REQ-0075 的结构化查询要求，因此不采用。

### D3. 首批接入采用“清单 + 条件透传”

实现阶段必须形成首批敏感操作清单，至少评估系统设置、品牌证书、媒体/上传、SKU、Banner 等写审计日志位置。并非所有操作都强制包装为 Task Trace；只有已经存在或接收任务上下文的操作透传 `task_trace_id` / `task_type`。

### D4. Schema 以一致性确认为先

需求描述表明字段已预留，因此实现应先检查 SQLite demo、SQLite migration、MySQL baseline 和 MySQL migration 路径是否一致。若存在 drift，再补 schema、迁移、文档和测试；若已一致，则用测试锁定字段和索引行为。

## Risks / Trade-offs

| Risk | Mitigation |
|---|---|
| 将 REQ-0075 与已归档 Task Trace 展示能力重复实现 | Delta spec 只新增 audit log 写入和 audit 类型一致性验收，不重写 Task Trace 主模型。 |
| 调用方传入不可信 `task_trace_id` 被误用为权限依据 | 明确任务字段只用于观测关联，不参与权限判断；权限仍依赖认证上下文和服务端资源校验。 |
| metadata 脱敏遗漏 | 复用现有脱敏函数；新增测试覆盖 Authorization、Cookie、Token、密码、AccessKey、SecretKey、内部路径等字段。 |
| SQLite/MySQL schema drift | 实现前运行 schema drift 检查，必要时同步 schema、migration 和 `docs/04-database-design.md`。 |
| 管理端日志页横切回归 | 将 `admin-list` best-practice 转为任务和验收，覆盖分页 DOM、指标卡 DOM、fixed toast、无 `window.confirm` 和移动端 smoke。 |

## Migration Plan

1. 检查 `audit_logs` 在 SQLite 与 MySQL 中的 `task_trace_id`、`task_type` 字段和索引状态。
2. 扩展审计写入入口参数，保持调用方不传任务字段时的兼容行为。
3. 为首批敏感操作接入或透传任务上下文。
4. 校验日志列表/详情 API 对 audit 类型日志的任务摘要和详情分组返回。
5. 更新 Web 管理端展示和横切验收测试。
6. 同步 OpenAPI、Orval、数据库/API/错误码文档和测试。

Rollback:

- 回滚调用方透传时，保留审计写入接口可选参数和 nullable 字段，避免破坏历史日志读取。
- 若 UI 展示异常，可隐藏 audit 类型任务摘要列或详情 Task Trace 分组，保留基础日志审计查询。
- 若 schema 变更需要回滚，采用兼容 nullable 字段策略，不删除历史数据列。

## Open Questions

- 首批接入清单中 SKU/Banner 是否已有明确 Task Trace 上下文，需在 `/opsx-apply` 前通过代码勘查确认。
- `task_type` 枚举是否需要新增 `certificate_update`、`settings_update`、`media_admin_operation` 等值，需与现有 Task Trace 类型保持一致。
