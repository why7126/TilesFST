## 背景

`/spec-study` 学习和应用跨项目 Harness 经验时，当前容易同时生成一份 `study` 学习报告和一份 `governance` 治理日志。两份文档都描述同一批学习采纳内容，形成重复。`docs/spec-logs/` 应保持可检索、低噪声和一事一档，同一次 `/spec-study` 流程只需要一份正式 `study` 报告。

## 变更内容

- 约束 `/spec-study` 在同一次学习/应用流程中只生成一份 `YYYYMMDDhhmmss-study-xxx.md` 正式学习报告。
- `/spec-study` 触发的治理资产应用结果必须汇总到同一份 `study` 报告，不得额外生成内容重复的 `YYYYMMDDhhmmss-governance-xxx.md`。
- 学习阶段候选内容可在最终回复、active Change 文档或同一学习报告的阶段章节中承载，不得另起第二份 `study` 报告。
- 若发现同一学习对象和主题已有本次流程的 `study` 报告，必须更新该报告而不是创建新报告。
- 同步 `/spec-study`、`docs/spec-logs/README.md`、`rules/agent-context-budget.md` 与正式规格 delta。
- 生成本次 `/spec-opt` 治理迭代日志。

## 能力

### 新增能力

- 无。

### 修改能力

- `agent-workflow-tooling`：补充 `/spec-study` 学习报告单份落盘，以及禁止同一流程同时生成重复 `study` 和 `governance` 日志的规则。

## 影响

- 影响 `.agents/skills/spec-study/SKILL.md`、`docs/spec-logs/README.md`、`rules/agent-context-budget.md`、`docs/spec-logs/20260807112249-governance-spec-study-single-report.md` 与本 Change 文档。
- 不影响后端 API、数据库、Web、小程序、管理端业务实现。
- 不需要 Orval。
- 不需要 Docker Compose 验证。
