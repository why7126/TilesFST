---
name: "git-check"
description: "推送前 Git 安全检测 - 检查 staged/tracked 文件中的隐私数据、真实环境文件、运行时数据、数据库文件、大文件、密钥/Token/连接串、本机绝对路径和不应进入 Git 的本地数据"
created_at: 2026-08-10 23:28:57
updated_at: 2026-08-10 23:28:57
---

# git-check

Use this skill when the user asks to run `/git-check`, perform a pre-push Git safety check, or verify that repository changes do not contain secrets, real env files, runtime data, local databases, large artifacts, local absolute paths, or private data.

## Context Budget Guardrails（MUST）

### Guided User Feedback Contract（MUST）

当命令需要用户选择、确认、补充信息或处理阻塞时，MUST 采用引导式反馈：

- 优先使用原生交互卡片组织问题；当客户端或工具层不支持原生交互卡片时，MUST 先说明降级原因，再降级为文本结构化选项。
- 两种形态都必须包含结构化选项、推荐项和可补充说明入口，不得用大段开放式追问替代。
- 每轮只聚焦 1-3 个关键决策；每个决策点 SHOULD 给出 2-4 个互斥选项。
- 至少一个选项 MUST 标注“推荐”，并说明推荐理由或适用前提。
- 无需用户反馈的成功路径 SHOULD 保持紧凑，不为了套用格式追加无意义问卷。

### Force-proceed Follow-up Guardrails（MUST）

- `force-proceed` 仅允许继续当前命令的非阻断部分，MUST NOT 默认自动创建 follow-up REQ/BUG；除非用户在当前命令中明确授权自动 capture，否则只输出标准 capture 文案，并明确“未自动创建 Issue”。
- 标准 capture 文案 MUST 分条包含：建议命令、类型倾向、标题、背景、影响范围、建议验收或复现要点、来源 Change/Sprint/命令；多个 follow-up 事项 MUST 逐条输出，且每条可独立用于后续 capture。
- 如用户明确授权并实际创建 follow-up Issue，MUST 按 `/req-capture`、`/bug-capture` 或 `/capture` 规则落盘，并运行对应 `req.capture` 或 `bug.capture` Workflow Sync。

- MUST 遵守 `rules/agent-context-budget.md`。
- 已在同一会话读取过且无变更的规则和 Skill 文件，用摘要承接或摘要复用，不重复全量读取。
- 检索先用 `git diff --name-only`、`git ls-files` 或 `rg --files` 定位，再分段读取必要片段。
- 成功路径只输出扫描摘要、阻断项、warning 和下一步；不得输出完整密钥、Token、连接串、真实 `.env` 行或大段文件内容。

## Command

默认运行：

```bash
python scripts/git-check.py
```

深度复核时可运行：

```bash
python scripts/git-check.py --all
```

## Scope

- 默认扫描 staged、modified tracked 和 untracked 文件。
- `--all` 扫描全仓当前文件，但不扫描 Git 历史。
- 本地真实 `.env` 只要被 Git ignore 覆盖且未 staged/tracked，不应阻断。

## Checks

- 真实环境文件：`.env`、`.env.local`、`.env.*`、`deploy/**/*.env`、`scripts/build-images.env`。
- 运行时数据：数据库文件、`data/runtime/**`、`data/uploads/**`、`data/tmp/**`、`data/minio/**`、`data/mysql/**`、`data/s3/**` 等。
- 构建与本地产物：`dist/**`、`build/**`、`coverage/**`、压缩包、缓存和大文件。
- 敏感内容：密钥、Token、Authorization header、Cookie、数据库连接串、对象存储凭据、生产私有地址、本机绝对路径和疑似隐私数据；本机绝对路径作为 error 阻断。
- 合法占位符：`<access_token>`、`change-me-in-local-env`、`example`、`localhost` 等不应仅因关键词命中而失败。

## Guardrails

- 不自动修改 `.gitignore`。
- 不自动 unstage。
- 不删除本地文件。
- 不读取或输出 ignore 且未 staged/tracked 的真实 `.env` 内容。
- 不新增 `.claude/`、`.codex/`、`.cursor/`、`.kiro/`、`.opencode/`。

## Final Output Contract（MUST）

命令结束前，最终回复 MUST 明确包含：

```text
下一步：<可直接执行的命令；若没有则写“暂无可推进下一步”>
待用户决策/处理：
- <需要用户选择、确认、补充或处理的事项；若没有则写“无”>
```

- 如果存在明确可推进的下一步，MUST 给出可复制执行的命令。
- 如果下一步取决于用户选择，MUST 用条件化条目列出选项；已在「下一步」中给出的命令或动作，不得在「待用户决策/处理」中重复。
- 「待用户决策/处理」只列缺失输入、需用户选择的范围/策略/证据/验收/发布确认、阻塞项或需人工处理事项；没有则写“无”。
