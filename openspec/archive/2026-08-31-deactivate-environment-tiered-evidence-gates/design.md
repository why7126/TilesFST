---
created_at: 2026-08-31 10:23:00
updated_at: 2026-08-31 10:23:00
---

# 设计

## 当前问题

环境分层 evidence 最初用于避免开发阶段证据冒充体验版、真机或生产证据，并处理生产证据后置。但本项目现在不再区分 development / production 发布目标，继续把该脚本放在默认归档和发布门禁中，会制造与单一发布语义冲突的操作心智。

## 目标设计

默认工作流只保留与当前项目交付直接相关的门禁：

- release validator 不再自动调用环境分层 evidence。
- sprint archive readiness 不再把环境分层 evidence 纳入 blocker。
- archive evidence validator 不再把环境分层 evidence 纳入归档阻断。
- `validate-environment-tiered-evidence.py` 保留为手动诊断入口，用于排查证据来源描述是否混淆。

## 文案口径

新文案使用“证据来源声明 / 证据来源诊断”：

- 鼓励记录 `evidence_source`、`evidence_ref`、`network_summary`、`executed_at` 等可定位证据来源。
- 不再推荐把缺口写为 `production_only_pending`。
- 历史 `production_only_pending` 只作为兼容读取和诊断结果，不作为新流程默认字段。

## 验证策略

- 调整环境分层脚本测试为诊断工具自身测试。
- 调整 release、sprint archive、archive evidence 相关测试，确认默认链路不再被环境分层 evidence 阻断。
- 保持 OpenSpec、目录结构、上下文预算和文档表达卫生校验。
