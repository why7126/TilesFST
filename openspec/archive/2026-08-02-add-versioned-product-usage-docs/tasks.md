## 1. Release Metadata and Rules

- [x] 1.1 Extend `rules/release.md` with usage docs generation decision, generated/skipped/pending_confirmation states, `usage_docs_preview` gate, and old-version maintenance policy.
- [x] 1.2 Extend `rules/directory-structure.md` to allow `releases/<version>/usage-docs/` and document its boundary.
- [x] 1.3 Extend `rules/document-governance.md` with released usage-docs snapshot semantics, non-content maintenance, content correction traceability, and timestamp requirements.
- [x] 1.4 Update `releases/README.md` with usage docs layout, `/docs` browsing boundary, and generated/skipped behavior.
- [x] 1.5 Update release templates so `release.json` can express `usage_docs` metadata and `usage_docs_preview` gate without requiring every version to generate docs.

## 2. Usage Docs Generation and Validation

- [x] 2.1 Add usage docs templates under `releases/templates/usage-docs/` for overview, admin, miniapp, FAQ, and manifest.
- [x] 2.2 Implement usage docs generation command or script that requires explicit generation decision before writing `releases/<version>/usage-docs/**`.
- [x] 2.3 Implement skipped flow so confirmed non-generation records rationale in `release.json` and does not create an empty `usage-docs/` directory.
- [x] 2.4 Implement usage docs manifest generation with version, source version, source release, input files, page list, coverage, manual overrides, and automation policy.
- [x] 2.5 Implement usage docs validation for manifest structure, page/file consistency, Mintlify navigation, broken links, sensitive patterns, coverage, and old-version content rewrite policy.
- [x] 2.6 Ensure validation scans usage docs, manifest, announcement, release metadata, and Mintlify config for public-safety violations.

## 3. Release Workflow Integration

- [x] 3.1 Update `.agents/skills/release-prepare/SKILL.md` to ask/record whether usage docs generation is required before generation.
- [x] 3.2 Update `.agents/skills/release-publish/SKILL.md` to validate generated usage docs or accepted skipped rationale.
- [x] 3.3 Update `scripts/validate-release.py` or add an equivalent validator so release validation covers generated/skipped/pending_confirmation usage docs states.
- [x] 3.4 Update Mintlify config (`releases/mint.json` or `docs.json` if selected) to support versioned usage docs navigation when generated.
- [x] 3.5 Document `/docs` access deployment boundary without committing external credentials or production-only private endpoints.

## 4. Tests and Verification

- [x] 4.1 Add tests for release validation when usage docs are generated and all gates pass.
- [x] 4.2 Add tests for skipped usage docs flow: no empty `usage-docs/` directory required, rationale required, `usage_docs_preview` marked not applicable.
- [x] 4.3 Add tests for pending confirmation flow blocking release readiness.
- [x] 4.4 Add tests for manifest missing, navigation missing, broken links, sensitive content, and old-version unauthorized content rewrite failures.
- [x] 4.5 Run focused tests for release validation and directory structure validation.

## 5. Documentation Sync

- [x] 5.1 Update long-lived docs impacted by release usage docs governance, especially release and deployment references.
- [x] 5.2 Update OpenSpec trace and acceptance evidence with commands run and any remaining deployment-choice open questions.
- [x] 5.3 Run `openspec validate add-versioned-product-usage-docs --strict`.

## 验收返修记录

| 时间 | 反馈 | 调整 | 验证 |
|---|---|---|---|
| 2026-08-01 11:54:37 | 用户要求在已实现脚本基础上直接生成 `usage-docs-generate`、`usage-docs-update`、`usage-docs-validate` 三个 Skill。 | 新增 `.agents/skills/usage-docs-{generate,update,validate}/SKILL.md`，并同步 `rules/release.md`、`releases/README.md` 与 `release-prepare` skill 引用。 | 已通过 focused pytest、目录结构校验、OpenSpec strict、Workflow Sync 与 AI Usage hook。 |
| 2026-08-01 11:54:37 | 用户追问 Skill 目录只有 `SKILL.md`、没有处理脚本是否合理，并要求继续。 | 确认项目内 `.agents/skills/*` 当前约定为轻量 `SKILL.md`，底层处理脚本统一放项目级 `scripts/`；在三个 usage docs Skill 中补充 Bundled Resources 说明。 | 已通过 focused pytest、目录结构校验、OpenSpec strict、Workflow Sync 与 AI Usage hook。 |
