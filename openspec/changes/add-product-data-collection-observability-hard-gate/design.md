## 背景

REQ-0126 已通过 `add-product-data-collection-observability-standard` 建立通用产品数据采集与链路观测规范，覆盖 `usage_events`、`request_logs`、`task_traces`、`task_trace_spans`、链路 ID、保留周期和脱敏边界。REQ-0127 不改写该事实源正文，而是补齐治理入口：让相关变更在需求、OpenSpec、Sprint、实现和归档阶段必须读取、声明、校验和验收该规范。

当前项目已有 Workflow Sync、Sprint scope 校验、OpenSpec language 校验、API / DB / Test governance 校验等模式。本 Change 沿用这些模式，新增聚焦脚本检查“入口是否接入、触发范围是否声明、N/A 是否可审计”，避免把门禁只写成文档提醒。

## 目标与非目标

**目标：**

- 建立统一门禁触发范围：API、DB、日志审计、行为埋点、Task Trace、Web 请求封装、小程序请求封装、App 请求封装。
- 让 `AGENTS.md`、相关 `rules/`、req / opsx / sprint 技能都能路由到 `docs/standards/product-data-collection-observability.md`。
- 固化声明字段：`product_data_collection_observability`、`affected_layers`、`reason`、`validation`。
- 提供实现级校验脚本和测试，默认聚焦 active Change / 指定 REQ / 指定 Sprint / 当前 diff，不默认扫描全部历史 archive。
- 在 Change 材料中明确本 Change 不直接修改业务 `src/`、不改 API contract、不改数据库结构、不需要 Orval。

**非目标：**

- 不重写 `docs/standards/product-data-collection-observability.md` 的详细字段模型、保留周期或脱敏正文。
- 不批量修复历史归档 Change、历史 Sprint 或历史 REQ。
- 不引入 OpenTelemetry、外部 APM、第三方埋点平台、BI 大屏或实时告警。
- 不直接修改 Web、小程序、App、后端 API 或数据库业务实现。

## 设计决策

### 决策 1：事实源保持单一，入口只写门禁摘要

详细模型继续归属 `docs/standards/product-data-collection-observability.md`。`AGENTS.md`、`rules/` 和技能只写触发范围、声明字段、验收职责和路径引用。

替代方案是把完整规范复制进多个规则或技能文件；该方式会造成事实源漂移，也会膨胀上下文预算，因此不采用。

### 决策 2：声明字段统一为结构化块

相关需求、Change 或验收材料使用固定结构：

```yaml
product_data_collection_observability:
  status: applicable
  affected_layers:
    - api
    - database
    - request_logs
    - usage_events
    - task_trace
    - web_request_wrapper
    - miniapp_request_wrapper
    - app_request_wrapper
    - workflow_governance
  reason: 本 Change 将采集规范接入流程硬门禁。
  validation: 运行采集规范门禁校验脚本、OpenSpec 校验、Workflow Sync，并在验收材料记录摘要。
```

不适用时使用 `status: not_applicable`，`reason` 必须说明为什么不影响 API、DB、日志审计、行为埋点、Task Trace 或端请求封装，不得只写“无”或“不涉及”。

### 决策 3：校验脚本采用入口完整性 + 目标声明检查

脚本应先检查固定治理入口是否引用规范门禁，再对指定 Change / REQ / Sprint 或当前 diff 做触发范围识别。路径级触发覆盖 API、schema、repository、日志审计、Task Trace、Web 请求封装、小程序请求封装和 App 请求封装候选目录；语义级触发覆盖 `request_logs`、`usage_events`、`task_traces`、`task_trace_spans`、`behavior_trace_id`、`behavior_event_id`、`client_request_id`、`request_id`、日志审计、行为埋点、请求封装、保留周期、脱敏等关键词。

替代方案是只在 OpenSpec 文档里人工检查；该方式无法成为实现级硬门禁，因此不采用。

### 决策 4：Sprint 只保存摘要，不替代 Change 事实源

Sprint 技能在纳入、执行、归档阶段提示门禁状态，但验收事实仍落在 REQ、Change、tasks、acceptance 和校验脚本输出摘要中。Workflow Sync 负责范围回填，Sprint 文档不复制完整规范正文。

## 风险与权衡

- [Risk] 触发规则过宽导致误报 -> 允许 `not_applicable`，但必须写清具体边界和验证依据。
- [Risk] 技能文件修改范围较大，容易漏某个命令 -> 校验脚本必须覆盖 req / opsx / sprint 技能清单，并输出缺失文件。
- [Risk] App 目录当前不明确 -> 保留 App 请求封装门禁层级；若仓库未承载 App 实现，Change 可以声明 N/A 原因。
- [Risk] 父 Change 尚未 archive -> 本 Change 作为独立后续门禁扩展，delta spec 继续作用于 `product-data-collection-observability-standard`，归档时按 OpenSpec 合并顺序处理。

## 迁移计划

1. `/opsx-apply` 更新治理入口、规则、技能和校验脚本。
2. 运行新增脚本的聚焦校验、OpenSpec strict 校验、语言校验、Workflow Sync。
3. `/opsx-archive` 时确认采集规范门禁验收结果已记录，再合并 spec。

回滚策略：若校验脚本或门禁声明产生不可接受误报，可在同一 Change 返修触发关键词、路径范围和 N/A 规则；归档前不得绕过失败的硬门禁。

## 开放问题

- 无需用户额外决策；实现阶段可根据仓库实际目录细化 App 请求封装候选路径。

## 产品数据采集与链路观测声明

```yaml
product_data_collection_observability:
  status: applicable
  affected_layers:
    - api
    - database
    - request_logs
    - usage_events
    - task_trace
    - web_request_wrapper
    - miniapp_request_wrapper
    - app_request_wrapper
    - workflow_governance
  reason: 本 Change 直接把产品数据采集与链路观测规范接入 AGENTS、rules、req/opsx/sprint 技能和实现级校验脚本。
  validation: 后续实现必须运行采集规范门禁校验脚本，并在 acceptance / tasks 记录入口引用、声明字段、N/A 规则和校验摘要。
```
