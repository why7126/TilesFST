## ADDED Requirements

### Requirement: 文档事实唯一归属
系统 MUST 为长期治理事实维护唯一事实源；入口文档和命令技能可以摘要引用，但不得复制完整规则导致漂移。

#### Scenario: 新增或更新长期治理规则
- **WHEN** 命令修改 `AGENTS.md`、`rules/`、`docs/`、`.agents/skills/` 或 `scripts/`
- **THEN** 系统 MUST 判断该事实的唯一归属位置
- **AND** 其他位置 SHOULD 使用短摘要和相对链接指向事实源

### Requirement: 治理决策记录字段
系统 MUST 在治理类 Change、`/spec-study` 学习报告和 `/spec-opt` 治理日志中记录关键决策，而不是只记录文件清单。

#### Scenario: 应用治理学习或规范优化
- **WHEN** `/spec-study apply` 或 `/spec-opt` 完成治理资产更新
- **THEN** 报告 MUST 包含采纳原因、未采纳原因、替代方案或取舍、验证责任和后续触发条件
- **AND** 报告 MUST 不包含会话推理、未脱敏路径、密钥、用户隐私或学习对象源码

### Requirement: 文档 slop 与 CoT 泄漏审计
系统 MUST 提供长期文档卫生规则和轻量校验，帮助发现会话推理残留、临时草稿引用、review 对话、不可解析内部引用和不必要历史叙事。

#### Scenario: 修改长期治理文档
- **WHEN** 命令新增或修改 `docs/`、`rules/`、`AGENTS.md` 或 `.agents/skills/`
- **THEN** 系统 SHOULD 运行文档卫生校验或说明不适用原因
- **AND** 发现项 MUST 由人工或 Agent 语义判断后处理，不得由脚本自动删除事实性内容

### Requirement: 最小相关验证选择
系统 MUST 根据实际 diff scope 和影响面选择最小相关证据，同时不得跳过项目强制门禁。

#### Scenario: 治理变更完成
- **WHEN** 变更只触达治理文档、技能或校验脚本
- **THEN** 系统 SHOULD 运行治理相关脚本、目标 Change 校验和脚本自身校验
- **AND** 系统 SHOULD 明确业务测试不适用的原因
- **AND** 系统 MUST NOT 仅因为提交、归档或输出报告而重复运行已通过且未被新改动影响的无关检查

### Requirement: 防御性模式知识库模板
系统 MUST 支持将已发生或险些发生的问题沉淀为防御性模式，记录缺陷类别、预防规则和验证方式。

#### Scenario: 问题具备复用价值
- **WHEN** BUG、返修、发布事故、验收失败或治理复盘发现可复用的预防规则
- **THEN** 系统 SHOULD 建议写入 `docs/knowledge-base/best-practices/`
- **AND** 条目 SHOULD 使用防御性模式模板，避免写成长篇事故叙事
