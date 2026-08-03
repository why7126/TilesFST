## 1. Workflow Sync 子文档状态模型

- [x] 1.1 梳理 REQ/BUG 顶层 Markdown 子文档类型、状态字段来源和可安全同步规则。
- [x] 1.2 实现子文档状态扫描器，输出文件路径、字段来源、当前值、目标值、分类和安全性。
- [x] 1.3 实现常规状态传播 patcher，覆盖 `requirement.md`、`bug.md`、`acceptance.md`、`review.md`、`root-cause.md`、`workaround.md` 等顶层文档。
- [x] 1.4 区分常规状态同步与闭环 residual reconcile，禁止未闭环 Issue 通过 reconcile 写入。

## 2. 验收结果回填

- [x] 2.1 设计并实现 `acceptance.md` 验收结果块或等价字段结构。
- [x] 2.2 在 `opsx.apply` 后支持记录待验收状态和来源 Change。
- [x] 2.3 在 `opsx.archive` / `sprint.archive` 后支持记录验收结论、证据、失败项、来源 Change/Sprint。
- [x] 2.4 支持失败、部分通过和豁免场景，默认只输出 follow-up capture 文案，不自动创建 Issue。

## 3. Drift Check 与历史治理

- [x] 3.1 扩展 `sync-workflow-status.py --check` 或新增等价命令，检查 trace、registry、目录阶段、子文档状态和验收结果。
- [x] 3.2 为历史 archive 漂移提供 scan / classify / dry-run / apply / check 流程。
- [x] 3.3 apply 仅写入 dry-run 标记为可安全同步的项，并刷新 Markdown `updated_at`。
- [x] 3.4 将 issue archive promote residual gate 改为复用或兼容新的扫描分类结果。

## 4. Sprint Close 与输出契约

- [x] 4.1 在 Sprint close / `/sprint-archive` 前增加中间态 stale scan，覆盖 Issue 包和 Sprint 四件套。
- [x] 4.2 Workflow Sync 摘要输出增加子文档检查数、更新数、验收结果状态、drift warning 数量。
- [x] 4.3 详细输出模式保留逐文件诊断，摘要模式不展开大正文。
- [x] 4.4 确保扫描范围由目标 Issue/Sprint scope 定位，不默认扫描整个 archive、generated 或无关历史目录。

## 5. 规则、Skill 与测试

- [x] 5.1 更新 `rules/document-governance.md`、`rules/requirement-management.md`、`rules/bug-management.md`、`rules/issues-lifecycle.md` 中的状态同步和验收回填规则。
- [x] 5.2 更新 `.agents/skills/workflow-sync/SKILL.md` 和相关 req/bug/opsx/sprint 命令 Skill 的 Final Step 说明。
- [x] 5.3 增加 focused pytest，覆盖 REQ/BUG 常规同步、验收回填、drift check、历史 dry-run/apply、archive promote 阻断和摘要输出。
- [x] 5.4 更新或新增测试 fixture，确保 workflow snapshot / archive path / Issue 子文档状态契约兼容 active 与 archive 路径。
- [x] 5.5 运行相关 workflow sync、目录结构和 pytest 校验，记录验证摘要。
