---
name: "image-build"
description: "基于发布镜像构建计划执行镜像构建并生成 manifest"
created_at: "2026-07-29 15:51:41"
updated_at: "2026-08-01 11:16:36"
---

# image-build

Use this skill when the user asks `/image-build <version>` or wants to build release images and write image manifest evidence.

## Context Budget Guardrails（MUST）

### Force-proceed Follow-up Guardrails（MUST）

- `force-proceed` 仅允许继续当前命令的非阻断部分，MUST NOT 默认自动创建 follow-up REQ/BUG；除非用户在当前命令中明确授权自动 capture，否则只输出标准 capture 文案，并明确“未自动创建 Issue”。
- 标准 capture 文案 MUST 分条包含：建议命令、类型倾向、标题、背景、影响范围、建议验收或复现要点、来源 Change/Sprint/命令；多个 follow-up 事项 MUST 逐条输出，且每条可独立用于后续 capture。
- 如用户明确授权并实际创建 follow-up Issue，MUST 按 `/req-capture`、`/bug-capture` 或 `/capture` 规则落盘，并运行对应 `req.capture` 或 `bug.capture` Workflow Sync。

- MUST 遵守 `rules/agent-context-budget.md`；同一会话已读且无变更的规则和 Skill 用摘要承接。
- 从 `releases/<version>/image-build-plan.json` 开始，只按 plan 的 `input_files` 定位必要上下文。
- MUST NOT 从本地 shell 环境猜测 release version、image tag、build args、release dir 或 tar name。
- MUST NOT 默认打印完整 Docker build logs、完整 tarball 内容、完整 manifest JSON、raw env 文件或 secrets。

## Input

- `<version>`：必填，例如 `v0.2.0`。
- Optional：`--env-file <path>` 指定本地构建 env；默认 `scripts/build-images.env`。

## Must Read

```text
AGENTS.md
rules/release.md
rules/security.md
rules/environment.md
rules/document-governance.md
rules/agent-context-budget.md
releases/<version>/release.json
releases/<version>/image-build-plan.json
scripts/build-images.sh
scripts/validate-image-build.py
```

## Gates

`/image-build` MUST:

- 读取有效 `releases/<version>/image-build-plan.json`。
- 缺少 plan、plan blocked、版本不匹配、input hash 漂移时拒绝构建。
- 复用 `scripts/build-images.sh` 执行 backend/web 镜像构建、平台验证、后端依赖验证、Web Nginx 验证、tar 导出和 sha256 生成。
- 构建成功后生成或更新 `releases/<version>/image-manifest.json`。
- 构建成功后 MUST 立即运行 `python scripts/validate-image-build.py validate-manifest --release <version>`，确认 manifest、tarball、`.sha256` sidecar 和实际 tarball sha256 四者一致。
- 如果 `/image-build` 后又修改 `release.json` 的 stable fields 或镜像构建输入文件，MUST 重新执行 `/image-prepare <version>` 与 `/image-build <version>`；不得沿用旧 tarball 或旧 `.sha256`。`announcement.mdx` 不参与镜像构建输入 hash，状态文案刷新不要求重建镜像。
- Docker、buildx、网络、基础镜像源、依赖安装、镜像验证、tar 导出或 checksum 失败时记录 blocker，不写成功 manifest。
- 不写入真实 `.env` 内容、密钥、数据库连接串、Authorization header、Cookie、真实客户数据或本机绝对路径。

## Build Failure Contract（MUST）

If build fails before manifest generation, record a release blocker instead of writing a success manifest. The blocker MUST include the failing phase:

- `docker_access`
- `buildx`
- `base_image_or_network`
- `backend_build`
- `web_build`
- `backend_dependency_validation`
- `web_nginx_validation`
- `tar_export`
- `checksum_validation`

When sandbox or permission prevents Docker/buildx access, retry with the same command using the required approval path before declaring the blocker. Do not print full Docker logs in the final response; summarize the failing phase and the first actionable error.

## Command

```bash
python scripts/validate-image-build.py validate-plan --release <version>
python scripts/validate-image-build.py build --release <version>
python scripts/validate-image-build.py validate-manifest --release <version>
```

## Output

Report compact summary only:

- version
- image_required
- plan path
- manifest path
- image tag
- tarball path
- tarball sha256
- blocker count
- validation summary
- next command: `/release-publish <version>` only when release gates are ready
- if release validation is still blocked by `usage_docs.status=pending_confirmation`, do not imply the image flow can clear it; report both explicit unblock paths:

```text
python scripts/generate-usage-docs.py <version>
python scripts/generate-usage-docs.py <version> --skip --confirmed-by operator --rationale "<why usage docs are not needed for this release>"
```

## AI Usage Post-command Hook（MUST）

After the command completes or records blockers, run:

```bash
python scripts/extract-ai-usage.py \
  --post-command-hook \
  --workflow-event image.build \
  --release <version> \
  --json
```

Print only the compact hook summary.

## Final Output Contract（MUST）

命令结束前，最终回复 MUST 明确包含：

```text
下一步：<可直接执行的命令；若没有则写“暂无可推进下一步”>
待用户决策/处理：
- <需要用户选择、确认、补充或处理的事项；若没有则写“无”>
```

- 如果存在明确可推进的下一步，MUST 给出可复制执行的命令，例如 `/bug-review BUG-0122`。
- 如果下一步取决于用户选择，MUST 用条件化条目列出选项；已在「下一步」中给出的命令或动作，不得在「待用户决策/处理」中重复。
- 「待用户决策/处理」只列缺失输入、需用户选择的范围/策略/证据/验收/发布确认、阻塞项或需人工处理事项；没有则写“无”。
- 不得因为输出了下一步引导而自动执行下一命令；除非用户明确授权。
