---
name: "usage-docs-generate"
description: "确认需要后生成当前版本产品使用文档和 manifest"
---

# usage-docs-generate

Use this skill when the user asks `/usage-docs-generate <version>` or wants to generate product usage docs for a release version.

## Bundled Resources

This project keeps `.agents/skills/*` lightweight: each project skill contains `SKILL.md` only, while deterministic implementation lives in top-level project scripts. This skill intentionally does not bundle its own `scripts/` directory; use:

```text
scripts/generate-usage-docs.py
scripts/validate-usage-docs.py
scripts/validate-release.py
```

## Input

- `<version>`：必填，例如 `v0.3.2`。
- Flags：`--force` 仅用于当前版本已确认需要重新生成时覆盖当前版本 `usage-docs/`。

## Must Read

```text
AGENTS.md
rules/document-governance.md
rules/directory-structure.md
rules/release.md
rules/security.md
releases/<version>/release.json
releases/templates/usage-docs/
```

## Gate

Before running generation, confirm `releases/<version>/release.json` contains:

```json
{
  "usage_docs": {
    "generation_decision": {
      "required": true,
      "confirmed_at": "YYYY-MM-DD HH:mm:ss",
      "confirmed_by": "operator",
      "rationale": "..."
    }
  }
}
```

If confirmation is missing, BLOCKED. Ask the user whether this release needs usage docs generation or update. Do not infer confirmation from user-visible changes alone.

## Steps

1. Validate release directory exists.
2. Confirm generation decision is explicit and timestamped.
3. Run:

```bash
python scripts/generate-usage-docs.py <version>
```

Generation MUST inherit the full page set from the previous generated usage-docs version when one exists. Treat template-only generation as valid only for the first version with usage docs, or when the user explicitly authorizes a page-set reset/removal.

Use `--force` only when regenerating current-version usage docs after explicit confirmation:

```bash
python scripts/generate-usage-docs.py <version> --force
```

4. Confirm `scripts/generate-usage-docs.py` projected the inherited full page set into `mintlify/docs/<version>/`, refreshed `mintlify/docs/latest/`, and updated `mintlify/mint.json`.
5. Add system screenshots before validation:
   - every generated `usage-docs/**/*.mdx` page MUST include at least one local screenshot;
   - screenshots MUST live under `mintlify/assets/screenshots/` using content-hash filenames, with release manifest references;
   - `releases/<version>/usage-docs/assets/` MUST NOT exist;
   - update `usage-docs/manifest.json screenshots[]` with `path=/assets/screenshots/<file>`, `site_asset`, covered pages, caption, source, source_type, content_hash, first_used_in, used_by_versions, covered_pages, and reuse_reason;
   - source_type MUST be `runtime_system`, `qa_system`, `accepted_system_evidence`, `miniapp_devtools`, or `manual_system_capture`;
   - screenshots MUST come from the real running system, QA/acceptance real screenshots, miniapp device/devtools previews, or current-system manual captures;
   - BLOCKED if only product prototypes, design drafts, wireframes, Figma/HTML prototypes, or other non-system screenshots are available.
6. Run:

```bash
python scripts/validate-usage-docs.py --release-dir releases/<version>
python scripts/validate-release.py --release-dir releases/<version> --stage prepare
```

## Safety

- MUST NOT generate docs for old versions unless the user explicitly confirms current-version regeneration or authorized old-version maintenance.
- MUST NOT write secrets, real `.env` content, database connection strings, Authorization headers, Cookies, object storage credentials, production private domains, local absolute paths, or real customer data.
- MUST NOT create `usage-docs/` when user confirms docs are not needed; use `usage-docs-update` or skipped flow only as appropriate.
- MUST NOT leave generated usage docs as text-only pages; validation requires screenshot coverage.
- MUST NOT use product prototype images as usage-doc screenshots.
- MUST NOT use `mintlify/` as the only source of truth; release usage docs manifest remains the version fact source.

## Output

Report version, generated files, manifest path, release gate status, validation commands, blockers, and next release command.

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

