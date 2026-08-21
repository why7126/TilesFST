---
name: "release-prepare"
description: "执行发布前校验并生成或更新公开公告源文件"
---

# release-prepare

Use this skill when the user asks `/release-prepare <version>` or wants to run pre-release checks and generate/update the public announcement.

## Context Budget Guardrails（MUST）

### Force-proceed Follow-up Guardrails（MUST）

- `force-proceed` 仅允许继续当前命令的非阻断部分，MUST NOT 默认自动创建 follow-up REQ/BUG；除非用户在当前命令中明确授权自动 capture，否则只输出标准 capture 文案，并明确“未自动创建 Issue”。
- 标准 capture 文案 MUST 分条包含：建议命令、类型倾向、标题、背景、影响范围、建议验收或复现要点、来源 Change/Sprint/命令；多个 follow-up 事项 MUST 逐条输出，且每条可独立用于后续 capture。
- 如用户明确授权并实际创建 follow-up Issue，MUST 按 `/req-capture`、`/bug-capture` 或 `/capture` 规则落盘，并运行对应 `req.capture` 或 `bug.capture` Workflow Sync。

- MUST 遵守 `rules/agent-context-budget.md`；同一会话已读且无变更的规则和 Skill 用摘要承接，不重复全量读取。
- 从 `releases/<version>/release.json` 开始，只读取发布对象中列出的 Sprint / REQ / BUG / Change。
- 门禁失败时按脚本报告定位具体文件片段；不要全量读取 `docs/**`、`issues/**`、`iterations/**` 或归档目录。
- 测试、Docker、Orval、Mintlify 输出只保留摘要；失败时展开关键错误。
- 测试失败时 MUST 先做失败分类并写入输出或 release blockers：`archived_path_residual`（active Change 路径在归档后失效）、`fixture_schema_drift`（测试 fixture / snapshot 字段落后于契约）、`helper_payload_invalid`（共享 helper 仍提交废弃字段或非法 payload）、`product_regression`（真实产品行为回归）、`environment_blocker`（本地依赖、网络、权限或真实环境不可用）。
- 若失败属于前三类治理漂移，MUST 建议同步测试 helper、归档路径 resolver 或 fixture 契约；不得只要求人工复跑。

## Input

- `<version>`：必填，例如 `v0.1.0`。
- Flags：`--dry-run`、`--skip-tests`（不推荐）、`--skip-docker`（不推荐）、`--skip-mintlify`（不推荐）。

## Must Read

```text
AGENTS.md
rules/document-governance.md
rules/directory-structure.md
rules/release.md
rules/security.md
rules/testing.md
rules/agent-context-budget.md
releases/<version>/release.json
releases/templates/announcement.mdx
releases/templates/usage-docs/
src/shared/product-version.ts
```

按发布对象范围分段读取：

```text
iterations/change|archive/<sprint-id>/sprint.yaml
iterations/change|archive/<sprint-id>/release-note.md
iterations/change|archive/<sprint-id>/acceptance-report.md
openspec/archive/<date>-<change-id>/trace.md 或归档验证摘要
issues/requirements/{archive,review,plan}/<REQ>/trace.md
issues/bugs/{archive,review,plan}/<BUG>/trace.md
```

## Gates

Prepare MUST verify and record evidence for each applicable gate in `release.json`:

| Gate | Evidence |
|---|---|
| `openspec_archive` | All formal Changes are archived and merged into `openspec/specs/`; unarchived formal scope blocks publish. |
| `tests` | Relevant pytest / Vitest / smoke commands and pass summary. |
| `orval` | API changes have OpenAPI / Orval / docs sync evidence, or `na` rationale. |
| `docker_compose` | Deployment changes have Compose config/docs evidence, or `na` rationale. |
| `database_migration` | DB changes have schema/migration/docs/rollback evidence plus MySQL schema drift or target MySQL smoke evidence, or `na` rationale. |
| `env_example` | Env changes have `.env.example` evidence, or `na` rationale. |
| `product_version` | `PRODUCT_VERSION` equals release version, or rationale is explicit. |
| `mintlify_preview` | Mintlify build/preview or equivalent static MDX safety check evidence. |
| `usage_docs_preview` | First confirm whether usage docs are required. If generated, validate manifest/navigation/safety/coverage. If skipped, record rationale and do not create an empty `usage-docs/` directory. Pending confirmation blocks readiness. |
| `image_prepare` | When `image_required=true`, `releases/<version>/image-build-plan.json` exists, validates, and is referenced by release metadata. |
| `image_build` | In prepare, record `na` with a blocker / next step when `releases/<version>/image-manifest.json` is not yet generated; publish is the stage that requires manifest or approved external build evidence. |

Do not write `status: pass` without concrete command/path/time evidence.

When release scope includes backend runtime, Web build output, Dockerfile, Compose, build env, image build scripts, database schema / migration, API / Orval generated client, or offline image delivery:

- Set or keep `image_required=true` in `release.json`.
- Require `/image-prepare <version>` evidence before marking prepare complete.
- Point to `/image-build <version>` when a built image or offline tarball must be delivered.
- Do not execute the heavy image build from `/release-prepare` by default.

## Commands

Required structural and safety validation:

```bash
python scripts/validate-release.py --release-dir releases/<version> --stage prepare
python scripts/validate-usage-docs.py --release-dir releases/<version>  # only after usage_docs.status is generated or skipped
python scripts/validate-image-build.py validate-plan --release <version>
```

Run additional checks according to release scope. Common commands:

```bash
uv run pytest
pnpm --dir src/web test -- --run
python scripts/validate-api-standard.py
./scripts/generate-openapi-client.sh
docker compose config --quiet
python scripts/check-mysql-schema-drift.py --database-url "$DATABASE_URL"
```

Only run expensive or environment-dependent checks when they match release scope or user requested full validation. If a command cannot run locally, record the blocker; do not invent evidence.

If `impact_scope.database` is not `none` / `na` / `不涉及`, `database_migration` MUST be `pass` and its evidence MUST explicitly mention MySQL or `schema.mysql.sql`, a schema drift / target MySQL smoke check, and database rollback or backup evidence. Do not paste raw `DATABASE_URL` or credentials into release artifacts.

## Actionable Blockers（MUST）

When `/release-prepare` records blockers, each blocker MUST include:

- `classification` using the existing failure taxonomy where possible.
- `current_evidence` summarizing the command/path/time that exposed the blocker.
- `safe_remediation` with a concrete next command or manual action when known.
- `rerun_check` with the exact validation command to rerun after remediation.

Examples:

- `environment_blocker` for missing PIL/Pillow SHOULD mention restoring the backend uv environment and rerunning the affected `uv run python -m pytest ...` command.
- MySQL drift SHOULD name only the missing table/column categories, never credentials, and SHOULD suggest applying the existing idempotent migration entrypoint or the project-approved migration path before rerunning `scripts/check-mysql-schema-drift.py --json`.
- Missing image plan SHOULD point to `/image-prepare <version>`.
- Missing image manifest SHOULD point to `/image-build <version>` after image plan is valid.

The final response MUST group blockers into `已解决`, `仍阻塞`, and `仅 warning` when more than one gate changed during the command.

## Usage Docs Decision（MUST）

Before generating or validating current-version product usage docs, ask the user whether this release needs usage docs generation or update. Do not infer confirmation from the presence of user-visible changes alone.

- If user confirms **needed**:
  - Ensure `release.json usage_docs.generation_decision.required=true`, `confirmed_at`, `confirmed_by`, and `rationale` are recorded.
  - Run `/usage-docs-generate <version>` or `python scripts/generate-usage-docs.py <version>`.
  - Update `releases/mint.json` navigation for the generated pages.
  - Run `/usage-docs-validate <version>` or `python scripts/validate-usage-docs.py --release-dir releases/<version>`.
  - Set `gates.usage_docs_preview.status=pass` only with concrete command/path/time evidence.
- If user confirms **not needed**:
  - Run `python scripts/generate-usage-docs.py <version> --skip --rationale "<reason>" --confirmed-by "<source>"` or equivalent.
  - Keep `releases/<version>/usage-docs/` absent.
  - Set `gates.usage_docs_preview.status=na` with rationale.
- If user has **not confirmed**:
  - Set or keep `usage_docs.status=pending_confirmation`.
  - Do not create `usage-docs/`.
  - Record a blocker or pending item; do not mark publish ready.

Usage docs and release metadata MUST be public-safe: no real `.env` content, database connection strings, secrets, Authorization headers, Cookies, object storage credentials, production private domains, local absolute paths, or real customer data.

## Artifacts（非 `--dry-run` MUST）

Create or update:

```text
releases/<version>/release.json
releases/<version>/announcement.mdx
releases/<version>/usage-docs/**  # only when user confirmed generation is needed
```

Announcement MUST include version, release time, related Sprint, new features, bug fixes, release notes, known issues, upgrade steps, rollback instructions, and impact scope. It MUST be public-safe.

## Output

Report version, gate status summary, commands run, updated files, blockers, and whether publish is ready. If `usage_docs.status=pending_confirmation`, the output MUST explicitly list both unblock paths:

```text
python scripts/generate-usage-docs.py <version>
python scripts/generate-usage-docs.py <version> --skip --confirmed-by operator --rationale "<why usage docs are not needed for this release>"
```

If ready, next command:

```text
/release-publish <version>
```

## Final Step — AI Usage Post-command Hook (MUST)

After release preparation completes or records blockers, run:

```bash
python scripts/extract-ai-usage.py \
  --post-command-hook \
  --workflow-event release.prepare \
  --release <version> \
  [--release-sprint <sprint-id>] \
  [--sprint <sprint-id>] \
  [--req <REQ-id>] \
  [--bug <BUG-id>] \
  [--change <change-id>] \
  --json
```

- Pass Sprint / REQ / BUG / Change ids from `releases/<version>/release.json`.
- Pass `--release <version>` so the hook writes both release command run details under `data/ai-usage/command-runs/releases/<version>/<date>--release.prepare--<session-hash>.json` and the version artifact `data/ai-usage/command-runs/releases/<version>/release.prepare.json`.
- Treat the hook as incomplete if `outputs.command_runs` does not point under `data/ai-usage/command-runs/releases/<version>/`; release commands must not store their primary command-run details under `issues/` or `opsxs/` just because the release scope includes REQ / BUG / Change ids.
- Pass each release-scope Sprint with repeated `--release-sprint <sprint-id>` so the release artifact coverage records the full version scope.
- The hook accepts one `--sprint` value per invocation for Sprint snapshot refresh. For a release that spans multiple Sprint ids, run the hook once per Sprint only when you intentionally refresh Sprint snapshots; do not use repeated `--sprint` to express release scope.
- If no Sprint is associated, omit `--sprint`; Sprint snapshot output MUST be `skipped`.
- Print only the compact hook summary: `status`, `usage_mode`, `command_run_count`, `session_input`, `release_artifact`, `sprint_snapshot`, `warning_count`, and `recommended_action`.
- If local session input is unavailable, report `usage_mode: unavailable` and the recommended action; do not treat that as parent command failure.
- If the hook reports `unsafe-records-skipped:<count>`, treat it as a usage-data blocker to fix or explicitly report; do not replace it with a deliberately missing `--session-jsonl`.
- Release scope often includes IDs such as password or token; these business IDs are allowed in command-run metadata and must not be treated as secrets unless they appear as raw credentials, auth headers, `.env` content, assigned secret-like fields, or local absolute paths.

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
