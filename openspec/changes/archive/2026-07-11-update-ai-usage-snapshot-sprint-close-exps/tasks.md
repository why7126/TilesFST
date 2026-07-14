## 1. Snapshot 检查与生成入口

- [x] 1.1 设计并实现 Sprint AI usage snapshot 状态检查函数，返回 `present`、`missing`、`stale`、`failed`、`coverage`、`usage_mode`、`generated_at` 和 warnings。
- [x] 1.2 复用或扩展 REQ-0034 的 AI usage 事实源生成逻辑，为 `data/ai-usage/sprints/<sprint-id>.json` 提供生成或刷新入口。
- [x] 1.3 为 snapshot 新鲜度和覆盖范围增加校验：Sprint ID、生成时间、scope 覆盖、关键指标非空。

## 2. Sprint close / exps 流程接入

- [x] 2.1 更新 `/sprint-archive` 技能或对应脚本，在归档前检查或尝试生成 AI usage snapshot，并输出摘要报告。
- [x] 2.2 更新 `/sprint-exps` 技能或对应脚本，优先读取可用 snapshot，缺失、过期或失败时显式输出 `estimated_fallback`。
- [x] 2.3 确保成功路径只输出摘要，失败路径保留可执行 recommended action。

## 3. 文档与安全边界

- [x] 3.1 更新 `data/README.md` 或相关 AI usage 文档，说明 Sprint snapshot 文件的提交边界、脱敏规则和本地 session 输入边界。
- [x] 3.2 确认 snapshot 生成流程不持久化 prompt、系统指令、developer 指令、本机绝对路径、session JSONL 或工具输出全文。
- [x] 3.3 在 Change trace 或验收记录中引用 `docs/knowledge-base/retrospectives/sprint-006-retrospective.md` 的 A-001 行动项。

## 4. 测试与验证

- [x] 4.1 增加脚本级测试，覆盖 snapshot present、missing、stale、failed。
- [x] 4.2 增加 `/sprint-exps` 或 fact sheet 测试，验证 `actual` 与 `estimated_fallback` 输出口径。
- [x] 4.3 增加脱敏测试，确保 snapshot 不包含本机绝对路径、原始 session、prompt 或工具输出全文。
- [x] 4.4 运行相关测试，并记录命令与结果。
