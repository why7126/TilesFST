---
purpose: 全局规则
content: 团队研发规范和AI约束
source: AI自动生成初稿，项目团队确认
update_method: 项目初始化后由人工确认；后续由AI辅助更新并经人工Review
created_at: 2026-06-13 00:00:00
updated_at: 2026-08-03 00:00:00
note: 适用于瓷砖信息管理平台项目模板
---

# 语言规范

产品、需求、设计、测试、OpenSpec 规范正文和长期治理文档 MUST 使用中文优先编写；代码标识符使用英文；API 字段使用英文 snake_case 或 camelCase，按接口约定统一。

## OpenSpec 语言规则

- `openspec/specs/**/spec.md` 与 `openspec/changes/**/specs/**/spec.md` 中的业务能力标题、需求说明、场景名称和验收描述 MUST 使用中文。
- `openspec/changes/**/{proposal.md,design.md,tasks.md,trace.md,acceptance.md,test-plan.md}` 属于 OpenSpec Change 文档，MUST 中文优先；标题、章节名、任务项和验收描述不得保留 `Why`、`What Changes`、`Implementation`、`Validation`、`Root Cause` 等英文脚手架文案。
- OpenSpec 解析关键字 MAY 保留英文，例如 `Requirement`、`Scenario`、`MUST`、`SHALL`、`WHEN`、`THEN`、`AND`，以保证 CLI 校验稳定。
- API 路径、HTTP 方法、数据库表名、字段名、枚举值、代码类名、文件路径、命令、产品英文专名（如 Orval、Mintlify、Docker、Swagger）MAY 保留英文。
- Change 文档中的命令、路径、代码标识符、API 字段、错误码、版本号和 OpenSpec CLI 固定关键字 MAY 保留英文，但承载业务语义的自然语言句子 MUST 使用中文优先。
- OpenSpec CLI 或上游 schema 若在归档时提示 `proposal.md` 缺少 `## Why` / `## What Changes` 等英文标准标题，该提示在本项目中属于 CLI 兼容性提示；项目阻塞门禁以 `python scripts/validate-openspec-language.py` 为准，不得为消除提示回填英文脚手架标题。
- 归档后生成的 `Purpose` 不得保留 `TBD - created by archiving...` 等脚手架占位文案；应改为中文能力说明。
- 运行 OpenSpec 文档校验时 MUST 执行 `python scripts/validate-openspec-language.py` 或 `scripts/validate-openspec.sh`；归档前 active Change 不得存在英文脚手架标题或全英文任务项。
