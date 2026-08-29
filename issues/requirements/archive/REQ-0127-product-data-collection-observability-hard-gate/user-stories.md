---
requirement_id: REQ-0127-product-data-collection-observability-hard-gate
title: 产品数据采集与链路观测规范硬门禁 - 用户故事
created_at: 2026-08-26 19:55:31
updated_at: 2026-08-26 19:55:31
---

# 用户故事

## US-001 需求阶段识别采集规范门禁

作为产品负责人，我希望涉及 API、DB、日志审计、行为埋点、Task Trace 或端请求封装的需求在 PRD 阶段就声明产品数据采集与链路观测规范适用性，以便评审时能确认是否需要补充采集、脱敏、保留周期和验收要求。

验收要点：

- 需求文档能声明 `product_data_collection_observability` 适用状态。
- 需求文档能列出适用层级：API、DB、请求日志、行为事件、Task Trace、Web、小程序、App 或 N/A。
- N/A 必须写明具体原因，不得只写“无”或“不涉及”。

## US-002 OpenSpec 阶段形成实现前门禁

作为研发负责人，我希望 OpenSpec Change 在 propose 和 apply 阶段检查是否触发采集规范门禁，以便实现前确认读取范围、设计声明、任务项和测试计划没有遗漏。

验收要点：

- `proposal.md`、`design.md`、`tasks.md`、`trace.md` 或 `acceptance.md` 中有固定格式声明。
- 涉及 API contract 时声明 OpenAPI、Orval、API 文档和测试影响。
- 涉及 DB 字段、索引、迁移或保留周期时声明 SQLite / MySQL、数据库文档和测试影响。
- 不适用时记录明确边界和原因。

## US-003 Sprint 阶段跟踪门禁状态

作为 Sprint 负责人，我希望 Sprint 纳入、执行和归档时能看到采集规范门禁状态，以便关闭迭代前发现缺少声明、缺少验收或缺少校验证据的范围项。

验收要点：

- Sprint 相关技能能提示门禁适用、N/A 或缺失状态。
- Sprint archive 前能复核相关 Change 的采集规范验收结果。
- 输出只报告摘要和修复路径，不复制完整规范正文。

## US-004 AI Agent 获得明确读取路由

作为 AI / Codex Agent，我希望 `AGENTS.md` 和相关规则把采集规范接入必读路由，以便处理 API、DB、日志审计、行为埋点、Task Trace 或端请求封装变更时不会遗漏 `docs/standards/product-data-collection-observability.md`。

验收要点：

- `AGENTS.md` 的任务类型追加读取表包含采集规范路径。
- 相关 `rules/` 对触发范围、声明字段和验收要求有短摘要。
- 入口和规则只引用事实源，不复制完整规范正文。

## US-005 校验脚本提供实现级兜底

作为流程维护者，我希望有实现级校验脚本检查入口、规则、技能和 active Change 的采集规范门禁，以便把“应该记得检查”的流程要求变成可运行的质量门禁。

验收要点：

- 校验脚本能检查 `AGENTS.md`、相关 `rules/` 和 req / opsx / sprint 技能是否接入门禁。
- 校验脚本能识别触发关键词或路径，并检查 active Change 是否声明适用性或 N/A 原因。
- 校验脚本支持聚焦目标，避免默认扫描所有历史归档。
- 成功输出紧凑摘要，失败输出缺失文件、缺失字段和修复建议。

## US-006 安全和上下文预算边界不被放宽

作为安全与治理负责人，我希望门禁校验不读取或输出敏感信息，也不把完整规范复制到多个长期文档，以便降低泄漏风险和事实源漂移。

验收要点：

- 校验脚本不得读取或输出真实客户数据、密钥、`.env`、Authorization header、Cookie 或本机绝对路径。
- 成功路径不输出完整规范正文、完整 Workflow Sync 派生块或长日志。
- 事实源仍归属 `docs/standards/product-data-collection-observability.md`。
