---
req_id: REQ-0037-auto-token-fact-source-for-workflow-commands
status: done
created_at: 2026-07-12 09:52:06
updated_at: 2026-07-15 13:14:09
recorded_by: product
source: 用户输入
priority_hint: P1
parent_requirement: REQ-0034-ai-token-usage-observability
captured_via: capture
classification_rationale: 用户要求新增每个 /req-*、/bug-*、/opsx-*、/sprint-* 命令自动构建 Token 事实源，属于尚未交付的 Agent 工作流自动化能力增强，不是既有行为偏差。
---

# 一句话

每个 `/req-*`、`/bug-*`、`/opsx-*`、`/sprint-*` 工作流命令执行时，应自动构建或刷新对应的 AI Token 使用量事实源，减少手工运行 `extract-ai-usage` 的遗漏。

# 原始描述

新增 每个 /req-*、/bug-*、/opsx-*、/sprint-* 命令也会自动构建 Token 事实源

# 背景与关联

- 父需求：`REQ-0034-ai-token-usage-observability`
- 相关已交付能力：`data/ai-usage/`、`scripts/extract-ai-usage.py`、`scripts/generate-sprint-fact-sheet.py`
- 涉及命令族：`/req-*`、`/bug-*`、`/opsx-*`、`/sprint-*`
- 业务价值：让 AI Token 使用量事实源随工作流命令自然生成，避免 Sprint close / exps 前才发现 snapshot 缺失或过期。
- 预期后续：需要明确自动构建触发点、本地 session 输入来源、失败降级策略、安全脱敏边界与对每个命令技能的改造范围。

# 待澄清

- [ ] 自动构建是在每个命令结束后执行，还是在 Workflow Sync 成功后执行。
- [ ] 本地 Codex session JSONL 路径如何发现：由用户提供、环境变量配置、默认扫描 `~/.codex/sessions`，还是仅记录 recommended action。
- [ ] 命令执行中无法读取本地 session 或 snapshot 生成失败时，是否只写 warning，不阻断主命令。
- [ ] 是否所有命令族都必须写 command run 明细，还是仅在可归因到 REQ/BUG/Change/Sprint 时写 Sprint 聚合快照。
- [ ] `/req-capture`、`/bug-capture` 等尚未纳入 Sprint 的命令如何归属 snapshot：只写 command-runs，还是按 Issue 聚合。
- [ ] 自动构建是否需要新增脚本包装器，避免每个 skill 重复粘贴 `extract-ai-usage` 逻辑。
- [ ] 是否需要扩展 `workflow-sync` 或新增独立 post-command hook，而不是让 Workflow Sync 直接承担 Token 事实源职责。
- [ ] 是否需要更新 `rules/agent-context-budget.md`、`data/ai-usage/README.md` 和所有命令技能的 Final Step。

# 探索结论

（/req-explore 后人工确认写入）

# 分类说明（/capture）

该条目描述的是 AI 工作流命令自动生成 Token 使用量事实源的新能力，当前已知事实源构建仍以显式 `extract-ai-usage` 或 Sprint close gate 条件触发为主，因此判定为 REQ。
