---
requirement_id: REQ-0127-product-data-collection-observability-hard-gate
title: 产品数据采集与链路观测规范硬门禁 - 验收标准
acceptance_status: pending
owner: product
source: requirement.md
created_at: 2026-08-26 19:55:31
updated_at: 2026-08-26 21:03:12
---

# 验收标准

## 功能 AC

- [ ] AC-001 `AGENTS.md` 在任务类型追加读取路由中接入 `docs/standards/product-data-collection-observability.md`。
- [ ] AC-002 `AGENTS.md` 的触发范围至少覆盖 API、DB / 数据模型、日志审计、行为埋点、Task Trace、前端请求封装、小程序请求封装和 App 请求封装。
- [ ] AC-003 相关 `rules/` 明确采集规范的必读、必声明、必验收触发条件，并避免复制完整规范正文。
- [ ] AC-004 API 相关规则声明请求日志、链路字段、OpenAPI / Orval、错误码、响应字段或请求头变化时必须评估采集规范影响。
- [ ] AC-005 DB 相关规则声明 `usage_events`、`request_logs`、`task_traces`、`task_trace_spans`、索引、迁移或保留周期变化时必须评估采集规范影响。
- [ ] AC-006 测试相关规则声明相关变更必须验证或明确 N/A：行为事件、请求日志、直接 API、Task Trace、脱敏、保留周期和旧数据兼容。
- [ ] AC-007 文档治理或归档规则声明归档前必须复核采集规范门禁状态，并遵守事实唯一归属。
- [ ] AC-008 req 技能检查清单覆盖采集规范适用性声明、适用层级、N/A 原因和验收项。
- [ ] AC-009 opsx 技能检查清单覆盖 propose、apply、archive 阶段的采集规范读取、声明、验证和归档复核。
- [ ] AC-010 sprint 技能检查清单覆盖 Sprint 纳入、执行和归档阶段的采集规范门禁状态摘要。
- [ ] AC-011 实现级校验脚本能够检查 `AGENTS.md`、相关 `rules/` 和 req / opsx / sprint 技能是否引用采集规范门禁。
- [ ] AC-012 实现级校验脚本能够识别 active Change 或目标 diff 是否触发 API、DB、日志审计、行为埋点、Task Trace 或端请求封装范围。
- [ ] AC-013 实现级校验脚本能够检查触发范围内是否存在 `product_data_collection_observability` 或等价固定声明。
- [ ] AC-014 固定声明至少包含适用状态、适用层级、N/A 原因和验证摘要；推荐字段为 `product_data_collection_observability`、`affected_layers`、`reason`、`validation`。
- [ ] AC-015 N/A 声明必须说明为什么不影响 API、DB、日志审计、行为埋点、Task Trace 或端请求封装，不得只写“无”或“不涉及”。
- [ ] AC-016 校验脚本支持聚焦参数，例如按 Change、REQ、Sprint 或当前 diff 检查，默认不扫描全部历史 archive。
- [ ] AC-017 校验成功路径只输出紧凑摘要；失败路径输出具体缺失文件、缺失字段、触发依据和修复建议。
- [ ] AC-018 校验脚本不得读取或输出真实客户数据、密钥、`.env`、Authorization header、Cookie、本机绝对路径或完整工具输出正文。
- [ ] AC-019 后续 OpenSpec Change 设计必须说明本需求不直接修改业务 `src/`，除非进入已评审、已纳入 Sprint 的实现阶段。
- [ ] AC-020 验收材料必须记录 `docs/standards/product-data-collection-observability.md` 为详细事实源，入口和清单只保留路径引用与门禁摘要。
- [ ] AC-021 后续实现完成后，必须运行采集规范门禁校验脚本、Workflow Sync 和相关文档 / 技能校验，并记录摘要。

## Knowledge-base 横切检查

| 标签 | 引用文档 | 将写入 AC-XCUT 条数 | 说明 |
|---|---|---:|---|
| 无匹配 UI 标签 | - | 0 | 本 REQ 为治理门禁和流程规范，不新增具体管理端列表页、表单页、弹窗或媒体上传 UI；后续具体 UI 页面接入时再按对应标签引用 best-practices。 |

## 验收结果回填

```yaml
acceptance_status: pending
accepted_at: null
accepted_by: null
source_change: add-product-data-collection-observability-hard-gate
source_sprint: sprint-026
evidence: []
failed_items: []
source_event: opsx.apply
notes: 待验收；由 opsx.apply 标记，后续 archive 时回填结论。
```

