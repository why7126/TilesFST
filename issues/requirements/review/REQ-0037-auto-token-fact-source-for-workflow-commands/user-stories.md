---
requirement_id: REQ-0037-auto-token-fact-source-for-workflow-commands
title: 工作流命令自动构建 AI Token 事实源 - 用户故事
status: pending_review
created_at: 2026-07-12 09:56:48
updated_at: 2026-07-12 09:56:48
---

# 用户故事

## US-001 工作流命令结束后自动沉淀用量事实

作为 AI / Codex Agent，我希望每个 `/req-*`、`/bug-*`、`/opsx-*`、`/sprint-*` 命令完成后自动触发 AI usage fact source hook，以便不用依赖人工事后记得运行 `scripts/extract-ai-usage.py`。

验收要点：

- 命令主流程和 Workflow Sync 成功后，触发统一 usage hook。
- hook 输出短摘要，不打印原始 session、prompt 或工具输出正文。
- hook 失败默认不阻断主命令，并输出 recommended action。

## US-002 尚未纳入 Sprint 的 REQ/BUG 也可记录 command run

作为项目负责人，我希望 `/req-capture`、`/req-generate`、`/bug-capture`、`/bug-complete` 等早期命令也沉淀 command run 明细，以便 Sprint 复盘能看到完整流程成本。

验收要点：

- 无 `sprint_id` 时不伪造 Sprint snapshot。
- 可归因到 REQ/BUG 的命令写入 `requirements[]` 或 `bugs[]`。
- 输出中明确 `sprint_snapshot: skipped` 或等价说明。

## US-003 有 Sprint 归属时自动刷新聚合快照

作为开发负责人，我希望当命令可关联到 `sprint-xxx` 时，系统自动刷新 `data/ai-usage/sprints/<sprint-id>.json`，以便 `/sprint-exps` 使用真实统计。

验收要点：

- snapshot 包含 `generated_at`、coverage、totals、warnings。
- coverage 能反映 Sprint scope 中 REQ/BUG/Change 覆盖情况。
- 覆盖不足、指标为空或过期时不得标记为完整 `actual`。

## US-004 统一 hook 降低技能维护成本

作为流程维护者，我希望所有 source-command skill 只引用统一 hook，不重复粘贴复杂解析逻辑，以便后续修改脱敏、归因或输出格式时只改一个入口。

验收要点：

- 存在统一脚本、函数或等价封装。
- 各 skill 只声明调用时机、输入参数和输出摘要要求。
- 自动构建逻辑的失败处理与安全边界集中维护。

## US-005 安全负责人可确认不会泄露本地会话内容

作为安全 / 治理负责人，我希望自动构建只保存脱敏统计和低风险元数据，以便 `~/.codex/sessions` 中的原始 prompt、系统/developer 指令、本机路径和工具输出不会进入仓库。

验收要点：

- 持久化内容不包含原始 prompt、系统/developer 指令、技能全文或工具输出正文。
- 本机绝对路径、`.env`、密钥、Cookie、Authorization、Token 和真实客户数据必须被拦截或跳过。
- 不确定是否安全的文本默认不写入事实源，只写 warning。

## US-006 复盘读者能区分真实统计与降级状态

作为复盘读者，我希望命令输出和 Sprint 复盘明确区分 `actual`、`estimated_fallback` 与 `unavailable`，以便不会把缺失数据误读为真实统计。

验收要点：

- hook 摘要包含 `usage_mode` 或等价字段。
- 失败或缺失时包含 reason 和 recommended action。
- `/sprint-exps` 不得在 snapshot 不可用时编造具体 Token 数字。
