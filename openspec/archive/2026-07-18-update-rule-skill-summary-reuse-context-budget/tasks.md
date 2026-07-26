# Tasks

## 1. 规则与 Skill 更新

- [x] 1.1 更新 `rules/agent-context-budget.md`，新增规则/Skill 已读摘要复用定义、最小字段、失效条件与安全边界。
- [x] 1.2 更新命令 Skill 的 `Context Budget Guardrails`，统一表达同一会话已读且无变更的规则和 Skill 用摘要承接。

## 2. 校验与测试

- [x] 2.1 增强 `scripts/validate-agent-context-budget.py`，检查命令 Skill 是否包含摘要复用约束，并继续报告默认宽泛读取指令的文件与行号。
- [x] 2.2 补充或更新测试，覆盖摘要复用约束缺失、宽泛读取回退和合规 Skill 通过场景。

## 3. 验证与同步

- [x] 3.1 运行 `python scripts/validate-agent-context-budget.py`，确认命令 Skill 预算门禁通过。
- [x] 3.2 运行 OpenSpec 校验，确认 `agent-workflow-tooling` delta spec 合法。
- [x] 3.3 更新 REQ-0040 trace 与 Workflow Sync 状态，保持 Change 追溯一致。
