---
requirement_id: REQ-0035-ai-usage-snapshot-sprint-close-exps
title: AI usage snapshot 纳入 Sprint close / exps 默认流程 - 验收标准
status: done
created_at: 2026-07-11 23:46:16
updated_at: 2026-07-15 13:14:04
---

# 验收标准

## 功能 AC

- [ ] AC-001 Sprint close / archive 默认检查目标 Sprint 的 AI usage snapshot，并输出 `snapshot_status`、`snapshot_path`、`coverage`、`usage_mode`。
- [ ] AC-002 snapshot 缺失时，流程会尝试默认生成或输出明确的生成命令提示，不得静默跳过。
- [ ] AC-003 snapshot 生成失败时，命令输出必须标记失败原因和 recommended action，不得写出“真实统计已使用”的结论。
- [ ] AC-004 `/sprint-exps` 在 snapshot 可用时优先使用 `actual` 口径，并展示 command run、模型调用、工具调用、失败重跑和 token 汇总。
- [ ] AC-005 `/sprint-exps` 在 snapshot 不可用时允许估算 fallback，但必须显式输出 `ai_usage_mode: estimated_fallback`、原因和补救建议。
- [ ] AC-006 snapshot 新鲜度校验至少覆盖生成时间、Sprint ID、主要 REQ/BUG/Change 覆盖、必要指标是否为空。
- [ ] AC-007 过期或覆盖不足的 snapshot 必须标记为 `stale` 或 warning，不得作为完整真实统计使用。
- [ ] AC-008 Sprint close / archive 输出应包含 snapshot 状态摘要：状态、口径、生成时间、相对路径、warning 数量。
- [ ] AC-009 相关命令技能将 snapshot 生成或校验纳入默认步骤，至少覆盖 `/sprint-archive` 与 `/sprint-exps`。
- [ ] AC-010 snapshot 默认流程继承 REQ-0034 脱敏约束，不写入原始 prompt、系统指令、session JSONL、本机绝对路径、工具输出全文或敏感数据。

## 非功能 AC

- [ ] AC-NF-001 成功路径输出保持摘要化，不展开完整 session、trace、tasks 或工具日志。
- [ ] AC-NF-002 warning 必须可执行，包含缺失对象、影响范围和建议下一步。
- [ ] AC-NF-003 复盘 Markdown 必须清楚区分真实统计和估算 fallback，读者无需推断数据口径。
- [ ] AC-NF-004 生成或读取 snapshot 时遵守 `rules/agent-context-budget.md`，优先读取聚合文件和摘要。
- [ ] AC-NF-005 若无法访问本地 session 数据，流程仍可完成复盘，但必须保留明确的数据缺口说明。

## 横切 AC（knowledge-base）

无横切 AC。本需求为流程治理类需求，不涉及管理端列表、表单、弹窗或媒体上传 UI 场景；knowledge-base gate 为 N/A。
