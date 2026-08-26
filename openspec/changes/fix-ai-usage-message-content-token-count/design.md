---
change_id: fix-ai-usage-message-content-token-count
source_bug: BUG-0141-ai-usage-token-count-jsonl
sprint: sprint-026
created_at: 2026-08-25 15:28:00
updated_at: 2026-08-25 18:18:35
---

# 设计

## 根因摘要

`scripts/ai_usage.py` 的 `user_text()` 依赖 `safe_text()` 从字符串型 `text`、`content`、`message`、`cmd`、`command` 字段提取用户输入。新版 Codex session JSONL 将用户输入放在 `payload.content` 列表内，例如文本片段对象的 `text` 字段。

当 `safe_text()` 遇到列表时返回空字符串，`parse_session_jsonl()` 无法创建当前 command run。随后出现的 `payload.type=token_count` 事件虽然可被 `event_type()` 与 `is_token_event()` 识别，但因 `current is None` 被跳过，无法累计到 command run 或 Sprint snapshot。

## 修复方案

1. 扩展文本提取逻辑，支持从 `payload.content` 列表中提取文本片段。
2. 仅提取结构化文本片段中的必要 command 文本，继续依赖既有脱敏与 snapshot 写入边界，避免把原始 session JSONL 复制入仓库。
3. 保持 token_count 解析逻辑兼容：
   - `payload.type=token_count`
   - `payload.info.last_token_usage`
   - 现有旧格式 token 事件
4. 当新版用户消息成功建立 command run 后，后续 token_count 事件必须归属到该 command run，并累计 `model_call_count` 与 token totals。
5. 在 Sprint Usage Matrix 增加列级观测状态：
   - 已有 command run 覆盖的 workflow 列为 `observed`，单元格可显示真实数值，真实数值为 0 时保留 `0`。
   - 当前 snapshot 没有任何 command run 覆盖的 workflow 列为 `unknown`，Markdown 渲染层显示 `-`，表示未采集或未归因。
6. post-command hook 的目标 run 选择保持原上下文评分规则；仅在同等评分候选中，优先选择 `total_tokens`、`model_call_count` 或输入/输出 token 非零的 run。
7. `sprint-025` 回溯刷新只写入脱敏后的 AI usage 聚合 JSON 与复盘说明，不提交原始 session JSONL 或本机绝对路径。
8. Sprint snapshot 聚合在命中判定后，将 REQ/BUG/Change 覆盖与矩阵对象行裁剪到 `sprint.yaml` 正式 scope；与 Sprint Change 相关但未纳入当前 Sprint 的历史 issue 不进入当前 Sprint 复盘矩阵。

## 回归测试设计

- 在 `tests/test_ai_usage.py` 增加脱敏最小 JSONL fixture：
  - 用户消息：`payload.type=message`、`payload.role=user`、`payload.content=[{"type":"text","text":"..."}]`
  - token 事件：`payload.type=token_count`、`payload.info.last_token_usage`
- 断言生成 1 条 command run。
- 断言 workflow event、BUG/Change/Sprint 归因正确。
- 断言 `model_call_count` 与 token totals 正确累计。
- 断言不产生 `token-count-missing`。
- 断言 Sprint Usage Matrix 能标记未观测 workflow 列为 `unknown`。
- 断言渲染后的矩阵对未观测列输出 `-`，对已观测但数值为 0 的列继续输出 `0`。
- 断言 post-command hook 在同等上下文匹配分数下优先选择非零 token run。
- 断言 Sprint snapshot 不会把相关历史 REQ/BUG 扩展为当前 Sprint 矩阵行。

## 安全边界

- 测试 fixture 只能使用脱敏、手写、最小数据。
- 不提交原始 `~/.codex/sessions`、prompt 原文、系统或开发者指令、工具输出正文、本机绝对路径、Cookie、Authorization header、`.env` 内容或密钥。
- 输出 snapshot 继续遵守既有 `AI 命令使用量事实源` 与 `AI 使用量安全边界` 要求。

## 验收方式

- 聚焦运行 `python -m pytest tests/test_ai_usage.py`。
- 使用 post-command hook 生成本次命令 usage 摘要。
- 若本机 session 可用，重新检查目标 Sprint snapshot，确认从 estimated fallback 恢复为 actual 或具备可定位的非空指标。
- 重新渲染 `sprint-025` 复盘 Token 区，确认大量未归因阶段不再显示为普通 `0`。
- 扫描 `~/.codex/sessions` 回溯补齐 `sprint-025` lifecycle token 归因，确认矩阵覆盖正式 Sprint scope 内 REQ/BUG/Change。
- 按验收反馈复核 `sprint-025` 复盘矩阵，确认未观测阶段展示为 `-`，不再显示长文本 `unknown`。
