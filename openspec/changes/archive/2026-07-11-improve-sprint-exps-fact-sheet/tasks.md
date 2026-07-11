## 1. Fact Sheet 生成脚本

- [x] 1.1 新增 `scripts/generate-sprint-fact-sheet.py`，支持 `--sprint <sprint-id>` 并通过现有 Sprint lifecycle 规则解析 `iterations/change|archive/<sprint-id>/`。
- [x] 1.2 复用或抽取 `scripts/workflow_sync/collect.py` 的只读收集逻辑，汇总 Sprint、REQ、BUG、Change、archive 路径、trace 状态与 tasks 计数。
- [x] 1.3 生成 Markdown Fact Sheet，包含 Sprint 基础信息、Scope 汇总、Change tasks 表、Issue 状态表、验收摘要、token 风险与 evidence hints。
- [x] 1.4 支持 `--json` 输出机器可读结构，字段至少包含 `sprint`、`scope`、`changes`、`issues`、`warnings`、`token_risks`、`evidence_hints`。
- [x] 1.5 对 Sprint 不存在、缺少 `sprint.yaml` 或关键字段无法解析的情况返回非零退出码，并输出明确错误。

## 2. `/sprint-exps` 流程更新

- [x] 2.1 更新 `.agents/skills/source-command-sprint-exps/SKILL.md`，要求先运行或读取 Sprint Fact Sheet，再进入复盘分析。
- [x] 2.2 将原“读 sprint 四件套、全部 REQ/BUG/Change trace 与 tasks”改为“优先读 Fact Sheet，按 warning / evidence hints 分段回读原文”。
- [x] 2.3 在技能中补充 Fact Sheet 输出边界：不得复制原始 trace、tasks、acceptance report 或 generated 文件全文。
- [x] 2.4 保留“模型 Token 使用分析”要求，并要求优先使用 Fact Sheet 的 token 风险与回读建议。

## 3. 验证与质量门禁

- [x] 3.1 使用 `sprint-005` 验证 Markdown 输出覆盖 Sprint 005 复盘 A-004 所需事实。
- [x] 3.2 使用 `sprint-005` 验证 JSON 输出结构稳定且可解析。
- [x] 3.3 验证不存在 Sprint 的错误路径，确认命令返回非零并输出明确错误。
- [x] 3.4 运行 `openspec validate improve-sprint-exps-fact-sheet --strict`。
- [x] 3.5 运行 `python scripts/validate-agent-context-budget.py`，确认技能预算入口仍符合规则。
