---
created_at: 2026-08-31 14:06:32
updated_at: 2026-08-31 14:06:32
---

# 设计：证据来源声明规格收敛

## 设计原则

- 用“证据来源声明 / 证明边界 / 手动诊断”替代“环境分层 / 生产证据后置 / 强脚本门禁”作为新流程主语。
- 保留历史兼容字段的可读性，避免旧归档、旧测试或旧 release 数据无法解释。
- 正式规格标题的重命名通过 OpenSpec delta 表达，避免开发中直接改写 `openspec/specs/`。

## 影响范围

- OpenSpec delta：`agent-workflow-tooling`、`testing`、`media-acceptance-template`、`miniapp-device-evidence-template`。
- 治理日志：`docs/spec-logs/`。
- Sprint scope：`sprint-029` 承载该纯治理 Change。

## 验证策略

- `openspec validate rename-evidence-source-specs`
- `python scripts/validate-openspec-language.py`
- `python scripts/validate-directory-structure.py`
- `python scripts/validate-agent-context-budget.py`
- `python scripts/validate-sprint-scope.py sprint-029 --item rename-evidence-source-specs`
- 对本次触达 Markdown 运行聚焦文档表达卫生检查。

## 影响声明

- API：不适用。
- DB：不适用。
- Web：不适用。
- 小程序：不修改运行时代码，仅收敛小程序证据模板规格语义。
- 管理端：不适用。
- Orval：不适用。
- Docker Compose：不适用。
