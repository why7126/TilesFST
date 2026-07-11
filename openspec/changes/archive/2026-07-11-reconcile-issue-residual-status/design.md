## Context

`agent-workflow-tooling` 已有 Issue 归档子文档状态一致性门禁：当 REQ/BUG 包内 Markdown 子文档仍含非闭环 `status` 时，archive promote 会阻断并报告残留字段。实际使用中，阻断报告能发现问题，但修复仍需要人工逐文件同步 frontmatter 与 fenced YAML block，尤其在 Sprint 归档前批量处理多个 Issue 时容易反复失败。

本变更面向本地工作流脚本与 Skill 指引，不改变业务 API、数据库、Web、小程序或权限模型。

## Goals / Non-Goals

**Goals:**

- 在发现子文档残留状态时，输出可直接复制执行的精确修复命令。
- 提供自动 reconcile 能力，在主 Issue 与关联 Change 已闭环时同步子文档残留状态。
- 默认 dry-run，实际写入时展示修改摘要并刷新 Markdown `updated_at`。
- 保持归档门禁安全：未闭环 Issue 不允许通过 reconcile 被强制改成闭环状态。

**Non-Goals:**

- 不新增对外 HTTP API。
- 不改变 REQ/BUG 状态机、Sprint 状态机或 OpenSpec 归档规则。
- 不批量推断未评审需求或未验收 BUG 的最终状态。
- 不修改 Orval、前端页面或数据库 schema。

## Decisions

1. 复用 workflow sync 作为主入口，并允许脚本级显式 reconcile 参数。

   方案：在 `scripts/sync-workflow-status.py` 增加面向 Issue 子文档状态的 reconcile 模式，或提供同目录下的专用修复脚本，并由 workflow sync 报告输出明确命令。

   理由：状态同步事实源已经集中在 workflow sync，新增能力应贴近现有状态解析、trace 更新和 registry 更新逻辑，避免出现第二套状态判断。

   备选：只增强错误文案，不做自动写入。该方案实现更小，但无法减少批量手工修改成本，不能满足本变更目标。

2. reconcile 采用 dry-run first。

   方案：命令默认或推荐先 dry-run，报告 issue id、文件路径、字段来源、旧值、新值；实际写入需显式参数确认。

   理由：该能力会修改多个 Markdown 子文档，dry-run 可以让归档前批量处理保持可审计，并降低误改未完成文档的风险。

3. 闭环状态必须来自主状态与关联对象事实。

   方案：只有当 Issue `trace.md`、关联 Change 状态、必要 Sprint 状态满足既有归档闭环条件时，reconcile 才能把残留状态写为闭环状态；否则输出 blocker 与下一步命令建议。

   理由：reconcile 是一致性修复，不是流程推进命令。它不能替代 `/req-review`、`/bug-review`、`/opsx-archive` 或 `/sprint-archive`。

4. 修复命令必须足够具体。

   方案：门禁报告中给出包含 `--req` 或 `--bug`、`--event`、`--sprint auto`、`--dry-run` / 写入参数的命令，并指出目标 Issue 当前不满足闭环时应运行的上游命令。

   理由：让用户不需要再理解内部字段分布，也能按报告完成修复。

## Risks / Trade-offs

- [Risk] 自动写入误改尚未完成的子文档状态 → Mitigation: 只在主 Issue 与关联 Change 已闭环时允许写入；未闭环时只报告 blocker。
- [Risk] Markdown frontmatter 与 fenced YAML block 格式差异导致解析不完整 → Mitigation: 复用既有扫描逻辑并补充覆盖 frontmatter、fenced YAML、无 frontmatter 子文档的测试。
- [Risk] 报告命令与实际 CLI 参数漂移 → Mitigation: 将报告输出纳入测试断言，并在 workflow-sync Skill 中同步命令示例。
- [Risk] 批量修复输出过长 → Mitigation: 成功路径输出聚合摘要和路径清单，失败时仅展开 blocker 与必要字段明细，遵守上下文预算规则。
