---
requirement_id: REQ-0126-product-data-collection-observability-standard
title: 建立通用产品数据采集与链路观测规范 - 验收标准
acceptance_status: pending
owner: product
source: requirement.md
created_at: 2026-08-26 10:20:20
updated_at: 2026-08-26 19:39:49
---

# 验收标准

## 功能 AC

- [ ] AC-001 规范明确覆盖 Web 管理端、店主端、小程序、App 和后端 API。
- [ ] AC-002 规范明确所有业务 API 请求 MUST 写入 `request_logs`。
- [ ] AC-003 规范列出可排除 `request_logs` 的低价值高频请求，包括健康检查、静态资源、OpenAPI 文档资源、预检 OPTIONS、内部探活或等价请求。
- [ ] AC-004 规范明确用户行为事件采集口径：页面访问、业务点击、菜单切换、搜索、筛选、详情查看、表单提交、保存、删除、上传、分享、收藏、登录成功 / 失败等可命名业务行为 SHOULD 采集。
- [ ] AC-005 规范明确纯视觉交互、无业务含义 hover、tooltip 关闭、布局点击、重复无状态点击等 UI 噪音 MAY 排除。
- [ ] AC-006 规范明确 `behavior_trace_id`、`behavior_event_id`、`parent_behavior_event_id`、`request_id`、`client_request_id` 和 `task_trace_id` 的语义、生成方和可信边界。
- [ ] AC-007 规范明确统一四层链路模型：`usage_events -> request_logs -> task_traces -> task_trace_spans`。
- [ ] AC-008 规范明确界面触发入口使用 `behavior_trace_id` 串联一次用户行为触发的一个或多个 API 请求。
- [ ] AC-009 规范明确直接 API 调用不伪造 `usage_events`，允许 `behavior_trace_id` 为空，并继续从 `request_logs.request_id` 进入任务链路。
- [ ] AC-010 规范明确所有业务 API 有 request log，且长耗时、多步骤、批量、异步、导入导出、上传 / 对象存储、第三方服务调用、失败需定位节点、高风险写操作或关键业务数据变更 MUST 接入 Task Trace。
- [ ] AC-011 规范明确普通简单写操作 MAY 只保留 request log，但需在需求或设计中说明不接入 Task Trace 的理由。
- [ ] AC-012 规范明确 Task Trace span 写入失败 MUST 降级，不得覆盖主业务错误。
- [ ] AC-013 规范明确默认数据保留周期：`request_logs` 90 天、`usage_events` 明细 180 天、`task_traces/task_trace_spans` 90 天、聚合数据 1 年。
- [ ] AC-014 规范明确产品如需调整默认保留周期，必须记录原因、范围和审批依据。
- [ ] AC-015 规范明确超期明细数据 MUST 删除或匿名化，不允许无限期保留。
- [ ] AC-016 规范明确禁止采集或展示 Authorization、Cookie、Token、密码、真实密钥、数据库 DSN、MinIO AccessKey / SecretKey、完整请求体、完整响应体、本机绝对路径、完整内部对象 key 和真实客户敏感数据。
- [ ] AC-017 规范明确前端脱敏只作为展示优化，后端脱敏是安全边界。
- [ ] AC-018 规范明确 API contract 变化必须同步 Pydantic Schema、OpenAPI、Orval、API 文档和前后端测试。
- [ ] AC-019 规范明确 DB 字段或索引变化必须同步 SQLite / MySQL schema、迁移、数据库设计文档和测试。
- [ ] AC-020 规范提供新产品接入清单，至少覆盖前端 helper / SDK、后端 request log middleware、Task Trace helper、DB migration、OpenAPI/Orval、脱敏 helper、测试模板和验收清单。
- [ ] AC-021 规范明确后续 REQ、BUG、OpenSpec Change 和 Sprint 验收如何引用该规范。
- [ ] AC-022 规范明确首版不包含外部 APM、OpenTelemetry、第三方埋点平台、实时告警、BI 大屏、复杂用户画像或历史数据强制回填。
- [ ] AC-023 规范明确 `usage_events`、`request_logs`、`task_traces`、`task_trace_spans` 的最小标准字段、中文注释、可空规则、生成方、关联关系、索引建议和脱敏边界，并说明具体产品可在不改变字段语义和安全边界的前提下扩展。

## Knowledge-base 横切检查

| 标签 | 引用文档 | 将写入 AC-XCUT 条数 | 说明 |
|---|---|---:|---|
| 无匹配 UI 标签 | - | 0 | 本 REQ 为通用治理规范，不新增具体管理端列表页、表单页、弹窗或上传 UI；后续具体 UI 页面接入时再按对应标签引用 best-practices。 |

## 验收结果回填

```yaml
acceptance_status: pending
accepted_at: null
accepted_by: null
source_change: add-product-data-collection-observability-standard
source_sprint: sprint-026
evidence: []
failed_items: []
source_event: opsx.modify
notes: 待验收；由 opsx.apply 标记，后续 archive 时回填结论。
```

