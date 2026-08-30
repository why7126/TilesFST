---
title: 将本地 Codex sessions 设为 AI Usage 默认发现规范
created_at: 2026-08-30 08:50:35
updated_at: 2026-08-30 08:50:35
---

# 将本地 Codex sessions 设为 AI Usage 默认发现规范

## 背景

当前 AI Usage post-command hook 已支持从本地 Codex session JSONL 提取脱敏 command run 与 Sprint 聚合快照，但部分技能输出仍倾向提示用户显式传入 `--session-jsonl`。这会让常规 workflow 命令在实际存在 `~/.codex/sessions` 时仍被描述为“无法做成本分析”，降低 Sprint 归档和复盘的可操作性。

## 变更

- 将 `~/.codex/sessions/**/*.jsonl` 明确为 AI Usage 默认 session 发现目录，并允许通过 `AI_USAGE_SESSIONS_DIR` 覆盖。
- 统一 `workflow-sync`、`sprint-archive`、`sprint-exps` 等技能的 AI Usage 输出口径：先自动发现本地 session，再在失败、缺 token_count 或历史回溯时要求显式 `--session-jsonl`。
- 优化 AI Usage hook 的 recommended_action，避免成功路径默认暗示必须手工提供 session 文件。
- 补充 OpenSpec delta、治理日志和变更历史总账。

## 非目标

- 不修改业务 `src/` 代码。
- 不持久化原始 session JSONL、prompt、系统指令、developer 指令或工具输出正文。
- 不改变 AI Usage 的脱敏、安全跳过和 Sprint fresh gate 判定标准。

## 影响

本次变更影响治理规范、命令技能和 AI Usage 脚本提示文案。API、数据库、Web、小程序、管理端业务行为、Orval 和 Docker Compose 均不受影响。
