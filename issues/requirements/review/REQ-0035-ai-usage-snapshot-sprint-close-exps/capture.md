---
req_id: REQ-0035-ai-usage-snapshot-sprint-close-exps
status: captured
created_at: 2026-07-11 23:36:05
updated_at: 2026-07-11 23:36:05
recorded_by: product
source: 用户反馈
priority_hint: P1
parent_requirement: REQ-0034-ai-token-usage-observability
---

# 一句话

将 AI usage snapshot 生成纳入 Sprint close / exps 默认流程，避免后续 Sprint 复盘继续使用 estimated fallback。

# 原始描述

将 AI usage snapshot 生成纳入 Sprint close / exps 默认流程，避免继续 estimated fallback。

# 待澄清

- [ ] `Sprint close` 对应现有命令边界是 `/sprint-archive`、`/opsx-archive` 收尾，还是需要新增独立 close 阶段。
- [ ] AI usage snapshot 生成失败时，流程应阻断、降级为显式 warning，还是允许人工确认后继续。
- [ ] `sprint-exps` 是否必须优先读取 snapshot 事实源，并在缺失时输出明确缺口清单而非静默 estimated fallback。
- [ ] snapshot 文件命名、存放路径和覆盖策略是否沿用 REQ-0034 已落地的 token usage fact sheet 规则。
- [ ] 是否需要在 Sprint acceptance / release-note 中记录 snapshot 生成状态，便于归档门禁追踪。

# 探索结论

（/req-explore 后人工确认写入）
