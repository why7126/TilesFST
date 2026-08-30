---
title: AI Usage session 默认发现设计
created_at: 2026-08-30 08:50:35
updated_at: 2026-08-30 08:50:35
---

# AI Usage session 默认发现设计

## 现状

`scripts/ai_usage.py` 已按 `AI_USAGE_SESSIONS_DIR` 或 `~/.codex/sessions` 扫描最近 session JSONL，并结合 workflow event、Sprint、REQ、BUG 和 Change 关键词进行候选匹配。技能文档仍保留“优先显式 `--session-jsonl`”和“本地 session input 不可用”表述，容易让执行者跳过自动发现能力。

## 设计决策

- 默认发现顺序调整为：显式 `--session-jsonl`、`AI_USAGE_SESSION_JSONL`、`CODEX_SESSION_JSONL`、`AI_USAGE_SESSIONS_DIR`、`~/.codex/sessions/**/*.jsonl` 自动匹配。
- 技能输出说明从“缺本地 session 输入”改为“自动发现失败、候选不含 token_count 或需要历史回溯时再显式指定 session”。
- recommended_action 应优先提醒检查默认 sessions 目录和环境覆盖变量，再提示使用 `--session-jsonl` 指定单个文件。
- 成功路径只输出 compact hook summary，不输出具体本机绝对路径、原始 session 内容或完整 snapshot。

## 验证

- 运行 AI Usage dry-run hook，确认未显式传 `--session-jsonl` 时仍可从默认 session 目录得到 actual command run。
- 运行 AI Usage 相关聚焦测试。
- 运行上下文预算、OpenSpec 语言、目录结构和目标 Change 校验。
