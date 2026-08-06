---
sprint_id: sprint-021
status: published
created_at: 2026-08-06 09:01:00
updated_at: 2026-08-06 17:16:00
---

# Sprint 021 Release Note

## 计划发布内容

- 修复 Sprint Fact Sheet AI usage freshness baseline 对未来计划 `sprint.yaml:start_date` 的误判。
- 完整且真实的 Sprint AI usage snapshot 不再仅因未来计划开始时间降级为 `estimated_fallback`。
- 保留四件套 `updated_at` 等真实事实更新时间对陈旧 snapshot 的保护。
- 增强 Sprint Scope 与目标编号列表一致性校验，避免 `sprint.md` 人读目标遗漏正式范围项。
- 补齐 OpenSpec CLI stdout 中 proposal scaffold warning 的归档成功输出过滤缺口。

## 不包含

- 不调整 AI usage snapshot 文件结构。
- 不修改 `/sprint-exps` 的矩阵展示格式。
- 不改动 `sprint-020` 的事实源日期。
- 不涉及 API、数据库、Web、小程序、管理端或 Docker Compose。

## 发布状态

```yaml
publish_status: published
published_at: 2026-08-06 17:16:00
related_requirements:
  - REQ-0102-sprint-goal-scope-consistency-validation
related_changes:
  - fix-fact-sheet-ai-usage-start-date-freshness
related_bugs:
  - BUG-0118-fact-sheet-ai-usage-future-start-date-freshness
  - BUG-0123-openspec-archive-proposal-warning-stdout
```
