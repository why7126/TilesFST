---
requirement_id: REQ-0127-product-data-collection-observability-hard-gate
title: 产品数据采集与链路观测规范硬门禁
terminal: multi
version: v1
status: in_sprint
owner: product
source: capture.md
priority: P1
parent_requirement: REQ-0126-product-data-collection-observability-standard
created_at: 2026-08-26 19:52:14
updated_at: 2026-08-26 21:03:12
related_change: add-product-data-collection-observability-hard-gate
---

# REQ-0127 产品数据采集与链路观测规范硬门禁

## 1. 需求背景

`REQ-0126-product-data-collection-observability-standard` 已建立 `docs/standards/product-data-collection-observability.md`，用于统一产品行为事件、API 请求日志、Task Trace、流程节点、保留周期、脱敏边界和新产品接入清单。当前规范已经具备内容基础，但如果只作为参考文档存在，后续 API、DB、日志审计、行为埋点、Task Trace、前端 / 小程序 / App 请求封装相关变更仍可能遗漏读取、声明、验收和脚本校验。

本需求要求把该规范提升为流程硬门禁：在项目入口、规则文档、req / opsx / sprint 技能检查清单和实现级校验脚本中建立统一触发条件，使相关变更必须声明采集规范适用性、影响范围、N/A 原因、验收项和验证结果。

## 2. 目标用户

| 角色 | 核心诉求 |
|---|---|
| 产品负责人 | 在需求阶段确认涉及数据采集和链路观测的变更是否已声明适用范围和 N/A 原因。 |
| 研发负责人 | 在 OpenSpec 和实现阶段获得可执行门禁，避免只靠人工记忆引用采集规范。 |
| 后端开发 | API、DB、日志审计和 Task Trace 变更时明确请求日志、链路字段、保留周期、脱敏和测试要求。 |
| 前端 / 小程序 / App 开发 | 请求封装、行为埋点和链路 ID 透传变更时明确必须读取和声明采集规范。 |
| QA / 验收人员 | 用统一清单验收规范引用、适用性声明、N/A 原因、测试证据和脚本校验结果。 |
| AI / Codex Agent | 在 req、opsx、sprint 和实现校验中被明确路由到采集规范，减少流程漏项。 |

## 3. 需求目标

- 将 `docs/standards/product-data-collection-observability.md` 接入 `AGENTS.md` 的任务读取路由。
- 在相关 `rules/` 中明确产品数据采集与链路观测规范的触发条件和门禁要求。
- 在 req、opsx、sprint 技能检查清单中加入必读、必声明、必验收要求。
- 提供实现级校验脚本，检查入口、规则、技能和变更材料是否正确引用或声明该规范。
- 覆盖 API、DB、日志审计、行为埋点、Task Trace、前端请求封装、小程序请求封装和 App 请求封装相关变更。
- 允许明确 N/A，但必须记录原因；不得无声明地跳过采集规范门禁。
- 遵守事实唯一归属：详细采集模型继续以 `docs/standards/product-data-collection-observability.md` 为事实源，入口和清单只写短路由和门禁摘要。

## 4. 范围

### 4.1 本期包含

| 范围 | 说明 |
|---|---|
| `AGENTS.md` 读取路由 | 在 API、DB、日志审计、行为埋点、Task Trace、端请求封装等任务类型中追加读取采集规范。 |
| 相关 `rules/` 门禁 | 在 API、数据库、日志 / 审计、Task Trace、前端 / 小程序 / App 请求封装、测试或文档治理相关规则中接入规范引用和声明要求。 |
| req 技能检查清单 | 需求生成、完善、评审或需求转 Change 前，涉及触发范围时必须声明采集规范适用性。 |
| opsx 技能检查清单 | propose / apply / archive 阶段必须检查 Change 是否触发采集规范，并记录适用层级、N/A 原因和验收证据。 |
| sprint 技能检查清单 | Sprint 纳入、执行、归档时能发现相关范围是否缺少采集规范声明或验收结果。 |
| 实现级校验脚本 | 新增或增强脚本，检查规则、技能、Change 文档和验收材料中的规范引用与声明字段。 |
| 验收输出规范 | 成功路径必须报告采集规范门禁状态；不适用时必须报告 N/A 原因。 |

### 4.2 本期不包含

| 不包含 | 说明 |
|---|---|
| 改写采集规范详细正文 | 详细字段、链路模型和保留周期继续由 `docs/standards/product-data-collection-observability.md` 承载；本需求只做门禁化接入。 |
| 直接改造业务 API / DB / UI | 本需求不直接修改业务接口、数据库表、Web、小程序或 App 代码。 |
| 接入外部 APM 或第三方埋点平台 | 仍不引入 OpenTelemetry、第三方埋点、BI 大屏或实时告警。 |
| 批量修复历史归档材料 | 历史 archive 默认不批量改写；如需治理历史漂移，后续通过明确 dry-run 和人工确认处理。 |
| 自动创建新的 REQ / BUG / Change | 发现新问题时只输出建议或标准 capture 文案，除非用户明确授权自动落盘。 |

## 5. 功能要求

### FR-001 `AGENTS.md` 必须接入采集规范读取路由

- `AGENTS.md` MUST 在任务类型追加读取表中加入 `docs/standards/product-data-collection-observability.md`。
- 触发范围 MUST 至少覆盖 API 变更、DB / 数据模型、日志审计、行为埋点、Task Trace、前端请求封装、小程序请求封装和 App 请求封装。
- `AGENTS.md` SHOULD 使用短摘要和路径引用，不复制完整规范正文。
- 输出要求或完成检查清单 SHOULD 增加“是否触发产品数据采集与链路观测规范门禁、是否已声明适用性或 N/A 原因、是否已验证”的检查项。

### FR-002 相关规则必须声明触发条件

- 相关 `rules/` MUST 明确在触发范围内追加读取 `docs/standards/product-data-collection-observability.md`。
- API 规则 MUST 约束请求头、请求日志、OpenAPI / Orval、错误码或响应字段变化时声明采集规范影响。
- DB 规则 MUST 约束 `usage_events`、`request_logs`、`task_traces`、`task_trace_spans`、索引、迁移或保留周期变化时声明采集规范影响。
- 测试规则 MUST 要求相关变更补充或声明行为事件、请求日志、直接 API、Task Trace、脱敏、保留周期和旧数据兼容验证。
- 文档治理规则 MUST 要求归档前复核采集规范门禁状态，并避免把完整规范复制到多个长期文档。
- 若某个规则文件不适用，Change 设计或验收中 MUST 记录 N/A 原因。

### FR-003 req 技能必须在需求阶段形成声明

- `req-generate` / `req-complete` / `req-review` / `req-opsx` 相关技能 MUST 增加采集规范门禁检查。
- 当需求涉及 API、DB、日志审计、行为埋点、Task Trace 或端请求封装时，需求文档 MUST 声明采集规范适用层级。
- 需求文档 MUST 支持明确 N/A，并记录不适用原因。
- `req-complete` 生成的验收材料 SHOULD 包含采集规范检查项，包括 API、DB、端请求封装、脱敏、保留周期、测试和 Orval 影响。
- `req-review` SHOULD 将缺失采集规范声明视为评审风险或阻塞项，具体阻塞等级由后续设计定稿。

### FR-004 opsx 技能必须在 Change 阶段执行门禁

- `opsx-propose` MUST 在创建 Change 时判断是否触发采集规范门禁，并在 `proposal.md`、`design.md`、`tasks.md` 或 `trace.md` 中记录适用性。
- `opsx-apply` MUST 在实现前确认触发范围已读取采集规范并声明适用层级、N/A 原因和预期验证。
- `opsx-archive` MUST 在归档前确认验收材料包含采集规范门禁结果或 N/A 原因。
- Change 涉及 API contract 时 MUST 同步 OpenAPI / Orval / API 文档 / 测试，或记录不需要 Orval 的依据。
- Change 涉及 DB 结构、索引、迁移、保留周期时 MUST 同步 SQLite / MySQL schema、数据库文档和测试，或记录不适用依据。

### FR-005 sprint 技能必须在迭代阶段可追踪

- `sprint-propose` SHOULD 在纳入相关 REQ / BUG / Change 时提示采集规范门禁状态。
- `sprint-apply` SHOULD 在执行范围内检查相关 Change 是否已声明采集规范适用性或 N/A 原因。
- `sprint-archive` MUST 在关闭迭代前复核相关范围的采集规范验收状态，避免已知缺项进入归档。
- Sprint 输出 SHOULD 使用摘要形式报告门禁状态，不复制完整规范正文。

### FR-006 实现级校验脚本必须覆盖关键入口

- 系统 MUST 提供实现级校验脚本，推荐命名为 `scripts/validate-product-data-observability-gates.py` 或扩展现有同类脚本。
- 校验脚本 MUST 检查 `AGENTS.md`、相关 `rules/`、req / opsx / sprint 技能文件是否引用采集规范门禁。
- 校验脚本 SHOULD 检查 active Change 文档是否在触发范围内声明采集规范适用性或 N/A 原因。
- 校验脚本 SHOULD 支持聚焦参数，例如按 Change、REQ、Sprint 或当前 diff 检查，避免默认扫描全部历史 archive。
- 校验成功路径 SHOULD 输出紧凑摘要；失败路径 SHOULD 输出具体缺失文件、缺失字段或触发依据。
- 校验脚本不得读取或输出真实客户数据、密钥、`.env`、Authorization header、Cookie 或本机绝对路径。

### FR-007 触发范围识别必须覆盖路径与语义

- 门禁识别 MUST 同时支持路径级和语义级触发。
- 路径级触发 SHOULD 覆盖后端 API、schema、repository、request logging、Task Trace、日志审计服务、Web 请求封装、小程序请求封装和 App 请求封装候选目录。
- 语义级触发 SHOULD 覆盖 `request_logs`、`usage_events`、`task_traces`、`task_trace_spans`、`behavior_trace_id`、`behavior_event_id`、`client_request_id`、`request_id`、日志审计、行为埋点、请求封装、保留周期、脱敏等关键词。
- App 端若当前仓库没有具体源码目录，门禁 MAY 以规范项保留，并在 N/A 原因中说明仓库暂未承载 App 实现。
- 触发规则应尽量降低误报；误报时允许 N/A 声明，但必须记录原因。

### FR-008 N/A 声明必须可审计

- 相关需求、Change 或 Sprint 验收材料 MUST 支持固定格式记录采集规范不适用原因。
- 推荐字段为 `product_data_collection_observability: applicable | not_applicable`，并配套 `reason`、`affected_layers`、`validation`。
- 不适用原因 MUST 说明为什么不影响 API、DB、日志审计、行为埋点、Task Trace 或端请求封装。
- 不得使用“无”“不涉及”作为唯一说明；需要给出具体边界。

### FR-009 输出与验收必须保持可读且不膨胀

- 命令输出 MUST 报告采集规范门禁状态、适用层级、N/A 原因或缺失项。
- 成功路径 SHOULD 只输出摘要和校验命令，不输出完整规范正文或完整脚本日志。
- 失败路径 SHOULD 给出可执行修复路径，例如补充声明字段、更新验收项或运行聚焦校验。
- Workflow Sync、AI Usage hook 和采集规范门禁校验的输出应分别保留职责，避免互相替代。

## 6. UI / UE 约束

本需求不新增具体 Web 管理端、店主端、小程序或 App UI。

若后续在管理端展示采集规范门禁状态，应另行创建需求，并遵守 Design System semantic token、管理端权限边界和 OpenSpec Change 流程。

## 7. 数据与接口影响

| 范围 | 影响 |
|---|---|
| SQLite / MySQL | 本需求不直接改表；后续校验会约束相关 DB 变更必须声明采集规范影响并同步数据库文档和测试。 |
| Pydantic Schema | 本需求不直接改 Schema；后续请求日志、行为事件或链路字段变化时必须按规范声明。 |
| OpenAPI / Orval | 本需求不直接生成 Orval；后续 API contract 变化时门禁要求同步或记录不适用依据。 |
| Web 管理端 | 本需求不直接改页面；请求封装、日志审计和行为埋点变更会触发规范门禁。 |
| 店主端 / 小程序 / App | 本需求不直接改端代码；请求封装、行为事件、链路 ID 透传和离线 / 重试策略相关变更会触发规范门禁。 |
| 后端 API | 本需求不直接改接口；API、日志审计、Task Trace、保留周期和脱敏相关变更会触发规范门禁。 |
| 测试 | 后续实现阶段需要新增或更新治理校验脚本测试，覆盖触发范围、N/A 声明和缺失项报告。 |

## 8. 关联需求与规则

| 关联项 | 关系 | 说明 |
|---|---|---|
| `REQ-0126-product-data-collection-observability-standard` | 父需求 | 已建立通用产品数据采集与链路观测规范正文。 |
| `REQ-0124-log-audit-behavior-trace-model` | 上游实现参考 | 已在本项目落地行为链路、请求日志和 Task Trace 模型。 |
| `docs/standards/product-data-collection-observability.md` | 详细事实源 | 本需求要接入的核心规范文档。 |
| `docs/standards/task-trace-coverage.md` | 相关标准 | Task Trace 分级覆盖与流程节点治理参考。 |
| `docs/standards/api-governance.md` | 相关标准 | API contract、OpenAPI / Orval 与请求治理参考。 |
| `rules/requirement-management.md` | 流程规则 | 需求状态、trace、评审与后续命令门禁。 |
| `rules/document-governance.md` | 文档规则 | 长期文档事实源、同步、归档与表达卫生。 |
| `rules/agent-context-budget.md` | 上下文规则 | 校验和命令输出需要控制读取范围和日志体积。 |

## 9. 风险与待确认

| 风险 / 待确认 | 说明 |
|---|---|
| 校验脚本边界过宽 | 如果默认扫描所有历史 archive，容易造成噪音和无关阻塞；建议默认聚焦 active Change、当前 diff 或显式目标。 |
| App 目录不明确 | 当前仓库可能未承载 App 实现，需在门禁中保留 App 规范项并支持 N/A 原因。 |
| N/A 字段格式待定 | 建议在 req-complete 或 OpenSpec design 中定稿固定字段，降低后续脚本解析成本。 |
| 技能文件修改范围较大 | req、opsx、sprint 技能数量较多，后续实现应先列清单，再分批接入并用脚本兜底。 |
| 规则重复风险 | 多个入口都需要引用采集规范，但不得复制完整规范正文，避免事实源漂移。 |

## 10. 状态块

```yaml
requirement_id: REQ-0127-product-data-collection-observability-hard-gate
status: approved
lifecycle_stage: plan
priority: P1
readiness: Ready
parent_requirement: REQ-0126-product-data-collection-observability-standard
terminal: multi
target_clients:
  web_admin: included
  web_catalog: included
  wechat_miniapp: included
  app: included
  backend_api: included
expected_openspec_change: add-product-data-collection-observability-hard-gate
next_command: /opsx-archive REQ-0127-product-data-collection-observability-hard-gate
notes:
  - 已根据 capture 生成 requirement.md，并补齐用户故事、业务流程、验收标准和 trace 扩展。
  - 需求评审已通过并已纳入 sprint-026，OpenSpec Change 已创建。
  - 本需求只定义采集规范硬门禁，不直接修改业务 src 实现。
  - Knowledge-base UI 横切 gate 为 N/A。
```
openspec_changes:
  - change_id: add-product-data-collection-observability-hard-gate
    type: update
    status: applied
