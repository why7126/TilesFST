## ADDED Requirements

### Requirement: 产品版本发布对象
The system SHALL support a product release object that represents one public product version release and can associate that release with one or more Sprints.

#### Scenario: Multiple Sprints in one product version
- **WHEN** a product release is created for a version
- **THEN** the release SHALL support associating one or more Sprint IDs.
- **AND** the release SHALL distinguish product release scope from Sprint-level `release-note.md` scope.

#### Scenario: Release scope traceability
- **WHEN** release scope is prepared from associated Sprints
- **THEN** the release SHALL track related REQs, BUGs, and OpenSpec Changes.
- **AND** each formally released item SHALL be traceable back to its source issue or change document.

#### Scenario: Incomplete work excluded from formal release
- **WHEN** a REQ, BUG, Sprint, or OpenSpec Change is not reviewed, not in delivery scope, or not archived as required
- **THEN** the release process SHALL exclude it from formal released scope.
- **AND** the process MAY list it only as a known issue or follow-up plan with explicit non-release wording.

### Requirement: 公开 Mintlify 发布公告
The product release management capability SHALL generate or maintain public-facing release announcement source files for Mintlify static documentation.

#### Scenario: Announcement is static and public
- **WHEN** a release announcement is prepared
- **THEN** it SHALL be authored as static documentation source suitable for Mintlify.
- **AND** it SHALL NOT require a backend runtime API or database query to be displayed.

#### Scenario: Announcement build or preview validation
- **WHEN** release preparation runs validation
- **THEN** it SHALL run a Mintlify build, preview, or documented equivalent validation step.
- **AND** validation failure SHALL block release confirmation.

#### Scenario: Announcement source is reviewable
- **WHEN** a release announcement source file is created
- **THEN** it SHALL be suitable for Git review.
- **AND** it SHALL include project-standard time fields using `YYYY-MM-DD HH:mm:ss` where metadata records release time.

### Requirement: 发布公告内容结构
Each product release announcement SHALL include the minimum public release content needed by customers, shop owners, implementation, operations, and the project team.

#### Scenario: Required announcement sections
- **WHEN** a product release announcement is generated
- **THEN** it SHALL include version, release time, associated Sprint list, new features, fixed BUGs, release notes, known issues, upgrade steps, rollback notes, and impact scope.

#### Scenario: Impact scope categories
- **WHEN** impact scope is documented
- **THEN** it SHALL distinguish Web admin, owner Web, miniapp, backend, database, object storage, and Docker impact.

#### Scenario: Public safety
- **WHEN** announcement content is reviewed
- **THEN** it SHALL NOT expose secrets, real customer data, private database connection strings, MinIO credentials, non-public domains, or sensitive operations details.

### Requirement: 发布前校验门禁
The release process SHALL block release confirmation unless mandatory release readiness checks pass or are explicitly marked not applicable with rationale.

#### Scenario: Mandatory release checks
- **WHEN** release preparation runs
- **THEN** it SHALL check OpenSpec archive status, tests, Orval synchronization, Docker Compose synchronization, database migration synchronization, `.env.example` synchronization, `PRODUCT_VERSION` consistency, and Mintlify build or preview validation.

#### Scenario: API change gate
- **WHEN** the release scope contains API changes
- **THEN** the release gate SHALL require OpenAPI and Orval synchronization evidence.

#### Scenario: Database change gate
- **WHEN** the release scope contains database changes
- **THEN** the release gate SHALL require migration, database documentation, and rollback note evidence.

#### Scenario: Failed gate blocks release
- **WHEN** any mandatory release gate fails
- **THEN** release confirmation SHALL stop.
- **AND** the process SHALL report the failed gate and recommended remediation.

### Requirement: releases 目录治理
The project SHALL use a governed top-level `releases/` directory for product release objects and public release announcement source after directory rules are updated by this OpenSpec Change.

#### Scenario: Directory rule updated before use
- **WHEN** implementation creates the top-level `releases/` directory
- **THEN** `rules/directory-structure.md` SHALL already define its responsibility, boundaries, naming rules, and lifecycle.
- **AND** AGENTS guidance SHALL mention the directory when describing allowed top-level directories.

#### Scenario: Directory relationship documented
- **WHEN** `releases/` is introduced
- **THEN** documentation SHALL explain its relationship to `iterations/`, `issues/`, `openspec/changes/`, archived specs, and Mintlify documentation source.

#### Scenario: Directory boundaries
- **WHEN** release artifacts are stored under `releases/`
- **THEN** they SHALL represent product release material and public announcement source.
- **AND** they SHALL NOT replace Sprint four-piece artifacts, issue documents, OpenSpec changes, or runtime deployment data.

### Requirement: 发布命令族
The project SHALL define a release command family for proposing, preparing, and confirming product releases.

#### Scenario: Command source of truth
- **WHEN** release commands are added or modified
- **THEN** `.cursor/commands/` SHALL be the source of truth.
- **AND** `python scripts/sync-agent-commands.py` or the documented equivalent synchronization flow SHALL be run.

#### Scenario: Release propose command
- **WHEN** a release proposal command is used
- **THEN** it SHALL create or update a product release plan for a product version and selected Sprint scope.

#### Scenario: Release prepare command
- **WHEN** a release preparation command is used
- **THEN** it SHALL run release gates and generate or update Mintlify announcement source.

#### Scenario: Release publish command
- **WHEN** a release publish or confirmation command is used
- **THEN** it SHALL record release confirmation evidence without introducing a draft/pending/published/retracted state machine.

### Requirement: 不新增应用内公告入口
The product release management capability SHALL NOT add release announcement entry points inside the admin menu, login page, owner Web, or miniapp.

#### Scenario: No admin menu entry
- **WHEN** product release management is implemented
- **THEN** the Web admin sidebar or menu SHALL NOT add a release announcement entry.

#### Scenario: No owner or miniapp entry
- **WHEN** product release announcements are published
- **THEN** owner Web and miniapp SHALL NOT add release announcement entry points as part of this capability.

#### Scenario: No backend announcement service
- **WHEN** release announcements are implemented
- **THEN** the implementation SHALL NOT add a backend announcement API or database table unless a later OpenSpec Change explicitly requires it.
