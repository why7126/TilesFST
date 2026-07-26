---
created_at: 2026-07-21 10:35:42
updated_at: 2026-07-21 10:35:42
---

# database Specification Delta

## ADDED Requirements

### Requirement: 数据库发布必须验证 MySQL 目标路径
Database-impacting releases MUST validate MySQL compatibility before publish confirmation.

#### Scenario: MySQL schema drift check blocks release
- **GIVEN** a release has `impact_scope.database` marked as database-impacting
- **WHEN** release preparation validates the database gate
- **THEN** the release MUST include evidence from a MySQL schema drift check or equivalent target MySQL schema verification.
- **AND** missing target tables or columns MUST block release confirmation.

#### Scenario: MySQL compatibility evidence is explicit
- **WHEN** database migration evidence is recorded in `release.json`
- **THEN** the evidence SHALL name the MySQL check that was run and the schema source used.
- **AND** the evidence SHALL include rollback or backup evidence for the database change.
