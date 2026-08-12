## MODIFIED Requirements

### Requirement: 规范优化命令 spec-opt

`/spec-opt` MUST 作为项目治理规范优化入口，用于新增或修改 `.agents/skills/` 命令、`rules/` 文档、`docs/` 文档规范、`scripts/` 治理脚本、`AGENTS.md` 入口和 active OpenSpec Change 文档。`/spec-opt` MUST 只修改治理资产，不得修改业务 `src/` 运行时代码。`/spec-opt` 完成本项目规范、技能、脚本、目录边界或校验规则迭代后，MUST 在 `docs/spec-logs/` 写入治理迭代日志，并维护 `docs/spec-logs/CHANGELOG.md` 变更历史总账。

#### Scenario: 输出治理迭代日志

- **WHEN** `/spec-opt` 完成本项目规范、技能、脚本、目录边界或校验规则迭代
- **THEN** `/spec-opt` MUST 在 `docs/spec-logs/` 写入治理迭代日志
- **AND** 日志文件名 MUST 使用 `YYYYMMDDhhmmss-governance-xxx.md`
- **AND** `YYYYMMDDhhmmss` MUST 使用日志生成时刻的 `Asia/Shanghai` 日期时间，精确到秒
- **AND** `xxx` MUST 使用小写 kebab-case 表达治理主题
- **AND** 日志 MUST 包含迭代目标、变更摘要、影响范围、更新文件、验证结果和后续建议
- **AND** 日志 MUST NOT 包含用户隐私数据、真实客户数据、密钥、访问令牌、未脱敏日志、订单原文、聊天原文、工单原文、截图中的个人信息或学习对象源码
- **AND** 如需说明隐私相关风险，日志 MUST 使用脱敏占位符或聚合描述

#### Scenario: 维护治理变更历史总账

- **WHEN** `/spec-opt` 新增或更新本项目规范、技能、脚本、目录边界或校验规则
- **THEN** `/spec-opt` MUST 新增或更新 `docs/spec-logs/CHANGELOG.md`
- **AND** `CHANGELOG.md` MUST 按倒序记录治理资产变更历史
- **AND** 每条记录 MUST 至少包含时间、来源命令、关联 Change、类型、影响范围、更新文件、验证结果、详细日志链接和跨项目落地提示词
- **AND** 跨项目落地提示词 MUST 说明其他项目要落地同类规范时可直接给 AI 的 Prompt
- **AND** 跨项目落地提示词 MUST 可复制、脱敏、项目无关
- **AND** `CHANGELOG.md` MUST NOT 替代单次 `YYYYMMDDhhmmss-governance-*.md` 详细日志、OpenSpec Change、Sprint 或 Issue 事实源
- **AND** `CHANGELOG.md` MUST NOT 包含用户隐私数据、真实客户数据、密钥、访问令牌、未脱敏日志、订单原文、聊天原文、工单原文、截图中的个人信息或学习对象源码
