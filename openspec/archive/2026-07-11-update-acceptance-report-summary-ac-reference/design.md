## Context

REQ-0033 was approved to address sprint-005 retrospective action A-005: split `acceptance-report.md` into final acceptance summary and raw AC reference. The current report structure can show final archive success and unchecked raw AC lines in the same reading layer. That creates ambiguity for product, QA, and future retrospectives.

The change is documentation and workflow-tooling governance. It does not alter business functionality or the hard gates used by `/sprint-archive`.

## Goals / Non-Goals

**Goals:**

- Make final Sprint archive judgment readable from a short, stable summary.
- Preserve raw AC traceability without letting historical unchecked lines override archive facts.
- Keep human sign-off fields separate from Workflow Sync derived fields.
- Update Fact Sheet signal extraction to prefer final summary/archive facts over raw AC details.

**Non-Goals:**

- No bulk migration of all historical `acceptance-report.md` files by default.
- No change to REQ/BUG `acceptance.md` authoring or AC numbering.
- No relaxation of readiness gate, Change archive, tasks completion, Workflow Sync, or directory migration gates.
- No Web, API, database, storage, or miniapp behavior changes.

## Decisions

### D1. Use layered report sections

Future acceptance reports should separate:

1. final acceptance summary;
2. final archive check;
3. human sign-off record;
4. raw AC reference.

This keeps final archive state scan-friendly while preserving original evidence links. A single long checklist was rejected because it keeps the current ambiguity.

### D2. Treat unchecked raw AC as typed reference data

Unchecked raw AC items must be classified as one of:

- pending human sign-off;
- archive blocker;
- historical trace.

Only archive blockers affect closure. Historical trace and pending sign-off remain visible, but they do not automatically override final archive facts.

### D3. Workflow Sync updates derived areas only

Workflow Sync may refresh derived notes and status lines, but it must not overwrite manual final verdict, reviewer, or sign-off text. This avoids automated drift from erasing human review context.

### D4. Fact Sheet reads final summary first

Fact Sheet and retrospective flows should prioritize final summary/archive check fields when judging acceptance status. Raw AC text remains an evidence hint, not the first signal for Sprint completion.

## Risks / Trade-offs

| Risk | Mitigation |
|---|---|
| Historical reports remain inconsistent | Default scope affects new or actively updated reports; historical migration can be handled separately if needed. |
| Teams misread this as relaxed QA | Specs and acceptance explicitly keep `/sprint-archive` hard gates unchanged. |
| Workflow Sync cannot reliably find sections | Implement stable headings and narrowly scoped replacement logic. |
| Fact Sheet still catches raw "未完成" text | Adjust signal priority and tests to read final summary before raw AC reference. |

## Migration Plan

1. Update the acceptance-report template or generation path used by Sprint proposal/closure.
2. Update Workflow Sync acceptance-report patching to target derived status areas and preserve manual sign-off fields.
3. Update Fact Sheet signal extraction to prefer final summary/archive check.
4. Add focused tests or fixture checks using a report with final PASS and unchecked raw AC reference.
5. Leave archived reports unchanged unless explicitly selected for cleanup.

## Open Questions

- Should Sprint 005 `acceptance-report.md` be migrated as a one-off cleanup, or left as the motivating historical example?
- Should the final summary section name be fixed as `最终验收摘要`, or allow equivalent heading names with marker comments?
