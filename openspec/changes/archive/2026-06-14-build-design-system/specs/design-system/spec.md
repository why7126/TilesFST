## ADDED Requirements

### Requirement: Design System validation script

The project MUST provide `scripts/validate-design-system.py` to detect Hex hardcoding, arbitrary Tailwind color values, and unauthorized native HTML controls outside allowed Design System paths.

#### Scenario: Validation script exists

- **WHEN** a developer lists `scripts/validate-design-system.py`
- **THEN** the file MUST exist and be executable via `python scripts/validate-design-system.py`

#### Scenario: Baseline validation passes

- **WHEN** `python scripts/validate-design-system.py` runs on the repository baseline after Sprint-000 governance fixes
- **THEN** it MUST exit with code 0
- **AND** MUST report Design System validation passed

#### Scenario: Token definition paths exempt

- **WHEN** the validator scans `globals.css`, token definition files, or `/design-system` preview fixtures
- **THEN** those paths MUST be exempt from Hex hardcoding rules as documented in the script

### Requirement: Design System AI prompts

The project MUST maintain `src/shared/design-system/prompts/` with documented prompts for page, form, and table generation plus UI review rules for AI-assisted development.

#### Scenario: Prompt files present

- **WHEN** a developer lists `src/shared/design-system/prompts/`
- **THEN** MUST find at least `generate-page.md`, `generate-form.md`, `generate-table.md`, and `review-ui.md`

#### Scenario: Prompts reference semantic tokens

- **WHEN** a developer reads the prompt files
- **THEN** instructions MUST require semantic token classes and shared/ui component priority
- **AND** MUST NOT encourage bare Hex or ad-hoc native controls in production UI

### Requirement: Design System governance documentation

Sprint-000 MUST register Design System governance artifacts linking rules, shared tokens, Web styles, validation, and preview entry.

#### Scenario: Shared design-system README

- **WHEN** a developer reads `src/shared/design-system/spec.md` or equivalent README under `src/shared/design-system/`
- **THEN** MUST find token source-of-truth paths and consumption guidance for Web

#### Scenario: Sprint trace linkage

- **WHEN** a developer reads `issues/requirements/REQ-0000-build-design-system/trace.md`
- **THEN** MUST find `change_id: build-design-system` and iteration `sprint-000`
