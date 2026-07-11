# Design: Issue 子文档状态一致性归档门禁

## 问题分析

当前归档链路分为三层：

1. `sync-workflow-status.py` 同步主 `trace.md`、registry 与 Sprint 派生文档。
2. `promote-issues-for-archive.py` 根据 trace 状态和关联 Change 状态判断 issue 是否可迁入 `archive/`。
3. `promote-issue-stage.py` 执行 `review/` → `archive/` 目录迁移，并更新 `trace.md` 的 `lifecycle_stage`。

缺口在于：这些步骤不检查 issue 包内其他 Markdown 子文档的 frontmatter / YAML block `status`。因此主状态已闭环时，子文档仍可残留非闭环状态。

## 方案

### 1. 统一扫描函数

新增或抽取共享扫描能力，例如：

```text
scripts/workflow_sync/issue_status_residuals.py
```

扫描输入为单个 issue 目录，输出 residual 列表：

```yaml
- issue_id: BUG-0062-...
  file: issues/bugs/review/BUG-.../bug.md
  source: frontmatter | yaml_block
  status: draft
```

扫描规则：

- 仅扫描待归档 issue 目录内的 Markdown 文件。
- 读取 frontmatter 中的 `status`。
- 读取第一个 fenced `yaml` block 中的 `status`。
- 对无 `status` 字段的文件忽略。
- 对 `done`、`archived`、`resolved`、`closed` 等闭环状态放行。
- 对 `draft`、`pending_review`、`in_sprint`、`applied`、`todo`、`open` 等状态阻断。

### 2. promote 门禁

在 `promote-issues-for-archive.py` 对候选 issue 执行 `review/` → `archive/` 前调用扫描函数：

- 若存在 residual，候选不得进入 promote。
- 命令返回非零退出码。
- 报告输出 issue id、文件路径、状态来源、状态值、建议处理方式。

### 3. readiness / 技能说明

更新归档技能说明：

- `/opsx-archive` 在 workflow-sync 后、promote 前必须执行子文档状态门禁。
- `/sprint-archive` 队列中任一待归档 issue 存在 residual 时，整个 Sprint close 阶段不得完成。

### 4. 测试

新增 pytest 覆盖：

- BUG 子文档 frontmatter residual 阻断。
- REQ 子文档 fenced YAML block residual 阻断。
- 无 residual 时 promote 成功。
- 报告包含具体路径与状态值。

## 兼容性

- 不修改业务 API、数据库或前端代码。
- 不直接清理历史 archive 包。
- 既有 `generate-sprint-fact-sheet.py` 可继续保留 warning 行为；若抽取共享扫描函数，应复用同一状态集合，避免两套规则漂移。

## 测试策略

- 使用 pytest 构造临时 issue 包和 registry / trace 片段。
- 对 promote 脚本执行 CLI 级测试，断言返回码和输出。
- 保留现有 workflow-sync / sprint archive readiness 测试。
- 运行 OpenSpec 校验。
