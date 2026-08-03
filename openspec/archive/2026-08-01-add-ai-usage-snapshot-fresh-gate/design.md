## Context

当前 AI usage 事实源已经具备三段能力：`scripts/extract-ai-usage.py` 从本地 session 提取脱敏 command run 与 Sprint 聚合快照，`scripts/ai_usage.py::check_sprint_snapshot()` 检查 snapshot 状态，`scripts/generate-sprint-fact-sheet.py` 将检查结果暴露给 `/sprint-exps`。但 `/sprint-exps` 的默认行为仍允许在 snapshot 缺失、过期、覆盖不足或缺少 `usage_matrices` 时输出 `estimated_fallback`，这会让 Sprint 复盘无法量化真实成本。

约束：
- 不持久化原始 session JSONL、prompt、系统/开发者指令、工具输出全文、本机绝对路径或密钥。
- 不引入业务 API、数据库、Web、小程序或 Docker 行为变化。
- 遵守 `rules/agent-context-budget.md`，复盘默认使用 Fact Sheet summary，不读取大范围原始证据。

## Goals / Non-Goals

**Goals:**
- 在 `/sprint-exps` 默认生成真实 token 成本分析前，强制校验 Sprint AI usage snapshot freshness。
- 将通过条件定义为 `snapshot_status=present`、`usage_mode=actual`、`usage_matrices` 非空、关键 totals 非空、当前 Sprint scope coverage 全部通过。
- 失败时输出 compact blocker 和 recommended action，优先引导刷新 snapshot。
- 保留显式 fallback 路径，但让它成为人工选择的估算复盘，而不是默认成本量化结果。
- 用 pytest 覆盖 snapshot gate 的通过和阻断路径。

**Non-Goals:**
- 不改变 AI usage session 解析模型或 token 聚合口径。
- 不新增远程上传、外部监控或第三方成本系统。
- 不修改产品使用行为日志、业务数据库 schema、API 或 Orval 生成物。
- 不要求提交本地 `data/ai-usage` 明细或原始 session 文件。

## Decisions

1. 以 Fact Sheet summary 作为 `/sprint-exps` 默认门禁输入。
   - 原因：Fact Sheet 已聚合 sprint scope、warnings、AI usage snapshot 和 recommended action，符合上下文预算。
   - 替代方案：让 `/sprint-exps` 直接读取 `data/ai-usage/sprints/<sprint-id>.json`。该方案会重复 scope coverage 逻辑，也更容易让技能绕过统一摘要。

2. 在 `scripts/ai_usage.py` 中沉淀可复用的 fresh gate 判定。
   - 原因：`check_sprint_snapshot()` 已返回 snapshot 状态、coverage、totals、usage matrices 与 warnings；新增 gate 结果可避免多个调用方各自解释字段。
   - 替代方案：只改 `.agents/skills/sprint-exps/SKILL.md` 文案。该方案无法由测试稳定约束，后续容易回退到 fallback。

3. fresh gate 失败默认阻断真实成本分析，而不是自动 fallback。
   - 原因：用户目标是避免无法量化成本；默认 fallback 会把“缺少真实计量”变成复盘产物的一部分，掩盖需要补数的事实。
   - 替代方案：继续生成 fallback 并加 warning。该方案保留现状问题，只是文案更明确。

4. 显式 fallback 只用于非成本量化复盘。
   - 原因：有些历史 Sprint 可能无法获得 session 输入，需要允许经验复盘继续，但必须清楚标记“不能量化真实成本”。
   - 替代方案：完全禁止 fallback。该方案会阻断历史资料整理，不利于复盘流程。

## Risks / Trade-offs

- [Risk] 历史 Sprint 缺少 session 输入时 `/sprint-exps` 默认无法完成真实成本章节 → Mitigation: 输出刷新命令和显式 fallback 选项，并要求 fallback 不宣称真实成本分析完成。
- [Risk] coverage 判定过严导致 snapshot 虽有 token 数据但被标记 stale → Mitigation: recommended action 指向重新提取并覆盖当前 sprint scope，测试覆盖 scope mismatch。
- [Risk] 技能文档与脚本门禁口径漂移 → Mitigation: 将核心判定放入脚本测试，技能只消费 compact gate result。
- [Risk] snapshot 路径或 warnings 泄露本机路径 → Mitigation: Fact Sheet summary 继续输出仓库相对路径，hook 和 gate 输出保持 compact，不打印原始 session 路径。

## Migration Plan

1. 实现 snapshot fresh gate 判定并在 Fact Sheet summary 中暴露 compact 结果。
2. 更新 `/sprint-exps` 技能：默认路径遇到 gate 失败时先输出 blocker、recommended action 和显式 fallback 文案，不生成真实成本矩阵。
3. 补充 pytest 覆盖 pass、missing、stale、coverage missing、usage matrices missing。
4. 运行相关测试与 OpenSpec 校验。

回滚策略：回退脚本 gate 和技能文档变更后，`/sprint-exps` 恢复基于 `estimated_fallback` 的现有行为；不涉及数据迁移。

## Open Questions

- 是否需要为 `/sprint-exps` 增加显式 CLI/命令参数表达 “允许 fallback”，还是仅通过用户自然语言确认即可。实现阶段应优先沿用当前技能交互方式，除非已有脚本入口需要参数化。
