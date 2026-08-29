---
change_id: fix-ai-usage-message-content-token-count
source_bug: BUG-0141-ai-usage-token-count-jsonl
sprint: sprint-026
created_at: 2026-08-25 15:28:00
updated_at: 2026-08-25 18:18:35
---

# 修复 AI usage 新版 JSONL 用户消息、token_count 归属与矩阵 0/未观测语义

## 背景

`BUG-0141-ai-usage-token-count-jsonl` 已确认：新版 Codex session JSONL 中用户消息使用 `payload.type=message`、`payload.role=user`，且 `payload.content` 为文本片段列表。当前 AI usage extractor 只从字符串字段读取用户输入，导致无法建立 command run 边界。后续 `payload.type=token_count` 虽已可识别，也因没有可归属的 command run 被跳过，最终造成 `sprint-025` snapshot 缺失。

该缺陷影响项目治理指标、Sprint 复盘和 AI 使用量事实源，不影响业务运行时。后续复核发现 `sprint-025` 复盘矩阵虽然已恢复总 token，但大量未归因阶段被渲染为 `0`，容易被误读为这些命令阶段实际没有消耗；同时 post-command hook 在同一 workflow/sprint 有多个候选 run 时，需要优先选择带真实 token 指标的目标 run。

## 变更内容

- 增强 `scripts/ai_usage.py` 的用户消息文本提取能力，支持新版 `payload.content` 文本片段列表。
- 保持 `payload.type=token_count` 与 `payload.info.last_token_usage` 的既有解析路径，并确保 token_count 可归属到新版用户消息建立的 command run。
- 增加脱敏最小 JSONL 回归测试，覆盖新版用户消息列表结构与 token_count 累计。
- 修复后重新生成或检查目标 Sprint snapshot，确保不再因 required metrics 为空失败。
- 增强 Sprint AI Usage 矩阵语义，区分已观测的 `0` 与未采集/未归因状态；数据层列状态保留 `unknown`，复盘 Markdown 展示为 `-`。
- 优化 post-command hook 目标 run 选择，在同等上下文匹配分数下优先选择带模型/token 指标的 run，避免误选零 token turn。
- 回溯刷新 `sprint-025` AI usage snapshot，并修订 `sprint-025` 复盘 Token 说明，避免把未归因阶段误读为实际零消耗。

## 能力范围

### 修改能力

- `agent-workflow-tooling`：增强 AI usage extractor 对新版 Codex session JSONL 的兼容性。

### 非目标

- 不读取或提交原始 `~/.codex/sessions` 文件。
- 不改变业务 API、数据库模型、Web、小程序或管理端功能。
- 不提交或持久化原始 session JSONL。
- 不改业务 `src/`、后端 API、数据库、Web、小程序或管理端功能。
- 不重构 AI usage snapshot 的整体数据模型；本次仅增加矩阵列状态与渲染语义。

## 回滚计划

- 若修复引入解析误归属，可回退本 Change 对 `scripts/ai_usage.py` 与 `tests/test_ai_usage.py` 的修改。
- 回退后删除或重新生成受影响 Sprint 的 AI usage snapshot，避免保留错误统计。
- 回退不涉及数据库 migration、Orval 或 Docker Compose 配置。

## 验证计划

- 运行 `python -m pytest tests/test_ai_usage.py`。
- 运行 `python scripts/extract-ai-usage.py --post-command-hook --workflow-event bug.opsx --bug BUG-0141-ai-usage-token-count-jsonl --change fix-ai-usage-message-content-token-count --json`。
- 对目标 Sprint 执行 snapshot 检查，确认 `snapshot_status`、`usage_mode`、`model_call_count` 与 token totals 符合验收标准。
- 运行 `python scripts/generate-sprint-fact-sheet.py --sprint sprint-025 --ai-usage-markdown`，确认未观测阶段渲染为 `-`。
- 运行 `python scripts/validate-doc-prose-hygiene.py` 聚焦检查本次更新的长期文档。

## 影响

- API：不影响。
- 数据库：不影响。
- Web：不影响。
- 小程序：不影响。
- 管理端：不影响。
- Orval：不需要。
- Docker Compose：不需要。
- 测试：需要补充 `tests/test_ai_usage.py` 聚焦回归测试。
