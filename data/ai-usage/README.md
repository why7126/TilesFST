---
purpose: AI 使用量事实源说明
content: 定义 Codex session 派生用量事实的输入、输出、命名、留存和脱敏边界
source: REQ-0034 / add-ai-token-usage-observability
update_method: AI 使用量提取字段、输出目录或脱敏规则变化时同步更新
created_at: 2026-07-11 18:51:16
updated_at: 2026-07-11 18:51:16
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

## 允许持久化字段

- 数字指标：模型调用、input/cached/output/reasoning/total tokens、工具调用、工具输出字符数、失败重跑次数。
- 工作流 ID：REQ、BUG、OpenSpec Change、Sprint、workflow event。
- 来源摘要：session hash、turn hash、时间范围、源行号范围。
- 短安全标签与 warning。

## 禁止持久化内容

- 原始 prompt、系统指令、developer 指令、技能全文。
- 本机绝对路径、`.env` 内容、密钥、Cookie、Authorization、Token。
- 真实客户数据、手机号、门店资料。
- 工具输出正文、测试日志全文、OpenAPI/Orval 生成物 diff 全文。

当安全性不确定时，默认不写入文本，只写数字指标或 redaction warning。

## Retention

原始输入和中间文件保留在本机，由操作者按需清理。Sprint 聚合快照可随复盘保留；command run 明细在提交前必须确认不包含敏感文本。
