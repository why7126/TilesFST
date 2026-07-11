# Proposal: 修复归档后 issue 子文档状态一致性检查缺失

## 背景

`BUG-0062-archive-issue-subdoc-status-consistency` 发现，`/opsx-archive` 或 `/sprint-archive` 完成后，REQ / BUG 可以迁入 `issues/**/archive/`，主 `trace.md` 与 registry 显示 `done` / `archive`，但同一 issue 包内的 `bug.md`、`requirement.md`、`acceptance.md`、`root-cause.md`、`workaround.md`、`user-stories.md`、`business-flow.md` 等子文档仍可能保留 `draft`、`pending_review`、`in_sprint`、`applied` 等非闭环状态。

当前 `scripts/generate-sprint-fact-sheet.py` 已能识别类似 residual status，但该能力只作为复盘 warning，不参与归档阻断。归档门禁仍主要依赖 `trace.md` 状态、关联 Change 状态和 tasks 完成度。

## 目标

- 为 issue archive promote / 归档 readiness 增加 issue 子文档状态一致性门禁。
- 统一扫描 REQ / BUG 子文档 frontmatter 与 fenced YAML block 中的 `status` 字段。
- 将 `draft`、`pending_review`、`in_sprint`、`applied`、`todo`、`open` 等非闭环状态作为归档 blocker。
- 阻断报告必须包含 issue id、文件路径、状态值和处理建议。
- 补充测试覆盖 BUG / REQ、frontmatter / YAML block、阻断与通过路径。

## 非目标

- 不直接批量改写历史 `issues/**/archive/` 包的残留状态。
- 不修改业务 API、数据库 schema、Web、小程序或管理端业务 UI。
- 不改变 OpenSpec CLI 的 archive 语义。
- 不调整 Sprint 复盘 Fact Sheet 的输出格式，除非为了复用扫描逻辑所需。

## 修复范围

- `scripts/promote-issues-for-archive.py` 或其调用链中的归档门禁。
- 必要时抽取共享 issue 子文档状态扫描工具，供 promote/readiness/fact sheet 复用。
- `.agents/skills/source-command-opsx-archive/SKILL.md` 与 `.agents/skills/source-command-sprint-archive/SKILL.md` 的归档步骤说明。
- 对应 pytest 测试。

## Rollback Plan

若归档门禁误阻断：

1. 回退本 Change 引入的扫描/阻断逻辑与测试。
2. 保留历史 issue 包不做批量修改。
3. 恢复 `/opsx-archive` 与 `/sprint-archive` 仅按 trace / Change / tasks 门禁运行。
4. 重新运行 `python scripts/sync-workflow-status.py --sprint auto --check` 验证派生文档未漂移。

## 风险与缓解

- 风险：历史 archive 包中残留状态较多，严格门禁可能影响再次归档或补归档流程。
  - 缓解：门禁只针对待迁入 archive 的候选 issue 包；历史清理另行评审。
- 风险：部分子文档的 `status` 字段表达文档自身状态，而非 issue 主状态。
  - 缓解：明确 archive 包内子文档不允许保留非闭环状态；报告具体文件，由人工确认修正。
- 风险：扫描范围过宽造成上下文或执行成本增加。
  - 缓解：只扫描待归档 issue 包内 Markdown，不扫描全量 `issues/**`。
