---
change_id: fix-ai-usage-message-content-token-count
source_bug: BUG-0141-ai-usage-token-count-jsonl
sprint: sprint-026
created_at: 2026-08-25 15:28:00
updated_at: 2026-08-25 18:18:35
---

# 任务

- [x] 更新 `scripts/ai_usage.py`，支持从新版 `payload.content` 文本片段列表提取用户命令文本。
- [x] 确认新版用户消息建立 command run 后，后续 `payload.type=token_count` 可归属并累计 `payload.info.last_token_usage`。
- [x] 在 `tests/test_ai_usage.py` 增加脱敏最小 JSONL 回归测试，覆盖新版 message content 列表与 token_count 归属。
- [x] 运行 `python -m pytest tests/test_ai_usage.py`。
- [x] 运行 AI usage post-command hook，记录本次修复命令的 compact usage 摘要。
- [x] 检查目标 Sprint snapshot，确认不再因 `required-metrics-empty` 失败。
- [x] 评估是否需要在 `docs/knowledge-base/incidents/` 沉淀 AI usage extractor 兼容性事故复盘；若无新增可复用经验，记录不沉淀原因。
- [x] 增强 Sprint AI Usage 矩阵，支持未观测 workflow 列标记为 `unknown` 并在 Markdown 中渲染为 `-`。
- [x] 优化 post-command hook 目标 run 选择，同分候选优先真实 token/model 指标。
- [x] 补充 `tests/test_ai_usage.py` 与 Fact Sheet 渲染聚焦测试。
- [x] 回溯刷新 `sprint-025` AI usage snapshot，并更新 `sprint-025` 复盘 Token 说明。
- [x] 扫描 `~/.codex/sessions`，按 `sprint-025` 时间窗、REQ/BUG/Change scope 与命令阶段补齐 lifecycle token 归因。
- [x] 收紧 Sprint snapshot 聚合对象范围，避免相关历史 REQ/BUG 扩展进当前 Sprint 矩阵。
- [x] 运行聚焦验证、OpenSpec 校验、目录结构校验、文档表达卫生校验与 AI Usage hook。

## 验收返修记录

| 时间 | 反馈 | 调整 | 验证 |
|---|---|---|---|
| 2026-08-25 18:18:35 | AI Usage 矩阵未观测阶段不应显示长文本 `unknown`，应显示 `-` | 保留数据层 `status=unknown`，将 Fact Sheet Markdown 渲染层与复盘说明改为 `-` | `uv run pytest tests/test_ai_usage.py tests/test_generate_sprint_fact_sheet.py` 61 passed；Fact Sheet Markdown 渲染为 `-` |
