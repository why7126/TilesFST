## 1. 状态扫描与闭环判定

- [x] 1.1 梳理 `scripts/sync-workflow-status.py` 中 Issue 子文档状态扫描、archive promote blocker 与闭环状态判定逻辑。
- [x] 1.2 抽取或复用 Markdown frontmatter 与 fenced YAML block 的 `status` 字段定位结果，确保报告包含文件路径、状态来源、旧值与 Issue id。
- [x] 1.3 定义 REQ/BUG 子文档目标闭环状态映射，确保只从已闭环的主 Issue、关联 Change 与必要 Sprint 状态推导。

## 2. Reconcile 命令能力

- [x] 2.1 为 workflow sync 或配套脚本增加 Issue 子文档状态 reconcile dry-run 参数，输出将修改的文件、字段、旧状态、新状态与 `updated_at`。
- [x] 2.2 增加显式写入参数，在闭环前置条件满足时同步 frontmatter 与 fenced YAML block 状态，并刷新被修改 Markdown 的 `updated_at`。
- [x] 2.3 在闭环前置条件不满足时拒绝写入并返回非零退出码，报告缺失条件与应先执行的上游工作流命令。

## 3. 报告与技能指引

- [x] 3.1 增强 archive promote / workflow sync blocker 报告，输出可直接复制执行的 dry-run reconcile 命令与实际写入命令。
- [x] 3.2 更新 `.agents/skills/workflow-sync/SKILL.md`，说明 Issue 子文档 residual status 的 reconcile 使用方式与禁止绕过流程推进的约束。
- [x] 3.3 按需更新相关 source-command 技能中归档或同步失败后的处理建议，避免要求手工批量修改状态。

## 4. 测试与校验

- [x] 4.1 增加单元测试覆盖 REQ/BUG 子文档 frontmatter 残留状态、fenced YAML block 残留状态与双写字段同步。
- [x] 4.2 增加测试覆盖 dry-run 不写入、写入刷新 `updated_at`、未闭环 Issue 拒绝写入和报告命令输出。
- [x] 4.3 运行相关 pytest 与 OpenSpec 校验，确认 `agent-workflow-tooling` delta spec 可通过验证。

## 归档验证摘要

- 验证时间：2026-07-11 23:53:33
- 验证命令与结果：
  - `openspec validate reconcile-issue-residual-status --strict`：通过。
  - `uv run pytest tests/test_issue_status_residuals.py tests/test_sprint_archive_readiness.py`：15 passed。
  - `openspec archive reconcile-issue-residual-status -y`：已合并 `agent-workflow-tooling` 1 个 modified requirement，并归档 Change。
  - `python scripts/sync-workflow-status.py --event opsx.archive --change reconcile-issue-residual-status --sprint auto`：退出码 0，Sprint skipped（非 sprint scope）。
  - `python scripts/promote-issues-for-archive.py --change reconcile-issue-residual-status --reason "/opsx-archive reconcile-issue-residual-status"`：退出码 0，无 Issue eligible for promotion。
- 验收结论：通过。Issue 子文档 residual status reconcile 能力已实现，归档阻断报告可输出 dry-run 与写入修复命令。
- 关联 Issue / Sprint 状态：无直接 REQ/BUG 来源；未纳入 Sprint scope。
- 归档路径：`openspec/changes/archive/2026-07-11-reconcile-issue-residual-status/`。
