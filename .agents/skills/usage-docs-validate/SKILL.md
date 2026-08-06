---
name: "usage-docs-validate"
description: "校验版本化产品使用文档、manifest、Mintlify 导航和公开安全"
---

# usage-docs-validate

Use this skill when the user asks `/usage-docs-validate <version>` or wants to validate product usage docs for a release.

## Bundled Resources

This project keeps `.agents/skills/*` lightweight: each project skill contains `SKILL.md` only, while deterministic implementation lives in top-level project scripts. This skill intentionally does not bundle its own `scripts/` directory; use:

```text
scripts/validate-usage-docs.py
scripts/validate-release.py
```

## Input

- `<version>`：必填，例如 `v0.3.2`。

## Must Read

```text
AGENTS.md
rules/release.md
rules/security.md
releases/<version>/release.json
```

If `usage_docs.status=generated`, also read:

```text
releases/<version>/usage-docs/manifest.json
releases/mint.json
```

Then read only files named by `manifest.pages` when debugging failures.

## Steps

Run:

```bash
python scripts/validate-usage-docs.py --release-dir releases/<version>
python scripts/validate-release.py --release-dir releases/<version> --stage prepare
```

If validating publish readiness, run:

```bash
python scripts/validate-release.py --release-dir releases/<version> --stage publish
```

## Validation Scope

The validator checks:

- `usage_docs.status` is `generated`, `skipped`, or `pending_confirmation`.
- `pending_confirmation` blocks readiness.
- `skipped` has confirmation source, time, rationale, and no empty `usage-docs/`.
- `generated` has valid `usage-docs/manifest.json`.
- Manifest pages match actual `.mdx` files.
- Generated docs include local system screenshots.
- Every generated `usage-docs/**/*.mdx` page references at least one screenshot.
- `manifest.screenshots[]` references existing `mintlify/assets/screenshots/` shared assets and covers every page; `releases/<version>/usage-docs/assets/` must not exist.
- If a previous generated usage-docs version exists and `manifest.source_version` points to it, current `manifest.pages` must include every previous-version page unless page removal is explicitly authorized and recorded.
- If `manifest.site_projection` exists, `mintlify/docs/<version>/`, `mintlify/docs/latest/`, `mintlify/releases/<version>/announcement.mdx`, `mintlify/mint.json`, content hashes, and public safety are checked.
- `manifest.screenshots[]` declares a real-system source, uses an allowed source_type, and rejects product prototype sources.
- Mintlify navigation references generated release pages and projected site pages.
- Coverage includes admin, miniapp, and release impact scope.
- Public docs and release metadata do not contain sensitive patterns.
- Old-version content corrections require explicit authorization trace.

## Output

Report version, `usage_docs.status`, `usage_docs_preview` gate, validation commands, pass/fail summary, failing files, and suggested fix command.

## Final Output Contract（MUST）

命令结束前，最终回复 MUST 明确包含：

```text
下一步：<可直接执行的命令；若没有则写“暂无可推进下一步”>
待用户决策/处理：
- <需要用户选择、确认、补充或处理的事项；若没有则写“无”>
```

- 如果存在明确可推进的下一步，MUST 给出可复制执行的命令，例如 `/bug-review BUG-0122 --approve`。
- 如果下一步取决于用户选择，MUST 用条件化条目列出选项；已在「下一步」中给出的命令或动作，不得在「待用户决策/处理」中重复。
- 「待用户决策/处理」只列缺失输入、需用户选择的范围/策略/证据/验收/发布确认、阻塞项或需人工处理事项；没有则写“无”。
- 不得因为输出了下一步引导而自动执行下一命令；除非用户明确授权。

