## Context

REQ-0034 定义了 AI Token 使用量事实源：从本地 Codex session JSONL 派生 command run 明细与 Sprint 聚合快照，落在 `data/ai-usage/`，并禁止持久化原始 prompt、系统/developer 指令、本机绝对路径和工具输出正文。REQ-0035 已将 Sprint close / `/sprint-exps` 的 snapshot 检查、消费和 fallback 显式化纳入默认流程。

REQ-0037 的差异在于触发点：不再只等到 Sprint 收尾或复盘，而是在每个 `/req-*`、`/bug-*`、`/opsx-*`、`/sprint-*` 工作流命令完成后尝试构建或刷新 AI usage fact source。这样可以把命令级成本更早沉淀下来，尤其覆盖尚未纳入 Sprint 的 capture/generate/complete/review 阶段。

关联事实源：

- `issues/requirements/archive/REQ-0037-auto-token-fact-source-for-workflow-commands/requirement.md`
- `issues/requirements/archive/REQ-0037-auto-token-fact-source-for-workflow-commands/acceptance.md`
- `docs/knowledge-base/retrospectives/sprint-006-retrospective.md`：记录 AI usage snapshot 缺失导致 Token 分析只能 estimated fallback。

## Goals / Non-Goals

**Goals:**

- 建立统一 post-command AI usage hook，供所有命令技能引用。
- 在主命令和 Workflow Sync 成功后，自动尝试构建 command run 明细。
- 对可解析到 Sprint 的命令刷新 Sprint snapshot；无 Sprint 时不伪造 snapshot。
- 保持 hook 输出短摘要，清晰区分 `actual`、`estimated_fallback`、`unavailable`。
- hook 失败默认不阻断主命令，并给出 recommended action。
- 继承 REQ-0034 的脱敏、安全和上下文预算边界。

**Non-Goals:**

- 不改造 Codex Desktop 或模型 API 底层记录方式。
- 不提交原始 `~/.codex/sessions` JSONL。
- 不做精确费用、账单或额度核算。
- 不新增 Web / 管理端 / 小程序 UI。
- 不要求一次性回填所有历史会话。
- 不在本 Change 的 propose 阶段写 `src/` 或实现代码。

## Decisions

### D1. 使用统一 post-command hook，而不是在每个 skill 中复制提取逻辑

所有命令技能只声明调用时机、输入参数和输出要求。具体 session 输入发现、`extract-ai-usage` 调用、归因、脱敏、写入和摘要输出集中在一个脚本、函数或共享规则中。

备选方案：在每个 skill 的 Final Step 中复制 `extract-ai-usage.py` 调用和判断分支。该方案维护成本高，且容易出现脱敏边界和输出格式不一致，因此不采用。

### D2. hook 在 Workflow Sync 成功后运行

工作流命令的状态事实源仍由 trace、registry、Sprint 派生块和 Workflow Sync 负责。usage hook 应在 Workflow Sync 成功后读取更稳定的 workflow event、REQ/BUG/Change/Sprint 关联信息，减少错误归因。

备选方案：让 Workflow Sync 直接构建 Token 事实源。该方案会把状态同步职责和本地 session 处理职责混在一起，并增加敏感 session 内容进入通用 sync 流程的风险，因此不采用。

### D3. 无 Sprint 归属时只写 command run，不伪造 Sprint snapshot

`/req-capture`、`/req-generate`、`/bug-capture` 等早期命令可能尚未进入 Sprint。此时 hook 应通过 `requirements[]` 或 `bugs[]` 归因 command run，但不得创建虚假的 `data/ai-usage/sprints/<sprint-id>.json`。

备选方案：使用临时 Sprint 或 `sprint-auto` 聚合。该方案会污染 Sprint 事实源，不符合 sprint.yaml 的正式范围边界。

### D4. 失败默认 warning，不阻断主命令

本地 session 文件可能无法定位，或者当前环境无法访问 `~/.codex/sessions`。这些问题不应让 `/req-review`、`/bug-complete`、`/opsx-propose` 等主流程失败。hook 必须输出 `unavailable` 或 `estimated_fallback`、reason 和 recommended action。

备选方案：所有 hook 失败均阻断命令。该方案会让本地 session 可用性变成工作流硬依赖，影响需求/缺陷主流程推进。

### D5. 输出摘要优先，详细事实落文件

命令成功路径只输出 status、usage_mode、command_run_count、snapshot path/skipped、warning_count 和 recommended_action。详细 command run 和 snapshot 内容保存在 `data/ai-usage/`，由 Fact Sheet 或脚本检查读取。

备选方案：每个命令都打印完整 command run 或 snapshot。该方案会显著增加上下文成本，也更容易泄露敏感内容。

## Risks / Trade-offs

- 当前 session 自动定位不稳定 -> 支持显式参数、环境变量、本地配置和 recommended action fallback。
- 每个命令都运行 hook 可能增加耗时 -> 先 check，再增量构建；成功路径摘要化。
- 重复提取导致重复累计 -> 使用 session hash、turn hash 或 command run id 做幂等。
- 敏感上下文泄露风险 -> 只持久化数字指标、工作流 ID、hash、时间和 warning；不保存 prompt、系统指令、本机路径或工具输出正文。
- scope 归因不唯一 -> 支持多值关联和 attribution confidence，低置信度保留 warning。

## Migration Plan

1. 设计并实现统一 AI usage post-command hook，封装现有 `extract-ai-usage.py` 能力。
2. 增加 hook check/dry-run/recommended-action 模式，并定义短摘要输出结构。
3. 更新命令技能或共享规则，使 `/req-*`、`/bug-*`、`/opsx-*`、`/sprint-*` 在主流程和 Workflow Sync 成功后引用 hook。
4. 更新 `data/ai-usage/README.md` 和必要规则，说明自动构建触发场景、提交边界和失败降级。
5. 补充测试覆盖成功、缺 session、无 Sprint、snapshot stale、coverage missing、敏感内容跳过和重复提取幂等。
6. 通过 Workflow Sync 和 OpenSpec 校验确认 REQ、Change、spec、tasks 追溯一致。

## Open Questions

- 当前 Codex session 文件能否由本地环境稳定发现，还是第一版必须要求用户提供路径或配置环境变量？
- 统一 hook 应作为独立脚本、`scripts/ai_usage.py` 子命令，还是由 workflow command wrapper 调用？
- 对探索类命令 `/req-explore`、`/bug-explore`、`/opsx-explore` 是否默认写 command run，还是只在 session 输入显式可用时写入？
