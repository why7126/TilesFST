## ADDED Requirements

### Requirement: Sprint retrospective AI usage matrices require a fresh gate pass

`/sprint-exps` and its Sprint Fact Sheet tooling SHALL NOT output real AI usage cost matrices unless the AI usage snapshot passes the fresh gate.

#### Scenario: Snapshot is stale before retrospective matrix rendering
- **GIVEN** a Sprint Fact Sheet summary reports `ai_usage_snapshot.fresh_gate.status` as `blocker`
- **WHEN** `/sprint-exps` prepares the model token usage analysis
- **THEN** the command SHALL show the blocker reason, impact, freshness baseline, and recommended action
- **AND** SHALL request or run the snapshot refresh path before rendering real matrices
- **AND** SHALL rerun `generate-sprint-fact-sheet.py --summary` after refresh
- **AND** SHALL NOT output real `total_tokens`, `input_tokens`, `output_tokens`, or `model_call_count` matrices until the rerun summary reports `fresh_gate.status=pass`.

#### Scenario: Markdown rendering is requested with a blocked gate
- **GIVEN** `generate-sprint-fact-sheet.py --ai-usage-markdown` is run for a Sprint whose snapshot is missing, stale, failed, estimated, coverage-incomplete, metrics-empty, or matrix-missing
- **WHEN** the script renders the model token usage section
- **THEN** it SHALL output a blocker-oriented Token Usage Fact Sheet with recommended refresh action
- **AND** it SHALL NOT render any real matrix table.
