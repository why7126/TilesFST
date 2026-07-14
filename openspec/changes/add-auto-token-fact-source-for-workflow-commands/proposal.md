## Why

REQ-0034 已建立 AI Token 使用量事实源，REQ-0035 已把 Sprint close / `/sprint-exps` 纳入 snapshot 检查，但普通 `/req-*`、`/bug-*`、`/opsx-*`、`/sprint-*` 命令执行后仍不会自动构建事实源。REQ-0037 需要把 usage fact source 构建前移到每个工作流命令的后置步骤，减少事后补跑遗漏，并让早期 REQ/BUG 命令成本也可追溯。

## What Changes

- 为 `/req-*`、`/bug-*`、`/opsx-*`、`/sprint-*` 工作流命令增加统一 AI usage fact source 后置 hook 要求。
- 规定 hook 在主命令与 Workflow Sync 成功后运行；主命令或 Sync 失败时可跳过并说明原因。
- 要求统一 hook 复用 REQ-0034 的 `data/ai-usage/` 事实源、脱敏边界、Token 聚合口径和 snapshot 校验规则。
- 支持无 Sprint 归属的 REQ/BUG 命令仅生成 command run 明细；有 Sprint 归属时刷新 Sprint 聚合快照。
- 明确 hook 失败默认不阻断主命令，必须输出 `actual`、`estimated_fallback` 或 `unavailable` 口径、reason 和 recommended action。
- 要求 source-command skill 只引用统一 hook 或共享规则，不复制复杂解析逻辑。

## Capabilities

### New Capabilities

无。

### Modified Capabilities

- `agent-workflow-tooling`: 增强工作流命令后置 AI usage fact source 自动构建、统一 hook、失败降级、command run / Sprint snapshot 写入和安全输出要求。

## Impact

- 影响脚本：需要新增或扩展 `scripts/` 中的 AI usage post-command hook、session 输入发现、check/dry-run 和摘要输出。
- 影响项目技能：`.agents/skills/source-command-req-*`、`source-command-bug-*`、`source-command-opsx-*`、`source-command-sprint-*` 需要引用统一后置步骤或共享规则。
- 影响文档：`data/ai-usage/README.md`、`data/README.md`、必要时 `rules/agent-context-budget.md` 或工作流规则需要说明自动构建触发场景与安全边界。
- 影响测试：需要覆盖 command run 生成、无 Sprint 归属、Sprint snapshot 刷新、session 缺失、snapshot stale、coverage missing、敏感内容跳过和重复提取幂等。
- 不影响产品 API、数据库表结构、Web UI、小程序、MinIO 上传链路和 Orval。
