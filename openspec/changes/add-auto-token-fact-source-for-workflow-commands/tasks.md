## 1. Hook 设计与脚本入口

- [x] 1.1 设计统一 AI usage post-command hook 的输入、输出、状态枚举和 failure fallback。
- [x] 1.2 复用或扩展 `scripts/extract-ai-usage.py` / `scripts/ai_usage.py`，提供 workflow event、REQ/BUG/Change/Sprint 归因参数。
- [x] 1.3 增加 check/dry-run/recommended-action 模式，支持 session 输入不可用时输出安全摘要。
- [x] 1.4 确保 hook 成功路径只输出 status、usage_mode、计数、snapshot path/skipped、warning_count 和 recommended_action。

## 2. Command Run 与 Snapshot 构建

- [x] 2.1 实现无 Sprint 归属时的 command run 明细写入或明确 skipped/unavailable 输出。
- [x] 2.2 实现有 Sprint 归属时刷新 `data/ai-usage/sprints/<sprint-id>.json` 的流程。
- [x] 2.3 增强覆盖范围、新鲜度、必要指标和 usage mode 校验，避免 stale/empty snapshot 被标记为 actual。
- [x] 2.4 增强重复提取幂等处理，避免同一 session 或 turn 重复累计。

## 3. Source Command 流程接入

- [x] 3.1 更新 `/req-*` source-command 技能或共享规则，在 Workflow Sync 成功后引用统一 hook。
- [x] 3.2 更新 `/bug-*` source-command 技能或共享规则，在 Workflow Sync 成功后引用统一 hook。
- [x] 3.3 更新 `/opsx-*` source-command 技能或共享规则，在 Workflow Sync 成功后引用统一 hook。
- [x] 3.4 更新 `/sprint-*` source-command 技能或共享规则，保持与 REQ-0035 的 Sprint snapshot gate 一致。
- [x] 3.5 确认探索类命令的策略：无状态变更时只记录 command run 或输出 recommended action，不强制改变工作流状态。

## 4. 文档与安全边界

- [x] 4.1 更新 `data/ai-usage/README.md`，说明工作流命令自动构建触发场景、输出路径、提交边界和 failure fallback。
- [x] 4.2 如新增环境变量、本地配置或 hook 参数，更新相应 README / `.env.example` / 规则说明。
- [x] 4.3 确认自动构建流程不持久化 prompt、系统/developer 指令、本机绝对路径、原始 session JSONL 或工具输出正文。
- [x] 4.4 更新 Change trace，记录 REQ-0037 条件通过项和 knowledge-base 复盘依据。

## 5. 测试与验证

- [x] 5.1 增加 AI usage hook 测试，覆盖成功生成 command run、无 Sprint 归属和 Sprint snapshot 刷新。
- [x] 5.2 增加 failure fallback 测试，覆盖 session 缺失、JSONL 解析失败、缺少 token_count、coverage missing 和 stale snapshot。
- [x] 5.3 增加脱敏测试，确认不持久化本机绝对路径、原始 prompt、系统/developer 指令、密钥或工具输出正文。
- [x] 5.4 增加幂等测试，确认重复提取同一 session/turn 不重复累计。
- [x] 5.5 运行相关测试、Workflow Sync 和 OpenSpec 校验，并记录命令与结果。
