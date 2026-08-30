---
created_at: 2026-08-30 12:45:20
updated_at: 2026-08-30 12:45:20
---

# 设计

## 校验对象

新增脚本 `scripts/validate-environment-tiered-evidence.py` 支持三类入口：

| 入口 | 检查范围 |
|---|---|
| `--change <change-id>` | active 或 archived Change 的 `proposal.md`、`design.md`、`tasks.md`、`trace.md`、`acceptance.md`、`test-plan.md` |
| `--sprint <sprint-id>` | Sprint 四件套，以及 scope 内 Change 的归档或 active 文档 |
| `--release-dir releases/<version> --target development|production` | release metadata、announcement 和 release 状态文本中的环境证据语义 |

脚本默认输出 Markdown 报告；`--json` 输出机器可读结构，便于 `validate-release.py` 和测试复用。

## 阻断规则

第一版采用结构化字段与关键词启发式组合，避免引入复杂 NLP：

- 当文本同时出现开发证据来源和生产通过结论时阻断，例如 DevTools、本地测试、开发 API smoke 与“生产已通过”“正式环境通过”“production passed”同段出现。
- 当 `source: network_devtools`、`target_environment: development` 或 DevTools evidence 与体验版 / 真机通过结论同段出现时阻断。
- 当 `source: network_trial`、`source: real_device` 或体验版 / 真机 evidence 的 `status: passed` 缺少 evidence 引用或关键说明时阻断。
- 当 `production_only_pending` 缺少目标环境、阶段或阻塞范围上下文时阻断。
- 当 release 目标为 `production` 且仍存在 `production_only_pending` 时阻断，要求重新分类为生产 gate、N/A 或 blocker。

## 接入点

- `validate-archive-evidence.py`：归档后检查 archived Change 文档；失败时 `opsx-archive` 失败。
- `validate-sprint-archive-readiness.py`：Sprint close 前聚合 scope 内 Change 和 Sprint 四件套检查；失败时 readiness blocked。
- `validate-release.py`：`--status` 和 `--stage publish --target production` 读取环境证据结果，将错误归类为 `publish_evidence_missing` 或 `production_only_pending`。

## 产品数据采集与链路观测

本变更只新增治理脚本和测试，不修改运行时代码、API、DB、日志审计、行为埋点、Task Trace、Web 请求封装、小程序请求封装或 App 请求封装。

```yaml
product_data_collection_observability:
  applicability: not_applicable
  affected_layers: []
  reason: "纯治理脚本、规则和测试变更；不改变运行时代码、接口、数据库或端侧请求链路。"
  validation: "运行脚本聚焦测试、OpenSpec、目录、上下文预算和文档卫生校验。"
```

## 风险与取舍

- 已采纳：使用明确关键词和结构化字段阻断高价值误判，先覆盖最容易出事故的证据冒充场景。
- 未采纳：不做完整自然语言理解，也不强制所有历史文档一次性补齐字段，避免误伤大量既有归档。
- 取舍：脚本只对当前目标 Change、目标 Sprint 或目标 Release 做聚焦检查；全仓历史审计可后续另起治理 Change。
