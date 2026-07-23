---
created_at: 2026-07-21 10:35:42
updated_at: 2026-07-21 10:35:42
---

# Proposal: add-release-mysql-compatibility-gate

## Summary

Strengthen the product release workflow so any release with database impact must provide MySQL compatibility evidence before it can pass release preparation.

## Motivation

v0.0.4 exposed two production-only database compatibility gaps:

- production MySQL schema drift caused a miniapp API 500 because a required column was missing in the target database;
- SQLite-specific SQL reached a production query path and failed under MySQL.

The current release gate asks for migration, database documentation, and rollback evidence, but it does not force evidence from the target MySQL path. This change makes MySQL compatibility a release-blocking condition instead of a manual checklist item.

## Scope

- Add a MySQL schema drift checker for comparing `schema.mysql.sql` against a target MySQL database.
- Extend release metadata validation so database-impacting releases require MySQL compatibility evidence.
- Update release/database rules and the `/release-prepare` skill to document the new gate.
- Add focused tests for the validator and schema checker.

## Non-Goals

- Introduce a full migration framework or online migration runner.
- Automatically mutate production databases.
- Replace existing SQLite local development behavior.
- Backfill production data.
