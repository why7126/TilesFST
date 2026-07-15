---
purpose: AI 使用量事实源说明
content: 定义 Codex session 派生用量事实的输入、输出、命名、自动构建触发、留存和脱敏边界
source: REQ-0034 / add-ai-token-usage-observability；REQ-0037 / add-auto-token-fact-source-for-workflow-commands
update_method: AI 使用量提取字段、输出目录或脱敏规则变化时同步更新
created_at: 2026-07-11 18:51:16
updated_at: 2026-07-15 18:40:51
---

# AI 使用量事实源

`data/ai-usage/` 用于保存从本地 Codex session JSONL 派生的脱敏 AI command run 使用量事实。原始 `~/.codex/sessions/**/*.jsonl` 只作为本机输入，禁止复制进仓库。

## 目录

```text
data/ai-usage/
├── README.md
├── command-runs/        # 脱敏 command run 明细，按 issues / opsxs / sprints / releases 分组；提交前必须人工确认安全
├── sprints/             # Sprint 聚合快照，供 Fact Sheet 和 /sprint-exps 读取
├── samples/             # 可提交的脱敏样例
├── raw/                 # 本地原始或近原始输入，gitignore
└── local/               # 本地临时中间文件，gitignore
```

## 文件命名

- Command run 明细：`command-runs/<scope-type>/<scope>/<date>--<workflow-event|session>--<session-hash-prefix>.json`
- Sprint 快照：`sprints/<sprint-id>.json`
- Release 命令 artifact：`command-runs/releases/<version>/<workflow-event>.json`
- 手工映射：建议放 `local/<sprint-id>-manual-map.json`

命名示例：

```text
command-runs/issues/REQ-0038-brand-certificate-management/2026-07-15--opsx.apply--67fcbdffcff818b3.json
command-runs/issues/REQ-0038-brand-certificate-management/2026-07-14--session--95207864e3d25a49.json
command-runs/opsxs/standalone-change/2026-07-15--opsx.explore--abcd1234.json
command-runs/sprints/sprint-007/2026-07-15--sprint.archive--0aa983d782ae4684.json
command-runs/releases/v0.0.3/2026-07-15--release.prepare--4d44dd7ca82b97fd.json
command-runs/releases/v0.0.3/release.prepare.json
```

`scope` 目录规则：

- release 命令提供 `--release <version>` 时，command run 明细优先使用 `releases/<version>/`；即使同一命令同时传入 REQ / BUG / Change，也不得落入 `issues/` 或 `opsxs/`。
- 非 release 命令优先使用 `issues/<requirements[0]>` 的完整 canonical ID，例如 `issues/REQ-0038-brand-certificate-management`。
- 没有关联 REQ 但有关联 BUG 时，使用 `issues/<bugs[0]>` 的完整 canonical ID。
- 纯 OpenSpec Change 且无 REQ/BUG 时，使用 `opsxs/<change-id>/`。
- 仅有 Sprint 归属时，使用 `sprints/<sprint-id>/`。
- Release 命令 artifact 固定使用 `releases/<version>/<workflow-event>.json`，与 release command run 明细同位于 `command-runs/releases/<version>/` 下。
- 完全无法归属时，使用 `_unscoped/`。

当同一个 session 文件内有多条 workflow command run 时，文件名中的 `workflow-event` 使用 `session`，避免同一 session 被拆成多个明细文件；末尾 hash 仍用于稳定去重和合并。若同一 run 关联多个 REQ/BUG，文件落在排序后的第一个 issue scope 目录中，run 记录本身仍保留完整 `requirements` / `bugs` 数组，Sprint snapshot 以记录内容聚合覆盖所有关联项。

## 工作流命令自动构建

`/req-*`、`/bug-*`、`/opsx-*`、`/sprint-*` 命令技能在主命令成功且 Workflow Sync 成功后，应调用统一 post-command hook；`/release-*` 命令没有 Workflow Sync 事件，必须在发布计划、准备或确认步骤完成并记录结果后直接调用同一个 hook：

```bash
python scripts/extract-ai-usage.py \
  --post-command-hook \
  --workflow-event <event> \
  [--req <REQ-id>] \
  [--bug <BUG-id>] \
  [--change <change-id>] \
  [--sprint <sprint-id>] \
  [--release-sprint <sprint-id>] \
  [--release <version>] \
  [--session-jsonl <local-session.jsonl>] \
  --json
```

Release 命令事件名固定为：

```text
release.propose
release.prepare
release.publish
```

Hook 输入优先级：

1. 显式 `--session-jsonl <local-session.jsonl>`。
2. 环境变量 `AI_USAGE_SESSION_JSONL`。
3. 环境变量 `CODEX_SESSION_JSONL`。
4. 当以上均缺失且命令提供了 `--workflow-event`、`--req` / `--bug` / `--change` / `--sprint` 上下文时，hook 可在本机 `~/.codex/sessions/**/*.jsonl` 中按这些安全关键词自动定位最近候选 session。

这些环境变量与自动发现只用于本机脚本定位 Codex session 输入，不属于应用运行时配置；不得写入 `.env.example` 或提交真实本机路径。自动发现只输出 `session_input: auto` 等短状态，不输出本机 session 绝对路径。

历史回溯或补录已有 Sprint/REQ/BUG 的 AI usage 时，MUST 优先使用显式 `--session-jsonl` 与 `--manual-map`；不得依赖自动发现。原因是当前回溯会话本身也可能包含目标 REQ、BUG、Change 或 Sprint 关键词，自动发现会优先选择最近 session，造成把回溯命令误归因到历史 Sprint。若历史命令文本使用 `REQ 0035`、技能链接名或其他非标准写法，MUST 用 `turn_hash` 手工映射 `workflow_event`、完整 canonical REQ/BUG、Change 与 Sprint。

输出策略：

- 有 session 且解析成功：写入 `command-runs/<scope>/`；若提供 `--sprint sprint-xxx`，刷新 `sprints/<sprint-id>.json`。
- release 命令必须传 `--release <version>`，并写入 `command-runs/releases/<version>/<date>--<workflow-event>--<session-hash>.json` 明细与 `command-runs/releases/<version>/<workflow-event>.json` 版本 artifact；artifact 结构包含 `release_version`、`workflow_event`、`coverage`、`totals` 与脱敏 `command_runs`。
- release 命令若覆盖多个 Sprint，必须用可重复的 `--release-sprint <sprint-id>` 传入版本范围；`--sprint` 只表示要刷新某一个 Sprint snapshot，不得用重复 `--sprint` 表示 release 范围。
- 无 Sprint 归属：只写 command run 或输出无法写入原因，Sprint snapshot 必须标记 `skipped`。
- 无 session、session 不存在、解析失败或缺少 `token_count`：输出 `usage_mode: unavailable` 或 `estimated_fallback`、warning 和 recommended action；普通工作流命令不因此失败。
- 安全扫描发现单条 command run 含不允许持久化的文本时，hook MUST 跳过该条并输出 `unsafe-records-skipped:<count>`；若仍有安全记录，必须继续写入安全记录并刷新可用 snapshot。
- 若全部候选 command run 都因安全扫描被跳过，hook MUST 输出 `usage_mode: unavailable`、`no-safe-command-runs` 与 recommended action，不得抛异常中断父命令。
- 合法工作流 ID 中包含 `password`、`token` 等业务词时（例如修改密码缺陷或 Token fact source 需求），不得仅因词面命中而判为敏感；只有密钥、认证头、`.env`、本机绝对路径或赋值形态的敏感字段才应阻断持久化。
- `--dry-run` 只输出摘要，不写事实源文件，适合探索类命令或诊断。

成功路径只输出短摘要：`status`、`usage_mode`、`command_run_count`、`session_input`、`sprint_snapshot`、`warning_count`、`recommended_action`。

Release 命令成功路径还应输出 `release_artifact`，其 `path` 指向 `data/ai-usage/command-runs/releases/<version>/<workflow-event>.json`。若缺少 `--release`，hook 仍可写兼容 command run，但必须把 `release_artifact` 标记为 `skipped`，不得把 release 数据混同为某个 Sprint snapshot。Release artifact 的 `coverage.sprints` 来自 `--release-sprint`，并可合并命令文本中自动解析到的 Sprint。

## 允许持久化字段

- 数字指标：模型调用、input/cached/output/reasoning/total tokens、工具调用、工具输出字符数、失败重跑次数。
- 模型指标：`model_name`、`model_provider`、`service_tier`、`reasoning_effort`、`reasoning_summary`、`model_speed_tier`、`model_rate_limit_name`、`model_context_window`。
- 工作流 ID：REQ、BUG、OpenSpec Change、Sprint、workflow event。
- 来源摘要：session hash、来源 JSONL 文件、turn hash、时间范围、源行号范围。
- Snapshot 元数据：`generated_at`、`coverage`、`snapshot_status` 派生判断所需的安全字段。
- Release 元数据：`release_version`、`workflow_event`、版本范围 coverage 与聚合 totals。

`warnings` 只允许出现在命令运行摘要或 snapshot 校验结果中，用于提示缺 session、缺 token、覆盖不足、过期等诊断信息；不得持久化到 `command-runs/**/*.json` 或 `sprints/*.json`。

来源 JSONL 文件必须写为 home-relative 路径，例如 `~/.codex/sessions/2026/07/14/xxx.jsonl`；不得持久化 `/Users/<name>/...` 等本机绝对路径。Sprint snapshot 使用 `source_data_files` 汇总参与聚合的来源文件列表。

`model_speed_tier` 由脚本优先按 `model_name`，其次按 rate limit 名称归一生成，用于复盘阅读：`spark → ultra_fast`、`luna/mini → fast`、`terra → balanced`、`sol/gpt-5.5 → frontier`。原始可追溯字段仍保留在 `model_name` 与 `model_rate_limit_name`。

## 禁止持久化内容

- 原始 prompt、系统指令、developer 指令、技能全文。
- 本机绝对路径、`.env` 内容、密钥、Cookie、Authorization、Token。
- 真实客户数据、手机号、门店资料。
- 工具输出正文、测试日志全文、OpenAPI/Orval 生成物 diff 全文。

当安全性不确定时，默认不写入文本，只写数字指标或 redaction warning。

不要通过传入不存在的 `--session-jsonl` 来让 hook 返回成功。该方式只能用于诊断 `session-jsonl-not-found` 降级路径，不能作为已生成 AI usage 数据的证据。

## ID 规范化

- `requirements` 与 `bugs` 必须持久化 issue 目录名中的完整 canonical ID，例如 `REQ-0038-brand-certificate-management`。
- 不得同时持久化同一 issue 的短号与完整号，例如 `REQ-0038` 与 `REQ-0038-brand-certificate-management` 只能保留后者。
- 当短号能在 `issues/requirements/*/` 或 `issues/bugs/*/` 中唯一解析为完整目录名时，生成脚本必须自动提升为完整 ID；无法唯一解析时才保留原值。
- Sprint snapshot 的 `coverage.requirements` / `coverage.bugs` 必须使用同一规范，避免同一 issue 被重复统计。

## opsx 归因

- `opsx.*` command run 若包含 `changes`，且该 change 能从 `openspec/changes/<change-id>/trace.md`、`proposal.md`、`openspec/changes/archive/YYYY-MM-DD-<change-id>/trace.md`、归档 proposal 或 `issues/**/trace.md` 关联到 REQ/BUG，则 `requirements` 或 `bugs` 必须同步填写。
- 只有不经 REQ/BUG 创建的纯 OpenSpec change，才允许 `requirements` 与 `bugs` 同时为空。
- 生成脚本必须在写入 `command-runs/**/*.json` 和刷新 Sprint snapshot 前自动反查 change → issue 关系，避免 opsx 用量只归到 change 而丢失需求/缺陷覆盖。

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

`--min-generated-at` 传入时间 SHOULD 使用带时区 ISO-8601，例如 `2026-07-15T05:20:00Z`。若使用项目文档时间 `YYYY-MM-DD HH:mm:ss`，调用方 MUST 先确认脚本按 UTC 解释还是按 `Asia/Shanghai` 转换，避免把已刷新 snapshot 误判为 `stale`。
