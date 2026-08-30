---
created_at: 2026-08-30 12:45:20
updated_at: 2026-08-30 12:45:20
---

# 提案

## 背景

环境分层验收与生产证据后置规范已经归档，但目前仍主要依赖人工遵守。若开发证据被写成生产通过、缺体验版或真机 Network 却标记 `passed`、或 `production_only_pending` 在生产发布前未重新判定，现有脚本无法稳定阻断。

本变更将该规则落为强脚本门禁，优先覆盖 OpenSpec 归档、Sprint 归档和 Release 状态 / 发布校验，避免治理规范只停留在文本层。

## 变更内容

- 新增 `scripts/validate-environment-tiered-evidence.py`，检查 Change、Sprint 和 Release 文档中的环境证据语义。
- 阻断开发证据冒充生产通过、DevTools evidence 冒充体验版或真机通过、缺体验版或真机 Network 却标记 `passed`。
- 对 `production_only_pending` 要求明确 `target_environment`、`phase`、`blocking_scope` 或等价上下文；生产发布目标下必须重新判定为生产 gate、N/A 或 blocker。
- 将门禁接入 `validate-archive-evidence.py`、`validate-sprint-archive-readiness.py` 和 `validate-release.py`。
- 更新 `opsx-archive`、`sprint-archive`、`release-status`、`release-publish` 技能说明，以及相关规则和测试。

## 能力范围

### 新增能力

- 无。

### 修改能力

- `agent-workflow-tooling`: workflow 归档命令必须运行环境分层证据脚本门禁。
- `product-release-management`: release status / publish 必须在生产目标下重新判定 `production_only_pending`。
- `testing`: 测试治理必须包含可执行的环境证据校验脚本和聚焦测试。

## 影响范围

- 影响治理脚本、脚本测试、规则文档、命令技能和 OpenSpec delta spec。
- 不修改后端 API、数据库 schema、Web、小程序或管理端业务代码。
- 不需要 OpenAPI / Orval。
- 不需要 Docker Compose 验证。
