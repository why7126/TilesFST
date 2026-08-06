---
created_at: 2026-08-04 23:30:00
updated_at: 2026-08-04 23:58:00
---

# 设计：Sprint AI usage snapshot 新鲜度下限

## 根因

`build_fact_sheet()` 当前传入：

```text
min_generated_at = project_time_to_utc_iso(sprint_yaml.end_date or sprint_yaml.start_date)
```

这把计划结束时间当成“事实最后更新时间”。当 Sprint 因提前归档而 `end_date` 仍为未来计划值时，真实 snapshot 会被判 stale，`usage_mode` 降级为 `estimated_fallback`，`sprint-exps` 因 fresh gate blocker 不输出矩阵。

## 方案

新增 `ai_usage_min_generated_at()`：

- 读取 `sprint.yaml` 的 `start_date`。
- 仅当 `end_date` 不晚于当前时间时才纳入 freshness baseline。
- 读取 Sprint 四件套 Markdown frontmatter 中的 `updated_at`。
- 取可解析时间中的最大值作为 `min_generated_at`。
- 返回调试摘要 `ai_usage_freshness_baseline`，包含 baseline、来源路径/字段、跳过的未来 `end_date`。

新增 Fact Sheet retrospective-ready Markdown 输出：

- 增加 `--ai-usage-markdown` CLI 参数。
- 直接输出 `## 模型 Token 使用分析`、`Token Usage Fact Sheet` 与四张矩阵表。
- 表格结构对齐历史 `sprint-015-retrospective.md`，避免 `/sprint-exps` 在执行时临场把 JSON 矩阵转换为 Markdown。
- fields 模式继续保留，作为调试或兼容 fallback 使用。

## 行为变化

- 已归档 Sprint 且计划 `end_date` 在未来：fresh gate 使用四件套实际更新时间，不再误判 stale。
- 未归档或正常历史 Sprint：若 snapshot 早于最新四件套更新时间，仍判 stale。
- Snapshot 缺 coverage、totals 或 matrices 时，仍按既有 blocker 处理。

## 风险与缓解

| 风险 | 缓解 |
|------|------|
| 未来 end_date 被忽略后过旧 snapshot 误通过 | 四件套 `updated_at` 继续作为事实更新时间；Workflow Sync 和 sprint-exps 会刷新相关文档 |
| Markdown frontmatter 缺失 updated_at | 回退到 `start_date` 和非未来 `end_date`，并保留 baseline summary 便于诊断 |
| 复盘文档输出矩阵过长 | 技能要求只在 fresh gate pass 后调用 `--ai-usage-markdown`；summary 仍保持 compact |

## 测试

- 单元测试覆盖未来 `end_date` 不导致 actual snapshot stale。
- 单元测试覆盖 `--ai-usage-markdown` 输出 sprint-015 风格表格章节。
- 既有 stale snapshot 测试保留，保证真实过期仍阻断。
- 运行聚焦 pytest：`tests/test_generate_sprint_fact_sheet.py`、`tests/test_ai_usage.py`。
