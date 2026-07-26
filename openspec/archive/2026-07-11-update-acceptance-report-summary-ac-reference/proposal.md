## Why

Sprint `acceptance-report.md` currently mixes final archive facts with long raw AC checklists. In Sprint 005 this left a report that clearly passed archive readiness while still showing many unchecked historical AC items, making it easy to misread an archived Sprint as unfinished.

## What Changes

- Split Sprint acceptance reports into a final acceptance summary and a raw AC reference section.
- Make the final summary the primary source for archive-readiness reading, including readiness gate, Change status, task completion, Sprint lifecycle, and human sign-off.
- Keep raw AC content as traceability/reference material with explicit semantics for unchecked items.
- Constrain Workflow Sync and Fact Sheet consumers to prefer final summary/archive facts over raw AC checklist residue.
- Preserve existing `/sprint-archive` gates; this change does not relax task, Change archive, or Workflow Sync requirements.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `sprint-planning-governance`: define acceptance-report layering and archive judgment semantics for Sprint acceptance and archive governance.

## Impact

- Affects Sprint documentation templates and generated/updated `iterations/*/<sprint>/acceptance-report.md`.
- Affects Workflow Sync acceptance-report refresh behavior in `scripts/workflow_sync/patch.py`.
- Affects Sprint archive closing notes and Fact Sheet/readiness signal extraction in `scripts/generate-sprint-fact-sheet.py`.
- Does not affect backend APIs, database schema, MinIO storage, Web UI, miniapp, Orval, or customer-facing behavior.
