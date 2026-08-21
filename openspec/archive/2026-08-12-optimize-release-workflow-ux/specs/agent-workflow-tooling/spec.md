## ADDED Requirements

### Requirement: Release workflow commands provide explicit operator decision summaries

Release workflow commands SHALL preserve and echo operator decisions for usage documentation, public announcement generation, and image build requirements before moving to the next release stage.

#### Scenario: Release proposal captures publication decisions
- **GIVEN** an operator proposes a release
- **WHEN** usage docs, announcement, or image build decisions are known
- **THEN** the command SHALL record those decisions in the release artifact
- **AND** the final response SHALL summarize each decision and any remaining missing decision.

### Requirement: Release blockers include actionable remediation paths

Release prepare and image commands SHALL distinguish resolved blockers, true release blockers, and warnings, and SHALL provide an actionable next command or remediation path when one is known.

#### Scenario: Prepare finds target MySQL drift
- **GIVEN** release preparation detects target MySQL schema drift
- **WHEN** the command records the blocker
- **THEN** the output SHALL identify the missing table or field category without exposing credentials
- **AND** SHALL suggest a safe migration or drift-check rerun path.

### Requirement: Publish confirmation avoids image evidence loops

Release publish SHALL write publish confirmation only to non-stable publish metadata and SHALL NOT require image rebuild for status-only announcement generation after publish.

#### Scenario: Operator requests public announcement after publish
- **GIVEN** image manifest validation already passed
- **WHEN** the operator asks to generate public announcement copy after publish
- **THEN** the workflow MAY update announcement content and non-stable release metadata
- **AND** SHALL re-run publish validation and image manifest validation
- **AND** SHALL NOT require image rebuild unless stable release scope or image input files changed.
