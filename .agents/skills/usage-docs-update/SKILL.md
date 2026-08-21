---
name: "usage-docs-update"
description: "更新当前版本产品使用文档，或在明确授权下维护旧版本文档"
---

# usage-docs-update

Use this skill when the user asks `/usage-docs-update <version>` or wants to update existing product usage docs.

## Bundled Resources

This project keeps `.agents/skills/*` lightweight: each project skill contains `SKILL.md` only, while deterministic implementation lives in top-level project scripts. This skill intentionally does not bundle its own `scripts/` directory; use:

```text
scripts/generate-usage-docs.py
scripts/validate-usage-docs.py
scripts/validate-release.py
```

## Input

- `<version>`：必填，例如 `v0.3.2`。
- Flags：`--force-regenerate` 使用生成脚本覆盖当前版本文档；默认优先做小范围手工/AI 辅助更新。

## Must Read

```text
AGENTS.md
rules/document-governance.md
rules/directory-structure.md
rules/release.md
rules/security.md
releases/<version>/release.json
releases/<version>/usage-docs/manifest.json
```

Then read only the impacted `usage-docs/**/*.mdx` pages.

## Gate

Determine whether `<version>` is the current release being prepared or an old published version.

- Current version: updates require `usage_docs.status=generated` and an explicit update reason.
- Old version: content changes require explicit authorization and MUST be recorded in `manifest.manual_overrides`.
- Non-content maintenance for old versions is allowed for broken links, frontmatter/manifest completion, Mintlify config migration, formatting, navigation references, sensitive information removal, or directory migration.

BLOCKED if the request would change old-version product behavior, operation steps, availability, version differences, or known issue history without explicit authorization.

## Steps

1. Identify impacted pages and whether the change is content correction or non-content maintenance.
2. Update only the relevant `usage-docs/**/*.mdx` files and `manifest.json`, then refresh the corresponding `mintlify/docs/<version>/` projection when applicable.
3. When adding or materially changing a user-facing page, ensure the page includes at least one real system screenshot from `mintlify/assets/screenshots/` and update `manifest.screenshots[]` with `path=/assets/screenshots/<file>`, `site_asset`, pages, caption, source, source_type, content_hash, first_used_in, used_by_versions, covered_pages, and reuse_reason. Do not create `releases/<version>/usage-docs/assets/`.
4. When updating the current version after generation, preserve the previous generated version's full page set unless the user explicitly authorizes page removal.
4. For content correction, append a `manifest.manual_overrides[]` entry with:
   - `change_type: "content_correction"`
   - `authorized: true`
   - `reason`
   - `confirmed_by`
   - `confirmed_at`
   - `files`
   - `summary`
5. If full current-version regeneration is explicitly requested, run:

```bash
python scripts/generate-usage-docs.py <version> --force
```

6. Validate:

```bash
python scripts/validate-usage-docs.py --release-dir releases/<version>
python scripts/validate-release.py --release-dir releases/<version> --stage prepare
```

## Safety

- Keep old versions snapshot-safe by default.
- Remove sensitive information immediately if found, and record the maintenance scope.
- Do not change `release.json` release scope, API/DB contracts, or runtime behavior from this skill.
- Do not leave generated/current-version usage docs as text-only pages; each page must keep screenshot coverage.
- Do not use product prototypes, design drafts, wireframes, Figma/HTML prototypes, or other non-system screenshots as usage-doc screenshots.

## Output

Report version, update type, changed pages, manifest update, validation commands, remaining blockers, and whether release prepare/publish can proceed.

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

