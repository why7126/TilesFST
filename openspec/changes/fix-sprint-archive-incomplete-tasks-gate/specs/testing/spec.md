## ADDED Requirements

### Requirement: Sprint Archive Tasks Gate

The workflow tooling MUST provide an executable Sprint archive readiness gate that blocks `/sprint-archive` before any archive or Sprint close mutation when a Sprint-scoped OpenSpec Change has incomplete tasks.

#### Scenario: Incomplete active change blocks archive

- **WHEN** a Sprint references an active OpenSpec Change whose `tasks.md` contains one or more `- [ ]` items
- **THEN** the Sprint archive readiness gate MUST return a non-zero exit code
- **AND** the report MUST identify the blocked change and incomplete task count.

#### Scenario: Incomplete archived change blocks Sprint close

- **WHEN** a Sprint references an already archived OpenSpec Change whose archived `tasks.md` contains one or more `- [ ]` items
- **THEN** the Sprint archive readiness gate MUST return a non-zero exit code
- **AND** the report MUST NOT skip the change only because it is already under `openspec/changes/archive/`.

#### Scenario: Completed Sprint changes pass

- **WHEN** every Sprint-scoped OpenSpec Change has a present `tasks.md` with all checklist items marked `- [x]`
- **THEN** the Sprint archive readiness gate MUST return exit code 0
- **AND** the report MUST declare a PASS verdict.

#### Scenario: Missing tasks file blocks archive

- **WHEN** a Sprint-scoped OpenSpec Change has no `tasks.md`
- **THEN** the Sprint archive readiness gate MUST return a non-zero exit code
- **AND** the report MUST identify the missing tasks file as a blocker.
