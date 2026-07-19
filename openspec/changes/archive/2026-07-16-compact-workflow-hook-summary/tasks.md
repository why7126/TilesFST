## 1. Workflow Sync Summary

- [x] 1.1 Inspect current Workflow Sync report builder and identify default summary/detail output paths.
- [x] 1.2 Ensure default successful Workflow Sync output aggregates event, focus object, Sprint resolution, updated count, skipped count and errors count.
- [x] 1.3 Ensure default successful Workflow Sync output suppresses full `Skipped (no delta)` file lists and long derived block content.
- [x] 1.4 Preserve explicit detailed output mode for per-file updated/skipped diagnostics with unchanged write behavior and exit code.
- [x] 1.5 Ensure error, drift and marker failure paths still print each actionable error reason and return non-zero.

## 2. AI Usage Hook Summary

- [x] 2.1 Inspect `scripts/extract-ai-usage.py` and shared AI usage summary builders for post-command hook output.
- [x] 2.2 Ensure standard workflow hook output exposes only `status`, `usage_mode`, `command_run_count`, `sprint_snapshot`, `warning_count` and `recommended_action` to command-facing summaries.
- [x] 2.3 Ensure unavailable, estimated fallback, unsafe-record skipped and Sprint snapshot skipped cases produce compact summaries with actionable `recommended_action`.
- [x] 2.4 Confirm local session input unavailable remains a non-fatal hook result for parent workflow commands.
- [x] 2.5 Confirm release hook extra `release_artifact` behavior remains compatible with existing release command contracts.

## 3. Skill And Documentation Alignment

- [x] 3.1 Update `.agents/skills/workflow-sync/SKILL.md` to describe the compact summary contract and detailed-mode escape hatch.
- [x] 3.2 Update req、bug、opsx、sprint command skills that invoke Workflow Sync or AI usage hook so they ask for summary output only on success.
- [x] 3.3 Keep skill instructions free of copied session parsing logic, raw hook JSON examples and long success-path logs.

## 4. Tests And Validation

- [x] 4.1 Add or update tests for Workflow Sync default summary output with multiple no-delta skipped files.
- [x] 4.2 Add or update tests for Workflow Sync detail mode preserving per-file results.
- [x] 4.3 Add or update tests for Workflow Sync error/drift output preserving actionable diagnostics.
- [x] 4.4 Add or update tests for AI usage hook compact summary fields in success, unavailable and unsafe-record scenarios.
- [x] 4.5 Run focused tests for Workflow Sync and AI usage scripts.
- [x] 4.6 Run `openspec validate compact-workflow-hook-summary --strict` or the project-equivalent OpenSpec validation command.
- [x] 4.7 Run `python scripts/validate-agent-context-budget.py` after skill updates.
