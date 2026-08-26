## 背景

当前 `.agents/skills/*/SKILL.md` 已普遍包含命令最终输出契约，但契约以尖括号占位模板和通用示例表达，容易在命令最终回复中被原样输出；部分命令族的旧 Output 示例还会同时在【下一步】和【待用户决策/处理】中描述同一动作，造成用户需要再次判断到底是可执行命令、人工确认还是阻塞项。

本 Change 将命令最终输出契约从“可复制模板”优化为“判定规则 + 命令族专属正反例 + 脚本校验”，降低重复、占位符泄漏和规范语气泄漏风险。

## 变更内容

- 将 `.agents/skills/*/SKILL.md` 的 Final Output Contract 改为禁止原样输出尖括号占位符、通用 BUG 示例和 MUST/SHOULD 规范句。
- 补强 `/sprint-propose`、`/req-opsx`、`/bug-opsx`、`/upgrade-plan`、`/upgrade-validate` 的命令族专属正反例，明确三态输出：有唯一下一步、被用户决策阻塞、有下一步且存在额外人工事项。
- 更新 `AGENTS.md`、`rules/agent-context-budget.md` 和 `docs/README.md` 的摘要契约，保持事实唯一归属。
- 扩展 `scripts/validate-agent-context-budget.py`，检查技能文件是否残留可被原样输出的占位模板、通用 BUG 示例、重复诱因和规范语气泄漏风险。
- 写入治理迭代日志，并维护 `docs/spec-logs/CHANGELOG.md`。

## 能力范围

### 新增能力

- 无。

### 修改能力

- `agent-workflow-tooling`: 强化命令最终输出契约，要求命令技能用真实可执行命令、明确的“暂无可推进下一步”和去重后的用户处理事项收尾；禁止最终回复暴露规范模板、占位符、MUST/SHOULD 规则文本或与当前命令无关的通用示例。

## 影响

- 技能：影响 `.agents/skills/*/SKILL.md` 的最终输出契约段落和部分命令族 Output 示例。
- 规则入口：影响 `AGENTS.md`、`rules/agent-context-budget.md`、`docs/README.md` 的命令输出摘要。
- 校验脚本：影响 `scripts/validate-agent-context-budget.py`。
- OpenSpec / Sprint：本 Change 为纯治理 Change，已纳入 `sprint-026`。
- API / DB / Orval：不影响业务 API、Pydantic Schema、SQLite/MySQL schema、OpenAPI 或 Orval。
- Web / 小程序 / 管理端：不修改业务运行时代码。
