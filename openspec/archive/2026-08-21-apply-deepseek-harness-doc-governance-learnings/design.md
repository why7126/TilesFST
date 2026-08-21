## 设计说明

本次应用不复制 deepseek-harness 的 `.agents/notes/` 树、Cordis/plugin 架构或 Node 测试体系，只吸收治理原则，并适配到本项目已有 `rules/`、`docs/standards/`、`docs/knowledge-base/`、`.agents/skills/` 和 `scripts/`。

## 采纳策略

### 文档事实唯一归属

- 在 `rules/document-governance.md` 补充“一个事实一个归属”规则。
- `AGENTS.md` 保持入口摘要；详细规则归属到 `rules/`、`docs/standards/` 或具体 Skill。
- 重复内容不在本次批量清理，先建立后续变更的判断标准。

### 治理决策记录轻量化

- 不新增 `.agents/notes/`，避免扩展 AI 工具入口。
- 在 `docs/spec-logs/` 学习报告和治理日志中明确决策字段：已采纳原因、未采纳原因、替代方案、验证责任和后续触发条件。
- OpenSpec Change 的 `design.md` 也记录关键取舍，归档后由 spec-log 承载长期事实。

### 文档 slop / CoT 泄漏审计

- 新增 `docs/standards/document-prose-hygiene.md`，定义长期文档禁止的会话推理残留、临时草稿引用、review 对话、不可解析内部引用和不必要历史叙事。
- 新增 `scripts/validate-doc-prose-hygiene.py`，提供轻量可复核扫描；默认聚焦 `docs/`、`rules/`、`AGENTS.md` 和 `.agents/skills/`，排除 `docs/spec-logs/` 历史记录、archive、generated 和依赖目录。

### 最小相关验证选择规则

- 更新 `docs/standards/command-execution-order.md`：先看 diff scope，再选择最小相关验证；不要因为提交或归档重复跑已通过且未受影响的检查。
- 保留本项目 OpenSpec / Sprint / Workflow Sync MUST 校验，不以最小相关为由跳过强制门禁。

### 防御性模式知识库模板

- 新增 `docs/knowledge-base/best-practices/defensive-pattern-template.md`，用于沉淀缺陷类别、预防规则和验证方式。
- 与 `rules/root-cause-evidence.md` 互补：root-cause 记录单个问题证据，defensive pattern 沉淀可复用预防规则。

## 边界

- 不修改业务 `src/`。
- 不引入 `.agents/notes/`、`.claude/` 或其他新工具入口。
- 不迁移 deepseek-harness 的插件架构、Node 测试体系或文档双语流程。
- 文档卫生脚本只做启发式扫描，发现项需要人工判断；脚本不自动改文档。
