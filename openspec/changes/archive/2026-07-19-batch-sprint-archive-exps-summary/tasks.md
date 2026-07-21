## 1. Batch Summary Core

- [x] 1.1 Review `scripts/generate-sprint-fact-sheet.py` and `scripts/validate-sprint-archive-readiness.py` Change collection paths and identify the shared data needed for batch summaries.
- [x] 1.2 Implement deterministic Change batching for Sprint scopes with 10+ changes, defaulting to a maximum of 5 changes per batch.
- [x] 1.3 Extend Fact Sheet JSON output with `change_batches` or an equivalent machine-readable structure containing batch id, change ids, ordering basis, counts, warnings, blockers and evidence hints.
- [x] 1.4 Extend readiness JSON or queue reporting to reuse the same batch summary structure for `/sprint-archive` diagnostics.
- [x] 1.5 Ensure batch summaries contain only aggregate facts, workflow ids, repository-relative evidence paths and short warning labels.

## 2. Workflow Skill Updates

- [x] 2.1 Update `.agents/skills/sprint-archive/SKILL.md` so 10+ Change Sprint runs and consumes batch summaries before reading raw `tasks.md` or `trace.md` details.
- [x] 2.2 Update `.agents/skills/sprint-exps/SKILL.md` so 10+ Change Sprint复盘优先使用 Fact Sheet batch summary，并只按 evidence hints 分段回读细节。
- [x] 2.3 Keep Workflow Sync and AI usage post-command hook success output compact, and document failure-path diagnostics by batch id and Change id.

## 3. Tests and Validation

- [x] 3.1 Add or update `tests/test_generate_sprint_fact_sheet.py` to cover 10+ Change batch summary JSON and small Sprint non-applicable behavior.
- [x] 3.2 Add or update `tests/test_sprint_archive_readiness.py` to cover batch blocker/warning diagnostics and compact readiness output fields.
- [x] 3.3 Add or update `tests/test_validate_agent_context_budget.py` if skill guardrail wording changes require budget validation coverage.
- [x] 3.4 Run focused pytest for fact sheet, sprint archive readiness and context budget validation.
- [x] 3.5 Run `openspec validate batch-sprint-archive-exps-summary --strict` and fix any spec format or scenario issues.
