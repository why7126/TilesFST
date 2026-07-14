---
purpose: AI 使用量事实源说明
content: 定义 Codex session 派生用量事实的输入、输出、命名、自动构建触发、留存和脱敏边界
source: REQ-0034 / add-ai-token-usage-observability；REQ-0037 / add-auto-token-fact-source-for-workflow-commands
update_method: AI 使用量提取字段、输出目录或脱敏规则变化时同步更新
created_at: 2026-07-11 18:51:16
updated_at: 2026-07-12 10:35:00
---

# AI 使用量事实源

`data/ai-usage/` 用于保存从本地 Codex session JSONL 派生的脱敏 AI command run 使用量事实。原始 `~/.codex/sessions/**/*.jsonl` 只作为本机输入，禁止复制进仓库。

## 目录

```text
data/ai-usage/
├── README.md
├── command-runs/        # 脱敏 command run 明细；提交前必须人工确认安全
├── sprints/             # Sprint 聚合快照，供 Fact Sheet 和 /sprint-exps 读取
├── samples/             # 可提交的脱敏样例
├── raw/                 # 本地原始或近原始输入，gitignore
└── local/               # 本地临时中间文件，gitignore
```

## 文件命名

- Command run 明细：`command-runs/<session-hash-prefix>.json`
- Sprint 快照：`sprints/<sprint-id>.json`
- 手工映射：建议放 `local/<sprint-id>-manual-map.json`

## 工作流命令自动构建

`/req-*`、`/bug-*`、`/opsx-*`、`/sprint-*` source-command 技能在主命令成功且 Workflow Sync 成功后，应调用统一 post-command hook：

```bash
python scripts/extract-ai-usage.py \
  --post-command-hook \
  --workflow-event <event> \
  [--req <REQ-id>] \
  [--bug <BUG-id>] \
  [--change <change-id>] \
  [--sprint <sprint-id>] \
  [--session-jsonl <local-session.jsonl>] \
  --json
```

Hook 输入优先级：

1. 显式 `--session-jsonl <local-session.jsonl>`。
2. 环境变量 `AI_USAGE_SESSION_JSONL`。
3. 环境变量 `CODEX_SESSION_JSONL`。

这些环境变量只用于本机脚本定位 Codex session 输入，不属于应用运行时配置；不得写入 `.env.example` 或提交真实本机路径。

输出策略：

- 有 session 且解析成功：写入 `command-runs/`；若提供 `--sprint sprint-xxx`，刷新 `sprints/<sprint-id>.json`。
- 无 Sprint 归属：只写 command run 或输出无法写入原因，Sprint snapshot 必须标记 `skipped`。
- 无 session、session 不存在、解析失败或缺少 `token_count`：输出 `usage_mode: unavailable` 或 `estimated_fallback`、warning 和 recommended action；普通工作流命令不因此失败。
- `--dry-run` 只输出摘要，不写事实源文件，适合探索类命令或诊断。

成功路径只输出短摘要：`status`、`usage_mode`、`command_run_count`、`sprint_snapshot`、`warning_count`、`recommended_action`。

## 允许持久化字段

- 数字指标：模型调用、input/cached/output/reasoning/total tokens、工具调用、工具输出字符数、失败重跑次数。
- 工作流 ID：REQ、BUG、OpenSpec Change、Sprint、workflow event。
- 来源摘要：session hash、turn hash、时间范围、源行号范围。
- Snapshot 元数据：`generated_at`、`coverage`、`snapshot_status` 派生判断所需的安全字段。
- 短安全标签与 warning。

## 禁止持久化内容

- 原始 prompt、系统指令、developer 指令、技能全文。
- 本机绝对路径、`.env` 内容、密钥、Cookie、Authorization、Token。
- 真实客户数据、手机号、门店资料。
- 工具输出正文、测试日志全文、OpenAPI/Orval 生成物 diff 全文。

当安全性不确定时，默认不写入文本，只写数字指标或 redaction warning。

## Retention

原始输入和中间文件保留在本机，由操作者按需清理。Sprint 聚合快照可随复盘保留；command run 明细在提交前必须确认不包含敏感文本。

## Sprint Snapshot 校验

默认路径为 `data/ai-usage/sprints/<sprint-id>.json`。`/sprint-archive` 与 `/sprint-exps` 读取前应通过 Fact Sheet 或脚本检查：

```bash
python scripts/generate-sprint-fact-sheet.py --sprint <sprint-id> --json
python scripts/extract-ai-usage.py --check-snapshot --sprint <sprint-id> --json
```

可用 snapshot 需要满足：

- `snapshot_status: present`
- `ai_usage_mode: actual`
- `sprint_id` 与目标 Sprint 一致
- `generated_at` 不早于 Sprint 最近关键收尾时间
- `coverage` 覆盖 Sprint scope 中的主要 REQ/BUG/Change
- `totals` 中 command run、模型调用、工具调用和 token 指标不为空

缺失、过期、解析失败、覆盖不足或指标为空时，消费方必须输出 `ai_usage_mode: estimated_fallback`、原因和 recommended action；不得静默把估算结果当作真实 token 统计。
